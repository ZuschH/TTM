const I18N = {
  en: {
    "alerts.eyebrow":"Messages","alerts.title":"Information, warnings & critical conditions","alerts.clear":"No active messages","alerts.info":"Information","alerts.warning":"Warning","alerts.critical":"Critical","alerts.threshold":"Threshold","alerts.system":"Host system","alerts.storage":"Storage","alerts.retentionRisk":"Storage duration is shorter than the configured retention period",
    "info.eyebrow":"Device","info.title":"Device information","info.waiting":"Waiting for device information …","info.family":"Model family","info.configured":"Configured device","info.slave":"Modbus address","info.capacity":"Capacity code","info.series":"Series code","info.cpu":"CPU / application version","info.cpu2":"CPU2 version","info.eeprom":"EEPROM version","info.unavailable":"Not reported",
    "diag.rate":"Stored samples/s","diag.average":"Average poll time","diag.maximum":"Maximum poll time","diag.bus":"Estimated bus load","diag.retries":"Retries","diag.success":"Read success","diag.inverterCpu":"Inverter CPU","diag.hostCpu":"Host CPU","diag.hostMemory":"Host memory","diag.disk":"Data disk","diag.temperature":"Host temperature","diag.notAvailable":"Not exposed by inverter",
    "header.eyebrow":"TMM · Version 1.0","header.title":"Toshiba Modbus Monitor","language":"Language","status.connecting":"Connecting …","status.healthy":"Online","status.degraded":"Partially degraded","status.stale":"No current data","status.starting":"Waiting for data","status.unavailable":"Database unavailable",
    "io.eyebrow":"Hardware","io.title":"Terminals & analog output","io.waiting":"Waiting for I/O data …","io.none":"No I/O monitors are configured for this profile.","io.enablePrefix":"To display data here, enable","io.enableSuffix":"in Measurement channels as Live or Record.","io.analog":"FM analog output","io.noAnalog":"No analog data","io.on":"ON","io.off":"OFF",
    "fault.eyebrow":"Diagnostic memory","fault.title":"Trips & retained operating values","fault.waiting":"Waiting for diagnostic data …","fault.none":"No diagnostic-memory registers are configured for this profile.","fault.note":"FE10 = most recent stored trip","fault.current":"Current","fault.latest":"Latest trip","fault.previous":"Previous","fault.third":"3rd entry","fault.oldest":"Oldest","fault.unknown":"Unknown trip code","fault.noneError":"No error","fault.frequency":"Output frequency","fault.currentOut":"Output current","fault.dc":"DC link","fault.voltage":"Output voltage","fault.status":"Status word",
    "live.title":"Current measurements","live.noData":"No data yet","live.asOf":"As of","live.orderHint":"Drag cards to arrange them. The order is retained.",
    "history.eyebrow":"History","history.title":"Measurement history","history.metric":"Metric","history.empty":"No history data available.","history.min":"Min","history.max":"Max",
    "comm.eyebrow":"Diagnostics","comm.title":"Communication","comm.manual":"User manual","comm.api":"API documentation","comm.drives":"Inverters","comm.success":"Successful","comm.failed":"Failed","comm.age":"Data age",
    "storage.eyebrow":"Data","storage.title":"Storage & export","storage.exportAll":"Export all data as CSV","storage.hint":"The export is limited to the maximum row count defined in the configuration.","storage.used":"Storage used","storage.samples":"Samples","storage.cycles":"Poll cycles","storage.retention":"Retention","storage.unlimited":"Unlimited","storage.days":"days","storage.exportMetric":"as CSV",
    "storage.free":"Disk space free","storage.growth":"Estimated growth/day","storage.remaining":"Estimated time remaining","storage.calculating":"Calculating (at least 5 minutes of data required)","storage.retentionLimited":"Retention is expected to limit growth","duration.years":"years","duration.days":"days","duration.hours":"hours",
    "footer.summary":"read-only · refreshes every 3 seconds","footer.contact":"Contact",
    "metric.output_frequency":"Output frequency","metric.frequency_setpoint":"Frequency setpoint","metric.operating_status":"Operating status","metric.output_current":"Output current","metric.dc_input_voltage":"DC-link voltage","metric.output_voltage":"Output voltage","metric.braking_resistor_load":"Braking resistor load (OLr)","metric.inverter_internal_temperature":"Internal device temperature","metric.power_board_temperature":"Power-board temperature","metric.trip_code":"Trip code","metric.alarm_information_1":"Alarm word 1","metric.alarm_information_2":"Alarm word 2"
  },
  de: {
    "alerts.eyebrow":"Meldungen","alerts.title":"Informationen, Warnungen & kritische Zustände","alerts.clear":"Keine aktiven Meldungen","alerts.info":"Information","alerts.warning":"Warnung","alerts.critical":"Kritisch","alerts.threshold":"Schwellwert","alerts.system":"Host-System","alerts.storage":"Speicher","alerts.retentionRisk":"Speicherlaufzeit ist kürzer als die konfigurierte Aufbewahrungszeit",
    "info.eyebrow":"Gerät","info.title":"Geräteinformationen","info.waiting":"Warte auf Geräteinformationen …","info.family":"Modellfamilie","info.configured":"Konfiguriertes Gerät","info.slave":"Modbus-Adresse","info.capacity":"Leistungscode","info.series":"Baureihencode","info.cpu":"CPU-/Applikationsversion","info.cpu2":"CPU2-Version","info.eeprom":"EEPROM-Version","info.unavailable":"Nicht gemeldet",
    "diag.rate":"Gespeicherte Werte/s","diag.average":"Mittlere Abfragezeit","diag.maximum":"Maximale Abfragezeit","diag.bus":"Geschätzte Buslast","diag.retries":"Wiederholungen","diag.success":"Leseerfolg","diag.inverterCpu":"Umrichter-CPU","diag.hostCpu":"Host-CPU","diag.hostMemory":"Host-Arbeitsspeicher","diag.disk":"Datenträger","diag.temperature":"Host-Temperatur","diag.notAvailable":"Vom Umrichter nicht bereitgestellt",
    "header.eyebrow":"TMM · Version 1.0","header.title":"Toshiba Modbus Monitor","language":"Sprache","status.connecting":"Verbinde …","status.healthy":"Online","status.degraded":"Teilweise gestört","status.stale":"Keine aktuellen Daten","status.starting":"Warte auf Daten","status.unavailable":"Datenbank nicht erreichbar",
    "io.eyebrow":"Hardware","io.title":"Klemmen & Analogausgang","io.waiting":"Warte auf E/A-Daten …","io.none":"Für dieses Profil sind keine E/A-Monitore konfiguriert.","io.enablePrefix":"Um Daten hier anzuzeigen, aktivieren Sie","io.enableSuffix":"unter Messkanäle als Live oder Aufzeichnen.","io.analog":"FM-Analogausgang","io.noAnalog":"Keine Analogdaten","io.on":"EIN","io.off":"AUS",
    "fault.eyebrow":"Diagnosespeicher","fault.title":"Trips & festgehaltene Betriebswerte","fault.waiting":"Warte auf Diagnosedaten …","fault.none":"Für dieses Profil sind keine Diagnosespeicher-Register konfiguriert.","fault.note":"FE10 = jüngster gespeicherter Trip","fault.current":"Aktuell","fault.latest":"Letzter Trip","fault.previous":"Vorletzter","fault.third":"3. Eintrag","fault.oldest":"Ältester","fault.unknown":"Unbekannter Trip-Code","fault.noneError":"Kein Fehler","fault.frequency":"Ausgangsfrequenz","fault.currentOut":"Ausgangsstrom","fault.dc":"Zwischenkreis","fault.voltage":"Ausgangsspannung","fault.status":"Statuswort",
    "live.title":"Aktuelle Messwerte","live.noData":"Noch keine Daten","live.asOf":"Stand","live.orderHint":"Karten per Drag & Drop anordnen. Die Reihenfolge bleibt erhalten.",
    "history.eyebrow":"Verlauf","history.title":"Messwert-Historie","history.metric":"Messwert","history.empty":"Noch keine Verlaufsdaten vorhanden.","history.min":"Min","history.max":"Max",
    "comm.eyebrow":"Diagnose","comm.title":"Kommunikation","comm.manual":"Benutzerhandbuch","comm.api":"API-Dokumentation","comm.drives":"Umrichter","comm.success":"Erfolgreich","comm.failed":"Fehlgeschlagen","comm.age":"Datenalter",
    "storage.eyebrow":"Daten","storage.title":"Speicher & Export","storage.exportAll":"Alle Daten als CSV","storage.hint":"Der Export ist auf die konfigurierte maximale Zeilenzahl begrenzt.","storage.used":"Belegter Speicher","storage.samples":"Messpunkte","storage.cycles":"Messzyklen","storage.retention":"Aufbewahrung","storage.unlimited":"Unbegrenzt","storage.days":"Tage","storage.exportMetric":"als CSV",
    "storage.free":"Freier Speicherplatz","storage.growth":"Geschätzter Zuwachs/Tag","storage.remaining":"Geschätzte Restlaufzeit","storage.calculating":"Berechnung läuft (mindestens 5 Minuten Daten erforderlich)","storage.retentionLimited":"Aufbewahrungsfrist begrenzt den Zuwachs voraussichtlich","duration.years":"Jahre","duration.days":"Tage","duration.hours":"Stunden",
    "footer.summary":"nur lesend · Aktualisierung alle 3 Sekunden","footer.contact":"Kontakt",
    "metric.output_frequency":"Ausgangsfrequenz","metric.frequency_setpoint":"Frequenzvorgabe","metric.operating_status":"Betriebsstatus","metric.output_current":"Ausgangsstrom","metric.dc_input_voltage":"Zwischenkreisspannung","metric.output_voltage":"Ausgangsspannung","metric.braking_resistor_load":"Bremswiderstand-Auslastung (OLr)","metric.inverter_internal_temperature":"Interne Gerätetemperatur","metric.power_board_temperature":"Leistungsteilplatinen-Temperatur","metric.trip_code":"Trip-Code","metric.alarm_information_1":"Alarmwort 1","metric.alarm_information_2":"Alarmwort 2"
  },
  fr: {
    "alerts.eyebrow":"Messages","alerts.title":"Informations, avertissements et états critiques","alerts.clear":"Aucun message actif","alerts.info":"Information","alerts.warning":"Avertissement","alerts.critical":"Critique","alerts.threshold":"Seuil","alerts.system":"Système hôte","alerts.storage":"Stockage","alerts.retentionRisk":"La durée de stockage est inférieure à la période de conservation configurée",
    "info.eyebrow":"Appareil","info.title":"Informations sur l’appareil","info.waiting":"En attente des informations appareil…","info.family":"Famille de modèle","info.configured":"Appareil configuré","info.slave":"Adresse Modbus","info.capacity":"Code de capacité","info.series":"Code de série","info.cpu":"Version CPU / application","info.cpu2":"Version CPU2","info.eeprom":"Version EEPROM","info.unavailable":"Non communiqué",
    "diag.rate":"Mesures enregistrées/s","diag.average":"Temps moyen requête","diag.maximum":"Temps maximal requête","diag.bus":"Charge bus estimée","diag.retries":"Répétitions","diag.success":"Lectures réussies","diag.inverterCpu":"CPU variateur","diag.hostCpu":"CPU hôte","diag.hostMemory":"Mémoire hôte","diag.disk":"Disque de données","diag.temperature":"Température hôte","diag.notAvailable":"Non fourni par le variateur",
    "header.eyebrow":"TMM · Version 1.0","header.title":"Toshiba Modbus Monitor","language":"Langue","status.connecting":"Connexion…","status.healthy":"En ligne","status.degraded":"Partiellement perturbé","status.stale":"Aucune donnée récente","status.starting":"En attente de données","status.unavailable":"Base de données indisponible",
    "io.eyebrow":"Matériel","io.title":"Bornes et sortie analogique","io.waiting":"En attente des données E/S…","io.none":"Aucun moniteur E/S configuré pour ce profil.","io.enablePrefix":"Pour afficher des données ici, activez","io.enableSuffix":"dans Canaux de mesure, en Direct ou Enregistrer.","io.analog":"Sortie analogique FM","io.noAnalog":"Aucune donnée analogique","io.on":"ON","io.off":"OFF",
    "fault.eyebrow":"Mémoire de diagnostic","fault.title":"Défauts et valeurs mémorisées","fault.waiting":"En attente des données de diagnostic…","fault.none":"Aucun registre de diagnostic configuré pour ce profil.","fault.note":"FE10 = dernier défaut mémorisé","fault.current":"Actuel","fault.latest":"Dernier défaut","fault.previous":"Précédent","fault.third":"3e entrée","fault.oldest":"Plus ancien","fault.unknown":"Code défaut inconnu","fault.noneError":"Aucun défaut","fault.frequency":"Fréquence de sortie","fault.currentOut":"Courant de sortie","fault.dc":"Bus continu","fault.voltage":"Tension de sortie","fault.status":"Mot d’état",
    "live.title":"Mesures actuelles","live.noData":"Aucune donnée","live.asOf":"État au","live.orderHint":"Faites glisser les cartes pour les organiser. L’ordre est conservé.",
    "history.eyebrow":"Historique","history.title":"Historique des mesures","history.metric":"Mesure","history.empty":"Aucune donnée historique disponible.","history.min":"Min","history.max":"Max",
    "comm.eyebrow":"Diagnostic","comm.title":"Communication","comm.manual":"Manuel utilisateur","comm.api":"Documentation API","comm.drives":"Variateurs","comm.success":"Réussies","comm.failed":"Échouées","comm.age":"Âge des données",
    "storage.eyebrow":"Données","storage.title":"Stockage et export","storage.exportAll":"Exporter toutes les données en CSV","storage.hint":"L’export est limité au nombre maximal de lignes configuré.","storage.used":"Espace utilisé","storage.samples":"Mesures","storage.cycles":"Cycles","storage.retention":"Conservation","storage.unlimited":"Illimitée","storage.days":"jours","storage.exportMetric":"en CSV",
    "storage.free":"Espace disque libre","storage.growth":"Croissance estimée/jour","storage.remaining":"Durée restante estimée","storage.calculating":"Calcul en cours (5 minutes de données requises)","storage.retentionLimited":"La conservation devrait limiter la croissance","duration.years":"ans","duration.days":"jours","duration.hours":"heures",
    "footer.summary":"lecture seule · actualisation toutes les 3 secondes","footer.contact":"Contact",
    "metric.output_frequency":"Fréquence de sortie","metric.frequency_setpoint":"Consigne de fréquence","metric.operating_status":"État de fonctionnement","metric.output_current":"Courant de sortie","metric.dc_input_voltage":"Tension du bus continu","metric.output_voltage":"Tension de sortie","metric.braking_resistor_load":"Charge résistance de freinage (OLr)","metric.inverter_internal_temperature":"Température interne appareil","metric.power_board_temperature":"Température carte de puissance","metric.trip_code":"Code défaut","metric.alarm_information_1":"Mot d’alarme 1","metric.alarm_information_2":"Mot d’alarme 2"
  },
  ja: {
    "alerts.eyebrow":"メッセージ","alerts.title":"情報・警告・重大状態","alerts.clear":"有効なメッセージはありません","alerts.info":"情報","alerts.warning":"警告","alerts.critical":"重大","alerts.threshold":"しきい値","alerts.system":"ホストシステム","alerts.storage":"ストレージ","alerts.retentionRisk":"ストレージ残存期間が設定された保存期間より短くなっています",
    "info.eyebrow":"装置","info.title":"装置情報","info.waiting":"装置情報を待機中…","info.family":"モデル系列","info.configured":"設定装置名","info.slave":"Modbusアドレス","info.capacity":"容量コード","info.series":"シリーズコード","info.cpu":"CPU／アプリケーション版","info.cpu2":"CPU2版","info.eeprom":"EEPROM版","info.unavailable":"未取得",
    "diag.rate":"保存値/秒","diag.average":"平均ポーリング時間","diag.maximum":"最大ポーリング時間","diag.bus":"推定バス使用率","diag.retries":"再試行","diag.success":"読取成功率","diag.inverterCpu":"インバータCPU","diag.hostCpu":"ホストCPU","diag.hostMemory":"ホストメモリ","diag.disk":"データディスク","diag.temperature":"ホスト温度","diag.notAvailable":"インバータから取得不可",
    "header.eyebrow":"TMM · バージョン1.0","header.title":"Toshiba Modbus Monitor","language":"言語","status.connecting":"接続中…","status.healthy":"オンライン","status.degraded":"一部異常","status.stale":"最新データなし","status.starting":"データ待機中","status.unavailable":"データベース利用不可",
    "io.eyebrow":"ハードウェア","io.title":"端子・アナログ出力","io.waiting":"I/Oデータ待機中…","io.none":"このプロファイルにはI/Oモニターがありません。","io.enablePrefix":"ここに表示するには、","io.enableSuffix":"を「計測チャンネル」でライブまたは記録に設定します。","io.analog":"FMアナログ出力","io.noAnalog":"アナログデータなし","io.on":"ON","io.off":"OFF",
    "fault.eyebrow":"診断メモリ","fault.title":"トリップ・保持運転値","fault.waiting":"診断データ待機中…","fault.none":"このプロファイルには診断レジスタがありません。","fault.note":"FE10 = 最新の保存トリップ","fault.current":"現在","fault.latest":"最新トリップ","fault.previous":"前回","fault.third":"3件目","fault.oldest":"最古","fault.unknown":"不明なトリップコード","fault.noneError":"異常なし","fault.frequency":"出力周波数","fault.currentOut":"出力電流","fault.dc":"直流リンク","fault.voltage":"出力電圧","fault.status":"ステータスワード",
    "live.title":"現在値","live.noData":"データなし","live.asOf":"更新","live.orderHint":"カードをドラッグして並べ替えます。順序は保持されます。",
    "history.eyebrow":"履歴","history.title":"計測履歴","history.metric":"計測項目","history.empty":"履歴データがありません。","history.min":"最小","history.max":"最大",
    "comm.eyebrow":"診断","comm.title":"通信","comm.manual":"ユーザーマニュアル","comm.api":"APIドキュメント","comm.drives":"インバータ","comm.success":"成功","comm.failed":"失敗","comm.age":"データ経過時間",
    "storage.eyebrow":"データ","storage.title":"ストレージ・エクスポート","storage.exportAll":"全データをCSV出力","storage.hint":"エクスポート件数は設定された上限までです。","storage.used":"使用容量","storage.samples":"測定点","storage.cycles":"測定サイクル","storage.retention":"保存期間","storage.unlimited":"無期限","storage.days":"日","storage.exportMetric":"CSV出力",
    "storage.free":"空き容量","storage.growth":"推定増加量/日","storage.remaining":"推定残り時間","storage.calculating":"計算中（5分以上のデータが必要）","storage.retentionLimited":"保存期間により増加が制限される見込み","duration.years":"年","duration.days":"日","duration.hours":"時間",
    "footer.summary":"読み取り専用 · 3秒ごとに更新","footer.contact":"連絡先",
    "metric.output_frequency":"出力周波数","metric.frequency_setpoint":"周波数指令値","metric.operating_status":"運転状態","metric.output_current":"出力電流","metric.dc_input_voltage":"直流リンク電圧","metric.output_voltage":"出力電圧","metric.braking_resistor_load":"制動抵抗負荷率 (OLr)","metric.inverter_internal_temperature":"内部装置温度","metric.power_board_temperature":"パワー基板温度","metric.trip_code":"トリップコード","metric.alarm_information_1":"アラームワード1","metric.alarm_information_2":"アラームワード2"
  }
};

