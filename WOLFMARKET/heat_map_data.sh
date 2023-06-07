#!/bin/bash
clear
cat arte_start.txt
sleep 3
while true; do
    python3 heat_map_data.py
    if [ $? -ne 0 ]; then
        clear
        echo "El programa ha fallado con un error de Segmentation Fault. Reiniciando..." >> heat_map_data.log
        cat arte_ascii.txt
        for ((i=0; i<10; i++)); do
            # Calcular el progreso actual de la barra de carga

        echo "RESET IN 10 SECONDS..."
        echo -n "[                    ] 0%"

        percent=0
        for i in {1..20}
        do
            echo -ne "\r["
            for j in $(seq 1 $i); do echo -n "█"; done
            for j in $(seq $i 19); do echo -n " "; done
            percent=$(( i * 5 ))
            echo -n "] $percent%"
            sleep 0.5
        done

        echo -e "\nProceso completado."

        done
    fi
done

# █ 