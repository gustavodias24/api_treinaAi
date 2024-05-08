from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, request, jsonify

uri = "mongodb+srv://benicio:ebS3RM8Vew0hPt8y@cluster0.5g6o5p0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["db"]
col_users = db["users"]

app = Flask(__name__)


@app.route("/logar/user", methods=["POST"])
def logar_usuario():
    body = request.get_json()

    if col_users.find_one({"email": body.get('email'), "senha": body.get('senha')}):
        return jsonify({"resp": "sucess"}), 200

    return jsonify({"resp": "Email ou Senha Inválidos!"}), 400


@app.route("/criar/user", methods=["POST"])
def criar_usuario():
    body = request.get_json()

    col_users.insert_one({
        "nomeCompleto": body.get('nomeCompleto'),
        "username": body.get('username'),
        "email": body.get('email'),
        "senha": body.get('senha'),
    })

    return jsonify({"resp": "Conta Criada com Sucesso!"}), 200


@app.route("/atualizar/user", methods=["PUT"])
def atualizar_usuario():
    body = request.get_json()

    if not col_users.find_one({"email": body.get('email')}):
        return jsonify({"resp": "Email não Cadastrado no Banco de Dados!"}), 400

    col_users.update_one(
        {"email": body.get('email')},
        {"$set": {"senha": body.get("novaSenha")}}
    )

    return jsonify({"resp": "Senha Atualizada com Sucesso!"}), 200


if __name__ == "__main__":
    app.run(debug=True)