const EXTRA = {
  en:{"fault.code":"Toshiba trip code","state.trip":"Trip","state.emergency":"Emergency stop","state.alarm":"Alarm","state.forward":"Running forward","state.reverse":"Running reverse","state.ready":"Ready / stopped","state.stopped":"Stopped / not ready","alarm.none":"No active alarms","alarm.active":"active alarm(s)"},
  de:{"fault.code":"Toshiba-Tripcode","state.trip":"Trip","state.emergency":"Not-Halt","state.alarm":"Alarm","state.forward":"Läuft vorwärts","state.reverse":"Läuft rückwärts","state.ready":"Bereit / gestoppt","state.stopped":"Gestoppt / nicht bereit","alarm.none":"Keine aktiven Alarme","alarm.active":"aktive Alarme"},
  fr:{"fault.code":"Code défaut Toshiba","state.trip":"Défaut","state.emergency":"Arrêt d’urgence","state.alarm":"Alarme","state.forward":"Marche avant","state.reverse":"Marche arrière","state.ready":"Prêt / arrêté","state.stopped":"Arrêté / non prêt","alarm.none":"Aucune alarme active","alarm.active":"alarme(s) active(s)"},
  ja:{"fault.code":"東芝トリップコード","state.trip":"トリップ","state.emergency":"非常停止","state.alarm":"アラーム","state.forward":"正転運転","state.reverse":"逆転運転","state.ready":"準備完了 / 停止","state.stopped":"停止 / 未準備","alarm.none":"アラームなし","alarm.active":"件のアラーム"}
};
for (const code of Object.keys(EXTRA)) Object.assign(I18N[code], EXTRA[code]);

