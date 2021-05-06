#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters." 
    echo "Run with ./multipleV0.sh v0_step rep"
    exit 1
fi

# Disable plotting if enabled
sed -i -e 's/\"plot\": true/\"plot\": false/g' config.json

DT=$(echo "0.0000000000000001" | bc -l)
V0=10000
while (( $(echo "$V0 <= 100000" | bc -l) ))
do
    OUT=""
    for i in $(seq 1 $2)
    do
        AUX=$(./target/tp4-simu-1.0/radiation-interaction.sh -Ddt="$DT" -Dv0="$V0" -DdynamicSuf=_"$i" 2>&1 >/dev/null)
        OUT="$OUT $AUX"
    done
    python3.8 analysisRad.py $OUT
    echo "-----------------------------------"
    V0=$(echo "$V0 + $1" | bc -l)
done

# Reenable plotting
sed -i -e 's/\"plot\": false/\"plot\": true/g' config.json