#!/bin/bash
if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters." 
    echo "Run with ./multipleDt.sh dt_start dt_step dt_end"
    exit 1
fi

# Disable plotting if enabled
sed -i -e 's/\"plot\": true/\"plot\": false/g' config.json

DT="$1"
while (( $(echo "$DT <= $3" | bc -l) ))
do
    OUT1=$(./target/tp4-simu-1.0/damped-osc.sh -Dalgo=Verlet -Ddt="$DT" 2>&1 >/dev/null)
    OUT2=$(./target/tp4-simu-1.0/damped-osc.sh -Dalgo=Beeman -Ddt="$DT" 2>&1 >/dev/null)
    OUT3=$(./target/tp4-simu-1.0/damped-osc.sh -Dalgo=Gear -Ddt="$DT" 2>&1 >/dev/null)
    python3.8 analysisOsc.py "$OUT1" "$OUT2" "$OUT3"
    echo "-----------------------------------"
    DT=$(echo "$DT + $2" | bc -l)
done

# Reenable plotting
sed -i -e 's/\"plot\": false/\"plot\": true/g' config.json