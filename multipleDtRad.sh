#!/bin/bash
LC_NUMERIC="en_US.UTF-8"

if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters." 
    echo "Run with ./multipleV0.sh dt_start dt_step dt_end rep"
    exit 1
fi

# Disable plotting if enabled
sed -i -e 's/\"plot\": true/\"plot\": false/g' config.json

# TODO: Definir un V0 fijo correcto para el sistema
V0=10000
DT=$(printf "%.30f" $1)
STEP=$(printf "%.30f" $2)
DT_MAX=$(printf "%.30f" $3)
while (( $(echo "$DT <= $DT_MAX" | bc -l) ))
do
    OUT=""
    for i in $(seq 1 $4)
    do
        AUX=$(./target/tp4-simu-1.0/radiation-interaction.sh -Ddt="$DT" -Dv0="$V0" -DdynamicSuf=_"$i" 2>&1 >/dev/null)
        OUT="$OUT $AUX"
    done
    python3.8 analysisRad.py $OUT
    echo "-----------------------------------"
    DT=$(echo "$DT + $STEP" | bc -l)
done

# Reenable plotting
sed -i -e 's/\"plot\": false/\"plot\": true/g' config.json