"use strict";

/*
 * CSV interchange codec shared by the offline UI and Node-based acceptance
 * tests.  It deliberately retains every input cell: the viewer may not know a
 * future TMM column or measurement, but it must never discard it on export.
 */
(function exposeCsvCodec(root, factory) {
  const api = factory();
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.TmmCsvCodec = api;
}(globalThis, function csvCodecFactory() {
  const CANDIDATE_DELIMITERS = [",", ";", "\t"];

  function parseRecords(text, delimiter) {
    const records = [];
    let row = [], field = "", quoted = false;
    for (let index = 0; index < text.length; index += 1) {
      const character = text[index];
      if (quoted) {
        if (character === '"' && text[index + 1] === '"') { field += '"'; index += 1; }
        else if (character === '"') quoted = false;
        else field += character;
      } else if (character === '"') {
        quoted = true;
      } else if (character === delimiter) {
        row.push(field); field = "";
      } else if (character === "\n" || character === "\r") {
        if (character === "\r" && text[index + 1] === "\n") index += 1;
        row.push(field); records.push(row); row = []; field = "";
      } else {
        field += character;
      }
    }
    if (field.length || row.length) { row.push(field); records.push(row); }
    return records;
  }

  function detectDelimiter(text) {
    let best = { delimiter: ",", score: -1 };
    for (const delimiter of CANDIDATE_DELIMITERS) {
      const header = parseRecords(text, delimiter)[0] || [];
      const normalized = header.map((value, index) => (index === 0 ? value.replace(/^\uFEFF/, "") : value).trim());
      const known = ["observed_at", "inverter", "metric", "value", "unit"].filter(name => normalized.includes(name)).length;
      const score = known * 1000 + header.length;
      if (score > best.score) best = { delimiter, score };
    }
    return best.delimiter;
  }

  function parse(text) {
    const delimiter = detectDelimiter(text);
    const records = parseRecords(text, delimiter);
    const header = (records.shift() || []).map((value, index) => (index === 0 ? value.replace(/^\uFEFF/, "") : value).trim());
    return { delimiter, header, records };
  }

  function number(value) {
    let text = String(value ?? "").trim().replace(/[\s\u00a0]/g, "");
    if (!text) return null;
    const comma = text.lastIndexOf(",");
    const dot = text.lastIndexOf(".");
    if (comma >= 0 && dot >= 0) {
      if (comma > dot) text = text.replaceAll(".", "").replace(",", ".");
      else text = text.replaceAll(",", "");
    } else if (comma >= 0) {
      text = text.replace(",", ".");
    }
    const result = Number(text);
    return Number.isFinite(result) ? result : null;
  }

  function timestamp(value) {
    const direct = Date.parse(String(value ?? "").trim());
    if (Number.isFinite(direct)) return direct;
    const match = String(value ?? "").trim().match(/^(\d{1,2})\.(\d{1,2})\.(\d{4})[ T](\d{1,2}):(\d{2})(?::(\d{2})(?:[.,](\d{1,3}))?)?$/);
    if (!match) return NaN;
    const [, day, month, year, hour, minute, second = "0", milliseconds = "0"] = match;
    return new Date(Number(year), Number(month) - 1, Number(day), Number(hour), Number(minute), Number(second), Number(milliseconds.padEnd(3, "0"))).getTime();
  }

  function tmmRows(document, required) {
    const at = Object.fromEntries(document.header.map((name, index) => [name, index]));
    const missing = required.filter(name => at[name] === undefined);
    if (missing.length) return { missing, rows: [], rejected: document.records.length, sources: new Set() };
    const rows = [], sources = new Set();
    let rejected = 0;
    for (const fields of document.records) {
      const inverter = (fields[at.inverter] || "").trim();
      const metric = (fields[at.metric] || "").trim();
      const time = timestamp(fields[at.observed_at]);
      const value = number(fields[at.value]);
      if (inverter) sources.add(inverter);
      if (!Number.isFinite(time) || value === null || !inverter || !metric) { rejected += 1; continue; }
      rows.push({ time, inverter, slave: fields[at.slave_id], metric, metricLabel: at.metric_label === undefined ? "" : (fields[at.metric_label] || "").trim(), address: fields[at.register_address], raw: number(fields[at.raw_value]), value, unit: fields[at.unit] || "" });
    }
    return { missing, rows, rejected, sources };
  }

  function quote(value, delimiter) {
    const text = String(value ?? "");
    return /["\r\n]/.test(text) || text.includes(delimiter) ? `"${text.replaceAll('"', '""')}"` : text;
  }

  function serialize(header, records, delimiter = ",", lineEnding = "\n", withBom = false) {
    const rows = [header, ...records];
    return `${withBom ? "\uFEFF" : ""}${rows.map(row => header.map((_, index) => quote(row[index] ?? "", delimiter)).join(delimiter)).join(lineEnding)}${lineEnding}`;
  }

  return { parse, parseRecords, number, timestamp, tmmRows, serialize };
}));