const EXTENDED_METRICS = {
  en:{"metric.speed_feedback":"Speed feedback","metric.speed_feedback_filtered":"Speed feedback (1 s filter)","metric.calculated_motor_speed":"Calculated motor speed","metric.machine_speed":"Machine speed","metric.actual_output_current":"Calculated output current","metric.actual_output_voltage":"Calculated output voltage","metric.actual_motor_torque":"Calculated motor torque","metric.mechanical_power":"Calculated mechanical power","metric.torque":"Torque","metric.torque_command":"Torque command","metric.torque_current":"Torque current","metric.exciting_current":"Exciting current","metric.motor_overload_factor":"Motor overload factor","metric.inverter_overload_factor":"Inverter overload factor","metric.motor_load_factor":"Motor load factor","metric.inverter_load_factor":"Inverter load factor","metric.input_power":"Input power","metric.output_power":"Output power"},
  de:{"metric.speed_feedback":"Drehzahlrückführung","metric.speed_feedback_filtered":"Drehzahlrückführung (1-s-Filter)","metric.calculated_motor_speed":"Berechnete Motordrehzahl","metric.machine_speed":"Maschinendrehzahl","metric.actual_output_current":"Berechneter Ausgangsstrom","metric.actual_output_voltage":"Berechnete Ausgangsspannung","metric.actual_motor_torque":"Berechnetes Motordrehmoment","metric.mechanical_power":"Berechnete mechanische Leistung","metric.torque":"Drehmoment","metric.torque_command":"Drehmomentvorgabe","metric.torque_current":"Drehmomentstrom","metric.exciting_current":"Erregerstrom","metric.motor_overload_factor":"Motor-Überlastfaktor","metric.inverter_overload_factor":"Umrichter-Überlastfaktor","metric.motor_load_factor":"Motorauslastung","metric.inverter_load_factor":"Umrichterauslastung","metric.input_power":"Eingangsleistung","metric.output_power":"Ausgangsleistung"},
  fr:{"metric.speed_feedback":"Retour de vitesse","metric.speed_feedback_filtered":"Retour de vitesse (filtre 1 s)","metric.calculated_motor_speed":"Vitesse moteur calculée","metric.machine_speed":"Vitesse machine","metric.actual_output_current":"Courant de sortie calculé","metric.actual_output_voltage":"Tension de sortie calculée","metric.actual_motor_torque":"Couple moteur calculé","metric.mechanical_power":"Puissance mécanique calculée","metric.torque":"Couple","metric.torque_command":"Consigne de couple","metric.torque_current":"Courant de couple","metric.exciting_current":"Courant d’excitation","metric.motor_overload_factor":"Facteur de surcharge moteur","metric.inverter_overload_factor":"Facteur de surcharge variateur","metric.motor_load_factor":"Charge moteur","metric.inverter_load_factor":"Charge variateur","metric.input_power":"Puissance d’entrée","metric.output_power":"Puissance de sortie"},
  ja:{"metric.speed_feedback":"速度フィードバック","metric.speed_feedback_filtered":"速度フィードバック（1秒フィルター）","metric.calculated_motor_speed":"算出モーター速度","metric.machine_speed":"機械速度","metric.actual_output_current":"算出出力電流","metric.actual_output_voltage":"算出出力電圧","metric.actual_motor_torque":"算出モータートルク","metric.mechanical_power":"算出機械出力","metric.torque":"トルク","metric.torque_command":"トルク指令","metric.torque_current":"トルク電流","metric.exciting_current":"励磁電流","metric.motor_overload_factor":"モーター過負荷率","metric.inverter_overload_factor":"インバーター過負荷率","metric.motor_load_factor":"モーター負荷率","metric.inverter_load_factor":"インバーター負荷率","metric.input_power":"入力電力","metric.output_power":"出力電力"}
};
for (const code of Object.keys(EXTENDED_METRICS)) Object.assign(I18N[code], EXTENDED_METRICS[code]);
const RECORDING_I18N = {
  en:{"recording.eyebrow":"Recording","recording.title":"Investigation & database","recording.current":"Current reference","recording.newReference":"Reference for the new recording","recording.archive":"Archive database and start new recording","recording.danger":"Danger zone: permanently delete current database","recording.deleteHelp":"Enter DELETE three times, separated by spaces. This operation cannot be undone.","recording.delete":"Permanently delete and start new recording","recording.accepted":"Request accepted; waiting for the collector…","recording.referenceRequired":"Enter an investigation reference.","recording.complete":"New recording initialized.","recording.failed":"Operation failed"},
  de:{"recording.eyebrow":"Aufzeichnung","recording.title":"Untersuchung & Datenbank","recording.current":"Aktuelle Referenz","recording.newReference":"Referenz der neuen Aufzeichnung","recording.archive":"Datenbank archivieren und neue Aufzeichnung starten","recording.danger":"Gefahrenzone: aktuelle Datenbank endgültig löschen","recording.deleteHelp":"DELETE dreimal, durch Leerzeichen getrennt, eingeben. Dieser Vorgang kann nicht rückgängig gemacht werden.","recording.delete":"Endgültig löschen und neue Aufzeichnung starten","recording.accepted":"Auftrag angenommen; warte auf den Collector…","recording.referenceRequired":"Bitte eine Untersuchungsreferenz eingeben.","recording.complete":"Neue Aufzeichnung initialisiert.","recording.failed":"Vorgang fehlgeschlagen"},
  fr:{"recording.eyebrow":"Enregistrement","recording.title":"Étude et base de données","recording.current":"Référence actuelle","recording.newReference":"Référence du nouvel enregistrement","recording.archive":"Archiver la base et démarrer un nouvel enregistrement","recording.danger":"Zone dangereuse : supprimer définitivement la base actuelle","recording.deleteHelp":"Saisissez DELETE trois fois, séparé par des espaces. Cette opération est irréversible.","recording.delete":"Supprimer définitivement et recommencer","recording.accepted":"Demande acceptée ; attente du collecteur…","recording.referenceRequired":"Saisissez une référence d’étude.","recording.complete":"Nouvel enregistrement initialisé.","recording.failed":"Échec de l’opération"},
  ja:{"recording.eyebrow":"記録","recording.title":"調査とデータベース","recording.current":"現在の参照名","recording.newReference":"新しい記録の参照名","recording.archive":"データベースを保存して新規記録を開始","recording.danger":"危険領域：現在のデータベースを完全削除","recording.deleteHelp":"DELETE を空白区切りで3回入力してください。この操作は取り消せません。","recording.delete":"完全削除して新規記録を開始","recording.accepted":"要求を受け付けました。コレクターを待っています…","recording.referenceRequired":"調査参照名を入力してください。","recording.complete":"新しい記録を初期化しました。","recording.failed":"操作に失敗しました"}
};
for (const code of Object.keys(RECORDING_I18N)) Object.assign(I18N[code], RECORDING_I18N[code]);
const ENGINEERING_I18N = {
  en:{"engineering.eyebrow":"Configuration","engineering.title":"Engineering values","engineering.inverter":"Inverter","engineering.factor":"Machine-speed factor","engineering.unit":"Machine-speed unit","engineering.current":"Rated output current (A)","engineering.voltage":"Rated output voltage (V)","engineering.motorPower":"Motor rated power (kW, optional)","engineering.motorSpeed":"Motor rated speed (rpm, optional)","engineering.save":"Apply settings","engineering.saved":"Settings accepted and passed to the collector.","engineering.invalid":"Enter positive reference values; optional motor power and speed must be entered together."},
  de:{"engineering.eyebrow":"Konfiguration","engineering.title":"Engineering-Werte","engineering.inverter":"Umrichter","engineering.factor":"Faktor Maschinendrehzahl","engineering.unit":"Einheit Maschinendrehzahl","engineering.current":"Nennausgangsstrom (A)","engineering.voltage":"Nennausgangsspannung (V)","engineering.motorPower":"Motornennleistung (kW, optional)","engineering.motorSpeed":"Motornenndrehzahl (rpm, optional)","engineering.save":"Einstellungen übernehmen","engineering.saved":"Einstellungen übernommen und an den Collector übergeben.","engineering.invalid":"Positive Bezugswerte eingeben; optionale Motornennleistung und -drehzahl nur gemeinsam."},
  fr:{"engineering.eyebrow":"Configuration","engineering.title":"Valeurs d’ingénierie","engineering.inverter":"Variateur","engineering.factor":"Facteur de vitesse machine","engineering.unit":"Unité de vitesse machine","engineering.current":"Courant de sortie nominal (A)","engineering.voltage":"Tension de sortie nominale (V)","engineering.motorPower":"Puissance nominale moteur (kW, facultatif)","engineering.motorSpeed":"Vitesse nominale moteur (rpm, facultatif)","engineering.save":"Appliquer","engineering.saved":"Paramètres acceptés et transmis au collecteur.","engineering.invalid":"Saisissez des valeurs positives ; puissance et vitesse moteur facultatives doivent être saisies ensemble."},
  ja:{"engineering.eyebrow":"設定","engineering.title":"工学値","engineering.inverter":"インバーター","engineering.factor":"機械速度係数","engineering.unit":"機械速度単位","engineering.current":"定格出力電流 (A)","engineering.voltage":"定格出力電圧 (V)","engineering.motorPower":"モーター定格出力 (kW、任意)","engineering.motorSpeed":"モーター定格速度 (rpm、任意)","engineering.save":"設定を適用","engineering.saved":"設定を受け付け、コレクターへ渡しました。","engineering.invalid":"正の基準値を入力してください。任意のモーター出力と速度は同時に入力します。"}
};
for (const code of Object.keys(ENGINEERING_I18N)) Object.assign(I18N[code], ENGINEERING_I18N[code]);
const CHANNEL_I18N = {
  en:{"channels.eyebrow":"Recording","channels.title":"Measurement channels","channels.inverter":"Inverter","channels.hints":"Show measurement hints","channels.help":"Off reduces bus load; Live shows the current value without history; Record stores value changes; Hide records but omits the Live card.","channels.off":"Off","channels.live":"Live","channels.record":"Record","channels.hide":"Hide from Live","channels.save":"Apply channel selection","channels.saved":"Channel selection accepted and passed to the collector.","channels.protected":"Required for safe status monitoring","channels.enableLivePrefix":"To display data here, enable","channels.enableLiveSuffix":"in Measurement channels as Live or Record.","channels.enableRecordPrefix":"To create history here, set","channels.enableRecordSuffix":"to Record in Measurement channels."},
  de:{"channels.eyebrow":"Aufzeichnung","channels.title":"Messkanäle","channels.inverter":"Umrichter","channels.hints":"Messhinweise anzeigen","channels.help":"Aus reduziert die Buslast; Live zeigt nur den aktuellen Wert; Aufzeichnen speichert Werteänderungen; Ausblenden zeichnet weiter auf, unterdrückt aber die Live-Karte.","channels.off":"Aus","channels.live":"Live","channels.record":"Aufzeichnen","channels.hide":"In Live-Ansicht ausblenden","channels.save":"Kanalauswahl übernehmen","channels.saved":"Kanalauswahl übernommen und an den Collector übergeben.","channels.protected":"Für die sichere Zustandsüberwachung erforderlich","channels.enableLivePrefix":"Um Daten hier anzuzeigen, aktivieren Sie","channels.enableLiveSuffix":"unter Messkanäle als Live oder Aufzeichnen.","channels.enableRecordPrefix":"Um einen Verlauf zu speichern, setzen Sie","channels.enableRecordSuffix":"unter Messkanäle auf Aufzeichnen."},
  fr:{"channels.eyebrow":"Enregistrement","channels.title":"Canaux de mesure","channels.inverter":"Variateur","channels.hints":"Afficher les aides de mesure","channels.help":"Arrêt réduit la charge du bus ; Direct affiche sans historique ; Enregistrer conserve les changements ; Masquer enregistre mais retire la carte Direct.","channels.off":"Arrêt","channels.live":"Direct","channels.record":"Enregistrer","channels.hide":"Masquer de Direct","channels.save":"Appliquer la sélection","channels.saved":"Sélection acceptée et transmise au collecteur.","channels.protected":"Requis pour la surveillance sûre de l’état","channels.enableLivePrefix":"Pour afficher des données ici, activez","channels.enableLiveSuffix":"dans Canaux de mesure, en Direct ou Enregistrer.","channels.enableRecordPrefix":"Pour créer un historique, réglez","channels.enableRecordSuffix":"sur Enregistrer dans Canaux de mesure."},
  ja:{"channels.eyebrow":"記録","channels.title":"計測チャンネル","channels.inverter":"インバーター","channels.hints":"測定ヒントを表示","channels.help":"オフはバス負荷を低減、ライブは現在値のみ表示、記録は値の変化を保存します。ライブから非表示は記録を継続し、ライブカードのみを非表示にします。","channels.off":"オフ","channels.live":"ライブ","channels.record":"記録","channels.hide":"ライブから非表示","channels.save":"チャンネル設定を適用","channels.saved":"設定を受け付け、コレクターへ渡しました。","channels.protected":"安全な状態監視に必要","channels.enableLivePrefix":"ここに表示するには、","channels.enableLiveSuffix":"を「計測チャンネル」でライブまたは記録に設定します。","channels.enableRecordPrefix":"履歴を作成するには、","channels.enableRecordSuffix":"を「計測チャンネル」で記録に設定します。"}
};
for (const code of Object.keys(CHANNEL_I18N)) Object.assign(I18N[code], CHANNEL_I18N[code]);
const CHANNEL_METRIC_I18N = {
  en:{"metric.input_terminal_status":"Input terminals F/R/S1/S2/S3","metric.fm_analog_output":"FM analog output","metric.trip_output_frequency":"Trip snapshot: output frequency","metric.trip_operating_status":"Trip snapshot: operating status","metric.trip_output_current":"Trip snapshot: output current","metric.trip_dc_input_voltage":"Trip snapshot: DC-link voltage","metric.trip_output_voltage":"Trip snapshot: output voltage","metric.past_trip_1":"Stored trip 1","metric.past_trip_2":"Stored trip 2","metric.past_trip_3":"Stored trip 3","metric.past_trip_4":"Stored trip 4"},
  de:{"metric.input_terminal_status":"Eingangsklemmen F/R/S1/S2/S3","metric.fm_analog_output":"FM-Analogausgang","metric.trip_output_frequency":"Trip-Momentaufnahme: Ausgangsfrequenz","metric.trip_operating_status":"Trip-Momentaufnahme: Betriebsstatus","metric.trip_output_current":"Trip-Momentaufnahme: Ausgangsstrom","metric.trip_dc_input_voltage":"Trip-Momentaufnahme: Zwischenkreis","metric.trip_output_voltage":"Trip-Momentaufnahme: Ausgangsspannung","metric.past_trip_1":"Gespeicherter Trip 1","metric.past_trip_2":"Gespeicherter Trip 2","metric.past_trip_3":"Gespeicherter Trip 3","metric.past_trip_4":"Gespeicherter Trip 4"},
  fr:{"metric.input_terminal_status":"Bornes d’entrée F/R/S1/S2/S3","metric.fm_analog_output":"Sortie analogique FM","metric.trip_output_frequency":"Instantané défaut : fréquence de sortie","metric.trip_operating_status":"Instantané défaut : état de fonctionnement","metric.trip_output_current":"Instantané défaut : courant de sortie","metric.trip_dc_input_voltage":"Instantané défaut : bus continu","metric.trip_output_voltage":"Instantané défaut : tension de sortie","metric.past_trip_1":"Défaut mémorisé 1","metric.past_trip_2":"Défaut mémorisé 2","metric.past_trip_3":"Défaut mémorisé 3","metric.past_trip_4":"Défaut mémorisé 4"},
  ja:{"metric.input_terminal_status":"入力端子 F/R/S1/S2/S3","metric.fm_analog_output":"FMアナログ出力","metric.trip_output_frequency":"トリップ時出力周波数","metric.trip_operating_status":"トリップ時運転状態","metric.trip_output_current":"トリップ時出力電流","metric.trip_dc_input_voltage":"トリップ時直流リンク電圧","metric.trip_output_voltage":"トリップ時出力電圧","metric.past_trip_1":"保存トリップ1","metric.past_trip_2":"保存トリップ2","metric.past_trip_3":"保存トリップ3","metric.past_trip_4":"保存トリップ4"}
};
for (const code of Object.keys(CHANNEL_METRIC_I18N)) Object.assign(I18N[code], CHANNEL_METRIC_I18N[code]);
const BACKUP_I18N = {
  en:{"backup.eyebrow":"Parameters","backup.title":"PCM002Z parameter backup","backup.help":"Select an original PCM002Z .pcm file for the configured model. TMM uses its register list as a template and reads a new complete dataset.","backup.inverter":"Inverter","backup.template":"PCM template","backup.create":"Read parameter backup","backup.accepted":"Backup started. Monitoring pauses while the parameters are read.","backup.complete":"Backup complete","backup.partial":"Partial Modbus backup","backup.failed":"Backup failed","backup.select":"Select a PCM template first."},
  de:{"backup.eyebrow":"Parameter","backup.title":"PCM002Z-Parametersicherung","backup.help":"Eine originale PCM002Z-.pcm-Datei des konfigurierten Modells auswählen. TMM verwendet deren Registerliste als Vorlage und liest einen neuen vollständigen Datensatz.","backup.inverter":"Umrichter","backup.template":"PCM-Vorlage","backup.create":"Parametersicherung auslesen","backup.accepted":"Sicherung gestartet. Die Überwachung pausiert während des Auslesens.","backup.complete":"Sicherung abgeschlossen","backup.partial":"Modbus-Teilsicherung","backup.failed":"Sicherung fehlgeschlagen","backup.select":"Zuerst eine PCM-Vorlage auswählen."},
  fr:{"backup.eyebrow":"Paramètres","backup.title":"Sauvegarde de paramètres PCM002Z","backup.help":"Sélectionnez un fichier .pcm PCM002Z original du modèle configuré. TMM utilise sa liste de registres pour lire un nouveau jeu complet.","backup.inverter":"Variateur","backup.template":"Modèle PCM","backup.create":"Lire la sauvegarde","backup.accepted":"Sauvegarde démarrée. La surveillance est suspendue pendant la lecture.","backup.complete":"Sauvegarde terminée","backup.partial":"Sauvegarde Modbus partielle","backup.failed":"Échec de la sauvegarde","backup.select":"Sélectionnez d’abord un modèle PCM."},
  ja:{"backup.eyebrow":"パラメーター","backup.title":"PCM002Zパラメーターバックアップ","backup.help":"設定モデル用の元のPCM002Z .pcmファイルを選択してください。そのレジスター一覧を使って新しい完全なデータを読み取ります。","backup.inverter":"インバーター","backup.template":"PCMテンプレート","backup.create":"パラメーターを読み取る","backup.accepted":"バックアップを開始しました。読み取り中は監視を一時停止します。","backup.complete":"バックアップ完了","backup.partial":"Modbus部分バックアップ","backup.failed":"バックアップ失敗","backup.select":"先にPCMテンプレートを選択してください。"}
};
for (const code of Object.keys(BACKUP_I18N)) Object.assign(I18N[code], BACKUP_I18N[code]);
Object.assign(I18N.en,{"backup.delete":"Delete","backup.deleteConfirm":"Delete this parameter-backup file permanently? A paired report is deleted together.","backup.deleted":"Backup deleted"});
Object.assign(I18N.de,{"backup.delete":"Löschen","backup.deleteConfirm":"Diese Parametersicherungsdatei dauerhaft löschen? Ein zugehöriger Bericht wird ebenfalls gelöscht.","backup.deleted":"Sicherung gelöscht"});
Object.assign(I18N.fr,{"backup.delete":"Supprimer","backup.deleteConfirm":"Supprimer définitivement ce fichier de sauvegarde de paramètres ? Le rapport associé sera également supprimé.","backup.deleted":"Sauvegarde supprimée"});
Object.assign(I18N.ja,{"backup.delete":"削除","backup.deleteConfirm":"このパラメーターバックアップファイルを完全に削除しますか？関連レポートも削除されます。","backup.deleted":"バックアップを削除しました"});
Object.assign(I18N.en,{"backup.partialTag":"partial","backup.completeTag":"complete"});
Object.assign(I18N.de,{"backup.partialTag":"teilweise","backup.completeTag":"vollständig"});
Object.assign(I18N.fr,{"backup.partialTag":"partielle","backup.completeTag":"complète"});
Object.assign(I18N.ja,{"backup.partialTag":"部分","backup.completeTag":"完全"});
Object.assign(I18N.en,{"backup.currentTag":"current reference"});
Object.assign(I18N.de,{"backup.currentTag":"aktuelle Referenz"});
Object.assign(I18N.fr,{"backup.currentTag":"référence actuelle"});
Object.assign(I18N.ja,{"backup.currentTag":"現在の参照"});
const PREVIEW_I18N = {
  en:{"preview.eyebrow":"Import","preview.title":"PCM import preview","preview.help":"Compares a PCM file with the latest backup. This preview never writes to the inverter.","preview.inverter":"Inverter","preview.file":"Target PCM file","preview.compare":"Compare safely","preview.address":"Address","preview.current":"Current","preview.target":"Target","preview.class":"Class","preview.none":"No value differences found.","preview.select":"Select a target PCM file first.","preview.candidate":"Configuration candidate","preview.communication":"Communication — blocked","preview.special":"Special parameter — blocked","preview.monitor":"Monitor/internal — blocked","preview.unsupported":"Not readable via Modbus — blocked"},
  de:{"preview.eyebrow":"Import","preview.title":"PCM-Importvorschau","preview.help":"Vergleicht eine PCM-Datei mit der jüngsten Sicherung. Diese Vorschau schreibt niemals in den Umrichter.","preview.inverter":"Umrichter","preview.file":"Ziel-PCM-Datei","preview.compare":"Sicher vergleichen","preview.address":"Adresse","preview.current":"Aktuell","preview.target":"Ziel","preview.class":"Klasse","preview.none":"Keine Wertunterschiede gefunden.","preview.select":"Zuerst eine Ziel-PCM-Datei auswählen.","preview.candidate":"Konfigurationskandidat","preview.communication":"Kommunikation — gesperrt","preview.special":"Spezialparameter — gesperrt","preview.monitor":"Monitor/intern — gesperrt","preview.unsupported":"Nicht über Modbus lesbar — gesperrt"},
  fr:{"preview.eyebrow":"Import","preview.title":"Aperçu d’import PCM","preview.help":"Compare un fichier PCM à la sauvegarde la plus récente. Aucun paramètre n’est écrit.","preview.inverter":"Variateur","preview.file":"Fichier PCM cible","preview.compare":"Comparer en sécurité","preview.address":"Adresse","preview.current":"Actuel","preview.target":"Cible","preview.class":"Classe","preview.none":"Aucune différence trouvée.","preview.select":"Sélectionnez d’abord un fichier PCM cible.","preview.candidate":"Candidat de configuration","preview.communication":"Communication — bloqué","preview.special":"Paramètre spécial — bloqué","preview.monitor":"Moniteur/interne — bloqué","preview.unsupported":"Illisible via Modbus — bloqué"},
  ja:{"preview.eyebrow":"インポート","preview.title":"PCMインポートプレビュー","preview.help":"PCMファイルを最新バックアップと比較します。インバーターへの書き込みは行いません。","preview.inverter":"インバーター","preview.file":"対象PCMファイル","preview.compare":"安全に比較","preview.address":"アドレス","preview.current":"現在値","preview.target":"対象値","preview.class":"分類","preview.none":"値の差はありません。","preview.select":"対象PCMファイルを選択してください。","preview.candidate":"設定候補","preview.communication":"通信設定 — ブロック","preview.special":"特殊パラメーター — ブロック","preview.monitor":"モニター/内部 — ブロック","preview.unsupported":"Modbus読取不可 — ブロック"}
};
for (const code of Object.keys(PREVIEW_I18N)) Object.assign(I18N[code], PREVIEW_I18N[code]);
Object.assign(I18N.en,{"preview.csv":"Matching PCM002Z CSV limits"});
Object.assign(I18N.de,{"preview.csv":"Passende PCM002Z-CSV-Grenzen"});
Object.assign(I18N.fr,{"preview.csv":"Limites CSV PCM002Z correspondantes"});
Object.assign(I18N.ja,{"preview.csv":"対応するPCM002Z CSV制限"});
Object.assign(I18N.en,{"preview.backupAge":"Backup age:","preview.minutes":"min","preview.stale":"Backup is too old for writing; create a new backup."});
Object.assign(I18N.de,{"preview.backupAge":"Alter der Sicherung:","preview.minutes":"Min.","preview.stale":"Sicherung ist für das Schreiben zu alt; neue Sicherung erstellen."});
Object.assign(I18N.fr,{"preview.backupAge":"Âge de la sauvegarde :","preview.minutes":"min","preview.stale":"Sauvegarde trop ancienne pour l’écriture ; créez une nouvelle sauvegarde."});
Object.assign(I18N.ja,{"preview.backupAge":"バックアップ経過時間：","preview.minutes":"分","preview.stale":"書込みにはバックアップが古すぎます。新しいバックアップを作成してください。"});
Object.assign(I18N.en,{"preview.filter":"Show","preview.filterAll":"All changes","preview.filterCandidates":"Configuration candidates only"});
Object.assign(I18N.de,{"preview.filter":"Anzeigen","preview.filterAll":"Alle Änderungen","preview.filterCandidates":"Nur Konfigurationskandidaten"});
Object.assign(I18N.fr,{"preview.filter":"Afficher","preview.filterAll":"Toutes les modifications","preview.filterCandidates":"Candidats de configuration uniquement"});
Object.assign(I18N.ja,{"preview.filter":"表示","preview.filterAll":"すべての変更","preview.filterCandidates":"設定候補のみ"});
const WRITE_I18N = {
  en:{"write.title":"Write selected parameters","write.help":"Up to 32 configuration candidates are written sequentially. Before every parameter, TMM confirms standstill three times, writes, reads back, and logs the change. A failed batch is never rolled back automatically.","write.confirm":"Enter WRITE followed by all selected addresses in ascending order","write.button":"Write selected parameters","write.select":"Select between 1 and 32 configuration candidates.","write.accepted":"Write request accepted; waiting for the collector.","write.complete":"Parameters written and verified","write.partial":"Partial write: verified changes remain applied","write.failed":"Write rejected or failed"},
  de:{"write.title":"Ausgewählte Parameter schreiben","write.help":"Bis zu 32 Konfigurationskandidaten werden nacheinander geschrieben. Vor jedem Parameter prüft TMM dreimal den Stillstand, schreibt, liest zurück und protokolliert die Änderung. Ein fehlgeschlagener Stapel wird niemals automatisch zurückgerollt.","write.confirm":"WRITE gefolgt von allen ausgewählten Adressen in aufsteigender Reihenfolge eingeben","write.button":"Ausgewählte Parameter schreiben","write.select":"1 bis 32 Konfigurationskandidaten auswählen.","write.accepted":"Schreibauftrag angenommen; warte auf den Collector.","write.complete":"Parameter geschrieben und verifiziert","write.partial":"Teilschreibung: Verifizierte Änderungen bleiben übernommen","write.failed":"Schreiben abgelehnt oder fehlgeschlagen"},
  fr:{"write.title":"Écrire les paramètres sélectionnés","write.help":"Jusqu’à 32 candidats de configuration sont écrits séquentiellement. Avant chaque paramètre, TMM confirme trois fois l’arrêt, écrit, relit et journalise la modification. Un lot en échec n’est jamais annulé automatiquement.","write.confirm":"Saisissez WRITE suivi de toutes les adresses sélectionnées, dans l’ordre croissant","write.button":"Écrire les paramètres sélectionnés","write.select":"Sélectionnez entre 1 et 32 candidats de configuration.","write.accepted":"Demande acceptée ; attente du collecteur.","write.complete":"Paramètres écrits et vérifiés","write.partial":"Écriture partielle : les modifications vérifiées restent appliquées","write.failed":"Écriture refusée ou échouée"},
  ja:{"write.title":"選択したパラメーターを書き込む","write.help":"最大32個の設定候補を順に書き込みます。各パラメーターの前にTMMは停止を3回確認し、書込み、再読込み、記録します。失敗したバッチは自動的にロールバックされません。","write.confirm":"WRITE の後に選択したすべてのアドレスを昇順で入力","write.button":"選択パラメーターを書き込む","write.select":"設定候補を1～32個選択してください。","write.accepted":"書込み要求を受け付けました。コレクターを待っています。","write.complete":"パラメーターを書込み、検証しました","write.partial":"部分書込み：検証済みの変更は適用されたままです","write.failed":"書込みが拒否または失敗しました"}
};
for (const code of Object.keys(WRITE_I18N)) Object.assign(I18N[code], WRITE_I18N[code]);
Object.assign(I18N.en,{"write.none":"No configuration candidates selected.","write.tooMany":"More than 32 candidates selected; reduce the selection.","write.selected":"Selected:","write.expected":"Required confirmation:"});
Object.assign(I18N.de,{"write.none":"Keine Konfigurationskandidaten ausgewählt.","write.tooMany":"Mehr als 32 Kandidaten ausgewählt; Auswahl reduzieren.","write.selected":"Ausgewählt:","write.expected":"Erforderliche Bestätigung:"});
Object.assign(I18N.fr,{"write.none":"Aucun candidat de configuration sélectionné.","write.tooMany":"Plus de 32 candidats sélectionnés ; réduisez la sélection.","write.selected":"Sélection :","write.expected":"Confirmation requise :"});
Object.assign(I18N.ja,{"write.none":"設定候補が選択されていません。","write.tooMany":"32個を超える候補が選択されています。選択を減らしてください。","write.selected":"選択：","write.expected":"必要な確認："});
Object.assign(I18N.en,{"write.backupTooOld":"Writing is locked: create a current parameter backup first."});
Object.assign(I18N.de,{"write.backupTooOld":"Schreiben gesperrt: Zuerst eine aktuelle Parametersicherung erstellen."});
Object.assign(I18N.fr,{"write.backupTooOld":"Écriture verrouillée : créez d’abord une sauvegarde de paramètres actuelle."});
Object.assign(I18N.ja,{"write.backupTooOld":"書込みはロックされています。先に現在のパラメーターバックアップを作成してください。"});
Object.assign(I18N.en,{"write.previewOutdated":"Writing is locked: run the import preview again for the selected inverter."});
Object.assign(I18N.de,{"write.previewOutdated":"Schreiben gesperrt: Importvorschau für den ausgewählten Umrichter erneut ausführen."});
Object.assign(I18N.fr,{"write.previewOutdated":"Écriture verrouillée : relancez l’aperçu d’import pour le variateur sélectionné."});
Object.assign(I18N.ja,{"write.previewOutdated":"書込みはロックされています。選択したインバーターでインポートプレビューを再実行してください。"});
Object.assign(I18N.en,{"write.preflight":"Check write preconditions","write.preflightAccepted":"Preflight accepted; waiting for the collector.","write.preflightReady":"Write preconditions confirmed. The write itself will check again.","write.preflightBlocked":"Write preconditions blocked"});
Object.assign(I18N.de,{"write.preflight":"Schreibvoraussetzungen prüfen","write.preflightAccepted":"Prüfung angenommen; warte auf den Collector.","write.preflightReady":"Schreibvoraussetzungen bestätigt. Beim Schreiben wird erneut geprüft.","write.preflightBlocked":"Schreibvoraussetzungen gesperrt"});
Object.assign(I18N.fr,{"write.preflight":"Vérifier les conditions d’écriture","write.preflightAccepted":"Vérification acceptée ; attente du collecteur.","write.preflightReady":"Conditions d’écriture confirmées. L’écriture les vérifiera de nouveau.","write.preflightBlocked":"Conditions d’écriture bloquées"});
Object.assign(I18N.ja,{"write.preflight":"書込み条件を確認","write.preflightAccepted":"確認を受け付けました。コレクターを待っています。","write.preflightReady":"書込み条件を確認しました。書込み時に再確認します。","write.preflightBlocked":"書込み条件がブロックされています"});
const AUDIT_I18N = {
  en:{"audit.title":"Verified parameter changes","audit.help":"The latest verified writes, retained in the current SQLite recording.","audit.export":"Export audit CSV","audit.time":"Time","audit.inverter":"Inverter","audit.address":"Address","audit.old":"Old","audit.new":"New","audit.verified":"Verified","audit.empty":"No verified parameter changes in this recording."},
  de:{"audit.title":"Verifizierte Parameteränderungen","audit.help":"Die jüngsten verifizierten Schreibvorgänge der aktuellen SQLite-Aufzeichnung.","audit.export":"Audit-CSV exportieren","audit.time":"Zeit","audit.inverter":"Umrichter","audit.address":"Adresse","audit.old":"Alt","audit.new":"Neu","audit.verified":"Verifiziert","audit.empty":"Keine verifizierten Parameteränderungen in dieser Aufzeichnung."},
  fr:{"audit.title":"Modifications de paramètres vérifiées","audit.help":"Les dernières écritures vérifiées, conservées dans l’enregistrement SQLite actuel.","audit.export":"Exporter le journal CSV","audit.time":"Heure","audit.inverter":"Variateur","audit.address":"Adresse","audit.old":"Ancien","audit.new":"Nouveau","audit.verified":"Vérifié","audit.empty":"Aucune modification de paramètre vérifiée dans cet enregistrement."},
  ja:{"audit.title":"検証済みパラメーター変更","audit.help":"現在のSQLite記録に保存されている最新の検証済み書込みです。","audit.export":"監査CSVを出力","audit.time":"時刻","audit.inverter":"インバーター","audit.address":"アドレス","audit.old":"旧値","audit.new":"新値","audit.verified":"検証値","audit.empty":"この記録には検証済みパラメーター変更がありません。"}
};
for (const code of Object.keys(AUDIT_I18N)) Object.assign(I18N[code], AUDIT_I18N[code]);

