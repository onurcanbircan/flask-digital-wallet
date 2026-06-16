from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite Veritabanı Yapılandırması
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wallet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanı nesnesini başlatıyoruz
db = SQLAlchemy(app)


# VERİTABANI MODELLERİ (TABLOLAR)
class Wallet(db.Model):
    __tablename__ = 'wallets'
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=0.0, nullable=False)

    def to_dict(self):
        """Ön yüze JSON gönderirken kolaylık sağlaması için yardımcı metot"""
        return {
            "id": self.id,
            "owner": self.owner,
            "balance": self.balance
        }

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # 'deposit' veya 'transfer'
    wallet_id = db.Column(db.Integer, nullable=True)  # Yükleme yapılan cüzdan
    from_id = db.Column(db.Integer, nullable=True)    # Transferde gönderen cüzdan
    to_id = db.Column(db.Integer, nullable=True)      # Transferde alıcı cüzdan
    amount = db.Column(db.Float, nullable=False)

    def to_dict(self):
        """Ön yüzdeki JavaScript log yapısına tam uyum sağlaması için"""
        data = {
            "type": self.type,
            "amount": self.amount
        }

        if self.type == "deposit":
            data["wallet"] = self.wallet_id

        elif self.type == "transfer":
            data["from"] = self.from_id
            data["to"] = self.to_id
            
        return data


@app.get("/")
def home():
    return render_template("index.html")

# 1. Tüm Cüzdanları Listele
@app.get("/api/wallets")
def list_wallets():
    # Veritabanındaki tüm cüzdanları çekiyoruz
    wallets = Wallet.query.all()
    return jsonify([w.to_dict() for w in wallets]), 200

# 2. Yeni Cüzdan Oluştur
@app.post("/api/wallets")
def create_wallet():
    data = request.get_json(silent=True) or {}
    owner = (data.get("owner") or "").strip()

    if len(owner) < 2:
        return jsonify({"error": "owner en az 2 karakterden oluşmalıdır"}), 400
    
    # Yeni cüzdan nesnesi oluşturuluyor (ID'yi SQLite otomatik artıracak)
    new_wallet = Wallet(owner=owner, balance=0.0)
    
    db.session.add(new_wallet)
    db.session.commit()

    return jsonify(new_wallet.to_dict()), 201

# 3. ID ile Tek Bir Cüzdan Getir
@app.get("/api/wallets/<int:wallet_id>")
def get_wallet(wallet_id):
    wallet = Wallet.query.get(wallet_id)

    if not wallet:
        return jsonify({"error": "Wallet bulunamadı"}), 404
    
    return jsonify(wallet.to_dict()), 200

# 4. Cüzdana Para Yükleme
@app.post("/api/wallets/<int:wallet_id>/deposit")
def deposit_to_wallet(wallet_id):
    wallet = Wallet.query.get(wallet_id)
    if not wallet:
        return jsonify({"error": "Wallet bulunamadı"}), 404
    
    data = request.get_json() or {}
    amount = data.get("amount")

    if amount is None or not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Amount pozitif bir sayı olmalı"}), 400
    
    # Bakiyeyi güncelle
    wallet.balance = round(wallet.balance + amount, 2)
    
    # İşlem geçmişini (Log) veritabanına ekle
    new_tx = Transaction(type="deposit", wallet_id=wallet_id, amount=amount)
    db.session.add(new_tx)
    
    db.session.commit()
    
    return jsonify(wallet.to_dict()), 200

# 5. İki Cüzdan Arası Para Transferi
@app.post("/api/transfers")
def transfers():
    data = request.get_json() or {}

    from_id = data.get("from_wallet")
    to_id = data.get("to_wallet")
    amount = data.get("amount")

    from_wallet = Wallet.query.get(from_id)
    to_wallet = Wallet.query.get(to_id)

    if not from_wallet or not to_wallet:
        return jsonify({"error": "Cüzdanlardan biri veya ikisi bulunamadı"}), 404
    
    if from_id == to_id:
        return jsonify({"error": "Kendinize transfer yapamazsınız"}), 400
    
    if amount is None or not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Amount pozitif bir sayı olmalı"}), 400
    
    if from_wallet.balance < amount:
        return jsonify({"error": "Yetersiz bakiye"}), 400
    
    # Transfer işlemi ve bakiye güncelleme
    from_wallet.balance = round(from_wallet.balance - amount, 2)
    to_wallet.balance = round(to_wallet.balance + amount, 2)

    # Transfer logunu veritabanına ekle
    new_tx = Transaction(type="transfer", from_id=from_id, to_id=to_id, amount=amount)
    db.session.add(new_tx)
    
    db.session.commit()

    return jsonify({
         "message": "transfer başarılı",
         "from_balance": from_wallet.balance,
         "to_balance": to_wallet.balance
    }), 200

# 6. İşlem Geçmişi
@app.get("/api/transactions")
def list_transactions():
     transactions = Transaction.query.all()
     return jsonify([tx.to_dict() for tx in transactions]), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)