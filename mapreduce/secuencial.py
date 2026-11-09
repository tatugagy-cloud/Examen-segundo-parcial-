import csv
import time
from collections import defaultdict

inicio = time.time()

resultados = defaultdict(float)

archivo = "/data/input/ventas_125054560.csv"

with open(archivo, "r", encoding="utf-8") as f:
    lector = csv.DictReader(f)

    for fila in lector:
        try:
            categoria = fila["categoria"]
            mes = fila["fecha_hora"][:7]

            cantidad = int(fila["cantidad"])
            precio = float(fila["precio_unitario"])

            clave = (categoria, mes)

            resultados[clave] += cantidad * precio

        except (ValueError, KeyError):
            continue

fin = time.time()

for clave, ingreso in sorted(resultados.items()):
    print(f"{clave[0]}|{clave[1]}\t{ingreso:.2f}")

print(f"Tiempo secuencial: {fin - inicio:.2f} segundos")