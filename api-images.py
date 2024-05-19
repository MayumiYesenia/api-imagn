from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)

app.secret_key = "my_secret_key"

CORS(app, resources={r"/": {"origins": ""}}, supports_credentials=True)

db = mysql.connector.connect(
    host="database-proyecto.c45ddxrq8nnm.us-east-1.rds.amazonaws.com",
    user="admin",
    password="database-proyecto",
    database="imagenes"
)

cursor = db.cursor(dictionary=True)

@app.route("/images", methods=["GET"])
def get_images():
    query = "SELECT * FROM images"
    cursor.execute(query)
    images = cursor.fetchall()
    return jsonify(images)

@app.route("/image/<int:id>", methods=["GET"])
def get_image(id):
    query = "SELECT * FROM images WHERE id = %s"
    cursor.execute(query, (id,))
    image = cursor.fetchone()
    if image:
        return jsonify(image)
    else:
        return jsonify({"error": "Imagen no encontrada"}), 404

@app.route("/image", methods=["POST"])
def create_image():
    data = request.json
    if "name" in data and "description" in data and "url" in data:
        query = "INSERT INTO images (name, description, url) VALUES (%s, %s, %s)"
        values = (data["name"], data["description"], data["url"])
        cursor.execute(query, values)
        db.commit()
        return jsonify({"message": "Imagen creada exitosamente"}), 201
    else:
        return jsonify({"error": "Faltan datos en la solicitud"}), 400

@app.route("/image/<int:id>", methods=["PUT"])
def update_image(id):
    data = request.json
    if "name" in data or "description" in data or "url" in data:
        updates = []
        values = []
        if "name" in data:
            updates.append("name = %s")
            values.append(data["name"])
        if "description" in data:
            updates.append("description = %s")
            values.append(data["description"])
        if "url" in data:
            updates.append("url = %s")
            values.append(data["url"])

        query = "UPDATE images SET " + ", ".join(updates) + " WHERE id = %s"
        values.append(id)
        cursor.execute(query, tuple(values))
        db.commit()
        return jsonify({"message": "Imagen actualizada exitosamente"}), 200
    else:
        return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

@app.route("/image/<int:id>", methods=["DELETE"])
def delete_image(id):
    query = "DELETE FROM images WHERE id = %s"
    cursor.execute(query, (id,))
    db.commit()
    if cursor.rowcount > 0:
        return jsonify({"message": "Imagen eliminada exitosamente"}), 200
    else:
        return jsonify({"error": "Imagen no encontrada"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8002, debug=True)