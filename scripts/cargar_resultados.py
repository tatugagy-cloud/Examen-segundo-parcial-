import psycopg2
import os

conexion = psycopg2.connect(
    host=os.getenv("DB_HOST", "db"),
    database=os.getenv("POSTGRES_DB", "datamart"),
    user=os.getenv("POSTGRES_USER", "admin"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=5432
)

cursor = conexion.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS resultados (
        id SERIAL PRIMARY KEY,
        categoria VARCHAR(100) NOT NULL,
        mes VARCHAR(7) NOT NULL,
        ingreso_total NUMERIC(18,2) NOT NULL,
        UNIQUE(categoria, mes)
    )
""")

archivo = "/data/output/resultado/part-00000"

with open(archivo, "r") as f:
    for linea in f:
        try:
            clave, ingreso = linea.strip().split("\t")
            categoria, mes = clave.split("|")

            cursor.execute("""
                INSERT INTO resultados
                (categoria, mes, ingreso_total)
                VALUES (%s, %s, %s)
                ON CONFLICT (categoria, mes)
                DO UPDATE SET ingreso_total = EXCLUDED.ingreso_total
            """, (categoria, mes, float(ingreso)))

        except ValueError:
            continue

conexion.commit()
cursor.close()
conexion.close()

print("Resultados cargados correctamente.")