#!/bin/sh
# Download optional Sequent documentation from its official publisher and
# verify every file before making it available to TMM.
set -eu

DESTINATION=${1:-/opt/tmm/static/docs/sequent}
mkdir -p "$DESTINATION"

download_document() {
    filename=$1
    expected=$2
    url=$3
    temporary="$DESTINATION/.${filename}.download.$$"
    trap 'rm -f "$temporary"' EXIT HUP INT TERM
    curl --fail --location --silent --show-error --retry 3 --output "$temporary" "$url"
    if ! printf '%s  %s\n' "$expected" "$temporary" | sha256sum --check --status -; then
        echo "Checksum verification failed: $filename" >&2
        rm -f "$temporary"
        trap - EXIT HUP INT TERM
        return 1
    fi
    chmod 0644 "$temporary"
    mv -f "$temporary" "$DESTINATION/$filename"
    trap - EXIT HUP INT TERM
}

while IFS='|' read -r filename expected url; do
    [ -n "$filename" ] || continue
    download_document "$filename" "$expected" "$url" || exit 1
done <<'EOF'
16inpind-users-guide-v1.pdf|fe33ced8849dee50ebfa17fe868e48d8ef42104a1933a0ddfda39a4114eaa1fb|https://cdn.shopify.com/s/files/1/0534/4392/0067/files/16-INPUTS-UsersGuide_fe9f7d34-7077-4415-af79-57fdae1e534f.pdf?v=1704912646
16inpind-schematic-v2.pdf|7f9446c075cf1ef69a10b923359745f7d3d4e66f324d9b98394699073427bf2d|https://cdn.shopify.com/s/files/1/0534/4392/0067/files/16-INPUTS-Schematic.pdf?v=1643422376
24b8vin-users-guide-v1.2.pdf|e2ea0faa1282151d5a78bf31d241921119588c6b9a7f6ad34eee9d46fc3795ea|https://cdn.shopify.com/s/files/1/0534/4392/0067/files/8-24-Bit_Analog_Inputs-UsersGuide.pdf?v=1786810944
24b8vin-schematic-v1.1.pdf|ed4c2261bba7b0addc7fccb09a52030909ba6fbe96fa413be63a5d0b80534bf2|https://cdn.shopify.com/s/files/1/0534/4392/0067/files/8-24BIT-A2D-V1_1-Schematic.pdf?v=1738101478
multiio-users-guide-v1.3.pdf|5bfa6e419d2010ecb7eb476f428bacdd22484133f329c9014ec479037b4b9b53|https://cdn.shopify.com/s/files/1/0534/4392/0067/files/Multi-IO-UsersGuide.pdf?v=1719204229
multiio-schematic-v3.2.pdf|810fa5c37a57c4ff099137d3580c569e83ff24c2c3eb101eaabbf7964b4b7c9e|https://cdn.shopify.com/s/files/1/0534/4392/0067/files/MULTI-IO-SCHEMATIC-V3_2.pdf?v=1781918917
super-watchdog-users-guide-v6.pdf|12cf280be1393367cce16771d5de3500e1f4359e960760f0c24211f3e5ab62da|https://cdn.shopify.com/s/files/1/0534/4392/0067/files/WATCHDOG-UsersGuide-V6.pdf?v=1683864119
super-watchdog-schematic-v9.pdf|3a139e954e4dacef0fc677e1e1164eb788652632ae296f5fb5b1577375bc91ee|https://cdn.shopify.com/s/files/1/0534/4392/0067/files/Watchdog-V9-Schematic.pdf?v=1730944465
smart-fan-users-guide.pdf|5c3c9150f0edce7d973a4d5fa6f2eb4e3e5b242bb04f73f31bc3967904c2c81a|https://cdn.shopify.com/s/files/1/0534/4392/0067/files/SmartFan-UsersGuide.pdf?v=1643426365
smart-fan-schematic-v5.pdf|93396b1bc39a7001bf1cd334491ba941da7d478526ff7d6e33067c47bcf5f71c|https://cdn.shopify.com/s/files/1/0534/4392/0067/files/Smart-FAN-Schematic-V5.pdf?v=1680968853
EOF

printf 'window.TMM_SEQUENT_DOCS_LOCAL = true;\n' >"$DESTINATION/availability.js"
chmod 0644 "$DESTINATION/availability.js"
echo "Verified Sequent documentation installed in $DESTINATION"
