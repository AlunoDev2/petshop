from flask import Flask, jsonify, request
import jwt
import os
from datetime import datetime, timedelta

app = Flask(__name__)
SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-secreta")

produtos = [
    {"id": 1, "product_name": "Coleira", "product_description": "Coleira para cachorro de pequeno porte", "product_price": 23.90, "product_photo": "https://exemplo.com/coleira.jpg", "stock_quantity": 26},
    {"id": 2, "product_name": "Ração", "product_description": "Ração para cães adultos", "product_price": 119.90, "product_photo": "https://exemplo.com/racao.jpg", "stock_quantity": 40},
    {"id": 3, "product_name": "Brinquedo", "product_description": "Brinquedo de borracha para cães", "product_price": 15.00, "product_photo": "https://exemplo.com/brinquedo.jpg", "stock_quantity": 50}
]

def comprova_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split()[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route("/")
def home():
    return jsonify(message="API do Pet Shop ativa! Faça login para acessar os produtos.")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data and data.get("username") == "admin" and data.get("password") == "123":
        token = jwt.encode(
            {"user": data["username"], "exp": datetime.utcnow() + timedelta(minutes=30)},
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify(token=token)
    return jsonify(message="Credenciais inválidas"), 401

def ordenar_por_preco(lista, crescente=True):
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if (crescente and lista[j]["product_price"] > lista[j + 1]["product_price"]) or \
               (not crescente and lista[j]["product_price"] < lista[j + 1]["product_price"]):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista

@app.route("/products", methods=["GET"])
def listar_produtos():
    if not comprova_token():
        return jsonify(message="Token inválido ou ausente"), 403

    preco_asc = request.args.get("preco_asc")
    preco_desc = request.args.get("preco_desc")
    desc_part = request.args.get("description_part")

    resultado = produtos.copy()

    if preco_asc == "true":
        resultado = ordenar_por_preco(resultado, crescente=True)
    elif preco_desc == "true":
        resultado = ordenar_por_preco(resultado, crescente=False)
    elif desc_part:
        resultado = [p for p in resultado if desc_part.lower() in p["product_description"].lower()]

    return jsonify(resultado)

@app.route("/products/<int:produto_id>", methods=["GET"])
def produto_por_id(produto_id):
    if not comprova_token():
        return jsonify(message="Token inválido ou ausente"), 403

    for produto in produtos:
        if produto["id"] == produto_id:
            return jsonify(produto)

    return jsonify(message="Produto não encontrado"), 404