const SECTION_I18N = {
  en:{"sections.collapse":"Collapse","sections.expand":"Expand","sections.collapseAll":"Collapse all sections","sections.expandAll":"Expand all sections","sections.reorder":"Drag to reorder category"},
  de:{"sections.collapse":"Einklappen","sections.expand":"Ausklappen","sections.collapseAll":"Alle Kategorien einklappen","sections.expandAll":"Alle Kategorien ausklappen","sections.reorder":"Kategorie zum Sortieren ziehen"},
  fr:{"sections.collapse":"Réduire","sections.expand":"Développer","sections.collapseAll":"Réduire toutes les catégories","sections.expandAll":"Développer toutes les catégories","sections.reorder":"Faites glisser pour réorganiser la catégorie"},
  ja:{"sections.collapse":"折りたたむ","sections.expand":"展開","sections.collapseAll":"すべてのカテゴリを折りたたむ","sections.expandAll":"すべてのカテゴリを展開","sections.reorder":"ドラッグしてカテゴリを並べ替え"}
};
for (const code of Object.keys(SECTION_I18N)) Object.assign(I18N[code], SECTION_I18N[code]);

let language = localStorage.getItem("tmm-language") || "en";
let measurementHints = localStorage.getItem("tmm-measurement-hints") === "true";
const t = (key) => I18N[language]?.[key] || I18N.en[key] || key;
const metricName = (key) => t(`metric.${key}`) || key.replaceAll("_", " ");
function measurementHintText(key, item = {}) {
  const labels = {
    en:{monitor:"Toshiba read-only monitor",scale:"Scaling",parameter:"Related parameter",none:"no writable parameter (monitor value)",derived:"Derived value"},
    de:{monitor:"Toshiba-Monitorwert, nur lesend",scale:"Skalierung",parameter:"Zugehöriger Parameter",none:"kein schreibbarer Parameter (Monitorwert)",derived:"Berechneter Wert"},
    fr:{monitor:"Moniteur Toshiba en lecture seule",scale:"Échelle",parameter:"Paramètre associé",none:"aucun paramètre inscriptible (valeur moniteur)",derived:"Valeur calculée"},
    ja:{monitor:"東芝読取り専用モニター",scale:"スケーリング",parameter:"関連パラメーター",none:"書込み可能なパラメーターなし（モニター値）",derived:"計算値"},
  }[language] || {};
  const derived = { machine_speed:"Engineering: machine-speed factor", actual_output_current:"Engineering: rated output current", actual_output_voltage:"Engineering: rated output voltage", calculated_motor_speed:"Toshiba FE90 calculated motor-speed monitor", actual_motor_torque:"Engineering reference and torque monitor", mechanical_power:"Calculated from torque and motor speed" }[key];
  const address = item.register_address || item.address || "—"; const scale = item.scale ?? "—"; const unit = item.unit || "raw";
  return `${metricName(key)}\n${derived ? labels.derived : labels.monitor}: ${address}\n${labels.scale}: raw × ${scale} ${unit}\n${labels.parameter}: ${derived || labels.none}`;
}
function appendMeasurementHint(parent, key, item) {
  const hint = document.createElement("button"); hint.type = "button"; hint.className = "measurement-hint"; hint.textContent = "ⓘ";
  hint.title = measurementHintText(key, item); hint.setAttribute("aria-label", hint.title); parent.append(hint);
}
function applyMeasurementHints() {
  document.body.classList.toggle("measurement-hints-visible", measurementHints);
  const toggle = $("#measurement-hints"); if (toggle) toggle.checked = measurementHints;
}
function applyLanguage() {
  document.documentElement.lang = language;
  document.querySelectorAll("[data-i18n]").forEach((element) => { element.textContent = t(element.dataset.i18n); });
  document.querySelector("#language").value = language;
  document.querySelectorAll(".section-drag-handle").forEach(handle => { handle.title = t("sections.reorder"); handle.setAttribute("aria-label", t("sections.reorder")); });
  refreshCollapsibleLabels();
}

