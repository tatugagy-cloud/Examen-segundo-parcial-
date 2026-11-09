#!/usr/bin/env python3
import sys
import csv

for linea in sys.stdin:
    try:
        fila = next(csv.reader([linea]))

        if fila[0] == "id":
            continue

        if len(fila) != 8:
            continue

        fecha = fila[1]
        categoria = fila[3]
        cantidad = int(fila[5])
        precio = float(fila[6])

        mes = fecha[:7]
        ingreso = cantidad * precio

        clave = f"{categoria}|{mes}"

        print(f"{clave}\t{ingreso}")

    except (ValueError, IndexError, StopIteration):
        continue