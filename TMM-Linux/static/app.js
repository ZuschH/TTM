const I18N = {
  en: {
    "alerts.eyebrow":"Messages","alerts.title":"Information, warnings & critical conditions","alerts.clear":"No active messages","alerts.info":"Information","alerts.warning":"Warning","alerts.critical":"Critical","alerts.threshold":"Threshold","alerts.system":"Host system","alerts.storage":"Storage","alerts.retentionRisk":"Storage duration is shorter than the configured retention period",
    "info.eyebrow":"Device","info.title":"Device information","info.waiting":"Waiting for device information …","info.family":"Model family","info.configured":"Configured device","info.slave":"Modbus address","info.capacity":"Capacity code","info.series":"Series code","info.cpu":"CPU / application version","info.cpu2":"CPU2 version","info.eeprom":"EEPROM version","info.unavailable":"Not reported",
    "diag.rate":"Stored samples/s","diag.average":"Average poll time","diag.maximum":"Maximum poll time","diag.bus":"Estimated bus load","diag.retries":"Retries","diag.success":"Read success","diag.inverterCpu":"Inverter CPU","diag.hostCpu":"Host CPU","diag.hostMemory":"Host memory","diag.disk":"Data disk","diag.temperature":"Host temperature","diag.notAvailable":"Not exposed by inverter",
    "header.eyebrow":"TMM · Version 1.3","header.title":"Toshiba Modbus Monitor","language":"Language","status.connecting":"Connecting …","status.healthy":"Online","status.degraded":"Partially degraded","status.stale":"No current data","status.starting":"Waiting for data","status.unavailable":"Database unavailable",
    "io.eyebrow":"Hardware","io.title":"Terminals & analog output","io.waiting":"Waiting for I/O data …","io.none":"No I/O monitors are configured for this profile.","io.enablePrefix":"To display data here, enable","io.enableSuffix":"in Measurement channels as Live or Record.","io.analog":"FM analog output","io.noAnalog":"No analog data","io.on":"ON","io.off":"OFF",
    "fault.eyebrow":"Diagnostic memory","fault.title":"Trips & retained operating values","fault.waiting":"Waiting for diagnostic data …","fault.none":"No diagnostic-memory registers are configured for this profile.","fault.note":"FE10 = most recent stored trip","fault.current":"Current","fault.latest":"Latest trip","fault.previous":"Previous","fault.third":"3rd entry","fault.oldest":"Oldest","fault.unknown":"Unknown trip code","fault.noneError":"No error","fault.frequency":"Output frequency","fault.currentOut":"Output current","fault.dc":"DC link","fault.voltage":"Output voltage","fault.status":"Status word",
    "live.title":"Current measurements","live.noData":"No data yet","live.asOf":"As of","live.orderHint":"Drag cards to arrange them. The order is retained.",
    "history.eyebrow":"History","history.title":"Measurement history","history.metric":"Metric","history.empty":"No history data available.","history.min":"Min","history.max":"Max",
    "comm.eyebrow":"Diagnostics","comm.title":"Communication","comm.manual":"User manual","comm.api":"API documentation","comm.drives":"Inverters","comm.success":"Successful","comm.failed":"Failed","comm.age":"Data age",
    "storage.eyebrow":"Data","storage.title":"Storage & export","storage.exportAll":"Export all data as CSV","storage.hint":"The export is limited to the maximum row count defined in the configuration.","storage.used":"Storage used","storage.samples":"Samples","storage.cycles":"Poll cycles","storage.retention":"Retention","storage.unlimited":"Unlimited","storage.days":"days","storage.exportMetric":"as CSV",
    "storage.free":"Disk space free","storage.reusable":"Reusable SQLite space","storage.growth":"Estimated growth/day","storage.remaining":"Estimated time remaining","storage.calculating":"Calculating (at least 5 minutes of data required)","storage.stable":"No net growth detected","storage.retentionLimited":"Retention is expected to limit growth","duration.years":"years","duration.days":"days","duration.hours":"hours",
    "footer.summary":"read-only · refreshes every 3 seconds","footer.contact":"Contact",
    "metric.output_frequency":"Output frequency","metric.frequency_setpoint":"Frequency setpoint","metric.operating_status":"Operating status","metric.output_current":"Output current","metric.dc_input_voltage":"DC-link voltage","metric.output_voltage":"Output voltage","metric.braking_resistor_load":"Braking resistor load (OLr)","metric.inverter_internal_temperature":"Internal device temperature","metric.power_board_temperature":"Power-board temperature","metric.trip_code":"Trip code","metric.alarm_information_1":"Alarm word 1","metric.alarm_information_2":"Alarm word 2"
  },
  de: {
    "alerts.eyebrow":"Meldungen","alerts.title":"Informationen, Warnungen & kritische Zustände","alerts.clear":"Keine aktiven Meldungen","alerts.info":"Information","alerts.warning":"Warnung","alerts.critical":"Kritisch","alerts.threshold":"Schwellwert","alerts.system":"Host-System","alerts.storage":"Speicher","alerts.retentionRisk":"Speicherlaufzeit ist kürzer als die konfigurierte Aufbewahrungszeit",
    "info.eyebrow":"Gerät","info.title":"Geräteinformationen","info.waiting":"Warte auf Geräteinformationen …","info.family":"Modellfamilie","info.configured":"Konfiguriertes Gerät","info.slave":"Modbus-Adresse","info.capacity":"Leistungscode","info.series":"Baureihencode","info.cpu":"CPU-/Applikationsversion","info.cpu2":"CPU2-Version","info.eeprom":"EEPROM-Version","info.unavailable":"Nicht gemeldet",
    "diag.rate":"Gespeicherte Werte/s","diag.average":"Mittlere Abfragezeit","diag.maximum":"Maximale Abfragezeit","diag.bus":"Geschätzte Buslast","diag.retries":"Wiederholungen","diag.success":"Leseerfolg","diag.inverterCpu":"Umrichter-CPU","diag.hostCpu":"Host-CPU","diag.hostMemory":"Host-Arbeitsspeicher","diag.disk":"Datenträger","diag.temperature":"Host-Temperatur","diag.notAvailable":"Vom Umrichter nicht bereitgestellt",
    "header.eyebrow":"TMM · Version 1.3","header.title":"Toshiba Modbus Monitor","language":"Sprache","status.connecting":"Verbinde …","status.healthy":"Online","status.degraded":"Teilweise gestört","status.stale":"Keine aktuellen Daten","status.starting":"Warte auf Daten","status.unavailable":"Datenbank nicht erreichbar",
    "io.eyebrow":"Hardware","io.title":"Klemmen & Analogausgang","io.waiting":"Warte auf E/A-Daten …","io.none":"Für dieses Profil sind keine E/A-Monitore konfiguriert.","io.enablePrefix":"Um Daten hier anzuzeigen, aktivieren Sie","io.enableSuffix":"unter Messkanäle als Live oder Aufzeichnen.","io.analog":"FM-Analogausgang","io.noAnalog":"Keine Analogdaten","io.on":"EIN","io.off":"AUS",
    "fault.eyebrow":"Diagnosespeicher","fault.title":"Trips & festgehaltene Betriebswerte","fault.waiting":"Warte auf Diagnosedaten …","fault.none":"Für dieses Profil sind keine Diagnosespeicher-Register konfiguriert.","fault.note":"FE10 = jüngster gespeicherter Trip","fault.current":"Aktuell","fault.latest":"Letzter Trip","fault.previous":"Vorletzter","fault.third":"3. Eintrag","fault.oldest":"Ältester","fault.unknown":"Unbekannter Trip-Code","fault.noneError":"Kein Fehler","fault.frequency":"Ausgangsfrequenz","fault.currentOut":"Ausgangsstrom","fault.dc":"Zwischenkreis","fault.voltage":"Ausgangsspannung","fault.status":"Statuswort",
    "live.title":"Aktuelle Messwerte","live.noData":"Noch keine Daten","live.asOf":"Stand","live.orderHint":"Karten per Drag & Drop anordnen. Die Reihenfolge bleibt erhalten.",
    "history.eyebrow":"Verlauf","history.title":"Messwert-Historie","history.metric":"Messwert","history.empty":"Noch keine Verlaufsdaten vorhanden.","history.min":"Min","history.max":"Max",
    "comm.eyebrow":"Diagnose","comm.title":"Kommunikation","comm.manual":"Benutzerhandbuch","comm.api":"API-Dokumentation","comm.drives":"Umrichter","comm.success":"Erfolgreich","comm.failed":"Fehlgeschlagen","comm.age":"Datenalter",
    "storage.eyebrow":"Daten","storage.title":"Speicher & Export","storage.exportAll":"Alle Daten als CSV","storage.hint":"Der Export ist auf die konfigurierte maximale Zeilenzahl begrenzt.","storage.used":"Belegter Speicher","storage.samples":"Messpunkte","storage.cycles":"Messzyklen","storage.retention":"Aufbewahrung","storage.unlimited":"Unbegrenzt","storage.days":"Tage","storage.exportMetric":"als CSV",
    "storage.free":"Freier Speicherplatz","storage.reusable":"Von SQLite wiederverwendbar","storage.growth":"Geschätzter Zuwachs/Tag","storage.remaining":"Geschätzte Restlaufzeit","storage.calculating":"Berechnung läuft (mindestens 5 Minuten Daten erforderlich)","storage.stable":"Kein Nettozuwachs erkannt","storage.retentionLimited":"Aufbewahrungsfrist begrenzt den Zuwachs voraussichtlich","duration.years":"Jahre","duration.days":"Tage","duration.hours":"Stunden",
    "footer.summary":"nur lesend · Aktualisierung alle 3 Sekunden","footer.contact":"Kontakt",
    "metric.output_frequency":"Ausgangsfrequenz","metric.frequency_setpoint":"Frequenzvorgabe","metric.operating_status":"Betriebsstatus","metric.output_current":"Ausgangsstrom","metric.dc_input_voltage":"Zwischenkreisspannung","metric.output_voltage":"Ausgangsspannung","metric.braking_resistor_load":"Bremswiderstand-Auslastung (OLr)","metric.inverter_internal_temperature":"Interne Gerätetemperatur","metric.power_board_temperature":"Leistungsteilplatinen-Temperatur","metric.trip_code":"Trip-Code","metric.alarm_information_1":"Alarmwort 1","metric.alarm_information_2":"Alarmwort 2"
  },
  fr: {
    "alerts.eyebrow":"Messages","alerts.title":"Informations, avertissements et états critiques","alerts.clear":"Aucun message actif","alerts.info":"Information","alerts.warning":"Avertissement","alerts.critical":"Critique","alerts.threshold":"Seuil","alerts.system":"Système hôte","alerts.storage":"Stockage","alerts.retentionRisk":"La durée de stockage est inférieure à la période de conservation configurée",
    "info.eyebrow":"Appareil","info.title":"Informations sur l’appareil","info.waiting":"En attente des informations appareil…","info.family":"Famille de modèle","info.configured":"Appareil configuré","info.slave":"Adresse Modbus","info.capacity":"Code de capacité","info.series":"Code de série","info.cpu":"Version CPU / application","info.cpu2":"Version CPU2","info.eeprom":"Version EEPROM","info.unavailable":"Non communiqué",
    "diag.rate":"Mesures enregistrées/s","diag.average":"Temps moyen requête","diag.maximum":"Temps maximal requête","diag.bus":"Charge bus estimée","diag.retries":"Répétitions","diag.success":"Lectures réussies","diag.inverterCpu":"CPU variateur","diag.hostCpu":"CPU hôte","diag.hostMemory":"Mémoire hôte","diag.disk":"Disque de données","diag.temperature":"Température hôte","diag.notAvailable":"Non fourni par le variateur",
    "header.eyebrow":"TMM · Version 1.3","header.title":"Toshiba Modbus Monitor","language":"Langue","status.connecting":"Connexion…","status.healthy":"En ligne","status.degraded":"Partiellement perturbé","status.stale":"Aucune donnée récente","status.starting":"En attente de données","status.unavailable":"Base de données indisponible",
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
    "header.eyebrow":"TMM · バージョン1.3","header.title":"Toshiba Modbus Monitor","language":"言語","status.connecting":"接続中…","status.healthy":"オンライン","status.degraded":"一部異常","status.stale":"最新データなし","status.starting":"データ待機中","status.unavailable":"データベース利用不可",
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

Object.assign(I18N.en,{"addons.eyebrow":"Add-ons","addons.title":"External I/O","addons.none":"No external I/O add-ons are configured.","addons.offline":"Card unavailable","addons.stale":"No recent card data","addons.disabled":"Card disabled — no polling","addons.enable":"Enable card","addons.disable":"Disable card","addons.alert":"External I/O","addons.channels":"channels"});
Object.assign(I18N.de,{"addons.eyebrow":"Erweiterungen","addons.title":"Externe E/A","addons.none":"Keine externen E/A-Erweiterungen sind konfiguriert.","addons.offline":"Karte nicht erreichbar","addons.stale":"Keine aktuellen Kartendaten","addons.disabled":"Karte abgeschaltet — keine Abfrage","addons.enable":"Karte einschalten","addons.disable":"Karte abschalten","addons.alert":"Externe E/A","addons.channels":"Kanäle"});
Object.assign(I18N.fr,{"addons.eyebrow":"Extensions","addons.title":"E/S externes","addons.none":"Aucune extension E/S externe n’est configurée.","addons.offline":"Carte indisponible","addons.stale":"Aucune donnée récente de la carte","addons.disabled":"Carte désactivée — aucune interrogation","addons.enable":"Activer la carte","addons.disable":"Désactiver la carte","addons.alert":"E/S externes","addons.channels":"canaux"});
Object.assign(I18N.ja,{"addons.eyebrow":"アドオン","addons.title":"外部I/O","addons.none":"外部I/Oアドオンは設定されていません。","addons.offline":"カードに接続できません","addons.stale":"カードの最新データがありません","addons.disabled":"カードは無効です — ポーリングなし","addons.enable":"カードを有効化","addons.disable":"カードを無効化","addons.alert":"外部I/O","addons.channels":"チャンネル"});
Object.assign(I18N.fr,{"storage.reusable":"Espace SQLite réutilisable","storage.stable":"Aucune croissance nette détectée"});
Object.assign(I18N.ja,{"storage.reusable":"SQLite 再利用可能領域","storage.stable":"正味の増加は検出されていません"});
Object.assign(I18N.en,{"addons.verified":"Card communication verified — no measurement channels selected"});
Object.assign(I18N.de,{"addons.verified":"Kartenkommunikation bestätigt — keine Messkanäle ausgewählt"});
Object.assign(I18N.fr,{"addons.verified":"Communication avec la carte confirmée — aucun canal de mesure sélectionné"});
Object.assign(I18N.ja,{"addons.verified":"カード通信を確認済み — 測定チャンネルは未選択です"});
Object.assign(I18N.en,{"thermal.label":"Pi thermal protection","thermal.throttled":"Polling interval doubled","thermal.paused":"Polling paused until the Pi cools below 70 °C"});
Object.assign(I18N.de,{"thermal.label":"Pi-Thermoschutz","thermal.throttled":"Zyklusdauer auf den Faktor 2 erhöht","thermal.paused":"Messbetrieb pausiert, bis der Pi unter 70 °C abgekühlt ist"});
Object.assign(I18N.fr,{"thermal.label":"Protection thermique du Pi","thermal.throttled":"Intervalle d’interrogation doublé","thermal.paused":"Interrogation suspendue jusqu’à moins de 70 °C"});
Object.assign(I18N.ja,{"thermal.label":"Pi 温度保護","thermal.throttled":"ポーリング間隔を2倍にしました","thermal.paused":"Pi が70 °C未満になるまでポーリングを一時停止します"});
Object.assign(I18N.en,{"history.configure":"Configure channels","history.source":"Data source","history.selectAll":"All","history.selectNone":"None","history.resetView":"Reset zoom & pan","storage.exportSelected":"Export selected channels as CSV"});
Object.assign(I18N.de,{"history.configure":"Messkanäle konfigurieren","history.source":"Datenquelle","history.selectAll":"Alle","history.selectNone":"Keine","history.resetView":"Zoom & Verschieben zurücksetzen","storage.exportSelected":"Ausgewählte Kanäle als CSV exportieren"});
Object.assign(I18N.fr,{"history.configure":"Configurer les canaux","history.source":"Source de données","history.selectAll":"Tous","history.selectNone":"Aucun","history.resetView":"Réinitialiser zoom et déplacement","storage.exportSelected":"Exporter les canaux sélectionnés en CSV"});
Object.assign(I18N.ja,{"history.configure":"計測チャンネルを設定","history.source":"データソース","history.selectAll":"すべて","history.selectNone":"なし","history.resetView":"ズームと移動をリセット","storage.exportSelected":"選択したチャンネルをCSV出力"});
Object.assign(I18N.en,{"history.stopSourceRecording":"Stop recording this source","history.stopAllRecording":"Stop all recording","history.stopSourceConfirm":"Stop history recording for this data source? Live channels remain visible.","history.stopAllConfirm":"Stop history recording for every configured data source? Live channels remain visible.","history.recordingStopped":"History recording stopped."});
Object.assign(I18N.de,{"history.stopSourceRecording":"Aufzeichnung dieser Quelle stoppen","history.stopAllRecording":"Alle Aufzeichnungen stoppen","history.stopSourceConfirm":"Verlaufsaufzeichnung dieser Datenquelle stoppen? Live-Kanäle bleiben sichtbar.","history.stopAllConfirm":"Verlaufsaufzeichnung aller konfigurierten Datenquellen stoppen? Live-Kanäle bleiben sichtbar.","history.recordingStopped":"Verlaufsaufzeichnung gestoppt."});
Object.assign(I18N.fr,{"history.stopSourceRecording":"Arrêter l’enregistrement de cette source","history.stopAllRecording":"Arrêter tous les enregistrements","history.stopSourceConfirm":"Arrêter l’historique de cette source ? Les canaux en direct restent visibles.","history.stopAllConfirm":"Arrêter l’historique de toutes les sources ? Les canaux en direct restent visibles.","history.recordingStopped":"Enregistrement de l’historique arrêté."});
Object.assign(I18N.ja,{"history.stopSourceRecording":"このソースの記録を停止","history.stopAllRecording":"すべての記録を停止","history.stopSourceConfirm":"このデータソースの履歴記録を停止しますか？ライブチャンネルは表示されます。","history.stopAllConfirm":"すべてのデータソースの履歴記録を停止しますか？ライブチャンネルは表示されます。","history.recordingStopped":"履歴記録を停止しました。"});
Object.assign(I18N.en,{"history.style":"Curve","history.linear":"Linear","history.step":"Rectangle","history.spline":"Spline"});
Object.assign(I18N.de,{"history.style":"Kurve","history.linear":"Linear verbunden","history.step":"Rechteck","history.spline":"Spline"});
Object.assign(I18N.fr,{"history.style":"Courbe","history.linear":"Linéaire","history.step":"Rectangulaire","history.spline":"Spline"});
Object.assign(I18N.ja,{"history.style":"曲線","history.linear":"直線","history.step":"矩形","history.spline":"スプライン"});
Object.assign(I18N.en,{"history.styleStep":"Rectangle curve","history.styleLinear":"Linear curve","history.styleSpline":"Spline curve"});
Object.assign(I18N.de,{"history.styleStep":"Rechteck-Kurve","history.styleLinear":"Linear verbundene Kurve","history.styleSpline":"Spline-Kurve"});
Object.assign(I18N.fr,{"history.styleStep":"Courbe rectangulaire","history.styleLinear":"Courbe linéaire","history.styleSpline":"Courbe spline"});
Object.assign(I18N.ja,{"history.styleStep":"矩形曲線","history.styleLinear":"直線曲線","history.styleSpline":"スプライン曲線"});
Object.assign(I18N.en,{"history.axis":"Axis","history.axisAuto":"Automatic","history.axis1":"Axis 1","history.axis2":"Axis 2","history.axis3":"Axis 3","history.axis4":"Axis 4"});
Object.assign(I18N.de,{"history.axis":"Achse","history.axisAuto":"Automatisch","history.axis1":"Achse 1","history.axis2":"Achse 2","history.axis3":"Achse 3","history.axis4":"Achse 4"});
Object.assign(I18N.fr,{"history.axis":"Axe","history.axisAuto":"Automatique","history.axis1":"Axe 1","history.axis2":"Axe 2","history.axis3":"Axe 3","history.axis4":"Axe 4"});
Object.assign(I18N.ja,{"history.axis":"軸","history.axisAuto":"自動","history.axis1":"軸 1","history.axis2":"軸 2","history.axis3":"軸 3","history.axis4":"軸 4"});
Object.assign(I18N.en,{"history.recordStart":"Start recording","history.recordStop":"Stop recording","history.recordFixed":"Recording is fixed for this system metric"});
Object.assign(I18N.de,{"history.recordStart":"Aufzeichnung starten","history.recordStop":"Aufzeichnung beenden","history.recordFixed":"Aufzeichnung ist für diese Systemgröße fest eingestellt"});
Object.assign(I18N.fr,{"history.recordStart":"Démarrer l’enregistrement","history.recordStop":"Arrêter l’enregistrement","history.recordFixed":"L’enregistrement est fixe pour cette mesure système"});
Object.assign(I18N.ja,{"history.recordStart":"記録を開始","history.recordStop":"記録を停止","history.recordFixed":"このシステム計測値の記録は固定です"});
Object.assign(I18N.en,{"history.exportChannel":"Export this channel as CSV"});
Object.assign(I18N.de,{"history.exportChannel":"Diesen Kanal als CSV exportieren"});
Object.assign(I18N.fr,{"history.exportChannel":"Exporter ce canal en CSV"});
Object.assign(I18N.ja,{"history.exportChannel":"このチャンネルをCSV出力"});
Object.assign(I18N.en,{"history.exportSelect":"Include in selected CSV export","history.exportRemove":"Remove from selected CSV export"});
Object.assign(I18N.de,{"history.exportSelect":"Für Sammelexport vormerken","history.exportRemove":"Aus Sammelexport entfernen"});
Object.assign(I18N.fr,{"history.exportSelect":"Inclure dans l’export CSV sélectionné","history.exportRemove":"Retirer de l’export CSV sélectionné"});
Object.assign(I18N.ja,{"history.exportSelect":"選択CSV出力に追加","history.exportRemove":"選択CSV出力から除外"});
Object.assign(I18N.en,{"history.color":"Curve colour"});
Object.assign(I18N.de,{"history.color":"Kurvenfarbe"});
Object.assign(I18N.fr,{"history.color":"Couleur de courbe"});
Object.assign(I18N.ja,{"history.color":"曲線の色"});
Object.assign(I18N.en,{"ups.eyebrow":"System","ups.title":"System power & cooling","ups.none":"No system power or cooling add-on is configured.","ups.charge0":"Charging off","ups.charge1":"Charge complete","ups.charge2":"Charging","ups.charge3":"Charging fault"});
Object.assign(I18N.de,{"ups.eyebrow":"System","ups.title":"Systemversorgung & Kühlung","ups.none":"Kein Systemversorgungs- oder Kühlungs-Add-on konfiguriert.","ups.charge0":"Laden aus","ups.charge1":"Ladung vollständig","ups.charge2":"Lädt","ups.charge3":"Ladefehler"});
Object.assign(I18N.en,{"ups.remaining":"Estimated battery runtime","ups.learning":"Battery runtime is learning …","ups.mains":"Mains power present"});
Object.assign(I18N.de,{"ups.remaining":"Geschätzte Batterierestlaufzeit","ups.learning":"Batterierestlaufzeit wird ermittelt …","ups.mains":"Netzversorgung vorhanden"});
Object.assign(I18N.en,{"ups.chargeRemaining":"Estimated remaining charge time","ups.chargeLearning":"Charge time is learning …"});
Object.assign(I18N.de,{"ups.chargeRemaining":"Geschätzte Restladezeit","ups.chargeLearning":"Restladezeit wird ermittelt …"});
Object.assign(I18N.en,{"ups.timeout":"Power-loss confirmation (s)","ups.save":"Apply UPS timeout","ups.saved":"UPS timeout accepted."});
Object.assign(I18N.de,{"ups.timeout":"Bestätigungszeit bei Netzausfall (s)","ups.save":"USV-Timeout übernehmen","ups.saved":"USV-Timeout übernommen."});
Object.assign(I18N.fr,{"ups.eyebrow":"Système","ups.title":"Alimentation et refroidissement","ups.none":"Aucun module d’alimentation ou de refroidissement n’est configuré.","ups.charge0":"Charge arrêtée","ups.charge1":"Charge terminée","ups.charge2":"En charge","ups.charge3":"Défaut de charge","ups.remaining":"Autonomie batterie estimée","ups.learning":"Calcul de l’autonomie batterie en cours…","ups.mains":"Alimentation secteur présente","ups.chargeRemaining":"Temps de charge restant estimé","ups.chargeLearning":"Calcul du temps de charge en cours…","ups.timeout":"Confirmation de coupure secteur (s)","ups.save":"Appliquer le délai UPS","ups.saved":"Délai UPS accepté."});
Object.assign(I18N.ja,{"ups.eyebrow":"システム","ups.title":"電源と冷却","ups.none":"電源または冷却アドオンは設定されていません。","ups.charge0":"充電停止","ups.charge1":"充電完了","ups.charge2":"充電中","ups.charge3":"充電異常","ups.remaining":"推定バッテリー残り時間","ups.learning":"バッテリー残り時間を算出中…","ups.mains":"商用電源あり","ups.chargeRemaining":"推定充電残り時間","ups.chargeLearning":"充電時間を算出中…","ups.timeout":"電源喪失確認時間 (秒)","ups.save":"UPSタイムアウトを適用","ups.saved":"UPSタイムアウトを受け付けました。"});
Object.assign(I18N.en,{"history.markerDelete":"Delete marker","history.liveShow":"Show in Live view","history.liveHide":"Hide from Live view","backup.retained":"retained from template","backup.invalidFileSize":"invalid file size","preview.changes":"change(s)","write.csvRequired":"Select the matching PCM002Z CSV limits file.","write.parameters":"parameter(s)"});
Object.assign(I18N.de,{"history.markerDelete":"Marker löschen","history.liveShow":"In Live-Ansicht anzeigen","history.liveHide":"In Live-Ansicht ausblenden","backup.retained":"aus Vorlage übernommen","backup.invalidFileSize":"ungültige Dateigröße","preview.changes":"Änderung(en)","write.csvRequired":"Passende PCM002Z-CSV-Grenzdatei auswählen.","write.parameters":"Parameter"});
Object.assign(I18N.fr,{"history.markerDelete":"Supprimer le marqueur","history.liveShow":"Afficher dans la vue en direct","history.liveHide":"Masquer de la vue en direct","backup.retained":"conservé depuis le modèle","backup.invalidFileSize":"taille de fichier non valide","preview.changes":"modification(s)","write.csvRequired":"Sélectionnez le fichier CSV PCM002Z des limites correspondant.","write.parameters":"paramètre(s)"});
Object.assign(I18N.ja,{"history.markerDelete":"マーカーを削除","history.liveShow":"ライブ表示に表示","history.liveHide":"ライブ表示から隠す","backup.retained":"テンプレートから保持","backup.invalidFileSize":"無効なファイルサイズ","preview.changes":"件の変更","write.csvRequired":"一致するPCM002Z CSV制限ファイルを選択してください。","write.parameters":"パラメーター"});
Object.assign(I18N.en,{"fan.mode":"Cooling mode","fan.monitor":"Monitor only","fan.automatic":"Automatic","fan.manual":"Manual","fan.minimum":"Minimum power (%)","fan.start":"Start temperature (°C)","fan.full":"Full-speed temperature (°C)","fan.manualPower":"Manual power (%)","fan.save":"Apply cooling control"});
Object.assign(I18N.de,{"fan.mode":"Kühlmodus","fan.monitor":"Nur überwachen","fan.automatic":"Automatik","fan.manual":"Manuell","fan.minimum":"Mindestleistung (%)","fan.start":"Starttemperatur (°C)","fan.full":"Vollasttemperatur (°C)","fan.manualPower":"Manuelle Leistung (%)","fan.save":"Kühlungsregelung übernehmen"});
Object.assign(I18N.fr,{"fan.mode":"Mode de refroidissement","fan.monitor":"Surveillance seule","fan.automatic":"Automatique","fan.manual":"Manuel","fan.minimum":"Puissance minimale (%)","fan.start":"Température de démarrage (°C)","fan.full":"Température à pleine vitesse (°C)","fan.manualPower":"Puissance manuelle (%)","fan.save":"Appliquer la régulation"});
Object.assign(I18N.ja,{"fan.mode":"冷却モード","fan.monitor":"監視のみ","fan.automatic":"自動","fan.manual":"手動","fan.minimum":"最小出力 (%)","fan.start":"始動温度 (°C)","fan.full":"全速温度 (°C)","fan.manualPower":"手動出力 (%)","fan.save":"冷却制御を適用"});
Object.assign(I18N.en,{"admin.remoteDisabled":"Remote changes are disabled. Set web.allow_remote_administration to true in /etc/tmm/config.json and restart tmm-web."});
Object.assign(I18N.de,{"admin.remoteDisabled":"Fernänderungen sind deaktiviert. In /etc/tmm/config.json web.allow_remote_administration auf true setzen und tmm-web neu starten."});
Object.assign(I18N.fr,{"admin.remoteDisabled":"Les modifications à distance sont désactivées. Définissez web.allow_remote_administration sur true dans /etc/tmm/config.json, puis redémarrez tmm-web."});
Object.assign(I18N.ja,{"admin.remoteDisabled":"リモート変更は無効です。/etc/tmm/config.json の web.allow_remote_administration を true にし、tmm-web を再起動してください。"});
Object.assign(I18N.en,{"addons.configure":"Configure channels","addons.name":"Name","addons.mode":"Mode","addons.active":"Active","addons.record":"Record history","addons.recordAll":"Record all","addons.offAll":"Turn all off","addons.scale":"Scale","addons.offset":"Offset","addons.unit":"Unit","addons.decimals":"Decimals","addons.threshold":"Change threshold","addons.save":"Apply I/O settings","addons.saved":"I/O settings accepted; the card collector reloads them automatically."});
Object.assign(I18N.de,{"addons.configure":"Kanäle konfigurieren","addons.name":"Name","addons.mode":"Modus","addons.active":"Aktiv","addons.record":"Verlauf aufzeichnen","addons.recordAll":"Alle aufzeichnen","addons.offAll":"Alle ausschalten","addons.scale":"Faktor","addons.offset":"Offset","addons.unit":"Einheit","addons.decimals":"Nachkommastellen","addons.threshold":"Änderungs-Schwellwert","addons.save":"E/A-Einstellungen übernehmen","addons.saved":"E/A-Einstellungen übernommen; der Karten-Collector lädt sie automatisch neu."});
Object.assign(I18N.fr,{"addons.configure":"Configurer les canaux","addons.name":"Nom","addons.mode":"Mode","addons.active":"Actif","addons.record":"Enregistrer l’historique","addons.recordAll":"Tout enregistrer","addons.offAll":"Tout désactiver","addons.scale":"Échelle","addons.offset":"Décalage","addons.unit":"Unité","addons.decimals":"Décimales","addons.threshold":"Seuil de variation","addons.save":"Appliquer les réglages E/S","addons.saved":"Réglages E/S acceptés ; le collecteur les recharge automatiquement."});
Object.assign(I18N.ja,{"addons.configure":"チャンネル設定","addons.name":"名称","addons.mode":"モード","addons.active":"有効","addons.record":"履歴を記録","addons.recordAll":"すべて記録","addons.offAll":"すべてオフ","addons.scale":"倍率","addons.offset":"オフセット","addons.unit":"単位","addons.decimals":"小数桁","addons.threshold":"変化しきい値","addons.save":"I/O設定を適用","addons.saved":"I/O設定を受け付けました。カードコレクターが自動再読み込みします。"});
Object.assign(I18N.en,{"addons.gpioPin":"BCM GPIO","addons.gpioPull":"Internal pull","addons.gpioInvert":"Active LOW"});
Object.assign(I18N.de,{"addons.gpioPin":"BCM-GPIO","addons.gpioPull":"Interner Pull-Widerstand","addons.gpioInvert":"LOW-aktiv"});
Object.assign(I18N.fr,{"addons.gpioPin":"GPIO BCM","addons.gpioPull":"Résistance interne","addons.gpioInvert":"Actif à LOW"});
Object.assign(I18N.ja,{"addons.gpioPin":"BCM GPIO","addons.gpioPull":"内部プル抵抗","addons.gpioInvert":"LOW アクティブ"});
Object.assign(I18N.en,{"addons.gpioSafetyTitle":"Electrical safety — 3.3 V GPIO only","addons.gpioSafetyDetail":"Never connect 5 V, 24 V or machine signals directly. This passive terminal HAT provides no galvanic isolation or overvoltage protection. Use a suitable isolated interface."});
Object.assign(I18N.de,{"addons.gpioSafetyTitle":"Elektrische Sicherheit — ausschließlich 3,3-V-GPIO","addons.gpioSafetyDetail":"Niemals 5 V, 24 V oder Maschinensignale direkt anschließen. Dieser passive Klemmen-HAT besitzt weder galvanische Trennung noch Überspannungsschutz. Eine geeignete, galvanisch getrennte Schnittstelle verwenden."});
Object.assign(I18N.fr,{"addons.gpioSafetyTitle":"Sécurité électrique — GPIO 3,3 V uniquement","addons.gpioSafetyDetail":"Ne jamais raccorder directement du 5 V, du 24 V ou des signaux machine. Ce HAT passif ne fournit ni isolation galvanique ni protection contre les surtensions. Utilisez une interface isolée adaptée."});
Object.assign(I18N.ja,{"addons.gpioSafetyTitle":"電気安全 — GPIO は 3.3 V 専用","addons.gpioSafetyDetail":"5 V、24 V、または機械信号を直接接続しないでください。この端子 HAT には絶縁も過電圧保護もありません。適切な絶縁インターフェースを使用してください。"});
Object.assign(I18N.en,{"addons.notConfigured":"Not configured on this TMM","addons.reference":"Support reference — no polling","addons.setupHint":"Can be added through Setup","addons.hardware.raspberry_pi_gpio":"Raspberry Pi GPIO terminal HAT","addons.hardware.sequent_16inpind":"16 LV Digital Inputs","addons.hardware.sequent_24b8vin":"8 × 24-bit Analog Inputs DAQ","addons.hardware.sequent_multiio":"Multi-IO","addons.hardware.sequent_smart_fan":"Smart Fan","addons.hardware.sequent_super_watchdog":"Super Watchdog & UPS"});
Object.assign(I18N.de,{"addons.notConfigured":"Auf diesem TMM nicht konfiguriert","addons.reference":"Support-Referenz — keine Abfrage","addons.setupHint":"Kann über das Setup hinzugefügt werden","addons.hardware.raspberry_pi_gpio":"Raspberry-Pi-GPIO-Klemmen-HAT","addons.hardware.sequent_16inpind":"16 Niederspannungs-Digitaleingänge","addons.hardware.sequent_24b8vin":"8 × 24-Bit-Analogeingänge DAQ","addons.hardware.sequent_multiio":"Multi-I/O","addons.hardware.sequent_smart_fan":"Smart Fan","addons.hardware.sequent_super_watchdog":"Super Watchdog & UPS"});
Object.assign(I18N.fr,{"addons.notConfigured":"Non configuré sur ce TMM","addons.reference":"Référence support — aucune interrogation","addons.setupHint":"Peut être ajouté via la configuration","addons.hardware.raspberry_pi_gpio":"HAT à bornes GPIO Raspberry Pi","addons.hardware.sequent_16inpind":"16 entrées numériques basse tension","addons.hardware.sequent_24b8vin":"8 entrées analogiques 24 bits DAQ","addons.hardware.sequent_multiio":"Multi-IO","addons.hardware.sequent_smart_fan":"Smart Fan","addons.hardware.sequent_super_watchdog":"Super Watchdog & UPS"});
Object.assign(I18N.ja,{"addons.notConfigured":"この TMM では未設定","addons.reference":"サポート参照 — ポーリングなし","addons.setupHint":"セットアップから追加できます","addons.hardware.raspberry_pi_gpio":"Raspberry Pi GPIO 端子 HAT","addons.hardware.sequent_16inpind":"16 低電圧デジタル入力","addons.hardware.sequent_24b8vin":"8 × 24 ビットアナログ入力 DAQ","addons.hardware.sequent_multiio":"Multi-IO","addons.hardware.sequent_smart_fan":"Smart Fan","addons.hardware.sequent_super_watchdog":"Super Watchdog & UPS"});
Object.assign(I18N.en,{"addons.showReferences":"Show supported hardware"});
Object.assign(I18N.de,{"addons.showReferences":"Unterstützte Hardware anzeigen"});
Object.assign(I18N.fr,{"addons.showReferences":"Afficher le matériel pris en charge"});
Object.assign(I18N.ja,{"addons.showReferences":"対応ハードウェアを表示"});
Object.assign(I18N.en,{"header.eyebrow":"TMM · Version 1.3"});
Object.assign(I18N.de,{"header.eyebrow":"TMM · Version 1.3"});
Object.assign(I18N.fr,{"header.eyebrow":"TMM · Version 1.3"});
Object.assign(I18N.ja,{"header.eyebrow":"TMM · バージョン1.3"});
Object.assign(I18N.en,{"footer.summary":"monitoring with guarded parameter service · refreshes every 3 seconds","bridge.design":"Proxy inactive","bridge.help":"Configured inline path between HMI and inverter.","bridge.observability":"Observed data","bridge.warning":"Inline operation is unavailable. Check configuration and runtime diagnostics.","bridge.backendPending":"Backend reload pending"});
Object.assign(I18N.de,{"footer.summary":"Überwachung mit abgesichertem Parameterservice · Aktualisierung alle 3 Sekunden","bridge.design":"Proxy inaktiv","bridge.help":"Konfigurierter Inline-Pfad zwischen HMI und Umrichter.","bridge.observability":"Beobachtete Daten","bridge.warning":"Der Inline-Betrieb ist nicht verfügbar. Konfiguration und Laufzeitdiagnose prüfen.","bridge.backendPending":"Backend-Neustart ausstehend"});
Object.assign(I18N.fr,{"footer.summary":"surveillance avec service de paramètres sécurisé · actualisation toutes les 3 secondes","bridge.design":"Proxy inactif","bridge.help":"Chemin en ligne configuré entre l’IHM et le variateur.","bridge.observability":"Données observées","bridge.warning":"Le fonctionnement en ligne est indisponible. Vérifiez la configuration et le diagnostic d’exécution.","bridge.backendPending":"Redémarrage du backend en attente"});
Object.assign(I18N.ja,{"footer.summary":"監視および保護されたパラメータサービス・3秒ごとに更新","bridge.design":"プロキシ停止中","bridge.help":"HMI とインバータ間に設定されたインライン経路です。","bridge.observability":"監視データ","bridge.warning":"インライン動作を利用できません。設定と実行時診断を確認してください。","bridge.backendPending":"バックエンド再起動待ち"});

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
  en:{"recording.eyebrow":"Recording","recording.title":"Investigation & database","recording.current":"Current reference","recording.newReference":"Reference for the new recording","recording.archive":"Archive database and start new recording","recording.danger":"Danger zone: permanently delete current database","recording.deleteHelp":"Enter DELETE three times, separated by spaces. This operation cannot be undone.","recording.delete":"Permanently delete and start new recording","recording.accepted":"Request accepted; waiting for the collector…","recording.referenceRequired":"Enter an investigation reference.","recording.complete":"New recording initialized.","recording.failed":"Operation failed","recording.delayed":"The collector has not confirmed the request yet; status checks continue."},
  de:{"recording.eyebrow":"Aufzeichnung","recording.title":"Untersuchung & Datenbank","recording.current":"Aktuelle Referenz","recording.newReference":"Referenz der neuen Aufzeichnung","recording.archive":"Datenbank archivieren und neue Aufzeichnung starten","recording.danger":"Gefahrenzone: aktuelle Datenbank endgültig löschen","recording.deleteHelp":"DELETE dreimal, durch Leerzeichen getrennt, eingeben. Dieser Vorgang kann nicht rückgängig gemacht werden.","recording.delete":"Endgültig löschen und neue Aufzeichnung starten","recording.accepted":"Auftrag angenommen; warte auf den Collector…","recording.referenceRequired":"Bitte eine Untersuchungsreferenz eingeben.","recording.complete":"Neue Aufzeichnung initialisiert.","recording.failed":"Vorgang fehlgeschlagen","recording.delayed":"Der Collector hat den Auftrag noch nicht bestätigt; die Statusprüfung läuft weiter."},
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
  en:{"metric.input_terminal_status":"Input terminals F/R/S1/S2/S3","metric.terminal_f":"Terminal F","metric.terminal_r":"Terminal R","metric.terminal_s1":"Terminal S1","metric.terminal_s2":"Terminal S2","metric.terminal_s3":"Terminal S3","metric.fm_analog_output":"FM analog output","metric.trip_output_frequency":"Trip snapshot: output frequency","metric.trip_operating_status":"Trip snapshot: operating status","metric.trip_output_current":"Trip snapshot: output current","metric.trip_dc_input_voltage":"Trip snapshot: DC-link voltage","metric.trip_output_voltage":"Trip snapshot: output voltage","metric.past_trip_1":"Stored trip 1","metric.past_trip_2":"Stored trip 2","metric.past_trip_3":"Stored trip 3","metric.past_trip_4":"Stored trip 4"},
  de:{"metric.input_terminal_status":"Eingangsklemmen F/R/S1/S2/S3","metric.terminal_f":"Klemme F","metric.terminal_r":"Klemme R","metric.terminal_s1":"Klemme S1","metric.terminal_s2":"Klemme S2","metric.terminal_s3":"Klemme S3","metric.fm_analog_output":"FM-Analogausgang","metric.trip_output_frequency":"Trip-Momentaufnahme: Ausgangsfrequenz","metric.trip_operating_status":"Trip-Momentaufnahme: Betriebsstatus","metric.trip_output_current":"Trip-Momentaufnahme: Ausgangsstrom","metric.trip_dc_input_voltage":"Trip-Momentaufnahme: Zwischenkreis","metric.trip_output_voltage":"Trip-Momentaufnahme: Ausgangsspannung","metric.past_trip_1":"Gespeicherter Trip 1","metric.past_trip_2":"Gespeicherter Trip 2","metric.past_trip_3":"Gespeicherter Trip 3","metric.past_trip_4":"Gespeicherter Trip 4"},
  fr:{"metric.input_terminal_status":"Bornes d’entrée F/R/S1/S2/S3","metric.fm_analog_output":"Sortie analogique FM","metric.trip_output_frequency":"Instantané défaut : fréquence de sortie","metric.trip_operating_status":"Instantané défaut : état de fonctionnement","metric.trip_output_current":"Instantané défaut : courant de sortie","metric.trip_dc_input_voltage":"Instantané défaut : bus continu","metric.trip_output_voltage":"Instantané défaut : tension de sortie","metric.past_trip_1":"Défaut mémorisé 1","metric.past_trip_2":"Défaut mémorisé 2","metric.past_trip_3":"Défaut mémorisé 3","metric.past_trip_4":"Défaut mémorisé 4"},
  ja:{"metric.input_terminal_status":"入力端子 F/R/S1/S2/S3","metric.fm_analog_output":"FMアナログ出力","metric.trip_output_frequency":"トリップ時出力周波数","metric.trip_operating_status":"トリップ時運転状態","metric.trip_output_current":"トリップ時出力電流","metric.trip_dc_input_voltage":"トリップ時直流リンク電圧","metric.trip_output_voltage":"トリップ時出力電圧","metric.past_trip_1":"保存トリップ1","metric.past_trip_2":"保存トリップ2","metric.past_trip_3":"保存トリップ3","metric.past_trip_4":"保存トリップ4"}
};
for (const code of Object.keys(CHANNEL_METRIC_I18N)) Object.assign(I18N[code], CHANNEL_METRIC_I18N[code]);
Object.assign(I18N.en,{"metric.terminal_f":"Terminal F","metric.terminal_r":"Terminal R","metric.terminal_s1":"Terminal S1","metric.terminal_s2":"Terminal S2","metric.terminal_s3":"Terminal S3"});
Object.assign(I18N.de,{"metric.terminal_f":"Klemme F","metric.terminal_r":"Klemme R","metric.terminal_s1":"Klemme S1","metric.terminal_s2":"Klemme S2","metric.terminal_s3":"Klemme S3"});
Object.assign(I18N.fr,{"metric.terminal_f":"Borne F","metric.terminal_r":"Borne R","metric.terminal_s1":"Borne S1","metric.terminal_s2":"Borne S2","metric.terminal_s3":"Borne S3"});
Object.assign(I18N.ja,{"metric.terminal_f":"端子 F","metric.terminal_r":"端子 R","metric.terminal_s1":"端子 S1","metric.terminal_s2":"端子 S2","metric.terminal_s3":"端子 S3"});
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
Object.assign(I18N.en,{"conditions.eyebrow":"Monitoring","conditions.title":"Condition monitoring & milestones","conditions.help":"Create persistent events from measured conditions. Equality uses the configured tolerance.","conditions.name":"Rule name","conditions.channel":"Operand / channel","conditions.operator":"Operator","conditions.value":"Comparison value","conditions.duration":"Minimum duration (s)","conditions.hysteresis":"Hysteresis","conditions.tolerance":"Equality tolerance","conditions.severity":"Severity","conditions.enabled":"Enabled","conditions.save":"Save rule","conditions.new":"New rule","conditions.milestones":"Recent milestones","conditions.none":"No rules configured.","conditions.noMilestones":"No milestones recorded.","conditions.edit":"Edit","conditions.delete":"Delete","conditions.saved":"Rule accepted.","conditions.enter":"Condition entered","conditions.exit":"Condition cleared"});
Object.assign(I18N.de,{"conditions.eyebrow":"Überwachung","conditions.title":"Condition-Monitoring & Milestones","conditions.help":"Erzeugt dauerhafte Ereignisse aus Messbedingungen. Gleichheit verwendet die konfigurierte Toleranz.","conditions.name":"Regelname","conditions.channel":"Operand / Kanal","conditions.operator":"Operator","conditions.value":"Vergleichswert","conditions.duration":"Mindestdauer (s)","conditions.hysteresis":"Hysterese","conditions.tolerance":"Gleichheitstoleranz","conditions.severity":"Schweregrad","conditions.enabled":"Aktiv","conditions.save":"Regel speichern","conditions.new":"Neue Regel","conditions.milestones":"Letzte Milestones","conditions.none":"Keine Regeln konfiguriert.","conditions.noMilestones":"Noch keine Milestones aufgezeichnet.","conditions.edit":"Bearbeiten","conditions.delete":"Löschen","conditions.saved":"Regel übernommen.","conditions.enter":"Bedingung eingetreten","conditions.exit":"Bedingung aufgehoben"});
Object.assign(I18N.fr,{"conditions.eyebrow":"Surveillance","conditions.title":"Surveillance conditionnelle et jalons","conditions.help":"Crée des événements persistants à partir des mesures. L’égalité utilise la tolérance configurée.","conditions.name":"Nom de règle","conditions.channel":"Opérande / canal","conditions.operator":"Opérateur","conditions.value":"Valeur de comparaison","conditions.duration":"Durée minimale (s)","conditions.hysteresis":"Hystérésis","conditions.tolerance":"Tolérance d’égalité","conditions.severity":"Sévérité","conditions.enabled":"Activée","conditions.save":"Enregistrer","conditions.new":"Nouvelle règle","conditions.milestones":"Jalons récents","conditions.none":"Aucune règle configurée.","conditions.noMilestones":"Aucun jalon enregistré.","conditions.edit":"Modifier","conditions.delete":"Supprimer","conditions.saved":"Règle acceptée.","conditions.enter":"Condition déclenchée","conditions.exit":"Condition terminée"});
Object.assign(I18N.ja,{"conditions.eyebrow":"監視","conditions.title":"状態監視・マイルストーン","conditions.help":"測定条件から永続イベントを作成します。等価比較には設定した許容差を使用します。","conditions.name":"ルール名","conditions.channel":"オペランド／チャンネル","conditions.operator":"演算子","conditions.value":"比較値","conditions.duration":"最小継続時間（秒）","conditions.hysteresis":"ヒステリシス","conditions.tolerance":"等価許容差","conditions.severity":"重大度","conditions.enabled":"有効","conditions.save":"ルールを保存","conditions.new":"新規ルール","conditions.milestones":"最近のマイルストーン","conditions.none":"ルールはありません。","conditions.noMilestones":"マイルストーンはありません。","conditions.edit":"編集","conditions.delete":"削除","conditions.saved":"ルールを受け付けました。","conditions.enter":"条件成立","conditions.exit":"条件解除"});
Object.assign(I18N.en,{"conditions.expression":"Rule expression"});
Object.assign(I18N.de,{"conditions.expression":"Regelausdruck"});
Object.assign(I18N.fr,{"conditions.expression":"Expression de règle"});
Object.assign(I18N.ja,{"conditions.expression":"ルール式"});
Object.assign(I18N.en,{"conditions.logic":"Combine operands with","conditions.addOperand":"Add operand","conditions.removeOperand":"Remove","conditions.operand":"Additional operand"});
Object.assign(I18N.de,{"conditions.logic":"Operanden verknüpfen mit","conditions.addOperand":"Operand hinzufügen","conditions.removeOperand":"Entfernen","conditions.operand":"Weiterer Operand"});
Object.assign(I18N.fr,{"conditions.logic":"Combiner les opérandes avec","conditions.addOperand":"Ajouter un opérande","conditions.removeOperand":"Supprimer","conditions.operand":"Opérande supplémentaire"});
Object.assign(I18N.ja,{"conditions.logic":"オペランドの結合","conditions.addOperand":"オペランドを追加","conditions.removeOperand":"削除","conditions.operand":"追加オペランド"});
const BRIDGE_I18N={
  en:{"bridge.eyebrow":"Bus observability","bridge.title":"Communication bridge & bus observer","bridge.design":"Design phase · inactive","bridge.help":"Planned inline path between HMI and inverter. This development stage never opens a serial port.","bridge.hmi":"HMI / master","bridge.drive":"Inverter / slave","bridge.proxy":"Inline bridge","bridge.capture":"Forward & observe","bridge.phases":"Implementation phases","bridge.readiness":"Safety readiness","bridge.observability":"Planned observations","bridge.warning":"Inline operation remains locked until deterministic forwarding, write de-duplication, watchdog behaviour, and an external hardware bypass have been verified.","bridge.notConfigured":"Not configured","bridge.phase.passive_observer":"Passive observer and frame decoder","bridge.phase.transparent_proxy":"Deterministic transparent proxy","bridge.phase.scheduled_polling":"Scheduled TMM queries in verified idle windows","bridge.check.two_endpoints":"Two serial endpoints configured","bridge.check.distinct_endpoints":"Separate adapters assigned","bridge.check.stable_device_paths":"Stable /dev/serial/by-id paths","bridge.check.hardware_bypass_declared":"External hardware bypass declared","bridge.cap.frames":"Request and response frames","bridge.cap.latency":"Response latency","bridge.cap.exceptions":"Modbus exceptions","bridge.cap.crc_errors":"CRC and framing errors","bridge.cap.register_activity":"Register activity","bridge.cap.write_audit":"Write audit"},
  de:{"bridge.eyebrow":"Bus-Beobachtung","bridge.title":"Kommunikationsbrücke & Bus-Observer","bridge.design":"Entwurfsphase · inaktiv","bridge.help":"Geplanter Inline-Pfad zwischen HMI und Umrichter. Dieser Entwicklungsstand öffnet keine serielle Schnittstelle.","bridge.hmi":"HMI / Master","bridge.drive":"Umrichter / Slave","bridge.proxy":"Inline-Brücke","bridge.capture":"Weiterleiten & beobachten","bridge.phases":"Implementierungsstufen","bridge.readiness":"Sicherheitsbereitschaft","bridge.observability":"Geplante Beobachtungen","bridge.warning":"Der Inline-Betrieb bleibt gesperrt, bis deterministische Weiterleitung, Schreib-Deduplizierung, Watchdog-Verhalten und ein externer Hardware-Bypass verifiziert sind.","bridge.notConfigured":"Nicht konfiguriert","bridge.phase.passive_observer":"Passiver Observer und Telegrammdecoder","bridge.phase.transparent_proxy":"Deterministischer transparenter Proxy","bridge.phase.scheduled_polling":"Geplante TMM-Abfragen in verifizierten Buspausen","bridge.check.two_endpoints":"Zwei serielle Endpunkte konfiguriert","bridge.check.distinct_endpoints":"Getrennte Adapter zugeordnet","bridge.check.stable_device_paths":"Stabile /dev/serial/by-id-Pfade","bridge.check.hardware_bypass_declared":"Externer Hardware-Bypass angegeben","bridge.cap.frames":"Anfrage- und Antworttelegramme","bridge.cap.latency":"Antwortlatenz","bridge.cap.exceptions":"Modbus-Ausnahmen","bridge.cap.crc_errors":"CRC- und Rahmenfehler","bridge.cap.register_activity":"Registeraktivität","bridge.cap.write_audit":"Schreib-Audit"},
  fr:{"bridge.eyebrow":"Observation du bus","bridge.title":"Pont de communication et observateur de bus","bridge.design":"Phase de conception · inactive","bridge.help":"Chemin en ligne prévu entre l’IHM et le variateur. Cette version n’ouvre aucun port série.","bridge.hmi":"IHM / maître","bridge.drive":"Variateur / esclave","bridge.proxy":"Pont en ligne","bridge.capture":"Transmettre et observer","bridge.phases":"Phases de mise en œuvre","bridge.readiness":"Préparation de sécurité","bridge.observability":"Observations prévues","bridge.warning":"Le fonctionnement en ligne reste verrouillé jusqu’à validation du transfert déterministe, de la déduplication des écritures, du watchdog et d’un bypass matériel externe.","bridge.notConfigured":"Non configuré","bridge.phase.passive_observer":"Observateur passif et décodeur de trames","bridge.phase.transparent_proxy":"Proxy transparent déterministe","bridge.phase.scheduled_polling":"Requêtes TMM dans des fenêtres libres vérifiées","bridge.check.two_endpoints":"Deux ports série configurés","bridge.check.distinct_endpoints":"Adaptateurs distincts affectés","bridge.check.stable_device_paths":"Chemins /dev/serial/by-id stables","bridge.check.hardware_bypass_declared":"Bypass matériel externe déclaré","bridge.cap.frames":"Trames de requête et réponse","bridge.cap.latency":"Latence de réponse","bridge.cap.exceptions":"Exceptions Modbus","bridge.cap.crc_errors":"Erreurs CRC et de trame","bridge.cap.register_activity":"Activité des registres","bridge.cap.write_audit":"Audit des écritures"},
  ja:{"bridge.eyebrow":"バス監視","bridge.title":"通信ブリッジ・バスオブザーバー","bridge.design":"設計段階・無効","bridge.help":"HMIとインバーター間のインライン経路を計画中です。この段階ではシリアルポートを開きません。","bridge.hmi":"HMI / マスター","bridge.drive":"インバーター / スレーブ","bridge.proxy":"インラインブリッジ","bridge.capture":"転送・監視","bridge.phases":"実装段階","bridge.readiness":"安全準備状況","bridge.observability":"計画中の監視項目","bridge.warning":"決定論的転送、書込み重複防止、ウォッチドッグ動作、外部ハードウェアバイパスを検証するまでインライン運転はロックされます。","bridge.notConfigured":"未設定","bridge.phase.passive_observer":"パッシブ監視とフレーム解析","bridge.phase.transparent_proxy":"決定論的透過プロキシ","bridge.phase.scheduled_polling":"検証済みアイドル時間でのTMM照会","bridge.check.two_endpoints":"2つのシリアル端点を設定","bridge.check.distinct_endpoints":"別々のアダプターを割当","bridge.check.stable_device_paths":"安定した/dev/serial/by-idパス","bridge.check.hardware_bypass_declared":"外部ハードウェアバイパスを宣言","bridge.cap.frames":"要求・応答フレーム","bridge.cap.latency":"応答遅延","bridge.cap.exceptions":"Modbus例外","bridge.cap.crc_errors":"CRC・フレームエラー","bridge.cap.register_activity":"レジスター動作","bridge.cap.write_audit":"書込み監査"}
};
for(const code of Object.keys(BRIDGE_I18N))Object.assign(I18N[code],BRIDGE_I18N[code]);
Object.assign(I18N.en,{"bridge.backendPending":"Design phase · backend reload pending"});
Object.assign(I18N.de,{"bridge.backendPending":"Entwurfsphase · Backend-Neustart ausstehend"});
Object.assign(I18N.fr,{"bridge.backendPending":"Phase de conception · redémarrage du backend en attente"});
Object.assign(I18N.ja,{"bridge.backendPending":"設計段階・バックエンド再起動待ち"});
Object.assign(I18N.en,{"bridge.active":"Transparent proxy · active","bridge.helpActive":"Live inline path: HMI telegrams and inverter responses are forwarded unchanged and logged. TMM does not issue polling requests.","bridge.warningActive":"Availability note: an optional normally-closed hardware bypass can reconnect HMI and inverter directly if the host or either USB adapter is unavailable."});
Object.assign(I18N.de,{"bridge.active":"Transparenter Proxy · aktiv","bridge.helpActive":"Aktiver Inline-Pfad: HMI-Telegramme und Umrichterantworten werden unverändert weitergeleitet und protokolliert. TMM sendet keine eigenen Polling-Anfragen.","bridge.warningActive":"Verfügbarkeitshinweis: Ein optionaler, stromlos geschlossener Hardware-Bypass kann HMI und Umrichter direkt verbinden, falls Host oder USB-Adapter ausfallen."});
Object.assign(I18N.fr,{"bridge.active":"Proxy transparent · actif","bridge.helpActive":"Chemin en ligne actif : les télégrammes IHM et les réponses du variateur sont transmis sans modification et journalisés. TMM n’émet aucune requête d’interrogation.","bridge.warningActive":"Note de disponibilité : un bypass matériel normalement fermé, facultatif, peut reconnecter directement l’IHM et le variateur si l’hôte ou un adaptateur USB est indisponible."});
Object.assign(I18N.ja,{"bridge.active":"透過プロキシ・稼働中","bridge.helpActive":"稼働中のインライン経路です。HMI電文とインバーター応答を変更せず転送・記録し、TMM独自のポーリング要求は送信しません。","bridge.warningActive":"可用性に関する注記：オプションの常閉ハードウェアバイパスにより、ホストまたはUSBアダプター停止時にHMIとインバーターを直接再接続できます。"});
Object.assign(I18N.en,{"bridge.observability":"Observed data"});
Object.assign(I18N.de,{"bridge.observability":"Beobachtete Daten"});
Object.assign(I18N.fr,{"bridge.observability":"Données observées"});
Object.assign(I18N.ja,{"bridge.observability":"監視データ"});
Object.assign(I18N.en,{"bridge.statusError":"Bridge status unavailable"});
Object.assign(I18N.de,{"bridge.statusError":"Bridge-Status nicht verfügbar"});
Object.assign(I18N.fr,{"bridge.statusError":"État du pont indisponible"});
Object.assign(I18N.ja,{"bridge.statusError":"ブリッジ状態を取得できません"});
Object.assign(I18N.en,{"diag.proxyMode":"Operating mode","diag.proxy":"Transparent proxy","diag.transactions":"Transactions (60 s)","diag.forwarded":"Forwarded","diag.errors":"Proxy errors","diag.telegramAge":"Last telegram age","diag.telegramRate":"Telegrams/s","diag.responseAverage":"Average response time","diag.responseMaximum":"Maximum response time","diag.crcErrors":"CRC errors","diag.timeouts":"Response timeouts","diag.partial":"Partial requests","diag.noTelegrams":"No telegram received yet"});
Object.assign(I18N.de,{"diag.proxyMode":"Betriebsart","diag.proxy":"Transparenter Proxy","diag.transactions":"Transaktionen (60 s)","diag.forwarded":"Weitergeleitet","diag.errors":"Proxy-Fehler","diag.telegramAge":"Alter des letzten Telegramms","diag.telegramRate":"Telegramme/s","diag.responseAverage":"Mittlere Antwortzeit","diag.responseMaximum":"Maximale Antwortzeit","diag.crcErrors":"CRC-Fehler","diag.timeouts":"Antwort-Timeouts","diag.partial":"Unvollständige Anfragen","diag.noTelegrams":"Noch kein Telegramm empfangen"});
Object.assign(I18N.fr,{"diag.proxyMode":"Mode de fonctionnement","diag.proxy":"Proxy transparent","diag.transactions":"Transactions (60 s)","diag.forwarded":"Transmises","diag.errors":"Erreurs proxy","diag.telegramAge":"Âge du dernier télégramme","diag.telegramRate":"Télégrammes/s","diag.responseAverage":"Temps de réponse moyen","diag.responseMaximum":"Temps de réponse maximal","diag.crcErrors":"Erreurs CRC","diag.timeouts":"Délais de réponse dépassés","diag.partial":"Requêtes incomplètes","diag.noTelegrams":"Aucun télégramme reçu"});
Object.assign(I18N.ja,{"diag.proxyMode":"動作モード","diag.proxy":"透過プロキシ","diag.transactions":"トランザクション（60秒）","diag.forwarded":"転送済み","diag.errors":"プロキシエラー","diag.telegramAge":"最終電文からの経過時間","diag.telegramRate":"電文/秒","diag.responseAverage":"平均応答時間","diag.responseMaximum":"最大応答時間","diag.crcErrors":"CRCエラー","diag.timeouts":"応答タイムアウト","diag.partial":"不完全な要求","diag.noTelegrams":"電文はまだ受信されていません"});
Object.assign(I18N.en,{"bridge.configuredOffline":"Transparent proxy · configured, offline"});
Object.assign(I18N.de,{"bridge.configuredOffline":"Transparenter Proxy · konfiguriert, offline"});
Object.assign(I18N.fr,{"bridge.configuredOffline":"Proxy transparent · configuré, hors ligne"});
Object.assign(I18N.ja,{"bridge.configuredOffline":"透過プロキシ・設定済み、オフライン"});
Object.assign(I18N.en,{"bridge.warning":"Configure two distinct stable serial endpoints before enabling the inline proxy."});
Object.assign(I18N.de,{"bridge.warning":"Vor Aktivierung des Inline-Proxys müssen zwei getrennte, stabile serielle Endpunkte konfiguriert sein."});
Object.assign(I18N.fr,{"bridge.warning":"Configurez deux ports série stables et distincts avant d’activer le proxy en ligne."});
Object.assign(I18N.ja,{"bridge.warning":"インラインプロキシを有効にする前に、2つの異なる安定したシリアル端点を設定してください。"});
Object.assign(I18N.en,{"bridge.check.devices_present":"Both configured adapters are present","bridge.runtimeError":"Proxy connection"});
Object.assign(I18N.de,{"bridge.check.devices_present":"Beide konfigurierten Adapter sind vorhanden","bridge.runtimeError":"Proxy-Verbindung"});
Object.assign(I18N.fr,{"bridge.check.devices_present":"Les deux adaptateurs configurés sont présents","bridge.runtimeError":"Connexion du proxy"});
Object.assign(I18N.ja,{"bridge.check.devices_present":"設定済みの両方のアダプターが存在","bridge.runtimeError":"プロキシ接続"});
Object.assign(I18N.en,{"bridge.hmiPriority":"HMI priority active · TMM polling suppressed","bridge.persistenceHealthy":"Background logging queue healthy","bridge.persistenceDropped":"Background logging dropped diagnostic records"});
Object.assign(I18N.de,{"bridge.hmiPriority":"HMI-Priorität aktiv · TMM-Abfragen unterdrückt","bridge.persistenceHealthy":"Hintergrund-Protokollqueue fehlerfrei","bridge.persistenceDropped":"Hintergrund-Protokollierung hat Diagnosedatensätze verworfen"});
Object.assign(I18N.en,{"bridge.persistenceRecovered":"Background logging recovered; historical diagnostic gap","bridge.persistenceLost":"lost"});
Object.assign(I18N.de,{"bridge.persistenceRecovered":"Hintergrund-Protokollierung wiederhergestellt; historische Diagnoselücke","bridge.persistenceLost":"verloren"});
Object.assign(I18N.fr,{"bridge.hmiPriority":"Priorité IHM active · requêtes TMM supprimées","bridge.persistenceHealthy":"File de journalisation en arrière-plan opérationnelle","bridge.persistenceDropped":"La journalisation a rejeté des diagnostics"});
Object.assign(I18N.ja,{"bridge.hmiPriority":"HMI優先が有効・TMMポーリング抑止中","bridge.persistenceHealthy":"バックグラウンド記録キュー正常","bridge.persistenceDropped":"バックグラウンド記録が診断データを破棄"});
Object.assign(I18N.en,{"bridge.adapterPresent":"Serial converter connected","bridge.adapterMissing":"Serial converter not connected","alerts.proxy":"Communication proxy","alerts.adapterMissing":"Serial converter not connected"});
Object.assign(I18N.de,{"bridge.adapterPresent":"Serial-Konverter gesteckt","bridge.adapterMissing":"Serial-Konverter nicht gesteckt","alerts.proxy":"Kommunikations-Proxy","alerts.adapterMissing":"Serial-Konverter nicht gesteckt"});
Object.assign(I18N.fr,{"bridge.adapterPresent":"Convertisseur série connecté","bridge.adapterMissing":"Convertisseur série non connecté","alerts.proxy":"Proxy de communication","alerts.adapterMissing":"Convertisseur série non connecté"});
Object.assign(I18N.ja,{"bridge.adapterPresent":"シリアルコンバーター接続済み","bridge.adapterMissing":"シリアルコンバーター未接続","alerts.proxy":"通信プロキシ","alerts.adapterMissing":"シリアルコンバーター未接続"});
Object.assign(I18N.en,{"bridge.adaptersReady":"Both serial converters detected by the host"});
Object.assign(I18N.de,{"bridge.adaptersReady":"Beide Serial-Konverter wurden vom Host erkannt"});
Object.assign(I18N.fr,{"bridge.adaptersReady":"Les deux convertisseurs série sont détectés par l’hôte"});
Object.assign(I18N.ja,{"bridge.adaptersReady":"両方のシリアルコンバーターをホストが検出済み"});
Object.assign(I18N.en,{"bridge.hmiFriendly":"Adapter A · HMI / master","bridge.driveFriendly":"Adapter B · inverter / slave","bridge.usbSerial":"USB serial","bridge.swapped":"Serial adapters probably swapped","bridge.swappedDetail":"Valid Modbus master requests were repeatedly received on the configured inverter side. Check or exchange the adapter assignments."});
Object.assign(I18N.de,{"bridge.hmiFriendly":"Adapter A · HMI / Master","bridge.driveFriendly":"Adapter B · Umrichter / Slave","bridge.usbSerial":"USB-Seriennummer","bridge.swapped":"Serial-Konverter vermutlich vertauscht","bridge.swappedDetail":"Auf der konfigurierten Umrichter-Seite wurden wiederholt gültige Modbus-Masteranfragen empfangen. Adapterzuordnung prüfen oder tauschen."});
Object.assign(I18N.fr,{"bridge.hmiFriendly":"Adaptateur A · IHM / maître","bridge.driveFriendly":"Adaptateur B · variateur / esclave","bridge.usbSerial":"Numéro de série USB","bridge.swapped":"Convertisseurs série probablement inversés","bridge.swappedDetail":"Des requêtes maître Modbus valides ont été reçues plusieurs fois du côté variateur configuré. Vérifiez ou inversez les adaptateurs."});
Object.assign(I18N.ja,{"bridge.hmiFriendly":"アダプターA・HMI / マスター","bridge.driveFriendly":"アダプターB・インバーター / スレーブ","bridge.usbSerial":"USBシリアル番号","bridge.swapped":"シリアルコンバーターが逆の可能性","bridge.swappedDetail":"設定されたインバーター側で有効なModbusマスター要求を繰り返し検出しました。アダプター割当を確認または交換してください。"});
Object.assign(I18N.en,{"rtu.title":"Modbus RTU evidence logbook","rtu.help":"Recent raw proxy transactions with independently calculated CRC.","rtu.refresh":"Refresh","rtu.time":"Time","rtu.outcome":"Outcome","rtu.request":"HMI request","rtu.requestCrc":"Request CRC","rtu.response":"Inverter response","rtu.responseCrc":"Response CRC","rtu.latency":"Latency","rtu.empty":"No proxy transactions recorded.","rtu.received":"received","rtu.calculated":"calculated","rtu.slave":"Slave","rtu.function":"Function"});
Object.assign(I18N.de,{"rtu.title":"Modbus-RTU-Nachweislogbuch","rtu.help":"Letzte Proxy-Rohtelegramme mit unabhängig berechneter CRC.","rtu.refresh":"Aktualisieren","rtu.time":"Zeit","rtu.outcome":"Ergebnis","rtu.request":"HMI-Anfrage","rtu.requestCrc":"Anfrage-CRC","rtu.response":"Umrichterantwort","rtu.responseCrc":"Antwort-CRC","rtu.latency":"Laufzeit","rtu.empty":"Keine Proxy-Transaktionen aufgezeichnet.","rtu.received":"empfangen","rtu.calculated":"berechnet","rtu.slave":"Slave","rtu.function":"Funktion"});
Object.assign(I18N.fr,{"rtu.title":"Journal de preuve Modbus RTU","rtu.help":"Dernières trames brutes du proxy avec CRC calculé indépendamment.","rtu.refresh":"Actualiser","rtu.time":"Heure","rtu.outcome":"Résultat","rtu.request":"Requête IHM","rtu.requestCrc":"CRC requête","rtu.response":"Réponse variateur","rtu.responseCrc":"CRC réponse","rtu.latency":"Latence","rtu.empty":"Aucune transaction proxy enregistrée.","rtu.received":"reçu","rtu.calculated":"calculé","rtu.slave":"Esclave","rtu.function":"Fonction"});
Object.assign(I18N.ja,{"rtu.title":"Modbus RTU証跡ログ","rtu.help":"独立計算CRC付きの最新プロキシ生電文。","rtu.refresh":"更新","rtu.time":"時刻","rtu.outcome":"結果","rtu.request":"HMI要求","rtu.requestCrc":"要求CRC","rtu.response":"インバーター応答","rtu.responseCrc":"応答CRC","rtu.latency":"遅延","rtu.empty":"プロキシトランザクションは記録されていません。","rtu.received":"受信","rtu.calculated":"計算","rtu.slave":"スレーブ","rtu.function":"機能"});
Object.assign(I18N.en,{"rtu.origin":"Origin","rtu.originHmi":"HMI","rtu.originTmm":"TMM idle poll","diag.tmmPolls":"TMM idle polls (60 s)","diag.tmmPollSuccess":"TMM poll successful","diag.tmmPollErrors":"TMM poll errors","bridge.helpScheduled":"Live inline path with prioritized HMI forwarding. TMM inserts one bounded monitoring read at a time only in verified idle windows."});
Object.assign(I18N.de,{"rtu.origin":"Ursprung","rtu.originHmi":"HMI","rtu.originTmm":"TMM-Leerlaufabfrage","diag.tmmPolls":"TMM-Leerlaufabfragen (60 s)","diag.tmmPollSuccess":"TMM-Abfragen erfolgreich","diag.tmmPollErrors":"TMM-Abfragefehler","bridge.helpScheduled":"Aktiver Inline-Pfad mit priorisierter HMI-Weiterleitung. TMM fügt nur in verifizierten Buspausen jeweils eine zeitlich begrenzte Überwachungsabfrage ein."});
Object.assign(I18N.fr,{"rtu.origin":"Origine","rtu.originHmi":"IHM","rtu.originTmm":"Interrogation TMM au repos","diag.tmmPolls":"Interrogations TMM au repos (60 s)","diag.tmmPollSuccess":"Interrogations TMM réussies","diag.tmmPollErrors":"Erreurs d’interrogation TMM","bridge.helpScheduled":"Chemin actif avec priorité à l’IHM. TMM insère une seule lecture de surveillance limitée dans les fenêtres d’inactivité vérifiées."});
Object.assign(I18N.ja,{"rtu.origin":"送信元","rtu.originHmi":"HMI","rtu.originTmm":"TMMアイドル照会","diag.tmmPolls":"TMMアイドル照会（60秒）","diag.tmmPollSuccess":"TMM照会成功","diag.tmmPollErrors":"TMM照会エラー","bridge.helpScheduled":"HMI転送を優先するアクティブ経路。TMMは確認済みアイドル時間に限定監視読取りを1件ずつ挿入します。"});
Object.assign(I18N.en,{"bridge.activeScheduled":"Transparent proxy + TMM monitoring · active"});
Object.assign(I18N.de,{"bridge.activeScheduled":"Transparenter Proxy + TMM-Überwachung · aktiv"});
Object.assign(I18N.fr,{"bridge.activeScheduled":"Proxy transparent + surveillance TMM · actifs"});
Object.assign(I18N.ja,{"bridge.activeScheduled":"透過プロキシ + TMM監視・稼働中"});
Object.assign(I18N.en,{"diag.passiveReads":"HMI reads adopted (60 s)","diag.passiveSamples":"Measurements adopted from HMI","rtu.adopted":"measurements adopted","bridge.helpPassive":"Live inline path: TMM passively decodes valid HMI read responses and adopts matching configured measurements without generating bus traffic."});
Object.assign(I18N.de,{"diag.passiveReads":"Übernommene HMI-Lesevorgänge (60 s)","diag.passiveSamples":"Vom HMI übernommene Messwerte","rtu.adopted":"Messwerte übernommen","bridge.helpPassive":"Aktiver Inline-Pfad: TMM dekodiert gültige HMI-Leseantworten passiv und übernimmt passende konfigurierte Messwerte, ohne zusätzlichen Busverkehr zu erzeugen."});
Object.assign(I18N.fr,{"diag.passiveReads":"Lectures IHM reprises (60 s)","diag.passiveSamples":"Mesures reprises de l’IHM","rtu.adopted":"mesures reprises","bridge.helpPassive":"Chemin actif : TMM décode passivement les réponses de lecture IHM valides et reprend les mesures configurées correspondantes sans trafic de bus supplémentaire."});
Object.assign(I18N.ja,{"diag.passiveReads":"取り込んだHMI読取り（60秒）","diag.passiveSamples":"HMIから取り込んだ測定値","rtu.adopted":"測定値を取込み","bridge.helpPassive":"稼働中の経路：TMMは有効なHMI読取り応答を受動的に解析し、追加のバス通信を発生させずに一致する設定済み測定値を取り込みます。"});

let language = localStorage.getItem("tmm-language") || "en";
let measurementHints = localStorage.getItem("tmm-measurement-hints") === "true";
const t = (key) => I18N[language]?.[key] || I18N.en[key] || key;
const metricName = (key) => t(`metric.${key}`) || key.replaceAll("_", " ");
const OFFLINE_DOCUMENTS = {
  raspberry_pi_gpio: { base: "gpio", schematic: "raspberry-pi-gpio-input-schematic.pdf" },
  sequent_16inpind: { base: "sequent", manual: ["16inpind-users-guide-v1.pdf", "https://cdn.shopify.com/s/files/1/0534/4392/0067/files/16-INPUTS-UsersGuide_fe9f7d34-7077-4415-af79-57fdae1e534f.pdf?v=1704912646"], schematic: ["16inpind-schematic-v2.pdf", "https://cdn.shopify.com/s/files/1/0534/4392/0067/files/16-INPUTS-Schematic.pdf?v=1643422376"] },
  sequent_24b8vin: { base: "sequent", manual: ["24b8vin-users-guide-v1.2.pdf", "https://cdn.shopify.com/s/files/1/0534/4392/0067/files/8-24-Bit_Analog_Inputs-UsersGuide.pdf?v=1786810944"], schematic: ["24b8vin-schematic-v1.1.pdf", "https://cdn.shopify.com/s/files/1/0534/4392/0067/files/8-24BIT-A2D-V1_1-Schematic.pdf?v=1738101478"] },
  sequent_multiio: { base: "sequent", manual: ["multiio-users-guide-v1.3.pdf", "https://cdn.shopify.com/s/files/1/0534/4392/0067/files/Multi-IO-UsersGuide.pdf?v=1719204229"], schematic: ["multiio-schematic-v3.2.pdf", "https://cdn.shopify.com/s/files/1/0534/4392/0067/files/MULTI-IO-SCHEMATIC-V3_2.pdf?v=1781918917"] },
  sequent_super_watchdog: { base: "sequent", manual: ["super-watchdog-users-guide-v6.pdf", "https://cdn.shopify.com/s/files/1/0534/4392/0067/files/WATCHDOG-UsersGuide-V6.pdf?v=1683864119"], schematic: ["super-watchdog-schematic-v9.pdf", "https://cdn.shopify.com/s/files/1/0534/4392/0067/files/Watchdog-V9-Schematic.pdf?v=1730944465"] },
  sequent_smart_fan: { base: "sequent", manual: ["smart-fan-users-guide.pdf", "https://cdn.shopify.com/s/files/1/0534/4392/0067/files/SmartFan-UsersGuide.pdf?v=1643426365"], schematic: ["smart-fan-schematic-v5.pdf", "https://cdn.shopify.com/s/files/1/0534/4392/0067/files/Smart-FAN-Schematic-V5.pdf?v=1680968853"] },
};
function appendSequentDocumentation(parent, type) {
  const documents = OFFLINE_DOCUMENTS[type];
  if (!documents) return;
  const local = documents.base !== "sequent" || window.TMM_SEQUENT_DOCS_LOCAL === true;
  const labels = (local ? {
    en: ["Offline PDFs:", "User manual", "Schematic", "Open locally installed PDF"], de: ["Offline-PDFs:", "Benutzerhandbuch", "Schaltplan", "Lokal installiertes PDF öffnen"],
    fr: ["PDF hors ligne :", "Manuel utilisateur", "Schéma", "Ouvrir le PDF installé localement"], ja: ["オフラインPDF：", "ユーザーマニュアル", "回路図", "ローカルにインストールされたPDFを開く"],
  } : {
    en: ["Manufacturer documents:", "User manual", "Schematic", "Open official publisher PDF"], de: ["Herstellerdokumente:", "Benutzerhandbuch", "Schaltplan", "Offizielles Hersteller-PDF öffnen"],
    fr: ["Documents fabricant :", "Manuel utilisateur", "Schéma", "Ouvrir le PDF officiel du fabricant"], ja: ["メーカー資料：", "ユーザーマニュアル", "回路図", "メーカー公式PDFを開く"],
  })[language] || ["Manufacturer documents:", "User manual", "Schematic", "Open official publisher PDF"];
  const box = document.createElement("nav"); box.className = "addon-documents"; box.setAttribute("aria-label", labels[0]);
  const title = document.createElement("span"); title.textContent = labels[0];
  for (const [kind, reference] of Object.entries(documents)) {
    if (kind === "base") continue;
    const [filename, officialUrl] = Array.isArray(reference) ? reference : [reference, null];
    const link = document.createElement("a"); link.href = local ? `/static/docs/${documents.base}/${filename}` : officialUrl; link.target = "_blank"; link.rel = "noopener";
    link.textContent = kind === "manual" ? labels[1] : labels[2]; link.title = labels[3]; box.append(link);
  }
  parent.append(title, box);
}
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
const DASHBOARD_SECTION_ORDER_KEY = "tmm-dashboard-section-order";
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
  if (!collapsed && section.dataset.sectionId === "history-title") scheduleHistoryRender();
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
  if (!Array.isArray(order)) return false;
  const currentSet = new Set(current); const seen = new Set();
  const saved = order.filter(id => typeof id === "string" && currentSet.has(id) && !seen.has(id) && seen.add(id));
  if (!saved.length) return false;
  // Reorder known categories in their existing slots. Newly added categories
  // remain at their intended default position; removed categories are ignored.
  const savedSet = new Set(saved); let savedIndex = 0;
  const normalized = current.map(id => savedSet.has(id) ? saved[savedIndex++] : id);
  const main = $("main"); const byId = new Map(collapsibleSections.map(section => [section.dataset.sectionId, section]));
  for (const id of normalized) main.append(byId.get(id));
  collapsibleSections = normalized.map(id => byId.get(id));
  return true;
}
async function loadDashboardSectionOrder() {
  try {
    const localOrder = JSON.parse(localStorage.getItem(DASHBOARD_SECTION_ORDER_KEY) || "null");
    if (applyDashboardSectionOrder(localOrder)) return;
  } catch {}
  try {
    if (applyDashboardSectionOrder((await getJSON("/api/v1/dashboard-section-order")).order)) {
      localStorage.setItem(DASHBOARD_SECTION_ORDER_KEY, JSON.stringify(dashboardSectionOrder()));
    }
  }
  catch (error) { $("#last-error").textContent = error.message; }
}
function saveDashboardSectionOrder() {
  const order = dashboardSectionOrder();
  try { localStorage.setItem(DASHBOARD_SECTION_ORDER_KEY, JSON.stringify(order)); }
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
  if (Number.isFinite(Number(threshold.critical_low)) && Number(value) <= Number(threshold.critical_low)) return "critical";
  if (Number(value) >= Number(threshold.critical)) return "critical";
  if (Number.isFinite(Number(threshold.warning_low)) && Number(value) <= Number(threshold.warning_low)) return "warning";
  if (Number(value) >= Number(threshold.warning)) return "warning";
  return null;
}