const COLLAPSIBLE_SECTIONS_KEY = "tmm-collapsible-sections";
let collapsibleSections = [];
let sectionOrderDragging = false;

function collapsedSectionIds() {
  try { return new Set(JSON.parse(localStorage.getItem(COLLAPSIBLE_SECTIONS_KEY) || "[]")); }
  catch { return new Set(); }
}

function persistCollapsedSections() {
  localStorage.setItem(COLLAPSIBLE_SECTIONS_KEY, JSON.stringify(
    collapsibleSections.filter(section => section.classList.contains("is-collapsed")).map(section => section.dataset.sectionId)
  ));
}

function setSectionCollapsed(section, collapsed, persist = true) {
  section.classList.toggle("is-collapsed", collapsed);
  const toggle = section.querySelector(":scope > .section-heading .section-toggle");
  if (toggle) toggle.setAttribute("aria-expanded", String(!collapsed));
  if (!collapsed && section.dataset.sectionId === "history-title") requestAnimationFrame(() => renderChart(state.history));
  if (persist) persistCollapsedSections();
  refreshCollapsibleLabels();
}

function refreshCollapsibleLabels() {
  if (!collapsibleSections.length) return;
  for (const section of collapsibleSections) {
    const collapsed = section.classList.contains("is-collapsed");
    const toggle = section.querySelector(":scope > .section-heading .section-toggle");
    if (toggle) toggle.textContent = collapsed ? `+ ${t("sections.expand")}` : `− ${t("sections.collapse")}`;
  }
  const allButton = $("#section-toggle-all");
  if (allButton) {
    const allCollapsed = collapsibleSections.every(section => section.classList.contains("is-collapsed"));
    allButton.textContent = t(allCollapsed ? "sections.expandAll" : "sections.collapseAll");
  }
}

function initCollapsibleSections() {
  const saved = collapsedSectionIds();
  collapsibleSections = [...document.querySelectorAll("main > section")];
  for (const section of collapsibleSections) {
    const heading = section.querySelector(":scope > .section-heading");
    const title = heading?.querySelector("h2");
    if (!heading || !title) continue;
    const id = title.id || `section-${collapsibleSections.indexOf(section) + 1}`;
    section.dataset.sectionId = id;
    section.classList.add("collapsible-section");
    const content = document.createElement("div"); content.className = "section-content";
    for (const child of [...section.children]) if (child !== heading) content.append(child);
    section.append(content);
    const handle = document.createElement("button");
    handle.type = "button"; handle.className = "section-drag-handle"; handle.draggable = true;
    handle.textContent = "⠿"; handle.title = t("sections.reorder"); handle.setAttribute("aria-label", t("sections.reorder"));
    heading.prepend(handle);
    const toggle = document.createElement("button");
    toggle.type = "button"; toggle.className = "section-toggle";
    toggle.addEventListener("click", () => setSectionCollapsed(section, !section.classList.contains("is-collapsed")));
    heading.append(toggle);
    setSectionCollapsed(section, saved.has(id), false);
  }
  $("#section-toggle-all").addEventListener("click", () => {
    const collapse = !collapsibleSections.every(section => section.classList.contains("is-collapsed"));
    for (const section of collapsibleSections) setSectionCollapsed(section, collapse, false);
    persistCollapsedSections(); refreshCollapsibleLabels();
  });
  refreshCollapsibleLabels();
}

function dashboardSectionOrder() { return [...document.querySelectorAll("main > section")].map(section => section.dataset.sectionId); }
function applyDashboardSectionOrder(order) {
  const current = dashboardSectionOrder();
  if (!Array.isArray(order) || order.length !== current.length || new Set(order).size !== current.length || !order.every(id => current.includes(id))) return;
  const main = $("main"); const byId = new Map(collapsibleSections.map(section => [section.dataset.sectionId, section]));
  for (const id of order) main.append(byId.get(id));
  collapsibleSections = order.map(id => byId.get(id));
}
async function loadDashboardSectionOrder() {
  try { applyDashboardSectionOrder((await getJSON("/api/v1/dashboard-section-order")).order); }
  catch (error) { $("#last-error").textContent = error.message; }
}
async function saveDashboardSectionOrder() {
  try { await postJSON("/api/v1/dashboard-section-order", { order: dashboardSectionOrder() }); }
  catch (error) { $("#last-error").textContent = error.message; }
}
function installSectionDragAndDrop() {
  const main = $("main");
  main.addEventListener("dragstart", event => {
    const handle = event.target.closest(".section-drag-handle"); if (!handle) return;
    const section = handle.closest("section"); if (!section) return;
    sectionOrderDragging = true; section.classList.add("section-dragging");
    event.dataTransfer.effectAllowed = "move"; event.dataTransfer.setData("text/plain", section.dataset.sectionId);
  });
  main.addEventListener("dragover", event => {
    if (!sectionOrderDragging) return;
    const target = event.target.closest("section"); const dragged = main.querySelector(".section-dragging");
    if (!target || target.parentElement !== main || target === dragged) return;
    event.preventDefault(); main.querySelectorAll(".section-drop-target").forEach(section => section.classList.remove("section-drop-target"));
    target.classList.add("section-drop-target"); const rect = target.getBoundingClientRect();
    main.insertBefore(dragged, event.clientY < rect.top + rect.height / 2 ? target : target.nextSibling);
  });
  main.addEventListener("dragend", event => {
    const section = event.target.closest("section"); if (!section || !sectionOrderDragging) return;
    section.classList.remove("section-dragging"); main.querySelectorAll(".section-drop-target").forEach(entry => entry.classList.remove("section-drop-target"));
    collapsibleSections = [...main.querySelectorAll(":scope > section")]; sectionOrderDragging = false; saveDashboardSectionOrder();
  });
}
function renderFooter(metadata) {
  $("#footer-version").textContent = `Version ${metadata.version || "1.0.0"}`;
  const contact = metadata.contact || {};
  const name = String(contact.contact_name || "").trim();
  const rawUrl = String(contact.contact_url || "").trim();
  const row = $("#footer-contact");
  const link = $("#footer-contact-link");
  row.hidden = !name;
  link.textContent = name;
  link.removeAttribute("href");
  if (/^(https?:|mailto:)/i.test(rawUrl)) link.href = rawUrl;
  else if (rawUrl.includes("@") && !rawUrl.includes(" ")) link.href = `mailto:${rawUrl}`;
}
function localizedDecoded(item) {
  const raw = item.raw_value || 0;
  if (["operating_status", "trip_operating_status"].includes(item.metric)) {
    if (raw & (1 << 1)) return t("state.trip"); if (raw & (1 << 12)) return t("state.emergency"); if (raw & (1 << 2)) return t("state.alarm");
    if (raw & (1 << 10)) return raw & (1 << 9) ? t("state.reverse") : t("state.forward");
    return raw & (1 << 14) ? t("state.ready") : t("state.stopped");
  }
  if (item.metric.startsWith("alarm_information")) { const count = item.decoded?.active?.length || 0; return count ? `${count} ${t("alarm.active")}` : t("alarm.none"); }
  return item.decoded?.summary || "";
}

function thresholdSeverity(value, threshold) {
  if (!threshold || !Number.isFinite(Number(value))) return null;
  if (Number(value) >= Number(threshold.critical)) return "critical";
  if (Number(value) >= Number(threshold.warning)) return "warning";
  return null;
}

function renderAlerts(items, telemetry = {}, thresholds = { system: {}, metrics: {} }, storage = null) {
  const container = $("#alerts"); container.replaceChildren(); const messages = [];
  for (const item of items) {
    const threshold = thresholds.metrics?.[item.metric]; const severity = thresholdSeverity(item.value, threshold);
    if (severity) messages.push({ severity, source: item.inverter, label: metricName(item.metric), value: `${Number(item.value).toLocaleString(locale(), { maximumFractionDigits: 2 })} ${item.unit}`, threshold: threshold[severity] });
    if (["operating_status", "trip_code", "alarm_information_1", "alarm_information_2"].includes(item.metric) && ["warning", "critical"].includes(item.decoded?.severity)) {
      messages.push({ severity: item.decoded.severity, source: item.inverter, label: metricName(item.metric), value: localizedDecoded(item), threshold: null });
    }
  }
  const systemLabels = { cpu_percent: t("diag.hostCpu"), temperature_celsius: t("diag.temperature"), memory_percent: t("diag.hostMemory"), disk_percent: t("diag.disk") };
  for (const [key, threshold] of Object.entries(thresholds.system || {})) {
    const value = telemetry.system?.[key]; const severity = thresholdSeverity(value, threshold);
    if (severity) messages.push({ severity, source: t("alerts.system"), label: systemLabels[key] || key, value: `${Number(value).toLocaleString(locale(), { maximumFractionDigits: 1 })} ${key === "temperature_celsius" ? "°C" : "%"}`, threshold: threshold[severity] });
  }
  if (storage?.retention_exceeds_remaining_space) messages.push({ severity: "info", source: t("alerts.storage"), label: t("alerts.retentionRisk"), value: `${formatDuration(storage.estimated_seconds_to_full)} < ${Number(storage.retention_days).toLocaleString(locale())} ${t("storage.days")}`, threshold: null });
  const priority = { critical: 0, warning: 1, info: 2 };
  messages.sort((a, b) => priority[a.severity] - priority[b.severity]);
  const alertIndicator = $("#alert-indicator"); const highest = messages[0]?.severity || "clear";
  const alertDescription = messages.length ? `${messages.length} ${t(`alerts.${highest}`)}` : t("alerts.clear");
  alertIndicator.className = `alert-indicator ${highest}`; alertIndicator.title = alertDescription; alertIndicator.setAttribute("aria-label", alertDescription);
  $("#alert-indicator-count").textContent = messages.length.toLocaleString(locale());
  for (const message of messages) {
    const entry = document.createElement("article"); entry.className = `alert-message ${message.severity}`;
    const badge = document.createElement("strong"); badge.textContent = t(`alerts.${message.severity}`);
    const body = document.createElement("div"); const title = document.createElement("p"); title.className = "alert-title"; title.textContent = `${message.source} · ${message.label}`;
    const detail = document.createElement("p"); detail.className = "alert-detail"; detail.textContent = message.threshold == null ? message.value : `${message.value} · ${t("alerts.threshold")} ${Number(message.threshold).toLocaleString(locale())}`;
    body.append(title, detail); entry.append(badge, body); container.append(entry);
  }
  if (!messages.length) { const clear = document.createElement("p"); clear.className = "alert-clear"; clear.textContent = t("alerts.clear"); container.append(clear); }
}

const state = { metric: "output_frequency", inverter: null, latest: [], history: [], metadata: null, telemetry: null, storage: null, storageRefreshedAt: 0, engineering: [], channels: [], liveCardOrder: [], liveOrderLoaded: false, liveOrderDragging: false, previewBackupStale: false, previewTargetSha: null, previewInverter: null };
let refreshRunning = false;
const $ = (selector) => document.querySelector(selector);
const locale = () => ({ en:"en-US", de:"de-DE", fr:"fr-FR", ja:"ja-JP" })[language];
const timeText = (iso) => new Intl.DateTimeFormat(locale(), { dateStyle: "short", timeStyle: "medium" }).format(new Date(iso));

