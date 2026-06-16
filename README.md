# 💰 Flask Digital Wallet API & Management Dashboard

This project is a minimalist, secure, and production-ready **Digital Wallet Management System** built with **Flask (Python)** and **Vanilla JavaScript (Tailwind CSS)**. 

The primary objective of this project is to simulate core Financial Technology (Fintech) operations—such as balance management, structured depositing, and atomic peer-to-peer transfers—while adhering to clean code architecture, strict backend validations, and database persistence.

---

## 🚀 Key Features & Business Logic Validations

Unlike basic CRUD applications, this system enforces critical fintech business rules at the database and backend level:
* **Data Persistence (SQLite & SQLAlchemy):** Migrated from in-memory structures to an ORM-managed relational database.
* **Strict Payload Validation:** Rejecting invalid formats, preventing empty names (minimum 2 characters), and enforcing type checking (`isinstance` for `int` and `float`).
* **Precision Ledger & Anti-Floating Point Errors:** All balance evaluations utilize Python's `round(value, 2)` before database insertion to completely mitigate standard floating-point arithmetic anomalies.
* **Atomic P2P Transfer Invariants:** Double-entry ledger verification that blocks self-transfers, validates the existence of both accounts, and rollbacks/cancels operations on insufficient funds.
* **Live Reverse-Chronological Audit Trail:** Complete operation log displayed in real-time on the client side.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.12, Flask Web Framework, Flask-SQLAlchemy (ORM)
* **Database:** SQLite (Relational embedded database)
* **Frontend:** HTML5, Tailwind CSS v4 (via modern browser compiler), Asynchronous Vanilla JavaScript (Fetch API)

---

## 🔌 API Documentation (REST Endpoints)

### 1. List All Wallets
* **URL:** `/api/wallets`
* **Method:** `GET`
* **Response (200 OK):**
    ```json
    [
      { "id": 1, "owner": "Ahmet Yılmaz", "balance": 250.50 },
      { "id": 2, "owner": "Mehmet Demir", "balance": 0.0 }
    ]
    ```

### 2. Create a New Wallet
* **URL:** `/api/wallets`
* **Method:** `POST`
* **Payload:**
    ```json
    { "owner": "Ahmet Yılmaz" }
    ```
* **Response (201 Created):**
    ```json
    { "id": 1, "owner": "Ahmet Yılmaz", "balance": 0.0 }
    ```

### 3. Deposit to Wallet
* **URL:** `/api/wallets/<int:wallet_id>/deposit`
* **Method:** `POST`
* **Payload:**
    ```json
    { "amount": 150.50 }
    ```
* **Response (200 OK):**
    ```json
    { "id": 1, "owner": "Ahmet Yılmaz", "balance": 150.50 }
    ```

### 4. Peer-to-Peer Transfer
* **URL:** `/api/transfers`
* **Method:** `POST`
* **Payload:**
    ```json
    {
      "from_wallet": 1,
      "to_wallet": 2,
      "amount": 50.00
    }
    ```
* **Response (200 OK):**
    ```json
    {
      "message": "transfer başarılı",
      "from_balance": 100.50,
      "to_balance": 50.00
    }
    ```

---

## 📂 Project Structure

```text
├── main.py              # Application entrypoint, Database Models, and API Routes
├── instance/
│   └── wallet.db        # Automatically generated SQLite database file
├── templates/
│   └── index.html       # SPA Dashboard powered by Tailwind CSS & Async Fetch UI
├── requirements.txt     # Locked project dependencies
└── README.md            # System documentation
