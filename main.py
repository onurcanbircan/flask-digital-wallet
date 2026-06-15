from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

WALLETS = {}
NEXT_ID = 1
TRANSACTIONS = []

@app.get("/")
def home():
    return render_template("index.html")

# 1. Tüm Cüzdanları Listele
@app.get("/api/wallets")
def list_wallets():
    return jsonify(list(WALLETS.values())), 200

# 2. Yeni Cüzdan Oluştur
@app.post("/api/wallets")
def create_wallet():
    global NEXT_ID

    data = request.get_json(silent=True) or {}
    owner = (data.get("owner") or "").strip()

    if len(owner) < 2:
        return jsonify({"error": "owner en az 2 karakterden oluşmalıdır"}), 400
    
    wallet = {
        "id": NEXT_ID, 
        "owner": owner, 
        "balance": 0.0
    }
    
    WALLETS[NEXT_ID] = wallet
    NEXT_ID += 1

    return jsonify(wallet), 201

# 3. ID ile Tek Bir Cüzdan Getir
@app.get("/api/wallets/<int:wallet_id>")
def get_wallet(wallet_id):
    wallet = WALLETS.get(wallet_id)

    if not wallet:
        return jsonify({"error": "Wallet bulunamadı"}), 404
    
    return jsonify(wallet), 200

# 4. Cüzdana Para Yükleme
@app.post("/api/wallets/<int:wallet_id>/deposit")
def deposit_to_wallet(wallet_id):
    wallet = WALLETS.get(wallet_id)
    if not wallet:
        return jsonify({"error": "Wallet bulunamadı"}), 404
    
    data = request.get_json() or {}
    amount = data.get("amount")

    # Geliştirme: Gelen değerin sayı olup olmadığını kontrol ediyoruz
    if amount is None or not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Amount pozitif bir sayı olmalı"}), 400
    
    wallet["balance"] = round(wallet["balance"] + amount, 2)
    
    TRANSACTIONS.append({
        "type": "deposit",
        "wallet": wallet_id,
        "amount": amount
    })
    return jsonify(wallet), 200

# 5. İki Cüzdan Arası Para Transferi
@app.post("/api/transfers")
def transfers():
    data = request.get_json() or {}

    from_id = data.get("from_wallet")
    to_id = data.get("to_wallet")
    amount = data.get("amount")

    from_wallet = WALLETS.get(from_id)
    to_wallet = WALLETS.get(to_id)

    if not from_wallet or not to_wallet:
        return jsonify({"error": "Cüzdanlardan biri veya ikisi bulunamadı"}), 404
    
    if from_id == to_id:
        return jsonify({"error": "Kendinize transfer yapamazsınız"}), 400
    
    if amount is None or not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Amount pozitif bir sayı olmalı"}), 400
    
    if from_wallet["balance"] < amount:
        return jsonify({"error": "Yetersiz bakiye"}), 400
    
    # Transfer işlemi ve bakiye güncelleme
    from_wallet["balance"] = round(from_wallet["balance"] - amount, 2)
    to_wallet["balance"] = round(to_wallet["balance"] + amount, 2)

    TRANSACTIONS.append({
         "type": "transfer",
         "from": from_id,
         "to": to_id,
         "amount": amount
    })

    return jsonify({
         "message": "transfer başarılı",
         "from_balance": from_wallet["balance"],
         "to_balance": to_wallet["balance"]
    }), 200

# 6. İşlem Geçmişi
@app.get("/api/transactions")
def list_transactions():
     return jsonify(TRANSACTIONS), 200


if __name__ == "__main__":
    app.run(debug=True)