async function getJSON(url) {
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
  return response.json();
}
async function postJSON(url, body) {
  const response = await fetch(url, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(body) });
  if (!response.ok) throw new Error(`${response.status} ${await response.text()}`);
  return response.json();
}
async function deleteJSON(url) {
  const response = await fetch(url, { method:"DELETE" });
  if (!response.ok) throw new Error(`${response.status} ${await response.text()}`);
  return response.json();
}

function confirmAction(button) {
  if (!button) return;
  button.classList.add("action-confirmed");
  clearTimeout(button._confirmationTimer);
  button._confirmationTimer = setTimeout(() => button.classList.remove("action-confirmed"), 850);
}
function showTemporarySuccess(selector, message, button) {
  const result = $(selector); result.textContent = message; result.classList.add("temporary-success"); confirmAction(button);
  clearTimeout(result._messageTimer);
  result._messageTimer = setTimeout(() => {
    if (result.textContent === message) { result.textContent = ""; result.classList.remove("temporary-success"); }
  }, 5000);
}
function showPersistentResult(selector, message) {
  const result = $(selector); clearTimeout(result._messageTimer); result.classList.remove("temporary-success"); result.textContent = message;
}

async function refreshRecording() {
  const data = await getJSON("/api/v1/recording");
  $("#recording-current").textContent = data.reference || "—";
  if (data.last_operation?.status === "complete") $("#recording-result").textContent = t("recording.complete");
  else if (data.last_operation?.status === "error") $("#recording-result").textContent = `${t("recording.failed")}: ${data.last_operation.detail}`;
}

async function requestRecording(action) {
  const reference = $("#recording-reference").value.trim();
  if (!reference) { $("#recording-result").textContent = t("recording.referenceRequired"); return; }
  const confirmation = action === "delete" ? $("#recording-delete-confirmation").value : "";
  try {
    await postJSON("/api/v1/recording/reinitialize", { action, reference, confirmation });
    $("#recording-result").textContent = t("recording.accepted");
    setTimeout(refreshRecording, 2500);
  } catch (error) { $("#recording-result").textContent = `${t("recording.failed")}: ${error.message}`; }
}

function showEngineering(name) {
  const item = state.engineering.find(entry => entry.name === name); if (!item) return;
  const values = item.engineering || {};
  $("#engineering-factor").value = values.machine_speed_factor ?? "";
  $("#engineering-unit").value = values.machine_speed_unit ?? "rpm";
  $("#engineering-current").value = values.rated_output_current_a ?? "";
  $("#engineering-voltage").value = values.rated_output_voltage_v ?? "";
  $("#engineering-motor-power").value = values.motor_rated_power_kw ?? "";
  $("#engineering-motor-speed").value = values.motor_rated_speed_rpm ?? "";
}
async function loadEngineering() {
  const data = await getJSON("/api/v1/engineering"); state.engineering = data.inverters || [];
  const select = $("#engineering-inverter"); select.replaceChildren();
  for (const item of state.engineering) select.add(new Option(`${item.name} · ${item.model}`, item.name));
  showEngineering(select.value);
}
async function saveEngineering(event) {
  const engineering = {
    machine_speed_factor:Number($("#engineering-factor").value), machine_speed_unit:$("#engineering-unit").value.trim(),
    rated_output_current_a:Number($("#engineering-current").value), rated_output_voltage_v:Number($("#engineering-voltage").value),
    motor_rated_power_kw:$("#engineering-motor-power").value.trim(), motor_rated_speed_rpm:$("#engineering-motor-speed").value.trim(),
  };
  const motorPairEmpty=!engineering.motor_rated_power_kw&&!engineering.motor_rated_speed_rpm;
  const motorPairValid=Number(engineering.motor_rated_power_kw)>0&&Number(engineering.motor_rated_speed_rpm)>0;
  if (!engineering.machine_speed_unit || ![engineering.machine_speed_factor,engineering.rated_output_current_a,engineering.rated_output_voltage_v].every(value=>Number.isFinite(value)&&value>0) || (!motorPairEmpty&&!motorPairValid)) {
    showPersistentResult("#engineering-result",t("engineering.invalid")); return;
  }
  try {
    await postJSON("/api/v1/engineering", {inverter:$("#engineering-inverter").value, engineering});
    showTemporarySuccess("#engineering-result",t("engineering.saved"),event?.currentTarget); await loadEngineering();
  } catch(error) { showPersistentResult("#engineering-result",`${t("recording.failed")}: ${error.message}`); }
}

function showChannels(name) {
  const item=state.channels.find(entry=>entry.name===name); const container=$("#channel-list"); container.replaceChildren();
  if (!item) return;
  for (const channel of item.channels) {
    const row=document.createElement("div"); row.className=`channel-row ${channel.protected ? "protected" : ""}`;
    const text=document.createElement("div"); const title=document.createElement("strong"); title.textContent=metricName(channel.key); appendMeasurementHint(title, channel.key, channel);
    const meta=document.createElement("small"); meta.textContent=channel.protected ? t("channels.protected") : `${channel.sampling} · ${channel.unit}`; text.append(title,meta);
    const select=document.createElement("select"); select.dataset.channel=channel.key;
    for (const mode of ["off","live","record","hide"]) select.add(new Option(t(`channels.${mode}`),mode));
    select.value=channel.mode; select.disabled=channel.protected; row.append(text,select); container.append(row);
  }
}
async function loadChannels() {
  const data=await getJSON("/api/v1/channels"); state.channels=data.inverters || [];
  const select=$("#channels-inverter"); select.replaceChildren();
  for (const item of state.channels) select.add(new Option(`${item.name} · ${item.model}`,item.name));
  showChannels(select.value);
  if (state.latest.length) { renderIO(state.latest); renderFaultMemory(state.latest); }
  if (state.history.length < 2) renderChart(state.history);
}
function appendChannelEnableHint(container, keys, mode, fallback) {
  const candidates = keys.filter(key => state.channels.some(device => device.channels.some(channel => channel.key === key)));
  const hint = document.createElement("p");
  if (!candidates.length) { hint.className = "hint"; hint.textContent = fallback; container.append(hint); return; }
  const record = mode === "record";
  hint.className = "hint channel-enable-hint";
  hint.textContent = `${t(record ? "channels.enableRecordPrefix" : "channels.enableLivePrefix")} ${candidates.map(metricName).join(", ")} ${t(record ? "channels.enableRecordSuffix" : "channels.enableLiveSuffix")}`;
  container.append(hint);
}
async function saveChannels(event) {
  const channels=Object.fromEntries([...document.querySelectorAll("#channel-list select[data-channel]")].map(select=>[select.dataset.channel,select.value]));
  try {
    await postJSON("/api/v1/channels",{inverter:$("#channels-inverter").value,channels});
    showTemporarySuccess("#channels-result",t("channels.saved"),event?.currentTarget);
    // Off is a display choice as well as a collector choice.  Rebuild the
    // metric list now, rather than retaining an old selected snapshot until a
    // complete browser reload.
    state.metadata=null; state.history=[]; $("#metric").replaceChildren(); $("#export-selected").hidden=true;
    await loadChannels(); await refresh();
  }
  catch(error) { showPersistentResult("#channels-result",`${t("recording.failed")}: ${error.message}`); }
}
async function refreshParameterBackups() {
  const inverter=$("#backup-inverter").value; const suffix=inverter ? `?inverter=${encodeURIComponent(inverter)}` : ""; const data=await getJSON(`/api/v1/parameter-backups${suffix}`); const result=$("#backup-result");
  if (data.status==="complete") result.textContent=`${t("backup.complete")}: ${data.records} · ${data.file}`;
  else if (data.status==="complete_with_warnings") result.textContent=`${t("backup.partial")}: ${data.refreshed_records}/${data.records} · ${data.retained_records} retained from template · ${data.file}`;
  else if (data.status==="error") result.textContent=`${t("backup.failed")}: ${data.detail}`;
  const files=$("#backup-files"); files.replaceChildren();
  for (const item of data.files || []) { const entry=document.createElement("span"); entry.className="backup-file"; const link=document.createElement("a"); link.href=`/api/v1/parameter-backups/${encodeURIComponent(item.name)}`; const modified=item.modified_at ? timeText(item.modified_at) : "—"; link.textContent=`${item.name} · ${modified} · ${item.current ? t("backup.currentTag") : item.partial ? t("backup.partialTag") : t("backup.completeTag")} · ${formatBytes(item.bytes)}`; const remove=document.createElement("button"); remove.type="button"; remove.textContent=t("backup.delete"); remove.addEventListener("click",async()=>{ if (!confirm(`${t("backup.deleteConfirm")}\n${item.name}`)) return; try { await deleteJSON(`/api/v1/parameter-backups/${encodeURIComponent(item.name)}`); result.textContent=`${t("backup.deleted")}: ${item.name}`; await refreshParameterBackups(); } catch(error) { result.textContent=`${t("backup.failed")}: ${error.message}`; } }); entry.append(link,remove); files.append(entry); }
}
async function fileToBase64(file) {
  const bytes=new Uint8Array(await file.arrayBuffer()); let binary="";
  for (let offset=0; offset<bytes.length; offset+=8192) binary+=String.fromCharCode(...bytes.subarray(offset,offset+8192));
  return btoa(binary);
}
async function createParameterBackup() {
  const file=$("#backup-template").files[0]; if (!file) { $("#backup-result").textContent=t("backup.select"); return; }
  if (file.size < 1 || file.size > 300000) { $("#backup-result").textContent=`${t("backup.failed")}: invalid file size (${formatBytes(file.size)})`; return; }
  try {
    await postJSON("/api/v1/parameter-backups",{inverter:$("#backup-inverter").value,content_base64:await fileToBase64(file)}); $("#backup-result").textContent=t("backup.accepted");
  }
  catch(error) { $("#backup-result").textContent=`${t("backup.failed")}: ${error.message}`; }
}
async function createImportPreview() {
  const file=$("#preview-file").files[0]; if (!file) { $("#preview-result").textContent=t("preview.select"); return; }
  state.previewBackupStale=false; state.previewTargetSha=null; state.previewInverter=null;
  try {
    const data=await postJSON("/api/v1/parameter-import-preview",{inverter:$("#preview-inverter").value,content_base64:await fileToBase64(file)});
    const table=$("#preview-table"); const body=table.querySelector("tbody"); body.replaceChildren();
    for (const row of data.changes) { const tr=document.createElement("tr"); tr.dataset.class=row.classification; const select=document.createElement("input"); select.type="checkbox"; select.value=row.address; select.disabled=!row.selectable; select.addEventListener("change",updateWriteSelection); const selectCell=document.createElement("td"); selectCell.append(select); tr.append(selectCell); for (const value of [row.address,row.current,row.target,t(`preview.${row.classification}`)]) { const td=document.createElement("td"); td.textContent=value; tr.append(td); } body.append(tr); }
    state.previewBackupStale=Boolean(data.backup_stale); state.previewTargetSha=data.target_sha256 || null; state.previewInverter=data.inverter || null; table.hidden=!data.changes.length; const age=Math.ceil((data.current_backup_age_seconds || 0)/60); const ageText=`${t("preview.backupAge")} ${age} ${t("preview.minutes")}`;
    $("#preview-result").textContent=data.changes.length ? `${data.changes.length} change(s) · ${data.current_file} · ${ageText}${data.backup_stale ? ` · ${t("preview.stale")}` : ""}` : t("preview.none");
    filterImportPreview(); updateWriteSelection();
  } catch(error) { state.previewBackupStale=true; $("#preview-result").textContent=`${t("backup.failed")}: ${error.message}`; updateWriteSelection(); }
}
function updateWriteSelection() {
  const addresses=[...document.querySelectorAll('#preview-table input[type="checkbox"]:checked')].map((item)=>item.value).sort();
  const selection=$("#write-selection"); const button=$("#write-selected");
  if (state.previewInverter && state.previewInverter !== $("#preview-inverter").value) { selection.textContent=t("write.previewOutdated"); button.disabled=true; return; }
  if (state.previewBackupStale) { selection.textContent=t("write.backupTooOld"); button.disabled=true; return; }
  if (!addresses.length) { selection.textContent=t("write.none"); button.disabled=true; return; }
  if (addresses.length>32) { selection.textContent=t("write.tooMany"); button.disabled=true; return; }
  selection.textContent=`${t("write.selected")} ${addresses.length} · ${t("write.expected")} WRITE ${addresses.join(" ")}`;
  button.disabled=false;
}
function filterImportPreview() {
  const candidatesOnly=$("#preview-filter").value === "candidate";
  for (const row of document.querySelectorAll("#preview-table tbody tr")) row.hidden = candidatesOnly && row.dataset.class !== "candidate";
}
async function writeSelectedParameter() {
  const selected=[...document.querySelectorAll('#preview-table input[type="checkbox"]:checked')];
  if (!selected.length || selected.length>32) { $("#write-result").textContent=t("write.select"); return; }
  const file=$("#preview-file").files[0]; const csvFile=$("#preview-csv").files[0]; const addresses=selected.map((item)=>item.value).sort(); const confirmation=$("#write-confirmation").value.trim();
  if (!csvFile) { $("#write-result").textContent="Select the matching PCM002Z CSV limits file."; return; }
  try { await postJSON("/api/v1/parameter-write",{inverter:$("#preview-inverter").value,addresses,confirmation,preview_sha256:state.previewTargetSha,content_base64:await fileToBase64(file),csv_base64:await fileToBase64(csvFile)}); $("#write-result").textContent=`${t("write.accepted")} (${addresses.length})`; }
  catch(error) { $("#write-result").textContent=`${t("write.failed")}: ${error.message}`; }
}
async function requestWritePreflight() {
  try { await postJSON("/api/v1/parameter-preflight",{inverter:$("#preview-inverter").value}); $("#write-preflight-result").textContent=t("write.preflightAccepted"); }
  catch(error) { $("#write-preflight-result").textContent=`${t("write.preflightBlocked")}: ${error.message}`; }
}
async function refreshWritePreflight() {
  const data=await getJSON("/api/v1/parameter-preflight");
  if (data.status==="ready") $("#write-preflight-result").textContent=t("write.preflightReady");
  else if (data.status==="blocked" || data.status==="error") $("#write-preflight-result").textContent=`${t("write.preflightBlocked")}: ${data.detail || ""}`;
}
async function refreshWriteStatus() {
  const data=await getJSON("/api/v1/parameter-write"); const changes=data.changes||[]; const count=changes.length;
  const detail=changes.map((item)=>`${item.address}: ${item.old} → ${item.new}`).join(" · ");
  if(data.status==="complete") $("#write-result").textContent=`${t("write.complete")}: ${count} parameter(s)${detail ? ` · ${detail}` : ""}`;
  else if(data.status==="partial") $("#write-result").textContent=`${t("write.partial")}: ${count} parameter(s)${detail ? ` · ${detail}` : ""}. ${data.detail}`;
  else if(data.status==="error") $("#write-result").textContent=`${t("write.failed")}: ${data.detail}`;
}
async function refreshParameterAudit() {
  const data=await getJSON("/api/v1/parameter-changes"); const body=$("#parameter-audit-table tbody"); body.replaceChildren();
  for (const item of data.items || []) { const row=document.createElement("tr"); for (const value of [new Date(item.changed_at).toLocaleString(locale()),item.inverter,item.address,item.old,item.new,item.verified]) { const cell=document.createElement("td"); cell.textContent=value; row.append(cell); } body.append(row); }
  $("#parameter-audit-empty").textContent=(data.items||[]).length ? "" : t("audit.empty");
}