const liveSignalStates = new Map();
function liveSignalSeverity(item, threshold) {
  if (item.decoded?.severity) return item.decoded.severity;
  if (!Number.isFinite(Number(item.value)) || item.unit === "on/off" || item.unit === "raw" || typeof item.digitalState === "boolean") return null;
  const key = `${item.inverter}\u001f${item.metric}`; const value = Number(item.value);
  const previous = liveSignalStates.get(key);
  const decimals = Number(item.channel?.decimals ?? 2);
  const configuredDelta = Number(item.channel?.change_threshold);
  const changeThreshold = Number.isFinite(configuredDelta) && configuredDelta > 0 ? configuredDelta : .5 * 10 ** -Math.max(0, decimals);
  const absolute = thresholdSeverity(value, threshold);
  const changed = previous && Math.abs(value - previous.value) >= changeThreshold;
  const abnormal = absolute === "warning" || changed;
  const streak = abnormal ? (previous?.streak || 0) + 1 : 0;
  liveSignalStates.set(key, { value, streak });
  if (absolute === "critical" || streak >= 3) return "critical";
  if (abnormal) return "warning";
  return "normal";
}

function renderAlerts(items, telemetry = {}, thresholds = { system: {}, metrics: {} }, storage = null, addons = null) {
  const container = $("#alerts"); container.replaceChildren(); const messages = [];
  for (const item of items) {
    const threshold = thresholds.metrics?.[item.metric]; const severity = thresholdSeverity(item.value, threshold);
    if (severity) messages.push({ severity, source: item.inverter, label: metricName(item.metric), value: `${Number(item.value).toLocaleString(locale(), { maximumFractionDigits: 2 })} ${item.unit}`, threshold: threshold[severity] });
    if (["operating_status", "trip_code", "alarm_information_1", "alarm_information_2"].includes(item.metric) && ["warning", "critical"].includes(item.decoded?.severity)) {
      messages.push({ severity: item.decoded.severity, source: item.inverter, label: metricName(item.metric), value: localizedDecoded(item), threshold: null });
    }
  }
  for (const addon of addons?.items || []) {
    // An externally disabled card is intentionally not polled.  Its lack of
    // samples is therefore neither a fault nor useful information.
    if (addon.enabled === false) continue;
    const observedAt = addon.values?.[0]?.observed_at;
    const ageSeconds = observedAt ? (Date.now() - Date.parse(observedAt)) / 1000 : Infinity;
    const stale = ageSeconds > Math.max(5, Number(addon.interval_seconds || 1) * 4);
    // A UPS used solely for its independent protection function, and an I/O
    // card whose channels are all Off, are deliberately not observed in the
    // dashboard.  Their absence must not generate stale-data information.
    const hasActiveChannel = (addon.channels || []).some(channel=>channel.enabled !== false && (channel.live === true || channel.record === true));
    if (addon.health?.error) messages.push({ severity: "critical", source: t("addons.alert"), label: addon.label, value: addon.health.error, threshold: null });
    // A card which has not delivered a value recently may simply be powered
    // down or intentionally disconnected.  Keep this visible, but reserve
    // warnings for process limits and critical for actual card I/O errors.
    else if (hasActiveChannel && stale) messages.push({ severity: "info", source: t("addons.alert"), label: addon.label, value: t("addons.stale"), threshold: null });
  }
  for(const missing of state.bridge?.missing_adapters || []) {
    messages.push({severity:"critical",source:t("alerts.proxy"),label:t("alerts.adapterMissing"),value:`${missing.id==="hmi"?t("bridge.hmi"):t("bridge.drive")} · ${missing.device}`,threshold:null});
  }
  if(state.bridge?.wiring_diagnostic?.state==="adapters_swapped_suspected") messages.push({severity:"critical",source:t("alerts.proxy"),label:t("bridge.swapped"),value:t("bridge.swappedDetail"),threshold:null});
  const thermal=telemetry.thermal_protection;
  if (thermal?.state === "throttled" || thermal?.state === "paused") messages.push({
    severity: thermal.state === "paused" ? "critical" : "warning", source:t("alerts.system"), label:t("thermal.label"),
    value:`${t(`thermal.${thermal.state}`)} · ${Number(thermal.temperature_celsius).toLocaleString(locale(),{maximumFractionDigits:1})} °C`, threshold:null,
  });
  const systemLabels = { cpu_percent: t("diag.hostCpu"), temperature_celsius: t("diag.temperature"), memory_percent: t("diag.hostMemory"), disk_percent: t("diag.disk") };
  for (const [key, threshold] of Object.entries(thresholds.system || {})) {
    const value = telemetry.system?.[key]; const severity = thresholdSeverity(value, threshold);
    if (severity) messages.push({ severity, source: t("alerts.system"), label: systemLabels[key] || key, value: `${Number(value).toLocaleString(locale(), { maximumFractionDigits: 1 })} ${key === "temperature_celsius" ? "°C" : "%"}`, threshold: threshold[severity] });
  }
  if (storage?.retention_exceeds_remaining_space) {
    const remaining=Number(storage.estimated_seconds_to_full);
    messages.push({ severity:"info", source:t("alerts.storage"), label:t("alerts.retentionRisk"), value:`${formatDuration(remaining)} < ${Number(storage.retention_days).toLocaleString(locale())} ${t("storage.days")}`, threshold:null });
  }
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

const state = { metric: "output_frequency", inverter: null, latest: [], history: [], historySelected: new Set(), historyExportSelected: new Set(), historyHover: null, historyGeometry: null, historyView: null, historyPan: null, historyMarkers: [], milestones: [], conditions: [], conditionCatalog: [], bridge: null, metadata: null, telemetry: null, storage: null, storageRefreshedAt: 0, engineering: [], channels: [], communicationChannels: [], metricCatalogLoaded: false, metricCatalogLoading: false, liveCardOrder: [], liveGroupOrder: [], liveOrderLoaded: false, liveOrderDragging: false, liveGroupDragging: false, addonDragging: false, addonInteracting: false, addonInteractionTimer: null, systemInteracting: false, systemInteractionTimer: null, previewBackupStale: false, previewTargetSha: null, previewInverter: null };
let refreshRunning = false;
const $ = (selector) => document.querySelector(selector);
const locale = () => ({ en:"en-US", de:"de-DE", fr:"fr-FR", ja:"ja-JP" })[language];
const timeText = (iso) => new Intl.DateTimeFormat(locale(), { dateStyle: "short", timeStyle: "medium" }).format(new Date(iso));
const panelRefreshVisible = (titleId) => {
  const panel = $(`#${titleId}`)?.closest("section");
  return document.visibilityState === "visible" && Boolean(panel) && !panel.classList.contains("is-collapsed");
};

async function getJSON(url, timeoutMs=8000) {
  const controller=new AbortController(); const timeout=setTimeout(()=>controller.abort(),timeoutMs);
  try {
    const response = await fetch(url, { cache: "no-store", signal:controller.signal });
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
    return response.json();
  } finally { clearTimeout(timeout); }
}
async function responseError(response) {
  const text = await response.text();
  let detail = text;
  try { detail = JSON.parse(text)?.detail || text; } catch (_) { /* plain-text response */ }
  if (response.status === 403 && detail === "administration is restricted to localhost") return new Error(t("admin.remoteDisabled"));
  return new Error(`${response.status} ${detail || response.statusText}`);
}
async function postJSON(url, body) {
  const response = await fetch(url, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(body) });
  if (!response.ok) throw await responseError(response);
  return response.json();
}
async function deleteJSON(url) {
  const response = await fetch(url, { method:"DELETE" });
  if (!response.ok) throw await responseError(response);
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

async function refreshRecording(expectedOperationId=null) {
  const data = await getJSON("/api/v1/recording");
  $("#recording-current").textContent = data.reference || "—";
  const operation=data.last_operation;
  if (expectedOperationId && operation?.operation_id !== expectedOperationId) return false;
  if (operation?.status === "complete") { $("#recording-result").textContent = t("recording.complete"); return true; }
  if (operation?.status === "error") { $("#recording-result").textContent = `${t("recording.failed")}: ${operation.detail}`; return true; }
  if (data.pending_operation) $("#recording-result").textContent = t("recording.accepted");
  return false;
}

async function requestRecording(action) {
  const reference = $("#recording-reference").value.trim();
  if (!reference) { $("#recording-result").textContent = t("recording.referenceRequired"); return; }
  const confirmation = action === "delete" ? $("#recording-delete-confirmation").value : "";
  try {
    const accepted=await postJSON("/api/v1/recording/reinitialize", { action, reference, confirmation });
    $("#recording-result").textContent = t("recording.accepted");
    const buttons=[$("#recording-archive"),$("#recording-delete")]; buttons.forEach(button=>button.disabled=true);
    let complete=false;
    for(let attempt=0;attempt<120&&!complete;attempt++) {
      await new Promise(resolve=>setTimeout(resolve,1000));
      try { complete=await refreshRecording(accepted.operation_id); } catch (_) { /* transient dashboard/API outage */ }
    }
    if(!complete) $("#recording-result").textContent=t("recording.delayed");
    buttons.forEach(button=>button.disabled=false);
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

function showChannels(_name) { /* Channel modes are configured only in history cards. */ }
async function loadChannels() {
  const [data, communication]=await Promise.all([getJSON("/api/v1/channels"), getJSON("/api/v1/communication/channels")]);
  state.channels=data.inverters || []; state.communicationChannels=communication.channels || [];
  await populateMetricSelector([], false);
  showChannels(state.inverter || state.channels[0]?.name);
  if (state.latest.length) renderFaultMemory(state.latest);
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
    await postJSON("/api/v1/channels",{inverter:state.inverter,channels});
    showTemporarySuccess("#channels-result",t("channels.saved"),event?.currentTarget);
    // Off is a display choice as well as a collector choice.  Rebuild the
    // metric list now, rather than retaining an old selected snapshot until a
    // complete browser reload.
    state.metadata=null; state.history=[]; state.metricCatalogLoaded=false; $("#metric").replaceChildren(); $("#export-selected").hidden=true;
    await loadChannels(); await refresh();
  }
  catch(error) { showPersistentResult("#channels-result",`${t("recording.failed")}: ${error.message}`); }
}
async function refreshParameterBackups() {
  const inverter=$("#backup-inverter").value; const suffix=inverter ? `?inverter=${encodeURIComponent(inverter)}` : ""; const data=await getJSON(`/api/v1/parameter-backups${suffix}`); const result=$("#backup-result");
  if (data.status==="complete") result.textContent=`${t("backup.complete")}: ${data.records} · ${data.file}`;
  else if (data.status==="complete_with_warnings") result.textContent=`${t("backup.partial")}: ${data.refreshed_records}/${data.records} · ${data.retained_records} ${t("backup.retained")} · ${data.file}`;
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
  if (file.size < 1 || file.size > 300000) { $("#backup-result").textContent=`${t("backup.failed")}: ${t("backup.invalidFileSize")} (${formatBytes(file.size)})`; return; }
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
    $("#preview-result").textContent=data.changes.length ? `${data.changes.length} ${t("preview.changes")} · ${data.current_file} · ${ageText}${data.backup_stale ? ` · ${t("preview.stale")}` : ""}` : t("preview.none");
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
  if (!csvFile) { $("#write-result").textContent=t("write.csvRequired"); return; }
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
  if(data.status==="complete") $("#write-result").textContent=`${t("write.complete")}: ${count} ${t("write.parameters")}${detail ? ` · ${detail}` : ""}`;
  else if(data.status==="partial") $("#write-result").textContent=`${t("write.partial")}: ${count} ${t("write.parameters")}${detail ? ` · ${detail}` : ""}. ${data.detail}`;
  else if(data.status==="error") $("#write-result").textContent=`${t("write.failed")}: ${data.detail}`;
}
async function refreshParameterAudit() {
  const data=await getJSON("/api/v1/parameter-changes"); const body=$("#parameter-audit-table tbody"); body.replaceChildren();
  for (const item of data.items || []) { const row=document.createElement("tr"); for (const value of [new Date(item.changed_at).toLocaleString(locale()),item.inverter,item.address,item.old,item.new,item.verified]) { const cell=document.createElement("td"); cell.textContent=value; row.append(cell); } body.append(row); }
  $("#parameter-audit-empty").textContent=(data.items||[]).length ? "" : t("audit.empty");
}

function addonLiveItems(addons) {
  const result = [];
  for (const addon of addons?.items || []) {
    const channels = new Map((addon.channels || []).map(channel => [`${channel.signal || "input"}:${channel.channel}`, channel]));
    for (const item of addon.values || []) {
      const leaf = item.metric.split(".").at(-1) || "";
      if (leaf === "communication_status") continue;
      const system=["sequent_super_watchdog", "sequent_smart_fan"].includes(addon.type);
      if (system) {
        const channel=(addon.channels || []).find(entry=>entry.metric===leaf);
        // System measurements are opt-out: the eye button creates a channel
        // override only when an operator changes the default live state.
        if (channel && (channel.enabled === false || channel.live === false)) continue;
        result.push({ ...item, liveAddon:true, addonLabel:addon.label, channel:channel || {} });
        continue;
      }
      const match = leaf.match(/^(.+)_(\d+)$/); if (!match) continue;
      const [, signal, numberText] = match; const number = Number(numberText);
      const channel = channels.get(`${signal}:${number}`) || channels.get(`input:${number}`);
      if (!channel?.live) continue;
      result.push({ ...item, liveAddon: true, addonLabel: addon.label, channel });
    }
    if (addon.type === "sequent_super_watchdog" && addon.battery_estimate) {
      const estimate=addon.battery_estimate, charging=estimate.state.startsWith("charge_");
      const displayValue=["estimated", "charge_estimated"].includes(estimate.state) ? formatDuration(estimate.remaining_seconds) : estimate.state === "mains" ? t("ups.mains") : charging ? t("ups.chargeLearning") : t("ups.learning");
      result.push({
        inverter:`addon:${addon.id}`, metric:`addon.${addon.id}.estimated_battery_runtime`, liveAddon:true, addonLabel:addon.label,
        channel:{label:charging ? t("ups.chargeRemaining") : t("ups.remaining")}, unit:"", value:0,
        displayValue, digitalState:estimate.state === "mains" || charging,
        detail:estimate.battery_voltage == null ? "" : `${Number(estimate.battery_voltage).toLocaleString(locale(), {maximumFractionDigits:2})} V`,
      });
    }
  }
  return result;
}

function communicationLiveItems() {
  const communication=state.telemetry?.communication;
  if (!communication) return [];
  const definitions={
    "communication.samples_per_second": ["Samples per second", "samples/s", "samples_per_second", 1],
    "communication.average_cycle_ms": ["Average cycle time", "ms", "average_cycle_ms", 1],
    "communication.maximum_cycle_ms": ["Maximum cycle time", "ms", "maximum_cycle_ms", 1],
    "communication.bus_utilization_percent": ["Bus utilization", "%", "bus_utilization_percent", 1],
    "communication.retries": ["Retries per minute", "count", "retries", 0],
    "communication.success_percent": ["Successful reads", "%", "success_percent", 1],
  };
  return state.communicationChannels
    .filter(channel=>["live", "record"].includes(channel.mode) && definitions[channel.key])
    .map(channel=>{
      const [label, unit, property, decimals]=definitions[channel.key], value=Number(communication[property]);
      return { inverter:"communication", metric:channel.key, liveAddon:true, addonLabel:historySourceLabel("communication"),
        channel:{label, decimals}, unit, value:Number.isFinite(value) ? value : 0,
        observed_at:new Date().toISOString() };
    });
}

function renderCards(items, thresholds = {}, addons = state.addons) {
  const cards = $("#cards");
  cards.replaceChildren();
  const special = new Set(["communication_status", "trip_code", "trip_output_frequency", "trip_operating_status", "trip_output_current", "trip_dc_input_voltage", "trip_output_voltage", "past_trip_1", "past_trip_2", "past_trip_3", "past_trip_4", "inverter_capacity_code", "inverter_series_code", "cpu_version", "cpu2_version", "eeprom_version"]);
  const position = new Map(state.liveCardOrder.map((key, index) => [key, index]));
  const groupPosition = new Map(state.liveGroupOrder.map((key, index) => [key, index]));
  const derivedSources = { machine_speed:"calculated_motor_speed", actual_output_current:"output_current", actual_output_voltage:"output_voltage", actual_motor_torque:"torque", mechanical_power:"torque" };
  const visible = [...items.filter((item) => {
    if (special.has(item.metric)) return false;
    const channel = state.channels.find(device => device.name === item.inverter)?.channels.find(entry => entry.key === (derivedSources[item.metric] || item.metric));
    // Alert monitors may still be returned while their channel is Off. They
    // feed the global warning indicator, but must not reappear as Live cards.
    return channel && ["live", "record"].includes(channel.mode);
  }), ...addonLiveItems(addons), ...communicationLiveItems()];
  visible.sort((left, right) => (position.get(`${left.inverter}\u001f${left.metric}`) ?? Number.MAX_SAFE_INTEGER) - (position.get(`${right.inverter}\u001f${right.metric}`) ?? Number.MAX_SAFE_INTEGER));
  const groups = new Map();
  for (const item of visible) {
    const groupLabel = item.liveAddon ? item.addonLabel : item.inverter;
    const groupKey = item.inverter;
    let group = groups.get(groupKey);
    if (!group) {
      group = document.createElement("section"); group.className = "live-card-group"; group.dataset.liveGroupKey=groupKey; group.draggable=true;
      const heading = document.createElement("h3"); heading.textContent = groupLabel;
      const grid = document.createElement("div"); grid.className = "cards live-card-grid";
      group.append(heading, grid); cards.append(group); groups.set(groupKey, group);
    }
    const card = document.createElement("article");
    card.className = "card";
    if (item.displayValue != null) card.classList.add("status-card");
    card.draggable = true; card.dataset.cardKey = `${item.inverter}\u001f${item.metric}`;
    const metricLeaf = item.metric.split(".").at(-1);
    const signalLevel = liveSignalSeverity(item, thresholds[item.metric] || thresholds[metricLeaf]);
    if (signalLevel) card.classList.add(`severity-${signalLevel}`);
    const digitalState = typeof item.digitalState === "boolean" ? item.digitalState
      : item.unit === "on/off" && Number.isFinite(Number(item.value)) ? Number(item.value) !== 0 : null;
    if (digitalState !== null) {
      card.classList.add("digital-state", digitalState ? "is-on" : "is-off");
    }
    const label = document.createElement("p"); label.className = "label";
    label.textContent = item.liveAddon ? (item.channel.label || item.metric_label || metricName(item.metric)) : `${item.inverter} · ${metricName(item.metric)}`;
    if (!item.liveAddon) appendMeasurementHint(label, item.metric, item);
    const line = document.createElement("p"); line.className = "value";
    const value = document.createElement("span"); value.textContent = item.displayValue ?? (item.unit === "raw" ? `0x${Number(item.raw_value ?? item.value).toString(16).toUpperCase().padStart(4, "0")}` : Number(item.value).toLocaleString(locale(), { maximumFractionDigits: Number(item.channel?.decimals ?? 2) }));
    const unit = document.createElement("span"); unit.className = "unit"; unit.textContent = item.unit === "raw" ? "" : item.unit;
    line.append(value, unit);
    const raw = document.createElement("p"); raw.className = "raw"; raw.textContent = item.displayValue != null ? item.detail : item.liveAddon ? item.metric : `${item.register_address} · raw ${item.raw_value}`;
    card.append(label, line);
    if (item.decoded) {
      const summary = document.createElement("p"); summary.className = "decoded-summary"; summary.textContent = localizedDecoded(item); card.append(summary);
      if (item.decoded.active?.length) {
        const details = document.createElement("ul"); details.className = "decoded-details";
        for (const entry of item.decoded.active) { const detail = document.createElement("li"); detail.textContent = entry.label; details.append(detail); }
        card.append(details);
      }
    }
    card.append(raw); group.querySelector(".live-card-grid").append(card);
  }
  [...groups.values()].sort((left,right)=>(groupPosition.get(left.dataset.liveGroupKey) ?? Number.MAX_SAFE_INTEGER)-(groupPosition.get(right.dataset.liveGroupKey) ?? Number.MAX_SAFE_INTEGER)).forEach(group=>cards.append(group));
  if (items.length) $("#updated").textContent = `${t("live.asOf")} ${timeText(items[0].observed_at)}`;
}

async function loadLiveCardOrder() {
  const [cards, groups] = await Promise.all([getJSON("/api/v1/live-card-order"), getJSON("/api/v1/live-group-order")]);
  state.liveCardOrder = Array.isArray(cards.order) ? cards.order : [];
  state.liveGroupOrder = Array.isArray(groups.order) ? groups.order : [];
  state.liveOrderLoaded = true;
}
async function saveLiveCardOrder() {
  const order = [...$("#cards").querySelectorAll("[data-card-key]")].map(card => card.dataset.cardKey);
  state.liveCardOrder = order;
  try { await postJSON("/api/v1/live-card-order", { order }); }
  catch (error) { $("#last-error").textContent = error.message; }
}
async function saveLiveGroupOrder() {
  const order=[...$("#cards").querySelectorAll(".live-card-group")].map(group=>group.dataset.liveGroupKey);
  state.liveGroupOrder=order;
  try { await postJSON("/api/v1/live-group-order",{order}); }
  catch(error) { $("#last-error").textContent=error.message; }
}
function installLiveCardDragAndDrop() {
  const cards = $("#cards");
  cards.addEventListener("dragstart", event => {
    const card = event.target.closest("[data-card-key]");
    if (card) {
      state.liveOrderDragging = true; card.classList.add("dragging");
      event.dataTransfer.effectAllowed = "move"; event.dataTransfer.setData("text/plain", card.dataset.cardKey); return;
    }
    const group=event.target.closest(".live-card-group"); if (!group) return;
    state.liveGroupDragging=true; group.classList.add("group-dragging");
    event.dataTransfer.effectAllowed="move"; event.dataTransfer.setData("text/plain",group.dataset.liveGroupKey);
  });
  cards.addEventListener("dragover", event => {
    if (state.liveGroupDragging) {
      event.preventDefault(); const target=event.target.closest(".live-card-group"), dragged=cards.querySelector(".group-dragging");
      cards.querySelectorAll(".group-drop-target").forEach(group=>group.classList.remove("group-drop-target"));
      if (!target || target===dragged) return;
      target.classList.add("group-drop-target"); const rect=target.getBoundingClientRect();
      cards.insertBefore(dragged,event.clientY<rect.top+rect.height/2 ? target : target.nextSibling); return;
    }
    if (!state.liveOrderDragging) return; event.preventDefault();
    const target = event.target.closest("[data-card-key]"); const dragged = cards.querySelector(".dragging");
    cards.querySelectorAll(".drop-target").forEach(card => card.classList.remove("drop-target"));
    if (!target || target === dragged) return;
    target.classList.add("drop-target");
    const rect = target.getBoundingClientRect();
    const group = target.closest(".live-card-grid");
    if (group) group.insertBefore(dragged, event.clientY < rect.top + rect.height / 2 ? target : target.nextSibling);
  });
  cards.addEventListener("dragend", event => {
    const card = event.target.closest("[data-card-key]");
    if (card) {
      card.classList.remove("dragging"); cards.querySelectorAll(".drop-target").forEach(entry => entry.classList.remove("drop-target"));
      if (state.liveOrderDragging) saveLiveCardOrder(); state.liveOrderDragging = false; return;
    }
    const group=event.target.closest(".live-card-group"); if (!group) return;
    group.classList.remove("group-dragging"); cards.querySelectorAll(".group-drop-target").forEach(entry=>entry.classList.remove("group-drop-target"));
    if (state.liveGroupDragging) saveLiveGroupOrder(); state.liveGroupDragging=false;
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

function renderAddons(data) {
  if (state.addonDragging || state.addonInteracting) return;
  const container = $("#addon-devices"); const help = $("#addons-help");
  // Refreshes occur every few seconds.  Preserve an operator's open form and
  // unsaved draft instead of replacing it halfway through an edit.
  const drafts = new Map([...container.querySelectorAll(".addon-config[open]")].map((details) => {
    const values = new Map();
    for (const row of details.querySelectorAll(".addon-config-row")) {
      const key = `${row.dataset.signal}:${row.dataset.channel}`;
      values.set(key, [...row.querySelectorAll("[data-field]")].map((input) => [input.dataset.field, input.type === "checkbox" ? input.checked : input.value]));
    }
    return [details.dataset.addonId, values];
  }));
  container.replaceChildren();
  const showReferences=$("#hardware-reference-toggle")?.checked !== false;
  const addons = (data?.items || []).filter(addon => !["sequent_super_watchdog", "sequent_smart_fan"].includes(addon.type) && (showReferences || addon.configured !== false)); help.hidden = addons.length > 0;
  for (const addon of addons) {
    const device = document.createElement("article"); device.className = `addon-device ${addon.enabled === false ? "disabled" : ""} ${addon.configured === false ? "hardware-reference" : ""}`;
    device.addEventListener("pointerenter", () => { clearTimeout(state.addonInteractionTimer); state.addonInteracting = true; });
    device.addEventListener("pointerleave", () => { clearTimeout(state.addonInteractionTimer); state.addonInteractionTimer = setTimeout(() => { state.addonInteracting = false; }, 250); });
    const header = document.createElement("div"); header.className = "addon-header"; const name = document.createElement("h3"); name.textContent = addon.configured === false ? t(`addons.hardware.${addon.type}`) : addon.label;
    const meta = document.createElement("p"); meta.className = "slave"; meta.textContent = addon.type === "raspberry_pi_gpio" ? `${addon.type} · ${t("addons.gpioPin")}` : `${addon.type} · Stack ${addon.stack}`;
    header.append(name, meta); appendSequentDocumentation(header, addon.type);
    if (addon.configured !== false) { const enabledButton=document.createElement("button"); enabledButton.type="button"; enabledButton.className="compact-button addon-enabled-button";
      enabledButton.textContent=t(addon.enabled === false ? "addons.enable" : "addons.disable"); enabledButton.setAttribute("aria-pressed",String(addon.enabled !== false));
      enabledButton.addEventListener("click",async()=>{ try { enabledButton.disabled=true; await postJSON("/api/v1/addons/enabled",{id:addon.id,enabled:addon.enabled === false}); state.metricCatalogLoaded=false; await loadChannels(); await refresh(); } catch(error) { health.textContent=error.message; health.classList.add("offline"); enabledButton.disabled=false; } }); header.append(enabledButton); }
    const health = document.createElement("p"); health.className = "addon-health"; let showHealth = false;
    if (addon.configured === false) { health.textContent=`${t("addons.notConfigured")} · ${t("addons.reference")} · ${t("addons.setupHint")}`; showHealth=true; }
    else if (addon.enabled === false) { health.textContent=t("addons.disabled"); showHealth=true; }
    else if (addon.health?.error) { health.textContent = `${t("addons.offline")}: ${addon.health.error}`; health.classList.add("offline"); showHealth=true; }
    else {
      const hasActiveChannel = (addon.channels || []).some(channel=>channel.enabled !== false && (channel.live === true || channel.record === true));
      if (!hasActiveChannel && addon.health) {
        health.textContent = `${t("addons.verified")} · ${t("live.asOf")} ${timeText(addon.health.observed_at)}`;
        showHealth=true;
      } else {
        const observedAt = addon.values?.[0]?.observed_at;
        const ageSeconds = observedAt ? (Date.now() - Date.parse(observedAt)) / 1000 : Infinity;
        // Values are heartbeated once per second. Five seconds tolerates normal
        // SQLite/UI jitter while making a stuck acquisition clearly visible.
        if (ageSeconds > Math.max(5, Number(addon.interval_seconds || 1) * 4)) {
          health.textContent = observedAt ? `${t("addons.stale")} · ${t("live.asOf")} ${timeText(observedAt)}` : t("addons.stale");
          health.classList.add("offline"); showHealth=true;
        }
      }
    }
    // Values are intentionally shown in “Current measurements”, alongside
    // inverter cards.  This page remains the wiring/channel configuration.
    device.append(header);
    if (addon.type === "raspberry_pi_gpio" && addon.configured !== false) {
      const warning=document.createElement("aside"); warning.className="gpio-safety-warning"; warning.setAttribute("role","note");
      const warningTitle=document.createElement("strong"); warningTitle.textContent=`⚠ ${t("addons.gpioSafetyTitle")}`;
      const warningDetail=document.createElement("span"); warningDetail.textContent=t("addons.gpioSafetyDetail");
      warning.append(warningTitle,warningDetail); device.append(warning);
    }
    if (showHealth) device.append(health);
    container.append(device);
    if (addon.configured === false) continue;
    const edit = document.createElement("details"); edit.className = "addon-config"; edit.dataset.addonId = addon.id;
    const summary = document.createElement("summary"); summary.textContent = t("addons.configure"); edit.append(summary);
    const fields = document.createElement("div"); fields.className = "addon-config-fields";
    const headings = document.createElement("div"); headings.className = "addon-config-heading";
    for (const title of [t("addons.name"), t("addons.scale"), t("addons.offset"), t("addons.unit"), t("addons.decimals"), t("addons.threshold")]) { const heading = document.createElement("span"); heading.textContent = title; headings.append(heading); }
    fields.append(headings);
    for (const channel of addon.channels || []) {
      const row = document.createElement("div"); row.className = "addon-config-row"; row.dataset.signal = channel.signal || "input"; row.dataset.channel = channel.channel;
      const nameInput = document.createElement("input"); nameInput.value = channel.label || ""; nameInput.placeholder = t("addons.name"); nameInput.dataset.field = "label";
      row.append(nameInput);
      const analog = addon.type === "sequent_24b8vin" || ["voltage", "current", "temperature"].includes(channel.signal);
      if (analog) for (const [field, value] of [["scale", channel.scale ?? 1], ["offset", channel.offset ?? 0], ["unit", channel.unit ?? ""], ["decimals", channel.decimals ?? 3], ["change_threshold", channel.change_threshold ?? 0]]) { const input = document.createElement("input"); input.dataset.field = field; input.value = value; input.placeholder = t(`addons.${field}`); row.append(input); }
      if (addon.type === "raspberry_pi_gpio") {
        const pull=document.createElement("select"); pull.dataset.field="pull"; for(const key of ["down","up","none"]){const option=document.createElement("option");option.value=key;option.textContent=`${t("addons.gpioPull")}: ${key}`;option.selected=(channel.pull || "down")===key;pull.append(option);} row.append(pull);
        const invertLabel=document.createElement("label"); const invert=document.createElement("input");invert.type="checkbox";invert.dataset.field="active_low";invert.checked=Boolean(channel.active_low);invertLabel.append(invert,document.createTextNode(t("addons.gpioInvert")));row.append(invertLabel);
      }
      fields.append(row);
    }
    const draft = drafts.get(addon.id);
    if (draft) {
      edit.open = true;
      for (const row of fields.children) for (const [field, value] of draft.get(`${row.dataset.signal}:${row.dataset.channel}`) || []) {
        const input = row.querySelector(`[data-field="${field}"]`);
        if (input) input.type === "checkbox" ? input.checked = value : input.value = value;
      }
    }
    const save = document.createElement("button"); save.type = "button"; save.className = "button compact-button"; save.textContent = t("addons.save");
    save.addEventListener("click", async () => { const channels = [...fields.querySelectorAll(".addon-config-row")].map(row => { const item={signal:row.dataset.signal,channel:Number(row.dataset.channel)}; row.querySelectorAll("[data-field]").forEach(input => item[input.dataset.field] = input.type === "checkbox" ? input.checked : input.value); return item; }); try { await postJSON("/api/v1/addons/channels", {id:addon.id,channels}); state.metricCatalogLoaded=false; confirmAction(save); await refresh(); } catch (error) { health.textContent=error.message; health.classList.add("offline"); } });
    edit.append(fields, save); device.append(edit);
  }
}

function renderUps(data) {
  if (state.systemInteracting) return;
  const container = $("#ups-devices"); const help = $("#ups-help"); container.replaceChildren();
  const showReferences=$("#hardware-reference-toggle")?.checked !== false;
  const cards = (data?.items || []).filter(addon => ["sequent_super_watchdog", "sequent_smart_fan"].includes(addon.type) && (showReferences || addon.configured !== false)); help.hidden = cards.length > 0;
  for (const addon of cards) {
    const device = document.createElement("article"); device.className = `addon-device ${addon.configured === false ? "hardware-reference" : ""}`; device.dataset.addonId=addon.id;
    const releaseInteraction = () => { clearTimeout(state.systemInteractionTimer); state.systemInteractionTimer = setTimeout(() => { if (!device.contains(document.activeElement)) state.systemInteracting = false; }, 500); };
    device.addEventListener("pointerenter", () => { clearTimeout(state.systemInteractionTimer); state.systemInteracting = true; });
    device.addEventListener("pointerleave", releaseInteraction);
    device.addEventListener("focusin", () => { clearTimeout(state.systemInteractionTimer); state.systemInteracting = true; });
    device.addEventListener("focusout", releaseInteraction);
    const header = document.createElement("div"); header.className = "addon-header"; const name = document.createElement("h3"); name.textContent = addon.configured === false ? t(`addons.hardware.${addon.type}`) : addon.label; header.append(name); appendSequentDocumentation(header, addon.type);
    device.append(header);
    const health = document.createElement("p"); health.className="addon-health";
    if (addon.configured === false) { health.textContent=`${t("addons.notConfigured")} · ${t("addons.reference")} · ${t("addons.setupHint")}`; device.append(health); }
    else if (addon.health?.error) { health.textContent=`${t("addons.offline")}: ${addon.health.error}`; health.classList.add("offline"); device.append(health); }
    container.append(device);
    if (addon.configured === false) continue;
    if (addon.type === "sequent_super_watchdog") { const controls = document.createElement("div"); controls.className="ups-controls"; const label = document.createElement("label"); label.textContent=t("ups.timeout"); const input=document.createElement("input"); input.type="number"; input.min="1"; input.max="86400"; input.step="1"; input.value=data.ups_shutdown?.input_loss_delay_seconds ?? 30; label.append(input); const save=document.createElement("button"); save.type="button"; save.className="button compact-button"; save.textContent=t("ups.save"); save.addEventListener("click", async()=>{ try { await postJSON("/api/v1/ups/shutdown-policy", {input_loss_delay_seconds:Number(input.value)}); confirmAction(save); } catch(error) { health.textContent=error.message; health.classList.add("offline"); if(!health.isConnected)device.append(health); } }); controls.append(label,save); device.append(controls); }
    if (addon.type === "sequent_smart_fan") { const policy=addon.fan_control || {}; const controls=document.createElement("div"); controls.className="ups-controls"; const makeNumber=(key,label,min,max)=>{const field=document.createElement("label"); field.textContent=label; const input=document.createElement("input"); input.type="number"; input.min=min; input.max=max; input.step="1"; input.value=policy[key]; field.append(input); return [field,input];}; const modeField=document.createElement("label"); modeField.textContent=t("fan.mode"); const mode=document.createElement("select"); for(const key of ["monitor","automatic","manual"]){const option=document.createElement("option"); option.value=key; option.textContent=t(`fan.${key}`); option.selected=policy.mode===key; mode.append(option);} modeField.append(mode); const [minimumField,minimum]=makeNumber("minimum_power_percent",t("fan.minimum"),0,100); const [startField,start]=makeNumber("start_temperature_c",t("fan.start"),20,100); const [fullField,full]=makeNumber("full_temperature_c",t("fan.full"),25,110); const [manualField,manual]=makeNumber("manual_power_percent",t("fan.manualPower"),0,100); const update=()=>{minimumField.hidden=startField.hidden=fullField.hidden=mode.value!=="automatic"; manualField.hidden=mode.value!=="manual";}; mode.addEventListener("change",update); update(); const save=document.createElement("button"); save.type="button"; save.className="button compact-button"; save.textContent=t("fan.save"); save.addEventListener("click",async()=>{try{await postJSON("/api/v1/fans/control-policy",{id:addon.id,control:{mode:mode.value,minimum_power_percent:Number(minimum.value),start_temperature_c:Number(start.value),full_temperature_c:Number(full.value),manual_power_percent:Number(manual.value),failsafe_power_percent:100}});confirmAction(save);await refresh();}catch(error){health.textContent=error.message;health.classList.add("offline");if(!health.isConnected)device.append(health);}}); controls.append(modeField,minimumField,startField,fullField,manualField,save); device.append(controls); }
    appendSystemChannelConfiguration(device, addon, health);
  }
}

function appendSystemChannelConfiguration(device, addon, health) {
  const details=document.createElement("details"); details.className="addon-config system-channel-config";
  const summary=document.createElement("summary"); summary.textContent=t("addons.configure"); details.append(summary);
  const fields=document.createElement("div"); fields.className="system-channel-fields";
  for(const channel of addon.channels || []) {
    if(!channel.metric) continue;
    const row=document.createElement("label"); row.className="system-channel-row";
    const label=document.createElement("span"); label.textContent=channel.metric_label || channel.metric;
    const mode=document.createElement("select"); mode.dataset.metric=channel.metric;
    const current=channel.enabled === false ? "off" : channel.record === true ? (channel.live === false ? "hide" : "record") : "live";
    for(const key of ["off","live","record","hide"]) { const option=document.createElement("option"); option.value=key; option.textContent=t(`channels.${key}`); option.selected=key===current; mode.append(option); }
    row.append(label,mode); fields.append(row);
  }
  const save=document.createElement("button"); save.type="button"; save.className="button compact-button"; save.textContent=t("channels.save");
  save.addEventListener("click",async()=>{ try { const channels=[...fields.querySelectorAll("select[data-metric]")].map(select=>({metric:select.dataset.metric,mode:select.value})); await postJSON("/api/v1/addons/channels",{id:addon.id,channels}); state.metricCatalogLoaded=false; confirmAction(save); await loadChannels(); await refresh(); } catch(error) { health.textContent=error.message; health.classList.add("offline"); if(!health.isConnected)device.append(health); } });
  details.append(fields,save); device.append(details);
}

function renderHealth(data, telemetry = {}) {
  const badge = $("#connection");
  badge.className = `status ${data.status}`;
  badge.querySelector("strong").textContent = t(`status.${data.status}`) || data.status;
  const devices = data.devices || [];
  const proxyMode=data.mode==="transparent_proxy" || telemetry.mode==="transparent_proxy";
  const proxy=telemetry.proxy || data.proxy || {};
  const values = proxyMode ? [
    [t("diag.proxyMode"),t("diag.proxy")],
    [t("diag.transactions"),Number(proxy.transactions || 0).toLocaleString(locale())],
    [t("diag.forwarded"),Number(proxy.forwarded || 0).toLocaleString(locale())],
    [t("diag.errors"),Number(proxy.errors || 0).toLocaleString(locale())],
    [t("diag.telegramAge"),proxy.age_seconds == null?t("diag.noTelegrams"):`${Number(proxy.age_seconds).toLocaleString(locale(),{maximumFractionDigits:1})} s`],
  ] : [
    [t("comm.drives"), devices.length || "–"],
    [t("comm.success"), devices.length ? devices.reduce((sum, item) => sum + item.successful_reads, 0) : "–"],
    [t("comm.failed"), devices.length ? devices.reduce((sum, item) => sum + item.failed_reads, 0) : "–"],
    [t("comm.age"), data.age_seconds == null ? "–" : `${data.age_seconds.toFixed(1)} s`],
  ];
  const communication = telemetry.communication || {}; const system = telemetry.system || {};
  if (proxyMode) values.push(
    [t("diag.telegramRate"),Number(proxy.transactions_per_second || 0).toLocaleString(locale(),{maximumFractionDigits:2})],
    [t("diag.responseAverage"),`${Number(proxy.average_latency_ms || 0).toLocaleString(locale(),{maximumFractionDigits:1})} ms`],
    [t("diag.responseMaximum"),`${Number(proxy.maximum_latency_ms || 0).toLocaleString(locale(),{maximumFractionDigits:1})} ms`],
    [t("diag.crcErrors"),Number(proxy.crc_errors || 0).toLocaleString(locale())],
    [t("diag.timeouts"),Number(proxy.timeouts || 0).toLocaleString(locale())],
    [t("diag.partial"),Number(proxy.partial_requests || 0).toLocaleString(locale())],
    [t("diag.passiveReads"),Number(proxy.passive_transactions || 0).toLocaleString(locale())],
    [t("diag.passiveSamples"),Number(proxy.passive_samples || 0).toLocaleString(locale())],
    [t("diag.tmmPolls"),Number(proxy.tmm_poll_transactions || 0).toLocaleString(locale())],
    [t("diag.tmmPollSuccess"),Number(proxy.tmm_poll_successes || 0).toLocaleString(locale())],
    [t("diag.tmmPollErrors"),Number(proxy.tmm_poll_errors || 0).toLocaleString(locale())],
  );
  else if (telemetry.communication) values.push(
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
  $("#last-error").textContent = proxyMode ? (["ok","broadcast",null,undefined].includes(proxy.last_outcome) ? "" : String(proxy.last_outcome)) : devices.filter((item) => item.error).map((item) => `${item.inverter}: ${item.error}`).join(" · ");
}

let rtuLogbookLoading=false;
function crcEvidenceText(evidence) {
  if(!evidence) return {text:"—",className:""};
  const valid=Boolean(evidence.valid);
  return {text:`${valid?"✓":"✕"} ${t("rtu.received")}: ${evidence.received || "—"} · ${t("rtu.calculated")}: ${evidence.calculated || "—"}`,className:valid?"crc-good":"crc-bad"};
}
async function refreshRtuLogbook() {
  if(rtuLogbookLoading || !$("#rtu-logbook")?.open) return;
  rtuLogbookLoading=true;
  try {
    const data=await getJSON("/api/v1/proxy-transactions?limit=100"), body=$("#rtu-logbook-body"), empty=$("#rtu-logbook-empty");
    body.replaceChildren(); empty.hidden=Boolean(data.items?.length);
    for(const item of data.items || []) {
      const row=document.createElement("tr"); row.className=["ok","broadcast"].includes(item.outcome)?"good":"bad";
      const cell=value=>{const td=document.createElement("td"); td.textContent=value; return td;};
      const raw=(value,meta="")=>{const td=document.createElement("td"); const code=document.createElement("code"); code.textContent=value || "—"; td.append(code); if(meta){const small=document.createElement("small"); small.textContent=meta; td.append(document.createElement("br"),small);} return td;};
      const adopted=Number(item.observed_samples || 0);
      const requestMeta=item.slave==null?"":`${t("rtu.slave")}: ${item.slave} (0x${Number(item.slave).toString(16).toUpperCase().padStart(2,"0")}) · ${t("rtu.function")}: ${item.function==null?"—":`0x${Number(item.function).toString(16).toUpperCase().padStart(2,"0")}`}${adopted?` · ${adopted} ${t("rtu.adopted")}`:""}`;
      const requestCrc=crcEvidenceText(item.request_crc), responseCrc=crcEvidenceText(item.response_crc);
      const requestCrcCell=cell(requestCrc.text); requestCrcCell.className=requestCrc.className;
      const responseCrcCell=cell(responseCrc.text); responseCrcCell.className=responseCrc.className;
      row.append(cell(timeText(item.request_at)),cell(t(item.origin==="tmm"?"rtu.originTmm":"rtu.originHmi")),cell(item.outcome),raw(item.request_hex,requestMeta),requestCrcCell,raw(item.response_hex),responseCrcCell,cell(item.latency_ms==null?"—":`${Number(item.latency_ms).toLocaleString(locale(),{maximumFractionDigits:2})} ms`));
      body.append(row);
    }
  } catch(error) { $("#rtu-logbook-empty").hidden=false; $("#rtu-logbook-empty").textContent=error.message; }
  finally { rtuLogbookLoading=false; }
}

function formatBytes(bytes) {
  if (!bytes) return "0 B";
  const units = ["B", "KiB", "MiB", "GiB", "TiB"]; const index = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  return `${(bytes / 1024 ** index).toLocaleString(locale(), { maximumFractionDigits: 1 })} ${units[index]}`;
}

function renderBridge(data) {
  state.bridge=data;
  const stage=$("#bridge-stage"), help=$("#bridge-help") || document.querySelector(".bridge-panel .hint"), warning=$("#bridge-warning") || $(".bridge-warning");
  if(stage) stage.textContent=t(data.enabled?(data.runtime_active===false?"bridge.configuredOffline":data.scheduled_polling?.enabled?"bridge.activeScheduled":"bridge.active"):"bridge.design");
  if(help) help.textContent=t(data.scheduled_polling?.enabled?"bridge.helpScheduled":data.enabled&&data.scheduled_polling?.passive_decode?"bridge.helpPassive":data.enabled?"bridge.helpActive":"bridge.help");
  if(warning) { warning.textContent=t(data.enabled?"bridge.warningActive":"bridge.warning"); warning.classList.toggle("advisory",Boolean(data.enabled)); }
  const runtimeError=$("#bridge-runtime-error"), missing=data.missing_adapters || [], swapped=data.wiring_diagnostic?.state==="adapters_swapped_suspected";
  let adapterSummary=$("#bridge-adapter-summary");
  if(!adapterSummary && help) {
    adapterSummary=document.createElement("p"); adapterSummary.id="bridge-adapter-summary"; adapterSummary.className="bridge-adapter-summary";
    help.insertAdjacentElement("afterend",adapterSummary);
  }
  const allPresent=(data.endpoints || []).length===2 && (data.endpoints || []).every(endpoint=>endpoint.present===true || (data.runtime_active && Boolean(endpoint.device)));
  if(adapterSummary) {
    adapterSummary.hidden=!allPresent;
    adapterSummary.textContent=allPresent?`✓ ${t("bridge.adaptersReady")}`:"";
  }
  if(runtimeError) {
    const missingText=missing.map(item=>`${item.id==="hmi"?t("bridge.hmi"):t("bridge.drive")}: ${item.device}`).join(" · ");
    runtimeError.hidden=!missingText && !data.runtime_error && !swapped;
    runtimeError.textContent=swapped?`${t("bridge.swapped")}: ${t("bridge.swappedDetail")}`:missingText?`${t("bridge.adapterMissing")}: ${missingText}`:(data.runtime_error?`${t("bridge.runtimeError")}: ${data.runtime_error}`:"");
  }
  for(const endpoint of data.endpoints || []) {
    const device=$(`#bridge-${endpoint.id}-device`), format=$(`#bridge-${endpoint.id}-format`), presence=$(`#bridge-${endpoint.id}-presence`), card=$(`#bridge-${endpoint.id}-card`);
    if(!device || !format) continue;
    device.textContent=endpoint.device?`${t("bridge.usbSerial")}: ${endpoint.adapter_serial || endpoint.device}`:t("bridge.notConfigured");
    device.title=endpoint.device || "";
    format.textContent=`${endpoint.baudrate.toLocaleString(locale())} bit/s · 8${endpoint.parity}${endpoint.stopbits}`;
    const isPresent=endpoint.present===true || (data.runtime_active && Boolean(endpoint.device));
    const isMissing=Boolean(endpoint.device) && !isPresent;
    if(card) card.classList.toggle("missing-adapter",isMissing);
    if(card) card.classList.toggle("available-adapter",isPresent);
    if(card) card.classList.toggle("suspected-swapped",swapped);
    let indicator=presence;
    if(!indicator && card) { indicator=document.createElement("small"); indicator.id=`bridge-${endpoint.id}-presence`; card.append(indicator); }
    if(indicator) { indicator.textContent=endpoint.device?`${isPresent?"✓":"✕"} ${t(isMissing?"bridge.adapterMissing":"bridge.adapterPresent")}`:""; indicator.className=`bridge-presence ${isMissing?"missing":"present"}`; }
  }
  const phases=$("#bridge-phases");
  if(phases) { phases.replaceChildren(); const all=data.phases || [], active=Math.max(0,all.indexOf(data.active_phase)); for(const [index,phase] of all.entries()) { const item=document.createElement("li"); item.className=index<active?"complete":index===active?"current":"planned"; item.textContent=`${index<active?"✓ ":""}${t(`bridge.phase.${phase}`)}`; phases.append(item); } }
  const checks=$("#bridge-checks");
  if(checks) {
    checks.replaceChildren();
    for(const [key,ready] of Object.entries(data.checks || {})) { const item=document.createElement("li"); item.className=ready?"ready":"pending"; item.textContent=`${ready?"✓":"○"} ${t(`bridge.check.${key}`)}`; checks.append(item); }
    const priority=document.createElement("li"); priority.className="ready"; priority.textContent=`✓ ${t("bridge.hmiPriority")}`; checks.append(priority);
    const persistence=data.runtime_diagnostics?.persistence;
    if(persistence) {
      const queued=Number(persistence.queued || 0), dropped=Number(persistence.dropped || 0), failed=Number(persistence.failed || 0);
      const active=queued>0||Boolean(persistence.last_error), recovered=!active&&(dropped>0||failed>0);
      const item=document.createElement("li"); item.className=active?"pending":"ready";
      const key=active?"bridge.persistenceDropped":recovered?"bridge.persistenceRecovered":"bridge.persistenceHealthy";
      item.textContent=`${active?"○":"✓"} ${t(key)} · Queue ${queued}/${Number(persistence.capacity || 0)} · ${t("bridge.persistenceLost")} ${dropped+failed}`;
      checks.append(item);
    }
  }
  const capabilities=$("#bridge-capabilities");
  if(capabilities) { capabilities.replaceChildren(); for(const capability of data.capabilities || []) { const item=document.createElement("span"); item.textContent=t(`bridge.cap.${capability}`); capabilities.append(item); } }
}
async function refreshBridge() {
  try {
    const response=await fetch(`/api/v1/communication-bridge?_=${Date.now()}`,{cache:"no-store"});
    if(response.status===404) {
      throw new Error("404 Not Found");
    }
    if(!response.ok)throw new Error(`${response.status} ${response.statusText}`);
    renderBridge(await response.json());
  } catch(error) {
    try {
      const metadata=state.metadata || await getJSON(`/api/v1/metadata?_=${Date.now()}`);
      if(metadata.communication_bridge) { renderBridge(metadata.communication_bridge); return; }
    } catch(fallbackError) {
      const stage=$("#bridge-stage"); if(stage) stage.title=`${error.message}; ${fallbackError.message}`;
    }
    const stage=$("#bridge-stage"); if(stage) stage.textContent=`${t("bridge.statusError")} · ${error.message}`;
  }
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
    ...(Number(data.sqlite_reusable_bytes)>0 ? [[t("storage.reusable"),formatBytes(data.sqlite_reusable_bytes)]] : []),
    [t("storage.samples"), Number(data.sample_count).toLocaleString(locale())],
    [t("storage.cycles"), Number(data.cycle_count).toLocaleString(locale())],
    [t("storage.retention"), retention > 0 ? `${retention.toLocaleString(locale())} ${t("storage.days")}` : t("storage.unlimited")],
    [t("storage.growth"), data.growth_bytes_per_second == null ? t("storage.calculating") : formatBytes(data.growth_bytes_per_second * 86400)],
    ...(data.retention_expected_to_limit_growth ? [] : [[t("storage.remaining"), data.storage_capacity_stable ? t("storage.stable") : data.estimated_seconds_to_full == null ? t("storage.calculating") : formatDuration(data.estimated_seconds_to_full)]]),
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

function drawDigitalBars(context, rows, {start, end, pad, width, duration, y, laneHeight, color, minimumWidth}) {
  // The collector retains periodic samples even while a contact does not
  // change.  Render a contiguous HIGH period once, rather than one rectangle
  // per sample: adjacent canvas rectangles otherwise leave misleading seams.
  for (let row=0; row<rows.length; row++) {
    if (Number(rows[row].value) === 0 || (row && Number(rows[row-1].value) !== 0)) continue;
    let next=row+1;
    while (next < rows.length && Number(rows[next].value) !== 0) next++;
    const itemStart=Math.max(start,Date.parse(rows[row].observed_at));
    const itemEnd=Math.min(end,Math.max(itemStart,next < rows.length ? Date.parse(rows[next].observed_at) : end));
    const x=pad.left+width*(itemStart-start)/duration, right=pad.left+width*(itemEnd-start)/duration;
    const barHeight=Math.max(4,laneHeight-10), gradient=context.createLinearGradient(0,y+5,0,y+5+barHeight);
    gradient.addColorStop(0,`${color}c0`); gradient.addColorStop(.45,`${color}70`); gradient.addColorStop(1,`${color}18`);
    context.fillStyle=gradient; context.fillRect(x,y+5,Math.max(minimumWidth,right-x),barHeight);
    context.strokeStyle=`${color}d0`; context.lineWidth=1; context.beginPath(); context.moveTo(x,y+5.5); context.lineTo(right,y+5.5); context.stroke();
    row=next-1;
  }
}

function drawHistoryMarkers(context, {start, end, pad, width, height}) {
  context.save(); context.setLineDash([5,4]); context.lineWidth=1.25;
  const markers=[...state.historyMarkers.map(marker=>({...marker,colour:"#f0c95d"})),...state.milestones.map(item=>({timestamp:Date.parse(item.observed_at),colour:item.severity==="critical"?"#ff826f":item.severity==="warning"?"#f0c95d":"#72c7ff"}))];
  for (const marker of markers) {
    if (marker.timestamp < start || marker.timestamp > end) continue;
    const x=pad.left+width*(marker.timestamp-start)/Math.max(1,end-start);
    context.strokeStyle=marker.colour;
    context.beginPath(); context.moveTo(x,pad.top); context.lineTo(x,pad.top+height); context.stroke();
    context.fillStyle=marker.colour; context.beginPath(); context.arc(x,pad.top+4,3,0,Math.PI*2); context.fill();
  }
  context.restore();
}

function renderDigitalSeriesChart(context, series, rect) {
  const allItems=series.flatMap(entry=>entry.items);
  const dataStart=Math.min(...allItems.map(item=>Date.parse(item.observed_at))), dataEnd=Math.max(...allItems.map(item=>Date.parse(item.observed_at)));
  if (!state.historyView || state.historyView.start < dataStart || state.historyView.end > dataEnd || state.historyView.end <= state.historyView.start) state.historyView={start:dataStart,end:dataEnd};
  const start=state.historyView.start, end=state.historyView.end, duration=Math.max(1,end-start);
  const pad={left:Math.min(230, Math.max(82, rect.width*.27)),right:14,top:14,bottom:32}; const width=rect.width-pad.left-pad.right; const height=rect.height-pad.top-pad.bottom; const laneHeight=height/series.length;
  const colors=series.map((entry,index)=>historyCurveColor(entry.inverter || state.inverter,entry.sourceMetric || state.metric,index));
  context.font="12px system-ui"; context.textBaseline="middle";
  series.forEach((entry,index)=>{
    const y=pad.top+index*laneHeight;
    // Keep the last state before the viewport.  Otherwise a signal that was
    // already HIGH when the user zoomed/panned into the interval would appear
    // to turn on only at its next edge.
    const before=entry.items.filter(item=>Date.parse(item.observed_at)<start).at(-1);
    const rows=[...(before ? [before] : []), ...entry.items.filter(item=>{const stamp=Date.parse(item.observed_at); return stamp>=start && stamp<=end;})];
    context.strokeStyle="#34423f"; context.beginPath(); context.moveTo(pad.left,y+laneHeight-1); context.lineTo(rect.width-pad.right,y+laneHeight-1); context.stroke();
    context.fillStyle="#9faeaa"; context.textAlign="right"; const label=entry.metric.length>28?`${entry.metric.slice(0,27)}…`:entry.metric; context.fillText(label,pad.left-8,y+laneHeight/2);
    drawDigitalBars(context, rows, {start,end,pad,width,duration,y,laneHeight,color:colors[index%colors.length],minimumWidth:2});
  });
  drawHistoryMarkers(context,{start,end,pad,width,height});
  if (state.historyHover != null && state.historyHover >= start && state.historyHover <= end) { const x=pad.left+width*(state.historyHover-start)/duration; context.save(); context.setLineDash([4,4]); context.strokeStyle="rgba(255,255,255,.7)"; context.beginPath(); context.moveTo(x,pad.top); context.lineTo(x,pad.top+height); context.stroke(); context.restore(); }
  context.fillStyle="#9faeaa"; context.textBaseline="top"; for(const fraction of [0,.5,1]){const x=pad.left+width*fraction; context.textAlign=fraction===0?"left":fraction===1?"right":"center";context.fillText(timeText(new Date(start+duration*fraction).toISOString()),x,rect.height-pad.bottom+9);}
  state.historyGeometry={start,end,dataStart,dataEnd,duration,pad,width,height,rect,series,colors};
  const meta=$("#chart-meta"); meta.replaceChildren(); const legend=document.createElement("div"); legend.className="history-legend"; series.forEach((entry,index)=>{const item=document.createElement("span");item.className="history-legend-item";const swatch=document.createElement("i");swatch.style.backgroundColor=colors[index%colors.length];const label=document.createElement("span");label.textContent=historySeriesLabel(entry);item.append(swatch,label);legend.append(item);}); meta.append(legend);
}

function drawAnalogueSeries(context, rows, point, style) {
  if (rows.length < 2) return;
  const points=rows.map(item=>point(Number(item.value),item)); context.beginPath(); context.moveTo(...points[0]);
  if (style === "step") {
    points.slice(1).forEach(([x,y], index)=>{ const previous=points[index]; context.lineTo(x,previous[1]); context.lineTo(x,y); });
    return;
  }
  if (style === "spline") {
    const slopes=points.slice(1).map(([x,y],index)=>(y-points[index][1])/(x-points[index][0] || 1));
    // Fritsch-Carlson limiting: a smooth spline, but never an invented
    // overshoot above or below the neighbouring measured values.
    const tangents=points.map((_,index)=>{if(index===0)return slopes[0];if(index===points.length-1)return slopes.at(-1);const left=slopes[index-1],right=slopes[index];if(left*right<=0)return 0;let tangent=(left+right)/2;const ratioLeft=tangent/left,ratioRight=tangent/right,limit=Math.hypot(ratioLeft,ratioRight);if(limit>3)tangent*=3/limit;return tangent;});
    for(let index=0;index<points.length-1;index++) { const [x0,y0]=points[index], [x1,y1]=points[index+1], dx=(x1-x0)/3; context.bezierCurveTo(x0+dx,y0+tangents[index]*dx,x1-dx,y1-tangents[index+1]*dx,x1,y1); }
    return;
  }
  points.slice(1).forEach(([x,y])=>context.lineTo(x,y));
}

function historyRowsForViewport(entry, start, end, holdLastValue=false) {
  const previous=entry.items.filter(item=>Date.parse(item.observed_at)<start).at(-1);
  const rows=[...(previous?[previous]:[]),...entry.items.filter(item=>{const stamp=Date.parse(item.observed_at);return stamp>=start&&stamp<=end;})];
  // SQLite stores change points.  A missing later row therefore means "last
  // known value still applies", not "the signal disappeared".  Extend that
  // value to the viewport boundary without inventing another database sample.
  if(holdLastValue&&rows.length&&Date.parse(rows.at(-1).observed_at)<end)rows.push({...rows.at(-1),observed_at:new Date(end).toISOString()});
  return rows;
}

// Axis identities deliberately do not encode a screen side.  A view can grow
// from one axis to four without changing saved channel preferences; placement
// is merely a rendering concern (left, right, left, right).
const HISTORY_AXIS_LIMIT=4;
function historyAxisChoice(source, metric) { return JSON.parse(localStorage.getItem("tmm-history-axes") || "{}")[historySelectionKey(source,metric)] || "auto"; }
function setHistoryAxisChoice(source, metric, axis) { const axes=JSON.parse(localStorage.getItem("tmm-history-axes") || "{}"); axes[historySelectionKey(source,metric)]=axis; localStorage.setItem("tmm-history-axes",JSON.stringify(axes)); }
function automaticHistoryAxisId(entry) {
  const source=entry.inverter || state.inverter, metric=entry.sourceMetric || entry.metric;
  const selected=historyAxisChoice(source,metric); if (selected !== "auto") return selected;
  const magnitude=Math.max(...entry.items.map(item=>Math.abs(Number(item.value))).filter(Number.isFinite),1);
  // A unit alone is insufficient: 0–10 V and 0–400 V deserve independent
  // scales.  The decimal exponent is a compact, stable automatic grouping.
  const exponent=Math.floor(Math.log10(magnitude));
  return `auto:${entry.items[0]?.unit || "value"}:${exponent}`;
}
function historyAxisDomain(entries,start,end) {
  const all=entries.flatMap(entry=>entry.items), visible=all.filter(item=>{const stamp=Date.parse(item.observed_at);return stamp>=start&&stamp<=end;});
  const values=(visible.length ? visible : all).map(item=>Number(item.value)).filter(Number.isFinite);
  const min=Math.min(...values), max=Math.max(...values), measuredSpan=max-min;
  const referenceSpan=Math.max(measuredSpan,Math.max(Math.abs(min),Math.abs(max),1)*.02);
  const domainMin=min-referenceSpan*.12, domainMax=max+referenceSpan*.12;
  return {min,max,domainMin,domainMax,spread:domainMax-domainMin};
}
function buildHistoryAxes(entries,start,end,colors,series) {
  const groups=new Map();
  entries.forEach(entry=>{const id=automaticHistoryAxisId(entry);if(!groups.has(id))groups.set(id,[]);groups.get(id).push(entry);});
  const grouped=[...groups.entries()];
  // Four slots are already supported.  Should an automatic selection create
  // more groups, the last slot remains a safe aggregate rather than silently
  // dropping a curve; manual assignments can then deliberately regroup it.
  const retained=grouped.slice(0,HISTORY_AXIS_LIMIT);
  if (grouped.length>HISTORY_AXIS_LIMIT) retained.at(-1)[1].push(...grouped.slice(HISTORY_AXIS_LIMIT).flatMap(([,items])=>items));
  return retained.map(([id,entries],index)=>{
    const first=entries[0], seriesIndex=series.indexOf(first);
    return {id,entries,index,side:index%2 ? "right" : "left",rank:Math.floor(index/2),unit:first.items[0]?.unit || "",color:colors[seriesIndex%colors.length],...historyAxisDomain(entries,start,end)};
  });
}

let historyRenderFrame=0;
function scheduleHistoryRender() {
  if(historyRenderFrame)cancelAnimationFrame(historyRenderFrame);
  historyRenderFrame=requestAnimationFrame(()=>{
    historyRenderFrame=requestAnimationFrame(()=>{historyRenderFrame=0;renderChart(state.history);});
  });
}

function renderChart(items) {
  const inputSeries=items[0]?.items ? items : [{metric:state.metric,items}];
  const series=inputSeries.map(entry=>({...entry,items:(entry.items || []).filter(item=>Number.isFinite(Number(item.value))&&Number.isFinite(Date.parse(item.observed_at)))}));
  state.history = series;
  const drawableSeries=series.filter(entry=>entry.items.length);
  const allItems=drawableSeries.flatMap(entry=>entry.items);
  const canvas = $("#chart"); const empty = $("#chart-empty");
  empty.hidden = allItems.length > 1;
  if (allItems.length < 2) {
    const known = state.channels.some(device => device.channels.some(channel => channel.key === state.metric));
    empty.textContent = known ? `${t("channels.enableRecordPrefix")} ${metricName(state.metric)} ${t("channels.enableRecordSuffix")}` : t("history.empty");
  }
  const digitalCount=drawableSeries.filter(entry=>entry.items.every(item=>item.unit === "on/off")).length;
  const analogueCount=drawableSeries.length-digitalCount;
  const chartWrap=canvas.closest(".chart-wrap");
  if (!document.fullscreenElement) chartWrap.style.height=`${Math.max(analogueCount ? 380 + digitalCount * 34 : 150 + digitalCount * 42, window.innerWidth <= 680 ? 280 : 0)}px`;
  const rect = canvas.getBoundingClientRect();
  if((!document.fullscreenElement&&chartWrap.offsetParent===null)||rect.width<80||rect.height<80){state.historyGeometry=null;return;}
  const ratio = Math.min(2,window.devicePixelRatio || 1);
  canvas.width = Math.round(rect.width * ratio); canvas.height = Math.round(rect.height * ratio);
  const context = canvas.getContext("2d"); context.scale(ratio, ratio); context.clearRect(0, 0, rect.width, rect.height);
  if (allItems.length < 2) { state.historyGeometry=null; $("#chart-tooltip").hidden=true; return; }
  if (drawableSeries.length && drawableSeries.every(entry=>entry.items.every(item=>item.unit === "on/off"))) { renderDigitalSeriesChart(context, drawableSeries, rect); return; }
  const digitalSeries=drawableSeries.filter(entry=>entry.items.every(item=>item.unit === "on/off"));
  const analogueSeries=drawableSeries.filter(entry=>!digitalSeries.includes(entry));
  const dataStart=Math.min(...allItems.map(item=>Date.parse(item.observed_at))), dataEnd=Math.max(...allItems.map(item=>Date.parse(item.observed_at)));
  if (!state.historyView || state.historyView.start < dataStart || state.historyView.end > dataEnd || state.historyView.end <= state.historyView.start) state.historyView={start:dataStart,end:dataEnd};
  const start=state.historyView.start, end=state.historyView.end, duration=Math.max(1,end-start);
  const colors=drawableSeries.map((entry,index)=>historyCurveColor(entry.inverter || state.inverter,entry.sourceMetric || state.metric,index));
  const axes=buildHistoryAxes(analogueSeries,start,end,colors,drawableSeries);
  const leftAxes=axes.filter(axis=>axis.side==="left"), rightAxes=axes.filter(axis=>axis.side==="right");
  // Keep room for independently labelled scales on both sides.  The same
  // slot model works for one, two, three, or four axes.
  const pad = { left:Math.min(250, Math.max(digitalSeries.length ? rect.width*.18 : 64,64+leftAxes.length*52)), right:14+rightAxes.length*52, top:22, bottom:32 }; const width = rect.width - pad.left - pad.right; const height = rect.height - pad.top - pad.bottom;
  // Digital signals never share the numeric scale with engineering values.
  // Reserve clearly separated state lanes beneath the analogue plot instead.
  const digitalHeight=digitalSeries.length ? 34*digitalSeries.length : 0;
  const plotHeight=Math.max(60,height-digitalHeight);
  context.font="12px system-ui"; context.textBaseline="middle"; context.lineWidth = 1;
  const numberText = (value,spread) => Number(value).toLocaleString(locale(), {maximumFractionDigits: Math.abs(spread) < 1 ? 3 : 2});
  for (let row = 0; row <= 4; row++) { const y=pad.top+plotHeight*row/4; context.strokeStyle="#34423f"; context.beginPath(); context.moveTo(pad.left,y); context.lineTo(rect.width-pad.right,y); context.stroke(); }
  axes.forEach(axis=>{
    const x=axis.side==="left" ? pad.left-8-axis.rank*52 : rect.width-pad.right+8+axis.rank*52;
    context.fillStyle=axis.color; context.textAlign=axis.side==="left" ? "right" : "left"; context.textBaseline="bottom"; context.fillText(axis.unit,x,pad.top-4);
    context.textBaseline="middle";
    for(let row=0;row<=4;row++) { const value=axis.domainMax-axis.spread*row/4, y=pad.top+plotHeight*row/4; context.fillText(numberText(value,axis.spread),x,y); }
  });
  // The last sample before a zoomed viewport is deliberately retained so the
  // curve enters continuously at the left edge.  Clip it to the numeric plot;
  // otherwise its off-screen X coordinate can draw across axis labels.
  context.save(); context.beginPath(); context.rect(pad.left,pad.top,width,plotHeight); context.clip();
  analogueSeries.forEach(entry=>{ const index=drawableSeries.indexOf(entry), axis=axes.find(candidate=>candidate.entries.includes(entry)); const rows=historyRowsForViewport(entry,start,end,true); const point=(value,item)=>[pad.left+width*(Date.parse(item.observed_at)-start)/duration,pad.top+plotHeight*(1-(value-axis.domainMin)/axis.spread)]; const style=historyCurveStyle(entry.inverter || state.inverter,entry.sourceMetric || state.metric); drawAnalogueSeries(context,rows,point,style); context.strokeStyle=colors[index%colors.length];context.lineWidth=2;context.stroke(); });
  context.restore();
  if (digitalSeries.length) {
    const laneHeight=digitalHeight/digitalSeries.length;
    digitalSeries.forEach((entry,lane)=>{
      const index=drawableSeries.indexOf(entry), y=pad.top+plotHeight+lane*laneHeight;
      const rows=historyRowsForViewport(entry,start,end);
      context.strokeStyle="#60736e"; context.beginPath(); context.moveTo(pad.left,y+laneHeight-1); context.lineTo(rect.width-pad.right,y+laneHeight-1); context.stroke();
      context.fillStyle="#d3ded9"; context.textAlign="right"; const label=historySeriesLabel(entry); context.fillText(label.length>22?`${label.slice(0,21)}…`:label,pad.left-8,y+laneHeight/2);
      context.save(); context.beginPath(); context.rect(pad.left,pad.top+plotHeight,width,digitalHeight); context.clip();
      drawDigitalBars(context, rows, {start,end,pad,width,duration,y,laneHeight,color:colors[index%colors.length],minimumWidth:3});
      context.restore();
    });
  }
  state.historyGeometry={start,end,dataStart,dataEnd,duration,pad,width,height,rect,series:drawableSeries,colors,axes};
  drawHistoryMarkers(context,{start,end,pad,width,height});
  if (state.historyHover != null && state.historyHover >= start && state.historyHover <= end) {
    const x=pad.left+width*(state.historyHover-start)/duration;
    context.save(); context.setLineDash([4,4]); context.strokeStyle="rgba(255,255,255,.7)"; context.lineWidth=1;
    context.beginPath(); context.moveTo(x,pad.top); context.lineTo(x,pad.top+height); context.stroke(); context.restore();
  }
  context.fillStyle="#9faeaa"; context.textBaseline="top";
  for (const fraction of [0, .5, 1]) { const stamp=start+duration*fraction; const text=timeText(new Date(stamp).toISOString()); const x=pad.left+width*fraction; context.textAlign=fraction===0?"left":fraction===1?"right":"center"; context.fillText(text,x,rect.height-pad.bottom+9); }
  $("#chart-meta").replaceChildren();
  const legend=document.createElement("div"); legend.className="history-legend";
  drawableSeries.forEach((entry,index)=>{const item=document.createElement("span"); item.className="history-legend-item"; const swatch=document.createElement("i"); swatch.style.backgroundColor=colors[index%colors.length]; const label=document.createElement("span"); label.textContent=historySeriesLabel(entry); item.append(swatch,label);legend.append(item);});
  const range=document.createElement("span"); range.className="history-range"; range.textContent=axes.map(axis=>`${axis.unit || t("history.axis")} ${t("history.min")} ${numberText(axis.min,axis.spread)} · ${t("history.max")} ${numberText(axis.max,axis.spread)}`).join("  |  ");
  $("#chart-meta").append(legend, range);
}

function nearestHistoryValue(items, timestamp) {
  return items.reduce((best,item)=>Math.abs(Date.parse(item.observed_at)-timestamp)<Math.abs(Date.parse(best.observed_at)-timestamp)?item:best);
}
function markerTrashIcon() {
  const svg=document.createElementNS("http://www.w3.org/2000/svg","svg"); svg.setAttribute("viewBox","0 0 24 24"); svg.setAttribute("aria-hidden","true");
  const path=document.createElementNS("http://www.w3.org/2000/svg","path"); path.setAttribute("fill","none"); path.setAttribute("stroke","currentColor"); path.setAttribute("stroke-width","1.8"); path.setAttribute("stroke-linecap","round"); path.setAttribute("stroke-linejoin","round"); path.setAttribute("d","M4 7h16M9 7V4h6v3m-8 0 1 13h8l1-13M10 11v5m4-5v5"); svg.append(path); return svg;
}
function renderHistoryMarkers() {
  const container=$("#history-markers"); container.replaceChildren(); container.hidden=!state.historyMarkers.length;
  for (const marker of state.historyMarkers) {
    const card=document.createElement("article"); card.className="history-marker";
    const header=document.createElement("div"); header.className="history-marker-header";
    const title=document.createElement("strong"); title.textContent=timeText(new Date(marker.timestamp).toISOString());
    const remove=document.createElement("button"); remove.type="button"; remove.className="history-marker-remove"; remove.title=t("history.markerDelete"); remove.setAttribute("aria-label",remove.title); remove.append(markerTrashIcon()); remove.addEventListener("click",()=>{state.historyMarkers=state.historyMarkers.filter(item=>item.id!==marker.id);renderHistoryMarkers();renderChart(state.history);}); header.append(title,remove);
    const table=document.createElement("table"); const body=document.createElement("tbody");
    for (const entry of state.history) { if (!entry.items?.length) continue; const item=nearestHistoryValue(entry.items,marker.timestamp); const row=document.createElement("tr"); const name=document.createElement("th"); const value=document.createElement("td"); name.textContent=historySeriesLabel(entry); value.textContent=`${Number(item.value).toLocaleString(locale(),{maximumFractionDigits:3})}${item.unit ? ` ${item.unit}` : ""}`; row.append(name,value);body.append(row); }
    table.append(body); card.append(header,table); container.append(card);
  }
}
function addHistoryMarker(event) {
  const geometry=state.historyGeometry; if (!geometry) return;
  const x=Math.max(geometry.pad.left,Math.min(geometry.rect.width-geometry.pad.right,event.offsetX));
  const timestamp=geometry.start+(geometry.end-geometry.start)*(x-geometry.pad.left)/geometry.width;
  state.historyMarkers.push({id:`${Date.now()}-${Math.random()}`,timestamp}); renderHistoryMarkers(); renderChart(state.history);
}

function resetConditionForm() {
  $("#condition-form").reset(); $("#condition-id").value=""; $("#condition-enabled").checked=true; $("#condition-value").disabled=false; $("#condition-operands").replaceChildren(); $("#condition-result").textContent=""; renderConditionExpression();
}
const CONDITION_COLOURS=["#73e2ad","#72c7ff","#f0c95d","#df98ff","#ff9f7f","#8ed8cc"];
function conditionMetricColour(source,metric) { let hash=0; for (const character of `${source}\u001f${metric}`) hash=(hash*31+character.codePointAt(0))>>>0; return CONDITION_COLOURS[hash%CONDITION_COLOURS.length]; }
function conditionCatalogItem(source,metric) { return state.conditionCatalog.find(item=>item.inverter===source&&item.metric===metric); }
function conditionExpression(source,metric,operator,value,duration,unit="") {
  const fragment=document.createDocumentFragment(), item=conditionCatalogItem(source,metric), known=Boolean(item);
  const add=(text,className)=>{const span=document.createElement("span");span.className=`condition-token ${className}`;span.textContent=text;if(className==="metric")span.style.setProperty("--metric-colour",conditionMetricColour(source,metric));fragment.append(span);};
  add(historySourceLabel(source),"source"); add("·","source"); add(known ? (item.metric_label||metricName(metric)) : metric,"metric"); add(operator,`operator${operator==="NOT"?" not":""}`);
  if (operator!=="NOT") { add(Number(value).toLocaleString(locale(),{maximumFractionDigits:6}),"number"); if(unit||item?.unit)add(unit||item.unit,"unit"); }
  if(Number(duration)>0)add(`@ ${Number(duration).toLocaleString(locale())} s`,"duration");
  return fragment;
}
function conditionExpressionTree(expression,duration=0) {
  if(!expression?.logic)return conditionExpression(expression?.source||"",expression?.metric||"",expression?.operator||"=",expression?.value??0,duration);
  const fragment=document.createDocumentFragment(), open=document.createElement("span"), close=document.createElement("span"); open.className=close.className="condition-token source"; open.textContent="("; close.textContent=")"; fragment.append(open);
  if(expression.logic==="NOT"){const logic=document.createElement("span");logic.className="condition-token operator not";logic.textContent="NOT";fragment.append(logic);}
  expression.conditions.forEach((child,index)=>{if(index){const logic=document.createElement("span");logic.className="condition-token operator";logic.textContent=expression.logic;fragment.append(logic);}fragment.append(conditionExpressionTree(child,0));}); fragment.append(close);
  if(Number(duration)>0){const token=document.createElement("span");token.className="condition-token duration";token.textContent=`@ ${Number(duration).toLocaleString(locale())} s`;fragment.append(token);} return fragment;
}
function conditionFormLeaf(channel,operator,value,hysteresis,tolerance) { const [source="",metric=""]=channel.split("\u001f"); return {source,metric,operator,value:Number(value),hysteresis:Number(hysteresis),tolerance:Number(tolerance)}; }
function conditionFormExpression() {
  const leaves=[conditionFormLeaf($("#condition-channel").value,$("#condition-operator").value,$("#condition-value").value,$("#condition-hysteresis").value,$("#condition-tolerance").value)];
  for(const row of document.querySelectorAll(".condition-operand-row"))leaves.push(conditionFormLeaf(row.querySelector(".condition-extra-channel").value,row.querySelector(".condition-extra-operator").value,row.querySelector(".condition-extra-value").value,row.querySelector(".condition-extra-hysteresis").value,row.querySelector(".condition-extra-tolerance").value));
  return leaves.length===1 ? leaves[0] : {logic:$("#condition-logic").value,conditions:leaves};
}
function renderConditionExpression() { const output=$("#condition-expression"); if(!output)return; output.replaceChildren(); output.append(conditionExpressionTree(conditionFormExpression(),$("#condition-duration").value)); }
function fillConditionSelect(select,selected="") {
  select.replaceChildren(); const groups=new Map();
  for(const item of state.conditionCatalog){if(!groups.has(item.inverter)){const group=document.createElement("optgroup");group.label=historySourceLabel(item.inverter);groups.set(item.inverter,group);select.append(group);}groups.get(item.inverter).append(new Option(`●  ${item.metric_label||metricName(item.metric)}${item.unit?`  [${item.unit}]`:""}`,`${item.inverter}\u001f${item.metric}`));}
  if([...select.options].some(option=>option.value===selected))select.value=selected;
}
function addConditionOperand(predicate=null) {
  const row=document.createElement("div"); row.className="condition-operand-row";
  const field=(key,control)=>{const label=document.createElement("label"),span=document.createElement("span");span.textContent=t(key);label.append(span,control);return label;};
  const channel=document.createElement("select");channel.className="condition-extra-channel";fillConditionSelect(channel,predicate?`${predicate.source}\u001f${predicate.metric}`:"");
  const operator=document.createElement("select");operator.className="condition-extra-operator";for(const value of [">",">=","<","<=","=","!=","NOT"])operator.append(new Option(value,value));operator.value=predicate?.operator||">";
  const numberInput=(className,value,min=null)=>{const input=document.createElement("input");input.className=className;input.type="number";input.step="any";input.value=value;if(min!==null)input.min=min;return input;};
  const value=numberInput("condition-extra-value",predicate?.value??0), hysteresis=numberInput("condition-extra-hysteresis",predicate?.hysteresis??0,0), tolerance=numberInput("condition-extra-tolerance",predicate?.tolerance??0,0);
  const remove=document.createElement("button");remove.type="button";remove.className="condition-remove-operand";remove.textContent=t("conditions.removeOperand");remove.addEventListener("click",()=>{row.remove();renderConditionExpression();});
  const update=()=>{value.disabled=operator.value==="NOT";renderConditionExpression();}; row.addEventListener("input",update);row.addEventListener("change",update);
  row.append(field("conditions.operand",channel),field("conditions.operator",operator),field("conditions.value",value),field("conditions.hysteresis",hysteresis),field("conditions.tolerance",tolerance),remove);$("#condition-operands").append(row);update();
}
function populateConditionChannels() {
  const select=$("#condition-channel"), selected=select.value; fillConditionSelect(select,selected);
  for(const extra of document.querySelectorAll(".condition-extra-channel"))fillConditionSelect(extra,extra.value);
  renderConditionExpression();
}
function editCondition(rule) {
  $("#condition-operands").replaceChildren(); const expression=rule.expression||{source:rule.source,metric:rule.metric,operator:rule.operator,value:rule.value,hysteresis:rule.hysteresis,tolerance:rule.tolerance}; const leaves=expression.logic ? expression.conditions : [expression]; const primary=leaves[0];
  $("#condition-id").value=rule.id; $("#condition-name").value=rule.name; $("#condition-channel").value=`${rule.source}\u001f${rule.metric}`;
  $("#condition-channel").value=`${primary.source}\u001f${primary.metric}`; $("#condition-operator").value=primary.operator; $("#condition-value").value=primary.value; $("#condition-duration").value=rule.duration_seconds;
  $("#condition-hysteresis").value=primary.hysteresis; $("#condition-tolerance").value=primary.tolerance; $("#condition-severity").value=rule.severity; $("#condition-enabled").checked=rule.enabled; $("#condition-logic").value=expression.logic||"AND"; for(const predicate of leaves.slice(1))addConditionOperand(predicate);
  $("#condition-value").disabled=rule.operator==="NOT"; renderConditionExpression(); $("#condition-name").focus();
}
function renderConditions() {
  populateConditionChannels(); const rules=$("#condition-rules"); rules.replaceChildren();
  for (const rule of state.conditions) {
    const card=document.createElement("article"); card.className="condition-rule";
    const body=document.createElement("div"), title=document.createElement("strong"), detail=document.createElement("div"), status=document.createElement("small"); detail.className="condition-rule-expression";
    title.textContent=rule.name; detail.append(conditionExpressionTree(rule.expression||{source:rule.source,metric:rule.metric,operator:rule.operator,value:rule.value},rule.duration_seconds));
    status.textContent=`${t(`alerts.${rule.severity}`)} · ${rule.enabled ? t("conditions.enabled") : t("channels.off")}${rule.state?.active ? ` · ${t("conditions.enter")}` : ""}`; body.append(title,detail,status);
    const actions=document.createElement("div"); actions.className="condition-rule-actions";
    const edit=document.createElement("button"); edit.type="button"; edit.textContent=t("conditions.edit"); edit.addEventListener("click",()=>editCondition(rule));
    const remove=document.createElement("button"); remove.type="button"; remove.textContent=t("conditions.delete"); remove.addEventListener("click",async()=>{try{await deleteJSON(`/api/v1/conditions/${encodeURIComponent(rule.id)}`);await refreshConditions();}catch(error){$("#condition-result").textContent=error.message;}});
    actions.append(edit,remove); card.append(body,actions); rules.append(card);
  }
  if (!state.conditions.length) { const empty=document.createElement("p"); empty.className="hint"; empty.textContent=t("conditions.none"); rules.append(empty); }
  const milestones=$("#condition-milestones"); milestones.replaceChildren();
  for (const item of [...state.milestones].reverse().slice(0,50)) {
    const card=document.createElement("article"); card.className=`condition-milestone ${item.severity}`;
    const body=document.createElement("div"), title=document.createElement("strong"), time=document.createElement("small"), detail=document.createElement("div"); detail.className="condition-milestone-expression";
    title.textContent=`${item.rule_name} · ${t(`conditions.${item.event_type}`)}`; time.textContent=`${timeText(item.observed_at)} · ${Number(item.value).toLocaleString(locale())} ${item.unit || ""}`; detail.append(item.snapshot?.logic ? conditionExpressionTree(item.snapshot.logic) : conditionExpression(item.source,item.metric,item.operator,item.target_value,0,item.unit));
    body.append(title,detail,time); card.append(body); milestones.append(card);
  }
  if (!state.milestones.length) { const empty=document.createElement("p"); empty.className="hint"; empty.textContent=t("conditions.noMilestones"); milestones.append(empty); }
}
async function refreshConditions() {
  const [conditions,catalog,milestones]=await Promise.all([getJSON("/api/v1/conditions"),getJSON("/api/v1/metrics/catalog"),getJSON("/api/v1/milestones?limit=1000")]);
  state.conditions=conditions.rules || []; state.conditionCatalog=catalog.items || []; state.milestones=milestones.items || []; renderConditions(); renderChart(state.history);
}
async function saveCondition(event) {
  event.preventDefault(); const expression=conditionFormExpression(), primary=expression.logic?expression.conditions[0]:expression, {source,metric}=primary;
  const payload={id:$("#condition-id").value || undefined,name:$("#condition-name").value.trim(),source,metric,operator:$("#condition-operator").value,
    value:primary.value,duration_seconds:Number($("#condition-duration").value),hysteresis:primary.hysteresis,tolerance:primary.tolerance,severity:$("#condition-severity").value,enabled:$("#condition-enabled").checked,expression};
  try { await postJSON("/api/v1/conditions",payload); resetConditionForm(); $("#condition-result").textContent=t("conditions.saved"); await refreshConditions(); }
  catch(error) { $("#condition-result").textContent=error.message; }
}

let historyRequestGeneration=0;
async function refreshHistory(force=true) {
  const historyPanel=$("#history-title").closest("section");
  // A potentially large set of series is only useful while the history is
  // actually visible.  Keep direct user actions immediate, but do not issue
  // periodic multi-series SQLite reads for a collapsed or background panel.
  if (!force && (document.visibilityState !== "visible" || historyPanel?.classList.contains("is-collapsed"))) return;
  const selected=[...state.historySelected];
  if (!selected.length && state.metric && state.inverter) selected.push(historySelectionKey(state.inverter, state.metric));
  const generation=++historyRequestGeneration;
  const results=await Promise.allSettled(selected.map(async key=>{const [inverter, metric]=key.split("\u001f"); return {metric, inverter, sourceMetric:metric, items:(await getJSON(`/api/v1/metrics/history?metric=${encodeURIComponent(metric)}&inverter=${encodeURIComponent(inverter)}&limit=1000`)).items};}));
  if(generation!==historyRequestGeneration)return;
  const series=results.filter(result=>result.status==="fulfilled").map(result=>result.value);
  const failed=results.find(result=>result.status==="rejected");
  if(failed)$("#last-error").textContent=failed.reason?.message || String(failed.reason);
  if(!series.length&&selected.length)return;
  renderChart(series);
  renderHistoryMarkers();
}

const historySelectionKey = (source, metric) => `${source}\u001f${metric}`;
const HISTORY_COLORS=["#73e2ad","#72c7ff","#f0c95d","#c997ff","#ff967e","#60d6d6"];
function persistHistorySelection() { localStorage.setItem("tmm-history-selected", JSON.stringify([...state.historySelected])); }
function persistHistoryExportSelection() { localStorage.setItem("tmm-history-export-selected", JSON.stringify([...state.historyExportSelected])); }
function historyCurveStyle(source, metric) { return JSON.parse(localStorage.getItem("tmm-history-curve-styles") || "{}")[historySelectionKey(source, metric)] || "linear"; }
function setHistoryCurveStyle(source, metric, style) { const styles=JSON.parse(localStorage.getItem("tmm-history-curve-styles") || "{}"); styles[historySelectionKey(source, metric)]=style; localStorage.setItem("tmm-history-curve-styles",JSON.stringify(styles)); }
function historyCurveColor(source, metric, index=0) { return JSON.parse(localStorage.getItem("tmm-history-curve-colors") || "{}")[historySelectionKey(source, metric)] || HISTORY_COLORS[index % HISTORY_COLORS.length]; }
function setHistoryCurveColor(source, metric, color) { const colors=JSON.parse(localStorage.getItem("tmm-history-curve-colors") || "{}"); colors[historySelectionKey(source,metric)]=color; localStorage.setItem("tmm-history-curve-colors",JSON.stringify(colors)); }
function loadHistorySelection(source) {
  const stored=JSON.parse(localStorage.getItem("tmm-history-selected") || "[]");
  const exportStored=JSON.parse(localStorage.getItem("tmm-history-export-selected") || "[]");
  // Migrate the former per-source metric-only preference without losing it.
  const legacy=JSON.parse(localStorage.getItem(`tmm-history-${source}`) || "[]");
  state.historySelected=new Set([...stored, ...legacy.map(metric=>historySelectionKey(source, metric))]);
  state.historyExportSelected=new Set(exportStored.length ? exportStored : state.historySelected);
}
function curveStyleIcon(style) {
  const svg=document.createElementNS("http://www.w3.org/2000/svg","svg"); svg.setAttribute("viewBox","0 0 24 18"); svg.setAttribute("aria-hidden","true");
  const path=document.createElementNS("http://www.w3.org/2000/svg","path"); path.setAttribute("fill","none"); path.setAttribute("stroke","currentColor"); path.setAttribute("stroke-width","2"); path.setAttribute("stroke-linecap","round"); path.setAttribute("stroke-linejoin","round");
  path.setAttribute("d",style==="step"?"M2 15h7V4h13":style==="spline"?"M2 12c3-10 6 10 10 0s6 10 10-4":"M2 15 22 3"); svg.append(path); return svg;
}

function exportIcon() {
  const svg=document.createElementNS("http://www.w3.org/2000/svg","svg"); svg.setAttribute("viewBox","0 0 24 24"); svg.setAttribute("aria-hidden","true");
  const path=document.createElementNS("http://www.w3.org/2000/svg","path"); path.setAttribute("fill","none"); path.setAttribute("stroke","currentColor"); path.setAttribute("stroke-width","1.8"); path.setAttribute("stroke-linejoin","round"); path.setAttribute("d","M5 3h12l3 3v15H5zM8 3v7h8V3M8 18h8v-5H8z"); svg.append(path); return svg;
}

function exportSelectionIcon() {
  const svg=document.createElementNS("http://www.w3.org/2000/svg","svg"); svg.setAttribute("viewBox","0 0 24 24"); svg.setAttribute("aria-hidden","true");
  const path=document.createElementNS("http://www.w3.org/2000/svg","path"); path.setAttribute("fill","none"); path.setAttribute("stroke","currentColor"); path.setAttribute("stroke-width","1.8"); path.setAttribute("stroke-linecap","round"); path.setAttribute("stroke-linejoin","round"); path.setAttribute("d","M4 5h11M4 10h11M4 15h7M17 15l2 2 4-5"); svg.append(path); return svg;
}

function liveViewIcon(visible) {
  const svg=document.createElementNS("http://www.w3.org/2000/svg","svg"); svg.setAttribute("viewBox","0 0 24 24"); svg.setAttribute("aria-hidden","true");
  const path=document.createElementNS("http://www.w3.org/2000/svg","path"); path.setAttribute("fill","none"); path.setAttribute("stroke","currentColor"); path.setAttribute("stroke-width","1.8"); path.setAttribute("stroke-linecap","round"); path.setAttribute("stroke-linejoin","round"); path.setAttribute("d","M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6Zm9.5 2.8a2.8 2.8 0 1 0 0-5.6 2.8 2.8 0 0 0 0 5.6Z"); svg.append(path); return svg;
  svg.append(path);
  if (!visible) { const slash=document.createElementNS("http://www.w3.org/2000/svg","path"); slash.setAttribute("fill","none"); slash.setAttribute("stroke","currentColor"); slash.setAttribute("stroke-width","2.2"); slash.setAttribute("stroke-linecap","round"); slash.setAttribute("d","M4 4 20 20"); svg.append(slash); }
  return svg;
}

function historyRecordingInfo(source, metric) {
  if (source === "communication") {
    const channel=state.communicationChannels.find(item=>item.key===metric);
    return channel ? {record:["record", "hide"].includes(channel.mode), configurable:true, mode:channel.mode} : {record:false, configurable:false};
  }
  if (!source.startsWith("addon:")) {
    const channel=state.channels.find(item=>item.name===source)?.channels.find(item=>item.key===metric);
    return channel ? {record:channel.mode === "record" || channel.mode === "hide", configurable:!channel.protected, mode:channel.mode} : {record:false, configurable:false};
  }
  const addon=state.addons?.items?.find(item=>item.id===source.slice(6));
  const leaf=metric.split(".").at(-1) || "", [,signal="input",numberText="0"]=leaf.match(/^(.+)_(\d+)$/) || [];
  const configuredSignal=addon?.type === "raspberry_pi_gpio" && signal === "gpio" ? "input" : signal;
  const channel=addon?.channels?.find(item=>item.metric === leaf || ((item.signal || "input")===configuredSignal && Number(item.channel)===Number(numberText)));
  if (["sequent_super_watchdog","sequent_smart_fan"].includes(addon?.type)) {
    if (channel) { const mode=addonChannelMode(channel); return {record:["record","hide"].includes(mode), configurable:true, mode, addon, metric:leaf}; }
    return {record:false, configurable:true, mode:"off", addon, metric:leaf};
  }
  if (channel) { const mode=addonChannelMode(channel); return {record:["record","hide"].includes(mode), configurable:true, mode, addon, signal:configuredSignal, channel:Number(numberText)}; }
  const fieldCard=["raspberry_pi_gpio","sequent_16inpind","sequent_24b8vin"].includes(addon?.type) || (addon?.type === "sequent_multiio" && signal !== "input");
  return fieldCard ? {record:false, configurable:true, mode:"off", addon, signal:configuredSignal, channel:Number(numberText)} : {record:true, configurable:false};
}

function addonChannelMode(channel) {
  if (!channel || channel.enabled === false) return "off";
  if (channel.record === true) return channel.live === false ? "hide" : "record";
  return "live";
}

function historyLiveInfo(source, metric) {
  if (source === "communication") {
    const channel=state.communicationChannels.find(item=>item.key===metric);
    return channel ? {live:["live", "record"].includes(channel.mode), record:["record", "hide"].includes(channel.mode), configurable:true, mode:channel.mode} : {live:false, configurable:false};
  }
  if (!source.startsWith("addon:")) {
    const channel=state.channels.find(item=>item.name===source)?.channels.find(item=>item.key===metric);
    return channel ? {live:["live","record"].includes(channel.mode), record:["record","hide"].includes(channel.mode), configurable:!channel.protected, mode:channel.mode} : {live:false, configurable:false};
  }
  const info=historyRecordingInfo(source,metric);
  if (!info.addon) return {live:false, configurable:false};
  // Field-card entries have no `metric` member.  Comparing two undefined
  // values selected the first channel for every eye icon; only compare metric
  // identities when this is a system-card metric.
  const channel=info.addon.channels?.find(item=>(info.metric && item.metric===info.metric) || ((item.signal || "input")===info.signal && Number(item.channel)===Number(info.channel)));
  return {live:channel ? channel.enabled !== false && channel.live !== false : info.record, record:info.record, configurable:info.configurable, ...info};
}

async function toggleHistoryLive(source, metric) {
  const info=historyLiveInfo(source,metric); if (!info.configurable) return;
  // Visibility is independent from recording.  Re-showing a hidden recorded
  // channel must restore `record`, not silently degrade it to `live`.
  const next=info.live ? (info.record ? "hide" : "off") : (info.record ? "record" : "live");
  if (source === "communication") {
    const channels=Object.fromEntries(state.communicationChannels.map(channel=>[channel.key,channel.mode]));
    channels[metric]=next; await postJSON("/api/v1/communication/channels",{channels});
  }
  else if (source.startsWith("addon:")) {
    const system=["sequent_super_watchdog","sequent_smart_fan"].includes(info.addon.type);
    // Field I/O has a true per-channel live flag.  Do not translate an eye
    // click into a group mode; that used to couple visibility to recording.
    const update=system ? {metric:info.metric,mode:next} : {
      signal:info.signal, channel:info.channel,
      ...(info.live ? {live:false} : {enabled:true, live:true}),
    };
    await postJSON("/api/v1/addons/channels",{id:info.addon.id,channels:[update]});
  }
  else {
    const device=state.channels.find(item=>item.name===source), channels=Object.fromEntries(device.channels.map(channel=>[channel.key,channel.mode]));
    channels[metric]=next; await postJSON("/api/v1/channels",{inverter:source,channels});
  }
  // `refresh()` intentionally coalesces overlapping dashboard refreshes.  It
  // can therefore return while `state.addons` still represents the previous
  // source-wide response.  Fetch this mutation's result directly before
  // redrawing the per-channel eyes.
  const freshAddons=await getJSON("/api/v1/addons"); state.addons=freshAddons;
  await loadChannels();
  renderHistoryChannelList();
  await refresh();
}

async function toggleHistoryRecording(source, metric) {
  const info=historyRecordingInfo(source,metric); if (!info.configurable) return;
  const next=info.record ? (info.mode === "hide" ? "off" : "live") : "record";
  if (source === "communication") {
    const channels=Object.fromEntries(state.communicationChannels.map(channel=>[channel.key,channel.mode]));
    channels[metric]=next; await postJSON("/api/v1/communication/channels",{channels});
  }
  else if (source.startsWith("addon:")) await postJSON("/api/v1/addons/channels",{id:info.addon.id,channels:[info.metric ? {metric:info.metric,mode:next} : {signal:info.signal,channel:info.channel,mode:next}]});
  else {
    const device=state.channels.find(item=>item.name===source);
    const channels=Object.fromEntries(device.channels.map(channel=>[channel.key,channel.mode])); channels[metric]=next;
    await postJSON("/api/v1/channels",{inverter:source,channels});
  }
  if (source.startsWith("addon:")) state.addons=await getJSON("/api/v1/addons");
  await loadChannels(); renderHistoryChannelList(); await refresh();
}

const withoutRecording = mode => mode === "record" ? "live" : mode === "hide" ? "off" : mode;
async function stopSourceRecording(source) {
  if (source === "communication") {
    const channels=Object.fromEntries(state.communicationChannels.map(channel=>[channel.key,withoutRecording(channel.mode)]));
    await postJSON("/api/v1/communication/channels",{channels}); return;
  }
  if (source.startsWith("addon:")) {
    const addon=state.addons?.items?.find(item=>item.id===source.slice(6)); if(!addon)return;
    const channels=(addon.channels || []).map(channel=>channel.metric
      ? {metric:channel.metric,mode:withoutRecording(addonChannelMode(channel))}
      : {signal:channel.signal || "input",channel:Number(channel.channel),mode:withoutRecording(addonChannelMode(channel))});
    await postJSON("/api/v1/addons/channels",{id:addon.id,channels}); return;
  }
  const device=state.channels.find(item=>item.name===source); if(!device)return;
  const channels=Object.fromEntries(device.channels.map(channel=>[channel.key,withoutRecording(channel.mode)]));
  await postJSON("/api/v1/channels",{inverter:source,channels});
}
async function synchronizeRecordingControls() {
  state.addons=await getJSON("/api/v1/addons"); state.metricCatalogLoaded=false;
  await loadChannels(); renderAddons(state.addons); renderUps(state.addons); renderHistoryChannelList(); await refresh();
  $("#history-recording-result").textContent=t("history.recordingStopped");
}
async function stopAllRecording() {
  for(const device of state.channels) await stopSourceRecording(device.name);
  await stopSourceRecording("communication");
  for(const addon of state.addons?.items || []) if(addon.enabled !== false) await stopSourceRecording(`addon:${addon.id}`);
}

function renderHistoryChannelList() {
  const box=$("#history-channel-list"); box.replaceChildren();
  const options=[...$("#metric").options]
    .filter(option=>option.value.startsWith(`${state.inverter}\u001f`))
    .sort((left,right)=>left.value.localeCompare(right.value,undefined,{numeric:true}));
  for (const option of options) {
    const [,metric]=option.value.split("\u001f"), key=historySelectionKey(state.inverter,metric), digital=option.dataset.unit === "on/off";
    const card=document.createElement("div"), toggle=document.createElement("label"), input=document.createElement("input"), text=document.createElement("span"), name=document.createElement("strong"), api=document.createElement("small");
    card.className="history-channel-card"; input.type="checkbox"; input.value=metric; input.checked=state.historySelected.has(key); name.textContent=option.dataset.label || metricName(metric); api.textContent=`${state.inverter} · ${metric}`; text.append(name,api); toggle.append(input,text); card.append(toggle);
    input.addEventListener("change",async()=>{input.checked?state.historySelected.add(key):state.historySelected.delete(key); persistHistorySelection(); await refreshHistory(); updateSelectedExport();});
    const actions=document.createElement("div"); actions.className="history-channel-card-actions";
    const recording=historyRecordingInfo(state.inverter,metric), recordButton=document.createElement("button"); recordButton.type="button"; recordButton.className=`history-record-button ${recording.record ? "recording" : ""}`; recordButton.title=t(!recording.configurable ? "history.recordFixed" : recording.record ? "history.recordStop" : "history.recordStart"); recordButton.setAttribute("aria-label",recordButton.title); recordButton.disabled=!recording.configurable; recordButton.append(document.createElement("span")); recordButton.addEventListener("click",async()=>{try{await toggleHistoryRecording(state.inverter,metric);}catch(error){showPersistentResult("#channels-result",`${t("recording.failed")}: ${error.message}`);}});
    const live=historyLiveInfo(state.inverter,metric), liveButton=document.createElement("button"); liveButton.type="button"; liveButton.className=`history-live-button ${live.live ? "visible" : ""}`; liveButton.title=t(live.live ? "history.liveHide" : "history.liveShow"); liveButton.setAttribute("aria-label",liveButton.title); liveButton.setAttribute("aria-pressed",String(live.live)); liveButton.disabled=!live.configurable; liveButton.append(liveViewIcon(live.live)); liveButton.addEventListener("click",async(event)=>{event.preventDefault(); event.stopPropagation(); try{await toggleHistoryLive(state.inverter,metric);}catch(error){showPersistentResult("#channels-result",`${t("recording.failed")}: ${error.message}`);}});
    const exportLink=document.createElement("a"); exportLink.className="history-export-button"; exportLink.href=`/api/v1/export.csv?metric=${encodeURIComponent(metric)}&inverter=${encodeURIComponent(state.inverter)}`; exportLink.title=t("history.exportChannel"); exportLink.setAttribute("aria-label",exportLink.title); exportLink.append(exportIcon());
    const exportSelected=state.historyExportSelected.has(key), exportSelect=document.createElement("button"); exportSelect.type="button"; exportSelect.className=`history-export-select ${exportSelected ? "selected" : ""}`; exportSelect.title=t(exportSelected ? "history.exportRemove" : "history.exportSelect"); exportSelect.setAttribute("aria-label",exportSelect.title); exportSelect.setAttribute("aria-pressed",String(exportSelected)); exportSelect.append(exportSelectionIcon()); exportSelect.addEventListener("click",()=>{exportSelected?state.historyExportSelected.delete(key):state.historyExportSelected.add(key); persistHistoryExportSelection(); renderHistoryChannelList(); updateSelectedExport();});
    actions.append(recordButton,liveButton,exportLink,exportSelect); card.append(actions);
    const colour=document.createElement("input"), colourIndex=Math.max(0,[...state.historySelected].indexOf(key)); colour.type="color"; colour.className="history-colour-picker"; colour.value=historyCurveColor(state.inverter,metric,colourIndex); colour.title=t("history.color"); colour.setAttribute("aria-label",colour.title); colour.addEventListener("input",()=>{setHistoryCurveColor(state.inverter,metric,colour.value);renderChart(state.history);});
    if (digital) {
      card.append(colour);
    } else {
      const modes=document.createElement("div"); modes.className="history-curve-buttons";
      for(const style of ["step","linear","spline"]) { const button=document.createElement("button"); button.type="button"; button.className="curve-style-button"; button.title=t(`history.style${style[0].toUpperCase()}${style.slice(1)}`); button.setAttribute("aria-label",button.title); button.setAttribute("aria-pressed",String(historyCurveStyle(state.inverter,metric)===style)); button.append(curveStyleIcon(style)); button.addEventListener("click",()=>{setHistoryCurveStyle(state.inverter,metric,style); renderHistoryChannelList(); renderChart(state.history);}); modes.append(button); }
      const axis=document.createElement("select"); axis.className="history-axis-select"; axis.title=t("history.axis"); axis.setAttribute("aria-label",axis.title);
      for (const value of ["auto","axis1","axis2","axis3","axis4"]) { const option=document.createElement("option"); option.value=value; option.textContent=t(`history.${value === "auto" ? "axisAuto" : value}`); axis.append(option); }
      axis.value=historyAxisChoice(state.inverter,metric); axis.addEventListener("change",()=>{setHistoryAxisChoice(state.inverter,metric,axis.value);renderChart(state.history);});
      modes.prepend(colour); card.append(modes);
      card.append(axis);
    }
    const current=state.latest.find(item=>item.inverter===state.inverter && item.metric===metric), indicator=document.createElement("div"), fill=document.createElement("span");
    indicator.className=`history-value-indicator ${digital ? "digital" : "analogue"}`; indicator.title=current ? `${Number(current.value).toLocaleString(locale())}${current.unit ? ` ${current.unit}` : ""}` : t("history.empty");
    if (digital) { const active=current && Number(current.value)!==0; fill.style.height="100%"; fill.style.background=active ? colour.value : "#45514e"; indicator.classList.toggle("active",Boolean(active)); }
    else { const minimum=Number(option.dataset.minimum), maximum=Number(option.dataset.maximum), value=Number(current?.value); const level=Number.isFinite(value) && Number.isFinite(minimum) && Number.isFinite(maximum) ? maximum===minimum ? .5 : Math.max(0,Math.min(1,(value-minimum)/(maximum-minimum))) : 0; fill.style.height=`${level*100}%`; fill.style.background=colour.value; indicator.title=current && Number.isFinite(minimum) && Number.isFinite(maximum) ? `${indicator.title} · Min ${minimum.toLocaleString(locale())} · Max ${maximum.toLocaleString(locale())}` : indicator.title; }
    indicator.append(fill); card.append(indicator);
    box.append(card);
  }
}
function historySourceLabel(source) {
  if (source === "communication") return language === "de" ? "Kommunikation" : "Communication";
  if (!source.startsWith("addon:")) return source;
  const identifier=source.slice("addon:".length);
  return state.addons?.items?.find(addon=>addon.id===identifier)?.label || identifier;
}
function historySeriesLabel(entry) {
  const source=entry.inverter || state.inverter, metric=entry.sourceMetric || entry.metric;
  const option=[...$("#metric").options].find(item=>item.value===historySelectionKey(source,metric));
  return option?.dataset.label || entry.items?.[0]?.metric_label || metricName(metric);
}
async function populateMetricSelector(items, authoritative=false) {
  const select = $("#metric");
  const hadSelection = Boolean(select.options.length);
  // The catalog is authoritative for add-on sources.  A card disabled in
  // External I/O must disappear from the source selector, rather than remain
  // selectable merely because its options were added during an earlier poll.
  let prunedDisabledSource = false;
  if (authoritative) {
    const configuredAddonSources=(state.addons?.items || []).filter(addon=>addon.enabled !== false).map(addon=>`addon:${addon.id}`);
    const activeAddonSources = new Set([...configuredAddonSources,...items.filter(item=>item.inverter?.startsWith("addon:")).map(item=>item.inverter)]);
    for (const option of [...select.options]) {
      const source=option.value.split("\u001f")[0];
      if (source.startsWith("addon:") && !activeAddonSources.has(source)) {
        option.remove(); prunedDisabledSource=true;
      }
    }
    if (prunedDisabledSource) {
      const available = new Set([...select.options].map(option=>option.value));
      state.historySelected=new Set([...state.historySelected].filter(key=>available.has(key)));
      state.historyExportSelected=new Set([...state.historyExportSelected].filter(key=>available.has(key)));
      persistHistorySelection(); persistHistoryExportSelection();
    }
  }
  for (const item of items.filter((item) => item.metric !== "communication_status" && (item.unit !== "raw" || item.metric === "input_terminal_status" || item.metric.startsWith("alarm_information_") || item.inverter?.startsWith("addon:")))) {
    const value = `${item.inverter}\u001f${item.metric}`;
    const existing=[...select.options].find(option => option.value === value);
    if (existing) { if (authoritative) { existing.dataset.unit=item.unit || ""; existing.dataset.label=item.metric_label || metricName(item.metric); existing.dataset.minimum=item.minimum_value ?? ""; existing.dataset.maximum=item.maximum_value ?? ""; } continue; }
    const option = document.createElement("option");
    option.value = value;
    option.dataset.unit=item.unit || "";
    option.dataset.label=item.metric_label || metricName(item.metric);
    option.dataset.minimum=item.minimum_value ?? "";
    option.dataset.maximum=item.maximum_value ?? "";
    option.textContent = `${item.inverter} · ${item.metric_label || metricName(item.metric)}`;
    select.append(option);
  }
  // Profiles must remain configurable before their first live sample or
  // history row exists; the retired dropdown must not be needed as a fallback.
  for (const device of state.channels) for (const channel of device.channels) {
    const value=`${device.name}\u001f${channel.key}`;
    if ([...select.options].some(option=>option.value===value)) continue;
    const option=document.createElement("option");
    option.value=value; option.dataset.unit=channel.unit || "";
    option.dataset.label=metricName(channel.key); option.dataset.minimum=""; option.dataset.maximum="";
    option.textContent=`${device.name} · ${metricName(channel.key)}`; select.append(option);
  }
  // Configured add-on channels must remain selectable before their first
  // sample exists.  Otherwise setting every channel to Off removes the source
  // which is needed to switch a channel back on from Measurement history.
  for (const addon of state.addons?.items || []) {
    if (addon.enabled === false) continue;
    for (const channel of addon.channels || []) {
      const leaf=channel.metric || `${channel.signal || "input"}_${String(channel.channel).padStart(2,"0")}`;
      const metric=`addon.${addon.id}.${leaf}`, value=`addon:${addon.id}\u001f${metric}`;
      if ([...select.options].some(option=>option.value===value)) continue;
      const option=document.createElement("option"); option.value=value; option.dataset.unit=channel.unit || "";
      option.dataset.label=channel.metric_label || channel.label || metricName(metric); option.dataset.minimum=""; option.dataset.maximum="";
      option.textContent=`${addon.label} · ${option.dataset.label}`; select.append(option);
    }
  }
  const inverterSelect=$("#history-inverter"); const previousInverter=inverterSelect.value;
  // A powered-down drive has no current values, and a new installation may
  // not have retained samples yet.  It still belongs in the source selector:
  // operators must be able to see that it is configured and select any
  // history which becomes available without first re-establishing Modbus.
  const configuredSources=(state.metadata?.inverters || []).map(inverter=>inverter.name);
  const recordedSources=[...select.options].map(option=>option.value.split("\u001f")[0]);
  inverterSelect.replaceChildren(); for(const inverter of [...new Set([...configuredSources,...recordedSources])]) inverterSelect.add(new Option(historySourceLabel(inverter),inverter));
  if (previousInverter) inverterSelect.value=previousInverter;
  if (prunedDisabledSource && ![...select.options].some(option=>option.value.startsWith(`${state.inverter}\u001f`))) {
    const replacement=select.options[0];
    if (replacement) {
      [state.inverter,state.metric]=replacement.value.split("\u001f");
      if (!state.historySelected.size) state.historySelected.add(replacement.value);
      inverterSelect.value=state.inverter;
    }
  }
  if (hadSelection) { renderHistoryChannelList(); if (prunedDisabledSource) await refreshHistory(); return; }
  const preferred = [...select.options].find((option) => option.value.endsWith(`\u001f${state.metric}`));
  if (preferred) select.value = preferred.value;
  if (select.value) {
    [state.inverter, state.metric] = select.value.split("\u001f");
    loadHistorySelection(state.inverter); if(!state.historySelected.size) state.historySelected.add(historySelectionKey(state.inverter, state.metric));
    inverterSelect.value=state.inverter; renderHistoryChannelList(); showChannels(state.inverter);
    await refreshHistory();
  }
}

async function refresh() {
  if (refreshRunning) return;
  refreshRunning = true;
  // I/O cards must not retain an obsolete error merely because an unrelated
  // dashboard endpoint (for example slow Modbus diagnostics) is unavailable.
  const addonsRequest = getJSON("/api/v1/addons",2500);
  const latestRequest = getJSON("/api/v1/metrics/latest",2500);
  // The catalog aggregates the complete retained samples table.  It is
  // required when the page first opens or naming/configuration changed, but
  // never for the 3-second live refresh.  Repeating it made an open dashboard
  // increasingly CPU-expensive as the recording grew.
  const metricCatalogRequest = state.metricCatalogLoaded || state.metricCatalogLoading ? null : getJSON("/api/v1/metrics/catalog");
  if (metricCatalogRequest) state.metricCatalogLoading=true;
  addonsRequest.then((addons) => {
    state.addons = addons;
    renderAddons(addons);
    renderUps(addons);
    if (!state.liveOrderDragging && state.latest.length) renderCards(state.latest,state.metadata?.alert_thresholds?.metrics,addons);
    populateMetricSelector([], false).catch(()=>{});
  }).catch(() => {});
  // The external acquisition loop is independent of Modbus.  Let its values
  // populate the history selector even when a powered-down inverter makes a
  // different dashboard request fail.
  latestRequest.then(async (latest) => {
    state.latest = latest.items;
    if (!state.liveOrderDragging) renderCards(latest.items,state.metadata?.alert_thresholds?.metrics,state.addons);
    await populateMetricSelector(latest.items, false);
  }).catch(() => {});
  metricCatalogRequest?.then(async (catalog) => {
    await populateMetricSelector(catalog.items, true); state.metricCatalogLoaded=true;
  }).catch(() => {}).finally(() => { state.metricCatalogLoading=false; });
  try {
    const [health, latest, telemetry, addons] = await Promise.all([getJSON("/api/v1/health"), latestRequest, getJSON("/api/v1/diagnostics"), addonsRequest]);
    if (!state.metadata) state.metadata = await getJSON("/api/v1/metadata");
    if (!state.storage || Date.now() - state.storageRefreshedAt >= 60000) {
      state.storage = await getJSON("/api/v1/storage"); state.storageRefreshedAt = Date.now(); renderStorage(state.storage);
    }
    const metadata = state.metadata; renderFooter(metadata);
    if (metadata.communication_bridge) renderBridge(metadata.communication_bridge);
    if (!$("#backup-inverter").options.length) for (const inverter of metadata.inverters || []) {
      $("#backup-inverter").add(new Option(`${inverter.name} · ${inverter.model}`,inverter.name));
      $("#preview-inverter").add(new Option(`${inverter.name} · ${inverter.model}`,inverter.name));
    }
    if (!state.liveOrderLoaded) await loadLiveCardOrder();
    state.latest = latest.items; state.telemetry = telemetry; state.addons = addons; renderHealth(health, telemetry); renderAlerts(latest.items, telemetry, metadata.alert_thresholds, state.storage, addons); renderDeviceInformation(latest.items, metadata); renderAddons(addons); renderUps(addons); renderFaultMemory(latest.items); if (!state.liveOrderDragging) renderCards(latest.items, metadata.alert_thresholds?.metrics, addons);
    await populateMetricSelector(latest.items, false);
  } catch (error) {
    renderHealth({ status: "unavailable" }); $("#last-error").textContent = error.message;
  } finally {
    refreshRunning = false;
  }
}

$("#metric").addEventListener("change", async (event) => { [state.inverter, state.metric] = event.target.value.split("\u001f"); await refreshHistory(); });
function updateSelectedExport() {
  const link=$("#export-selected");
  const selected=[...state.historyExportSelected].map(key=>key.split("\u001f"));
  const sources=[...new Set(selected.map(([source])=>source))];
  if (!selected.length || sources.length !== 1) { link.hidden=true; return; }
  const metrics=selected.map(([,metric])=>metric);
  link.href = `/api/v1/export.csv?metrics=${encodeURIComponent(metrics.join(","))}&inverter=${encodeURIComponent(sources[0])}`;
  link.textContent = `${metrics.length} · ${t("storage.exportSelected")}`;
  link.hidden=false;
}
function updateHistoryHover(event) {
  if (state.historyPan) return;
  const geometry=state.historyGeometry;
  if (!geometry) return;
  const {start,duration,pad,width,rect,series,colors}=geometry;
  const x=Math.max(pad.left, Math.min(rect.width-pad.right, event.offsetX));
  const target=start+duration*(x-pad.left)/width;
  state.historyHover=target;
  const tooltip=$("#chart-tooltip"); tooltip.replaceChildren();
  const title=document.createElement("strong"); title.textContent=timeText(new Date(target).toISOString()); tooltip.append(title);
  series.forEach((entry,index)=>{
    if (!entry.items.length) return;
    const nearest=entry.items.reduce((best,item)=>Math.abs(Date.parse(item.observed_at)-target)<Math.abs(Date.parse(best.observed_at)-target)?item:best);
    const row=document.createElement("span"); row.className="chart-tooltip-row";
    const swatch=document.createElement("i"); swatch.style.backgroundColor=colors[index%colors.length];
    const name=document.createElement("b"); name.textContent=historySeriesLabel(entry);
    const value=document.createElement("em"); value.textContent=`${Number(nearest.value).toLocaleString(locale(), {maximumFractionDigits:3})} ${nearest.unit}`;
    row.append(swatch,name,value); tooltip.append(row);
  });
  tooltip.hidden=false;
  const gap=28, edge=8, tooltipWidth=tooltip.offsetWidth;
  // Prefer the value flyout to the right of the temporary ruler.  Once it no
  // longer fits there, move the complete flyout to the left so it never sits
  // on top of the inspected curve position.
  const fitsRight=event.offsetX+gap+tooltipWidth+edge<=rect.width;
  const left=fitsRight
    ? event.offsetX+gap
    : Math.max(edge,event.offsetX-gap-tooltipWidth);
  tooltip.style.left=`${left}px`; tooltip.style.top="8px";
  renderChart(state.history);
}
$("#chart").addEventListener("pointermove", updateHistoryHover);
$("#chart").addEventListener("pointerleave", ()=>{ if (state.historyHover == null) return; state.historyHover=null; $("#chart-tooltip").hidden=true; renderChart(state.history); });
$("#chart").addEventListener("wheel", event=>{ const geometry=state.historyGeometry; if(!geometry)return; event.preventDefault(); const fraction=Math.max(0,Math.min(1,(event.offsetX-geometry.pad.left)/geometry.width)); const span=geometry.end-geometry.start; const factor=event.deltaY<0?.75:1/.75; const next=Math.max(1000,Math.min(geometry.dataEnd-geometry.dataStart,span*factor)); const focus=geometry.start+span*fraction; let start=focus-next*fraction; start=Math.max(geometry.dataStart,Math.min(geometry.dataEnd-next,start)); state.historyView={start,end:start+next}; state.historyHover=null; $("#chart-tooltip").hidden=true; renderChart(state.history); },{passive:false});
$("#chart").addEventListener("pointerdown", event=>{ if(event.button!==0)return; const geometry=state.historyGeometry; if(!geometry)return; state.historyPan={x:event.clientX,view:{...state.historyView},moved:false}; event.currentTarget.setPointerCapture(event.pointerId); });
$("#chart").addEventListener("pointermove", event=>{ if(!state.historyPan || !state.historyGeometry)return; const geometry=state.historyGeometry; const delta=event.clientX-state.historyPan.x; if(Math.abs(delta)>3)state.historyPan.moved=true; if(!state.historyPan.moved)return; const span=state.historyPan.view.end-state.historyPan.view.start; const shift=delta/geometry.width*span; let start=state.historyPan.view.start-shift; start=Math.max(geometry.dataStart,Math.min(geometry.dataEnd-span,start)); state.historyView={start,end:start+span}; state.historyHover=null; $("#chart-tooltip").hidden=true; renderChart(state.history); });
$("#chart").addEventListener("pointerup", event=>{ if(event.button!==0)return; state.historyPan=null; event.currentTarget.releasePointerCapture?.(event.pointerId); });
$("#chart").addEventListener("contextmenu", event=>{ event.preventDefault(); addHistoryMarker(event); });
$("#chart").addEventListener("auxclick", event=>{ if(event.button===1)event.preventDefault(); });
$("#chart").addEventListener("dblclick", ()=>{ const chartWrap=$("#chart").closest(".chart-wrap"); if(document.fullscreenElement) document.exitFullscreen?.(); else chartWrap.requestFullscreen?.().catch(()=>{}); });
$("#history-reset-view").addEventListener("click", ()=>{ state.historyView=null; state.historyHover=null; $("#chart-tooltip").hidden=true; renderChart(state.history); });
document.addEventListener("fullscreenchange", scheduleHistoryRender);
$("#history-inverter").addEventListener("change",async event=>{state.inverter=event.target.value;const first=[...$("#metric").options].find(option=>option.value.startsWith(`${state.inverter}\u001f`));state.metric=first?.value.split("\u001f")[1] || null;renderHistoryChannelList();showChannels(state.inverter);await refreshHistory();updateSelectedExport();});
$("#history-select-all").addEventListener("click",async()=>{for(const input of $("#history-channel-list").querySelectorAll("input"))state.historySelected.add(historySelectionKey(state.inverter,input.value));persistHistorySelection();renderHistoryChannelList();await refreshHistory();updateSelectedExport();});
$("#history-select-none").addEventListener("click",async()=>{for(const key of [...state.historySelected])if(key.startsWith(`${state.inverter}\u001f`))state.historySelected.delete(key);persistHistorySelection();renderHistoryChannelList();await refreshHistory();updateSelectedExport();});
$("#history-stop-source-recording").addEventListener("click",async()=>{if(!state.inverter||!confirm(t("history.stopSourceConfirm")))return;try{await stopSourceRecording(state.inverter);await synchronizeRecordingControls();}catch(error){$("#history-recording-result").textContent=error.message;}});
$("#history-stop-all-recording").addEventListener("click",async()=>{if(!confirm(t("history.stopAllConfirm")))return;try{await stopAllRecording();await synchronizeRecordingControls();}catch(error){$("#history-recording-result").textContent=error.message;}});
$("#metric").addEventListener("change", updateSelectedExport);
$("#alert-indicator").addEventListener("click", () => {
  const section = $("#alerts-title").closest("section");
  if (section.classList.contains("is-collapsed")) setSectionCollapsed(section, false);
  section.scrollIntoView({ behavior:"smooth", block:"start" });
});
$("#language").addEventListener("change", (event) => { language = event.target.value; localStorage.setItem("tmm-language", language); state.metricCatalogLoaded=false; applyLanguage(); updateWriteSelection(); updateSelectedExport(); $("#metric").replaceChildren(); renderAlerts(state.latest, state.telemetry, state.metadata?.alert_thresholds, state.storage, state.addons); renderDeviceInformation(state.latest, state.metadata || { inverters: [] }); renderAddons(state.addons); renderUps(state.addons); renderFaultMemory(state.latest); renderCards(state.latest, state.metadata?.alert_thresholds?.metrics, state.addons); renderConditions(); if(state.bridge)renderBridge(state.bridge); renderChart(state.history); showChannels(state.inverter); refresh(); refreshParameterAudit(); });
const hardwareReferenceToggle=$("#hardware-reference-toggle"); hardwareReferenceToggle.checked=localStorage.getItem("tmm-show-hardware-references") !== "false"; hardwareReferenceToggle.addEventListener("change",()=>{localStorage.setItem("tmm-show-hardware-references",String(hardwareReferenceToggle.checked));renderAddons(state.addons);renderUps(state.addons);});
$("#recording-archive").addEventListener("click", () => requestRecording("archive"));
$("#recording-delete").addEventListener("click", () => requestRecording("delete"));
$("#rtu-logbook").addEventListener("toggle",event=>{if(event.target.open)refreshRtuLogbook();});
$("#rtu-refresh").addEventListener("click",refreshRtuLogbook);
$("#engineering-inverter").addEventListener("change", event => showEngineering(event.target.value));
$("#engineering-save").addEventListener("click", saveEngineering);
$("#measurement-hints")?.addEventListener("change", event => { measurementHints = event.target.checked; localStorage.setItem("tmm-measurement-hints", String(measurementHints)); applyMeasurementHints(); });
$("#backup-create").addEventListener("click",createParameterBackup);
$("#backup-inverter").addEventListener("change",refreshParameterBackups);
$("#preview-create").addEventListener("click",createImportPreview);
$("#preview-inverter").addEventListener("change",updateWriteSelection);
$("#preview-filter").addEventListener("change",filterImportPreview);
$("#write-preflight").addEventListener("click",requestWritePreflight);
$("#write-selected").addEventListener("click",writeSelectedParameter);
$("#condition-form").addEventListener("submit",saveCondition);
$("#condition-reset").addEventListener("click",resetConditionForm);
$("#condition-add-operand").addEventListener("click",()=>addConditionOperand());
for(const selector of ["#condition-channel","#condition-operator","#condition-value","#condition-duration"])$(selector).addEventListener("input",renderConditionExpression);
$("#condition-logic").addEventListener("change",renderConditionExpression);
$("#condition-operator").addEventListener("change",event=>{$("#condition-value").disabled=event.target.value==="NOT";renderConditionExpression();});
window.addEventListener("resize", scheduleHistoryRender);
document.addEventListener("visibilitychange",()=>{if(document.visibilityState==="visible")scheduleHistoryRender();});
if("ResizeObserver" in window){
  const historyResizeObserver=new ResizeObserver(entries=>{
    if(entries.some(entry=>entry.contentRect.width>=80&&entry.contentRect.height>=80))scheduleHistoryRender();
  });
  historyResizeObserver.observe($("#chart").closest(".chart-wrap"));
}
installLiveCardDragAndDrop(); initCollapsibleSections(); installSectionDragAndDrop(); loadDashboardSectionOrder(); applyLanguage(); applyMeasurementHints(); refresh(); refreshBridge(); refreshRecording(); loadEngineering(); loadChannels(); refreshConditions(); refreshParameterBackups(); refreshWriteStatus(); refreshWritePreflight(); refreshParameterAudit(); setInterval(refresh, 3000); setInterval(()=>refreshHistory(false), 30000); setInterval(()=>{if(panelRefreshVisible("bridge-title")) refreshBridge();}, 30000); setInterval(()=>{if($("#rtu-logbook").open) refreshRtuLogbook();}, 3000); setInterval(()=>{if(panelRefreshVisible("conditions-title")) refreshConditions();}, 10000); setInterval(()=>{if(panelRefreshVisible("recording-title")) refreshRecording();}, 30000); setInterval(()=>{if(panelRefreshVisible("parameter-backup-title")) refreshParameterBackups();}, 15000); setInterval(()=>{if(panelRefreshVisible("parameter-preview-title")) { refreshWriteStatus(); refreshWritePreflight(); }}, 3000); setInterval(()=>{if(panelRefreshVisible("parameter-preview-title")) refreshParameterAudit();}, 30000);
