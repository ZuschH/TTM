"""Condition-monitoring rules and persistent milestone evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
import math
import re
import sqlite3
from typing import Any


OPERATORS = {">", ">=", "<", "<=", "=", "!=", "NOT"}
LOGIC_OPERATORS = {"AND", "OR", "XOR", "NOT"}
SEVERITIES = {"info", "warning", "critical"}


@dataclass(frozen=True)
class ConditionRule:
    identifier: str
    name: str
    source: str
    metric: str
    operator: str
    value: float
    duration_seconds: float
    hysteresis: float
    tolerance: float
    severity: str
    enabled: bool
    revision: int
    expression: dict[str, Any]

    @property
    def signature(self) -> str:
        return json.dumps(self.as_dict(), sort_keys=True, separators=(",", ":"))

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.identifier, "name": self.name, "source": self.source,
            "metric": self.metric, "operator": self.operator, "value": self.value,
            "duration_seconds": self.duration_seconds, "hysteresis": self.hysteresis,
            "tolerance": self.tolerance, "severity": self.severity,
            "enabled": self.enabled, "revision": self.revision,
            "expression": self.expression,
        }


def _normalise_predicate(raw: dict[str, Any], identifier: str) -> dict[str, Any]:
    source = str(raw.get("source", "")).strip()
    metric = str(raw.get("metric", "")).strip()
    operator = str(raw.get("operator", "")).upper()
    if not source or len(source) > 120 or not re.fullmatch(r"[A-Za-z0-9_.-]{1,120}", metric):
        raise ValueError(f"invalid condition operand identity: {identifier}")
    if operator not in OPERATORS:
        raise ValueError(f"invalid condition operand operator: {identifier}")
    value = float(raw.get("value", 0)); hysteresis = float(raw.get("hysteresis", 0)); tolerance = float(raw.get("tolerance", 0))
    if not all(math.isfinite(item) for item in (value, hysteresis, tolerance)) or min(hysteresis, tolerance) < 0:
        raise ValueError(f"invalid numeric condition operand: {identifier}")
    return {"source": source, "metric": metric, "operator": operator, "value": value,
            "hysteresis": hysteresis, "tolerance": tolerance}


def _normalise_expression(raw: Any, identifier: str, depth: int = 0, counter: list[int] | None = None) -> dict[str, Any]:
    if depth > 8 or not isinstance(raw, dict):
        raise ValueError(f"invalid or excessively nested condition expression: {identifier}")
    counter = counter if counter is not None else [0]
    counter[0] += 1
    if counter[0] > 64:
        raise ValueError(f"condition expression contains too many nodes: {identifier}")
    if "logic" not in raw:
        return _normalise_predicate(raw, identifier)
    logic = str(raw.get("logic", "")).upper()
    children = raw.get("conditions")
    if logic not in LOGIC_OPERATORS or not isinstance(children, list) or not children:
        raise ValueError(f"invalid condition logic group: {identifier}")
    if logic == "NOT" and len(children) != 1:
        raise ValueError(f"NOT condition group requires exactly one operand: {identifier}")
    return {"logic": logic, "conditions": [
        _normalise_expression(child, identifier, depth + 1, counter) for child in children
    ]}


def expression_predicates(expression: dict[str, Any]) -> list[dict[str, Any]]:
    if "logic" not in expression:
        return [expression]
    return [leaf for child in expression["conditions"] for leaf in expression_predicates(child)]


def condition_rules(config: dict[str, Any]) -> list[ConditionRule]:
    raw_rules = config.get("condition_monitoring", {}).get("rules", [])
    if not isinstance(raw_rules, list):
        raise ValueError("condition_monitoring.rules must be a list")
    result: list[ConditionRule] = []
    identifiers: set[str] = set()
    for raw in raw_rules:
        if not isinstance(raw, dict):
            raise ValueError("condition rule must be an object")
        identifier = str(raw.get("id", "")).strip()
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", identifier) or identifier in identifiers:
            raise ValueError(f"invalid or duplicate condition rule id: {identifier!r}")
        identifiers.add(identifier)
        name = str(raw.get("name", "")).strip()
        severity = str(raw.get("severity", "warning")).lower()
        if not name or len(name) > 120:
            raise ValueError(f"invalid condition rule identity: {identifier}")
        if severity not in SEVERITIES:
            raise ValueError(f"invalid condition rule severity: {identifier}")
        legacy = {key: raw.get(key, default) for key, default in (
            ("source", ""), ("metric", ""), ("operator", ""), ("value", 0),
            ("hysteresis", 0), ("tolerance", 0))}
        expression = _normalise_expression(raw.get("expression", legacy), identifier)
        primary = expression_predicates(expression)[0]
        duration = float(raw.get("duration_seconds", 0))
        if not math.isfinite(duration) or duration < 0:
            raise ValueError(f"invalid numeric condition setting: {identifier}")
        result.append(ConditionRule(identifier, name, primary["source"], primary["metric"],
                                    primary["operator"], primary["value"], duration,
                                    primary["hysteresis"], primary["tolerance"], severity,
                                    bool(raw.get("enabled", True)), max(1, int(raw.get("revision", 1))),
                                    expression))
    return result


def rule_matches(rule: ConditionRule, value: float, active: bool = False) -> bool:
    margin = rule.hysteresis if active else 0.0
    if rule.operator == ">": return value > rule.value - margin
    if rule.operator == ">=": return value >= rule.value - margin
    if rule.operator == "<": return value < rule.value + margin
    if rule.operator == "<=": return value <= rule.value + margin
    if rule.operator == "=": return abs(value - rule.value) <= rule.tolerance + margin
    if rule.operator == "!=": return abs(value - rule.value) > max(0.0, rule.tolerance - margin)
    return not bool(value)


def predicate_matches(predicate: dict[str, Any], value: float, active: bool = False) -> bool:
    margin = predicate["hysteresis"] if active else 0.0
    target = predicate["value"]; operator = predicate["operator"]
    if operator == ">": return value > target - margin
    if operator == ">=": return value >= target - margin
    if operator == "<": return value < target + margin
    if operator == "<=": return value <= target + margin
    if operator == "=": return abs(value - target) <= predicate["tolerance"] + margin
    if operator == "!=": return abs(value - target) > max(0.0, predicate["tolerance"] - margin)
    return not bool(value)


class ConditionEvaluator:
    def __init__(self, connection: sqlite3.Connection, rules: list[ConditionRule]):
        self.connection = connection
        self.rules: dict[tuple[str, str], list[ConditionRule]] = {}
        self.latest: dict[tuple[str, str], tuple[float, str, str]] = {}
        self.configure(rules)

    def configure(self, rules: list[ConditionRule]) -> None:
        self.rules.clear()
        for rule in rules:
            if rule.enabled:
                for predicate in expression_predicates(rule.expression):
                    self.rules.setdefault((predicate["source"], predicate["metric"]), []).append(rule)
        valid = {rule.identifier for rule in rules}
        if valid:
            placeholders = ",".join("?" for _ in valid)
            self.connection.execute(f"DELETE FROM condition_states WHERE rule_id NOT IN ({placeholders})", tuple(sorted(valid)))
        else:
            self.connection.execute("DELETE FROM condition_states")
        self.connection.commit()

    def evaluate(self, observed_at: str, source: str, metric: str, value: float, unit: str) -> None:
        self.latest[(source, metric)] = (value, unit, observed_at)
        seen: set[str] = set()
        for rule in self.rules.get((source, metric), []):
            if rule.identifier in seen:
                continue
            seen.add(rule.identifier)
            row = self.connection.execute(
                "SELECT signature,active,pending_since FROM condition_states WHERE rule_id=?", (rule.identifier,)
            ).fetchone()
            signature = rule.signature
            if row is None or row[0] != signature:
                active, pending_since = False, None
            else:
                active, pending_since = bool(row[1]), row[2]
            evaluated = self._evaluate_expression(rule.expression, active)
            if evaluated is None:
                continue
            matches, operands = evaluated
            event_type: str | None = None
            if active and not matches:
                active, pending_since, event_type = False, None, "exit"
            elif not active and matches:
                pending_since = pending_since or observed_at
                elapsed = (datetime.fromisoformat(observed_at.replace("Z", "+00:00")) - datetime.fromisoformat(pending_since.replace("Z", "+00:00"))).total_seconds()
                if elapsed >= rule.duration_seconds:
                    active, event_type = True, "enter"
            elif not matches:
                pending_since = None
            if event_type:
                snapshot = json.dumps({"logic": rule.expression, "result": matches,
                                       "trigger": {"source": source, "metric": metric, "value": value, "unit": unit},
                                       "operands": operands}, ensure_ascii=False)
                self.connection.execute(
                    """INSERT INTO milestones(observed_at,rule_id,rule_revision,rule_name,event_type,severity,
                       source,metric,value,unit,operator,target_value,snapshot_json)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (observed_at, rule.identifier, rule.revision, rule.name, event_type, rule.severity,
                     source, metric, value, unit, rule.operator, rule.value, snapshot),
                )
            self.connection.execute(
                """INSERT INTO condition_states(rule_id,signature,active,pending_since,last_value,last_observed_at)
                   VALUES (?,?,?,?,?,?) ON CONFLICT(rule_id) DO UPDATE SET signature=excluded.signature,
                   active=excluded.active,pending_since=excluded.pending_since,last_value=excluded.last_value,
                   last_observed_at=excluded.last_observed_at""",
                (rule.identifier, signature, int(active), pending_since, value, observed_at),
            )

    def _evaluate_expression(self, expression: dict[str, Any], active: bool) -> tuple[bool, list[dict[str, Any]]] | None:
        if "logic" not in expression:
            key = (expression["source"], expression["metric"])
            current = self.latest.get(key)
            if current is None:
                return None
            value, unit, observed_at = current
            matches = predicate_matches(expression, value, active)
            return matches, [{**expression, "current_value": value, "unit": unit,
                              "observed_at": observed_at, "matches": matches}]
        children = [self._evaluate_expression(child, active) for child in expression["conditions"]]
        if any(child is None for child in children):
            return None
        results = [child[0] for child in children if child is not None]
        operands = [item for child in children if child is not None for item in child[1]]
        logic = expression["logic"]
        if logic == "AND": matches = all(results)
        elif logic == "OR": matches = any(results)
        elif logic == "XOR": matches = sum(bool(item) for item in results) == 1
        else: matches = not results[0]
        return matches, operands