function renderCards(items, thresholds = {}) {
  const cards = $("#cards");
  cards.replaceChildren();
  const special = new Set(["communication_status", "input_terminal_status", "fm_analog_output", "trip_code", "trip_output_frequency", "trip_operating_status", "trip_output_current", "trip_dc_input_voltage", "trip_output_voltage", "past_trip_1", "past_trip_2", "past_trip_3", "past_trip_4", "inverter_capacity_code", "inverter_series_code", "cpu_version", "cpu2_version", "eeprom_version"]);
  const position = new Map(state.liveCardOrder.map((key, index) => [key, index]));
  const derivedSources = { machine_speed:"calculated_motor_speed", actual_output_current:"output_current", actual_output_voltage:"output_voltage", actual_motor_torque:"torque", mechanical_power:"torque" };
  const visible = items.filter((item) => {
    if (special.has(item.metric)) return false;
    const channel = state.channels.find(device => device.name === item.inverter)?.channels.find(entry => entry.key === (derivedSources[item.metric] || item.metric));
    // Alert monitors may still be returned while their channel is Off. They
    // feed the global warning indicator, but must not reappear as Live cards.
    return channel && ["live", "record"].includes(channel.mode);
  });
  visible.sort((left, right) => (position.get(`${left.inverter}\u001f${left.metric}`) ?? Number.MAX_SAFE_INTEGER) - (position.get(`${right.inverter}\u001f${right.metric}`) ?? Number.MAX_SAFE_INTEGER));
  for (const item of visible) {
    const card = document.createElement("article");
    card.className = "card";
    card.draggable = true; card.dataset.cardKey = `${item.inverter}\u001f${item.metric}`;
    const thresholdLevel = thresholdSeverity(item.value, thresholds[item.metric]);
    if (thresholdLevel) card.classList.add(`severity-${thresholdLevel}`);
    const label = document.createElement("p"); label.className = "label"; label.textContent = `${item.inverter} · ${metricName(item.metric)}`; appendMeasurementHint(label, item.metric, item);
    const line = document.createElement("p"); line.className = "value";
    const value = document.createElement("span"); value.textContent = item.unit === "raw" ? `0x${item.raw_value.toString(16).toUpperCase().padStart(4, "0")}` : Number(item.value).toLocaleString(locale(), { maximumFractionDigits: 2 });
    const unit = document.createElement("span"); unit.className = "unit"; unit.textContent = item.unit === "raw" ? "" : item.unit;
    line.append(value, unit);
    const raw = document.createElement("p"); raw.className = "raw"; raw.textContent = `${item.register_address} · raw ${item.raw_value}`;
    card.append(label, line);
    if (item.decoded) {
      card.classList.add(`severity-${item.decoded.severity}`);
      const summary = document.createElement("p"); summary.className = "decoded-summary"; summary.textContent = localizedDecoded(item); card.append(summary);
      if (item.decoded.active?.length) {
        const details = document.createElement("ul"); details.className = "decoded-details";
        for (const entry of item.decoded.active) { const detail = document.createElement("li"); detail.textContent = entry.label; details.append(detail); }
        card.append(details);
      }
    }
    card.append(raw); cards.append(card);
  }
  if (items.length) $("#updated").textContent = `${t("live.asOf")} ${timeText(items[0].observed_at)}`;
}

async function loadLiveCardOrder() {
  const data = await getJSON("/api/v1/live-card-order");
  state.liveCardOrder = Array.isArray(data.order) ? data.order : [];
  state.liveOrderLoaded = true;
}
async function saveLiveCardOrder() {
  const order = [...$("#cards").querySelectorAll("[data-card-key]")].map(card => card.dataset.cardKey);
  state.liveCardOrder = order;
  try { await postJSON("/api/v1/live-card-order", { order }); }
  catch (error) { $("#last-error").textContent = error.message; }
}
function installLiveCardDragAndDrop() {
  const cards = $("#cards");
  cards.addEventListener("dragstart", event => {
    const card = event.target.closest("[data-card-key]"); if (!card) return;
    state.liveOrderDragging = true; card.classList.add("dragging");
    event.dataTransfer.effectAllowed = "move"; event.dataTransfer.setData("text/plain", card.dataset.cardKey);
  });
  cards.addEventListener("dragover", event => {
    if (!state.liveOrderDragging) return; event.preventDefault();
    const target = event.target.closest("[data-card-key]"); const dragged = cards.querySelector(".dragging");
    cards.querySelectorAll(".drop-target").forEach(card => card.classList.remove("drop-target"));
    if (!target || target === dragged) return;
    target.classList.add("drop-target");
    const rect = target.getBoundingClientRect();
    cards.insertBefore(dragged, event.clientY < rect.top + rect.height / 2 ? target : target.nextSibling);
  });
  cards.addEventListener("dragend", event => {
    const card = event.target.closest("[data-card-key]"); if (!card) return;
    card.classList.remove("dragging"); cards.querySelectorAll(".drop-target").forEach(entry => entry.classList.remove("drop-target"));
    if (state.liveOrderDragging) saveLiveCardOrder(); state.liveOrderDragging = false;
  });
}

function renderDeviceInformation(items, metadata) {
  const container = $("#device-information"); container.replaceChildren();
  const metrics = [
    ["inverter_capacity_code", t("info.capacity")], ["inverter_series_code", t("info.series")],
    ["cpu_version", t("info.cpu")], ["cpu2_version", t("info.cpu2")], ["eeprom_version", t("info.eeprom")],
  ];
  for (const inverter of metadata.inverters || []) {
    const byMetric = Object.fromEntries(items.filter((item) => item.inverter === inverter.name).map((item) => [item.metric, item]));
    const device = document.createElement("article"); device.className = "device-information-card";
    const heading = document.createElement("h3"); heading.textContent = inverter.name;
    const details = document.createElement("dl");
    const fields = [[t("info.family"), inverter.model], [t("info.configured"), inverter.name], [t("info.slave"), inverter.slave_id]];
    for (const [key, label] of metrics) {
      const item = byMetric[key];
      if (item) fields.push([label, `${item.raw_value} · 0x${item.raw_value.toString(16).toUpperCase().padStart(4, "0")}`]);
      else if (["inverter_capacity_code", "cpu_version"].includes(key)) fields.push([label, t("info.unavailable")]);
    }
    for (const [label, value] of fields) {
      const box = document.createElement("div"); const term = document.createElement("dt"); const description = document.createElement("dd");
      term.textContent = label; description.textContent = value; box.append(term, description); details.append(box);
    }
    device.append(heading, details); container.append(device);
  }
  if (!container.children.length) { const empty = document.createElement("p"); empty.className = "hint"; empty.textContent = t("info.waiting"); container.append(empty); }
}

function renderFaultMemory(items) {
  const container = $("#fault-memory"); container.replaceChildren();
  const inverterNames = [...new Set(items.filter((item) => item.metric === "trip_code").map((item) => item.inverter))];
  const tripKeys = ["trip_code", "past_trip_1", "past_trip_2", "past_trip_3", "past_trip_4"];
  const tripLabels = [t("fault.current"), t("fault.latest"), t("fault.previous"), t("fault.third"), t("fault.oldest")];
  const snapshotKeys = [
    ["trip_output_frequency", t("fault.frequency")], ["trip_output_current", t("fault.currentOut")],
    ["trip_dc_input_voltage", t("fault.dc")], ["trip_output_voltage", t("fault.voltage")],
    ["trip_operating_status", t("fault.status")],
  ];
  for (const inverter of inverterNames) {
    const byMetric = Object.fromEntries(items.filter((item) => item.inverter === inverter).map((item) => [item.metric, item]));
    if (!tripKeys.some((key) => byMetric[key])) continue;
    const device = document.createElement("article"); device.className = "fault-device";
    const header = document.createElement("div"); header.className = "fault-device-header";
    const title = document.createElement("h3"); title.textContent = inverter;
    const note = document.createElement("span"); note.className = "hint"; note.textContent = t("fault.note"); header.append(title, note);
    const trips = document.createElement("div"); trips.className = "trip-list";
    tripKeys.forEach((key, index) => {
      const item = byMetric[key]; const raw = item?.raw_value ?? 0; const decoded = item?.decoded;
      const entry = document.createElement("div"); entry.className = `trip-entry ${index === 0 ? "current" : ""} ${raw ? "active" : "clear"}`;
      const position = document.createElement("p"); position.className = "trip-position"; position.textContent = tripLabels[index];
      const code = document.createElement("strong"); code.className = "trip-code"; code.textContent = decoded?.code || (raw ? `0x${raw.toString(16).toUpperCase()}` : "nerr");
      const description = document.createElement("p"); description.className = "trip-description"; description.textContent = raw ? (language === "de" && decoded?.summary ? decoded.summary : `${t("fault.code")} ${decoded?.code || ""}`) : t("fault.noneError");
      entry.append(position, code, description); trips.append(entry);
    });
    const snapshot = document.createElement("div"); snapshot.className = "snapshot";
    for (const [key, label] of snapshotKeys) {
      const item = byMetric[key]; const box = document.createElement("div"); box.className = "snapshot-item";
      const caption = document.createElement("p"); caption.className = "snapshot-label"; caption.textContent = label;
      const value = document.createElement("p"); value.className = "snapshot-value";
      if (!item) value.textContent = "–";
      else if (item.unit === "raw") value.textContent = item.decoded ? `${localizedDecoded(item)} · 0x${item.raw_value.toString(16).toUpperCase().padStart(4, "0")}` : `0x${item.raw_value.toString(16).toUpperCase().padStart(4, "0")}`;
      else value.textContent = `${Number(item.value).toLocaleString(locale(), { maximumFractionDigits: 2 })} ${item.unit}`;
      box.append(caption, value); snapshot.append(box);
    }
    device.append(header, trips, snapshot); container.append(device);
  }
  if (!container.children.length) appendChannelEnableHint(container, [...tripKeys, ...snapshotKeys.map(([key]) => key), "alarm_information_1", "alarm_information_2"], "live", t("fault.none"));
}

function renderIO(items) {
  const container = $("#io-devices"); container.replaceChildren();
  const inverterNames = [...new Set(items.map((item) => item.inverter))];
  for (const inverter of inverterNames) {
    const digital = items.find((item) => item.inverter === inverter && item.metric === "input_terminal_status");
    const analog = items.find((item) => item.inverter === inverter && item.metric === "fm_analog_output");
    if (!digital && !analog) continue;
    const device = document.createElement("article"); device.className = "io-device";
    const identity = document.createElement("div"); const name = document.createElement("h3"); name.textContent = inverter;
    const slave = document.createElement("p"); slave.className = "slave"; slave.textContent = `Slave ${digital?.slave_id ?? analog?.slave_id}`; identity.append(name, slave);
    const bank = document.createElement("div"); bank.className = "signal-bank";
    const stateByLabel = Object.fromEntries((digital?.decoded?.states || []).map((item) => [item.label, item.active]));
    for (const label of ["F", "R", "S1", "S2", "S3"]) {
      const active = Boolean(stateByLabel[label]); const signal = document.createElement("div"); signal.className = `signal ${active ? "on" : ""}`; signal.dataset.state = active ? t("io.on") : t("io.off"); signal.textContent = label; bank.append(signal);
    }
    const analogBlock = document.createElement("div"); analogBlock.className = "analog-block";
    const analogRaw = analog?.raw_value ?? 0; const percent = Math.max(0, Math.min(100, Number(analog?.value ?? 0)));
    const heading = document.createElement("div"); heading.className = "analog-heading";
    const headingLabel = document.createElement("span"); headingLabel.textContent = t("io.analog");
    const headingValue = document.createElement("strong"); headingValue.textContent = `${percent.toLocaleString(locale(), { maximumFractionDigits: 1 })} %`;
    heading.append(headingLabel, headingValue);
    const gauge = document.createElement("div"); gauge.className = "gauge"; const fill = document.createElement("span"); fill.style.width = `${percent}%`; gauge.append(fill);
    const analogMeta = document.createElement("p"); analogMeta.className = "analog-raw"; analogMeta.textContent = analog ? `FE40 · raw ${analogRaw}` : t("io.noAnalog");
    analogBlock.append(heading, gauge, analogMeta); device.append(identity, bank, analogBlock); container.append(device);
  }
  if (!container.children.length) appendChannelEnableHint(container, ["input_terminal_status", "fm_analog_output"], "live", t("io.none"));
}

