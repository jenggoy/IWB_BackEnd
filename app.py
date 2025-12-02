# app.py
import os
import uuid
import jwt
import datetime
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from flask_cors import CORS
from MySQLdb.cursors import DictCursor
import MySQLdb.cursors

# load .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# DB config
app.config['MYSQL_HOST'] = os.getenv("DB_HOST")
app.config['MYSQL_PORT'] = int(os.getenv("DB_PORT", 3306))
app.config['MYSQL_USER'] = os.getenv("DB_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASS")
app.config['MYSQL_DB'] = os.getenv("DB_NAME")
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Secret key untuk JWT
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "rahasia_jwt")

mysql = MySQL(app)

# --- ROUTES ---

# ===================== GET PRODUCT =====================
@app.route("/produk", methods=["GET"])
def get_produk():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT ProductId, ProductDescription, ProductCategory,
               ProductPrice, PhotoURL, PhotoBase64,
               created_at, updated_at
        FROM msproduct
        ORDER BY updated_at DESC
    """)
    data = cur.fetchall()
    cur.close()
    return jsonify({ "data": data }), 200

@app.route("/produk/<id>", methods=["PUT"])
def update_product(id):
    data = request.json

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE msproduct 
        SET ProductDescription=%s, ProductCategory=%s, ProductPrice=%s,
            PhotoURL=%s, PhotoBase64=%s, updated_at=NOW()
        WHERE ProductId=%s
    """, (
        data.get("ProductDescription"),
        data.get("ProductCategory"),
        data.get("ProductPrice"),
        data.get("PhotoURL"),
        data.get("PhotoBase64"),
        id
    ))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Product updated!"}), 200

@app.route("/produk/<id>", methods=["DELETE"])
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM msproduct WHERE ProductId=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Product deleted!"}), 200


@app.route("/fighters", methods=["GET"])
def get_fighters():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM MsFighter")
    data = cur.fetchall()
    cur.close()

    exclude_fields = ["created_at", "updated_at"]

    rows = []
    for row in data:
        for f in exclude_fields:
            row.pop(f, None)
        rows.append(row)

    return jsonify(rows)

def classify_style(sa, sb):
    if sa > 1.5 * sb:
        return "Top Roll"
    elif 0.8 * sb < sa < 1.5 * sb:
        return "Hook"
    else:
        return "Press"

def classify_power(sa, sb):
    total = sa + sb
    if total < 50:
        return "Pemula"
    elif 50 <= total < 100:
        return "Menengah"
    else:
        return "Mahir"

@app.route("/fighters", methods=["POST"])
def add_fighter():
    data = request.json
    fighter_id = str(uuid.uuid4())

    sa = int(data.get("sa"))
    sb = int(data.get("sb"))

    style = classify_style(sa, sb)
    level = classify_power(sa, sb)
    power = sa + sb

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO MsFighter (id, name, email, city, photo, sa, sb, power, category, level)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        fighter_id,
        data.get("name"),
        data.get("email"),
        data.get("city"),
        data.get("photo"),
        sa,
        sb,
        power,
        style,   
        level    
    ))
    
    mysql.connection.commit()
    cur.close()

    return jsonify({
        "id": fighter_id,
        "message": "Fighter added!",
        "style": style,
        "power_level": power
    }), 201


@app.route("/produk", methods=["POST"])
def add_product():
    try:
        data = request.json
        product_id = str(uuid.uuid4())

        if not data.get("ProductDescription") or not data.get("ProductCategory") or data.get("ProductPrice") is None:
            return jsonify({"error": "Description, category dan price wajib!"}), 400

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO msproduct
            (ProductId, ProductDescription, ProductCategory, ProductPrice, PhotoURL, PhotoBase64, created_at, updated_at)
            VALUES (%s,%s,%s,%s,%s,%s, NOW(),NOW())
        """, (
            product_id,
            data.get("ProductDescription"),
            data.get("ProductCategory"),
            data.get("ProductPrice"),
            data.get("PhotoURL"),
            data.get("PhotoBase64")
        ))
        mysql.connection.commit()
        cur.close()

        return jsonify({
            "message": "Product added!",
            "data": {
                "ProductId": product_id,
                "ProductDescription": data.get("ProductDescription"),
                "ProductCategory": data.get("ProductCategory"),
                "ProductPrice": data.get("ProductPrice"),
                "PhotoURL": data.get("PhotoURL"),
                "PhotoBase64": data.get("PhotoBase64")
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/fighters/<id>", methods=["PUT"])
def update_fighter(id):
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE MsFighter
        SET name=%s, email=%s, city=%s, photo=%s, sa=%s, sb=%s
        WHERE id=%s
    """, (
        data.get("name"),
        data.get("email"),
        data.get("city"),
        data.get("photo"),
        data.get("sa"),
        data.get("sb"),
        id
    ))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Fighter updated!"})

@app.route("/fighters/<id>", methods=["DELETE"])
def delete_fighter(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM MsFighter WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Fighter deleted!"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email dan password wajib diisi"}), 400

    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT id, email FROM MsUser WHERE email=%s AND password=%s", (email, password))
    user = cur.fetchone()
    cur.close()

    if user:
        # Buat JWT token
        token = jwt.encode({
            "id": user["id"],
            "email": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=4)  # expired 1 jam
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({"message": "Login berhasil", "token": token}), 200
    else:
        return jsonify({"error": "Email atau password salah"}), 401

# Middleware untuk proteksi route
def token_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Ambil token dari header
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Token tidak ditemukan"}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token tidak valid"}), 401

        return f(*args, **kwargs)
    return decorated

@app.route("/admin", methods=["GET"])
@token_required
def admin_page():
    return jsonify({
        "message": "Selamat datang di halaman admin!",
        "user": request.user   # data dari token
    }), 200
if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 5000)), debug=True)
