from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

def conectar():
    return psycopg2.connect(
        host="db",
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=5432
    )

def crear_tabla():
    conexion = conectar()
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

    conexion.commit()
    cursor.close()
    conexion.close()

@app.route("/")
def inicio():
    return jsonify({"mensaje": "API DataMart funcionando"})

@app.route("/resultados", methods=["GET"])
def obtener_resultados():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, categoria, mes, ingreso_total
        FROM resultados
        ORDER BY mes, categoria
    """)

    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return jsonify([
        {
            "id": fila[0],
            "categoria": fila[1],
            "mes": fila[2],
            "ingreso_total": float(fila[3])
        }
        for fila in datos
    ])

@app.route("/resultados/<categoria>", methods=["GET"])
def filtrar_resultados(categoria):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, categoria, mes, ingreso_total
        FROM resultados
        WHERE categoria = %s
    """, (categoria,))

    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return jsonify([
        {
            "id": fila[0],
            "categoria": fila[1],
            "mes": fila[2],
            "ingreso_total": float(fila[3])
        }
        for fila in datos
    ])

@app.route("/resultados", methods=["POST"])
def insertar_resultado():
    datos = request.get_json()

    try:
        categoria = datos["categoria"]
        mes = datos["mes"]
        ingreso = datos["ingreso_total"]

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO resultados (categoria, mes, ingreso_total)
            VALUES (%s, %s, %s)
            ON CONFLICT (categoria, mes)
            DO UPDATE SET ingreso_total = EXCLUDED.ingreso_total
            RETURNING id
        """, (categoria, mes, ingreso))

        nuevo_id = cursor.fetchone()[0]

        conexion.commit()
        cursor.close()
        conexion.close()

        return jsonify({
            "mensaje": "Resultado guardado",
            "id": nuevo_id
        }), 201

    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Datos incompletos o inválidos"}), 400

@app.route("/resultados/<int:id>", methods=["DELETE"])
def eliminar_resultado(id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM resultados WHERE id = %s", (id,))

    eliminado = cursor.rowcount

    conexion.commit()
    cursor.close()
    conexion.close()

    if eliminado:
        return jsonify({"mensaje": "Resultado eliminado"})

    return jsonify({"error": "No encontrado"}), 404

if __name__ == "__main__":
    crear_tabla()
    app.run(host="0.0.0.0", port=5000)