function renderHealth(data, telemetry = {}) {
  const badge = $("#connection");
  badge.className = `status ${data.status}`;
  badge.querySelector("strong").textContent = t(`status.${data.status}`) || data.status;
  const cycle = data.last_cycle || {};
  const devices = data.devices || [];
  const values = [
    [t("comm.drives"), devices.length || "–"],
    [t("comm.success"), devices.length ? devices.reduce((sum, item) => sum + item.successful_reads, 0) : "–"],
    [t("comm.failed"), devices.length ? devices.reduce((sum, item) => sum + item.failed_reads, 0) : "–"],
    [t("comm.age"), data.age_seconds == null ? "–" : `${data.age_seconds.toFixed(1)} s`],
  ];
  const communication = telemetry.communication || {}; const system = telemetry.system || {};
  if (telemetry.communication) values.push(
    [t("diag.rate"), Number(communication.samples_per_second).toLocaleString(locale(), { maximumFractionDigits: 1 })],
    [t("diag.average"), `${Number(communication.average_cycle_ms).toLocaleString(locale(), { maximumFractionDigits: 1 })} ms`],
    [t("diag.maximum"), `${Number(communication.maximum_cycle_ms).toLocaleString(locale(), { maximumFractionDigits: 1 })} ms`],
    [t("diag.bus"), `${Number(communication.bus_utilization_percent).toLocaleString(locale(), { maximumFractionDigits: 1 })} %`],
    [t("diag.retries"), Number(communication.retries).toLocaleString(locale())],
    [t("diag.success"), `${Number(communication.success_percent).toLocaleString(locale(), { maximumFractionDigits: 2 })} %`],
    [t("diag.inverterCpu"), t("diag.notAvailable")],
  );
  if (telemetry.system) values.push(
    [t("diag.hostCpu"), `${Number(system.cpu_percent).toLocaleString(locale(), { maximumFractionDigits: 1 })} %`],
    [t("diag.hostMemory"), `${Number(system.memory_percent).toLocaleString(locale(), { maximumFractionDigits: 1 })} %`],
    [t("diag.disk"), `${Number(system.disk_percent).toLocaleString(locale(), { maximumFractionDigits: 1 })} %`],
    [t("diag.temperature"), system.temperature_celsius == null ? "–" : `${Number(system.temperature_celsius).toLocaleString(locale(), { maximumFractionDigits: 1 })} °C`],
  );
  const list = $("#diagnostics"); list.replaceChildren();
  for (const [term, description] of values) {
    const box = document.createElement("div"); const dt = document.createElement("dt"); const dd = document.createElement("dd");
    dt.textContent = term; dd.textContent = description; box.append(dt, dd); list.append(box);
  }
  $("#last-error").textContent = devices.filter((item) => item.error).map((item) => `${item.inverter}: ${item.error}`).join(" · ");
}

function formatBytes(bytes) {
  if (!bytes) return "0 B";
  const units = ["B", "KiB", "MiB", "GiB", "TiB"]; const index = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  return `${(bytes / 1024 ** index).toLocaleString(locale(), { maximumFractionDigits: 1 })} ${units[index]}`;
}

function formatDuration(seconds) {
  const hours = seconds / 3600; const days = hours / 24; const years = days / 365.25;
  if (years >= 1) return `${years.toLocaleString(locale(), { maximumFractionDigits: 1 })} ${t("duration.years")}`;
  if (days >= 1) return `${days.toLocaleString(locale(), { maximumFractionDigits: 1 })} ${t("duration.days")}`;
  return `${hours.toLocaleString(locale(), { maximumFractionDigits: 1 })} ${t("duration.hours")}`;
}

function renderStorage(data) {
  const retention = Number(data.retention_days);
  const values = [
    [t("storage.used"), formatBytes(data.bytes)],
    [t("storage.free"), formatBytes(data.filesystem_free_bytes)],
    [t("storage.samples"), Number(data.sample_count).toLocaleString(locale())],
    [t("storage.cycles"), Number(data.cycle_count).toLocaleString(locale())],
    [t("storage.retention"), retention > 0 ? `${retention.toLocaleString(locale())} ${t("storage.days")}` : t("storage.unlimited")],
    [t("storage.growth"), data.growth_bytes_per_second == null ? t("storage.calculating") : formatBytes(data.growth_bytes_per_second * 86400)],
    [t("storage.remaining"), data.retention_expected_to_limit_growth ? t("storage.retentionLimited") : data.estimated_seconds_to_full == null ? t("storage.calculating") : formatDuration(data.estimated_seconds_to_full)],
  ];
  const list = $("#storage"); list.replaceChildren();
  for (const [term, description] of values) {
    const box = document.createElement("div"); const dt = document.createElement("dt"); const dd = document.createElement("dd");
    dt.textContent = term; dd.textContent = description; box.append(dt, dd); list.append(box);
  }
}

function renderDigitalChart(context, items, rect) {
  const labels=["F","R","S1","S2","S3"];
  const states=items.map(item=>Object.fromEntries((item.decoded?.states || []).map(state=>[state.label,state.active])));
  const pad={left:42,right:10,top:12,bottom:12}; const width=rect.width-pad.left-pad.right; const laneHeight=(rect.height-pad.top-pad.bottom)/labels.length;
  context.font="700 12px system-ui"; context.textBaseline="middle";
  labels.forEach((label,lane)=>{
    const y=pad.top+lane*laneHeight; context.fillStyle="#9faeaa"; context.fillText(label,8,y+laneHeight/2);
    context.strokeStyle="#34423f"; context.beginPath(); context.moveTo(pad.left,y+laneHeight-1); context.lineTo(rect.width-pad.right,y+laneHeight-1); context.stroke();
    states.forEach((state,index)=>{ if (!state[label]) return; const x=pad.left+width*index/Math.max(1,states.length-1); const next=pad.left+width*Math.min(index+1,states.length-1)/Math.max(1,states.length-1); context.fillStyle="rgba(115,226,173,.42)"; context.fillRect(x,y+5,Math.max(2,next-x),laneHeight-10); });
  });
  const meta=$("#chart-meta"); meta.replaceChildren(); const left=document.createElement("span"); left.textContent=timeText(items[0].observed_at); const right=document.createElement("span"); right.textContent=timeText(items.at(-1).observed_at); meta.append(left,right);
}

function renderChart(items) {
  state.history = items;
  const canvas = $("#chart"); const empty = $("#chart-empty");
  empty.hidden = items.length > 1;
  if (items.length < 2) {
    const known = state.channels.some(device => device.channels.some(channel => channel.key === state.metric));
    empty.textContent = known ? `${t("channels.enableRecordPrefix")} ${metricName(state.metric)} ${t("channels.enableRecordSuffix")}` : t("history.empty");
  }
  const ratio = window.devicePixelRatio || 1; const rect = canvas.getBoundingClientRect();
  canvas.width = Math.round(rect.width * ratio); canvas.height = Math.round(rect.height * ratio);
  const context = canvas.getContext("2d"); context.scale(ratio, ratio); context.clearRect(0, 0, rect.width, rect.height);
  if (items.length < 2) return;
  if (state.metric === "input_terminal_status") { renderDigitalChart(context,items,rect); return; }
  const values = items.map((item) => Number(item.value)); const min = Math.min(...values); const max = Math.max(...values); const spread = max - min || 1;
  const pad = { x: 10, y: 22 }; const width = rect.width - pad.x * 2; const height = rect.height - pad.y * 2;
  context.strokeStyle = "#34423f"; context.lineWidth = 1;
  for (let row = 0; row <= 4; row++) { const y = pad.y + height * row / 4; context.beginPath(); context.moveTo(pad.x, y); context.lineTo(rect.width - pad.x, y); context.stroke(); }
  const gradient = context.createLinearGradient(0, pad.y, 0, rect.height); gradient.addColorStop(0, "rgba(115,226,173,.3)"); gradient.addColorStop(1, "rgba(115,226,173,0)");
  const point = (value, index) => [pad.x + width * index / (items.length - 1), pad.y + height * (1 - (value - min) / spread)];
  context.beginPath(); values.forEach((value, index) => { const [x, y] = point(value, index); index ? context.lineTo(x, y) : context.moveTo(x, y); });
  context.lineTo(rect.width - pad.x, rect.height - pad.y); context.lineTo(pad.x, rect.height - pad.y); context.closePath(); context.fillStyle = gradient; context.fill();
  context.beginPath(); values.forEach((value, index) => { const [x, y] = point(value, index); index ? context.lineTo(x, y) : context.moveTo(x, y); }); context.strokeStyle = "#73e2ad"; context.lineWidth = 2; context.stroke();
  $("#chart-meta").replaceChildren();
  const left = document.createElement("span"); left.textContent = `${timeText(items[0].observed_at)} · ${t("history.min")} ${min.toLocaleString(locale())}`;
  const right = document.createElement("span"); right.textContent = `${t("history.max")} ${max.toLocaleString(locale())} · ${timeText(items.at(-1).observed_at)}`;
  $("#chart-meta").append(left, right);
}

async function refreshHistory() {
  const inverter = state.inverter ? `&inverter=${encodeURIComponent(state.inverter)}` : "";
  const data = await getJSON(`/api/v1/metrics/history?metric=${encodeURIComponent(state.metric)}${inverter}&limit=1000`);
  renderChart(data.items);
}

async function refresh() {
  if (refreshRunning) return;
  refreshRunning = true;
  try {
    const [health, latest, telemetry] = await Promise.all([getJSON("/api/v1/health"), getJSON("/api/v1/metrics/latest"), getJSON("/api/v1/diagnostics")]);
    if (!state.metadata) state.metadata = await getJSON("/api/v1/metadata");
    if (!state.storage || Date.now() - state.storageRefreshedAt >= 60000) {
      state.storage = await getJSON("/api/v1/storage"); state.storageRefreshedAt = Date.now(); renderStorage(state.storage);
    }
    const metadata = state.metadata; renderFooter(metadata);
    if (!$("#backup-inverter").options.length) for (const inverter of metadata.inverters || []) {
      $("#backup-inverter").add(new Option(`${inverter.name} · ${inverter.model}`,inverter.name));
      $("#preview-inverter").add(new Option(`${inverter.name} · ${inverter.model}`,inverter.name));
    }
    if (!state.liveOrderLoaded) await loadLiveCardOrder();
    state.latest = latest.items; state.telemetry = telemetry; renderHealth(health, telemetry); renderAlerts(latest.items, telemetry, metadata.alert_thresholds, state.storage); renderDeviceInformation(latest.items, metadata); renderIO(latest.items); renderFaultMemory(latest.items); if (!state.liveOrderDragging) renderCards(latest.items, metadata.alert_thresholds?.metrics);
    const select = $("#metric");
    if (!select.options.length) {
      for (const item of latest.items.filter((item) => item.unit !== "raw" || item.metric === "input_terminal_status")) { const option = document.createElement("option"); option.value = `${item.inverter}\u001f${item.metric}`; option.textContent = `${item.inverter} · ${metricName(item.metric)}`; select.append(option); }
      const preferred = [...select.options].find((option) => option.value.endsWith(`\u001f${state.metric}`));
      if (preferred) select.value = preferred.value;
      if (select.value) [state.inverter, state.metric] = select.value.split("\u001f");
      await refreshHistory();
    }
  } catch (error) {
    renderHealth({ status: "unavailable" }); $("#last-error").textContent = error.message;
  } finally {
    refreshRunning = false;
  }
}

$("#metric").addEventListener("change", async (event) => { [state.inverter, state.metric] = event.target.value.split("\u001f"); await refreshHistory(); });
function updateSelectedExport() {
  const link=$("#export-selected");
  if (!state.metric || !state.inverter) { link.hidden=true; return; }
  link.href = `/api/v1/export.csv?metric=${encodeURIComponent(state.metric)}&inverter=${encodeURIComponent(state.inverter)}`;
  link.textContent = `${state.inverter} · ${metricName(state.metric)} ${t("storage.exportMetric")}`;
  link.hidden=false;
}
$("#metric").addEventListener("change", updateSelectedExport);
$("#alert-indicator").addEventListener("click", () => {
  const section = $("#alerts-title").closest("section");
  if (section.classList.contains("is-collapsed")) setSectionCollapsed(section, false);
  section.scrollIntoView({ behavior:"smooth", block:"start" });
});
$("#language").addEventListener("change", (event) => { language = event.target.value; localStorage.setItem("tmm-language", language); applyLanguage(); updateWriteSelection(); updateSelectedExport(); $("#metric").replaceChildren(); renderAlerts(state.latest, state.telemetry, state.metadata?.alert_thresholds, state.storage); renderDeviceInformation(state.latest, state.metadata || { inverters: [] }); renderIO(state.latest); renderFaultMemory(state.latest); renderCards(state.latest, state.metadata?.alert_thresholds?.metrics); renderChart(state.history); showChannels($("#channels-inverter").value); refresh(); refreshParameterAudit(); });
$("#recording-archive").addEventListener("click", () => requestRecording("archive"));
$("#recording-delete").addEventListener("click", () => requestRecording("delete"));
$("#engineering-inverter").addEventListener("change", event => showEngineering(event.target.value));
$("#engineering-save").addEventListener("click", saveEngineering);
$("#channels-inverter").addEventListener("change", event=>showChannels(event.target.value));
$("#measurement-hints").addEventListener("change", event => { measurementHints = event.target.checked; localStorage.setItem("tmm-measurement-hints", String(measurementHints)); applyMeasurementHints(); });
$("#channels-save").addEventListener("click",saveChannels);
$("#backup-create").addEventListener("click",createParameterBackup);
$("#backup-inverter").addEventListener("change",refreshParameterBackups);
$("#preview-create").addEventListener("click",createImportPreview);
$("#preview-inverter").addEventListener("change",updateWriteSelection);
$("#preview-filter").addEventListener("change",filterImportPreview);
$("#write-preflight").addEventListener("click",requestWritePreflight);
$("#write-selected").addEventListener("click",writeSelectedParameter);
window.addEventListener("resize", () => renderChart(state.history));
installLiveCardDragAndDrop(); initCollapsibleSections(); installSectionDragAndDrop(); loadDashboardSectionOrder(); applyLanguage(); applyMeasurementHints(); refresh(); refreshRecording(); loadEngineering(); loadChannels(); refreshParameterBackups(); refreshWriteStatus(); refreshWritePreflight(); refreshParameterAudit(); setInterval(refresh, 3000); setInterval(refreshHistory, 30000); setInterval(refreshRecording, 10000); setInterval(refreshParameterBackups, 5000); setInterval(refreshWriteStatus, 3000); setInterval(refreshParameterAudit, 10000);
