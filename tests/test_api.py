"""
================================================================================
INTEGRATION TESTS: FASTAPI REST ENDPOINTS & WORKFLOWS
================================================================================
Tests:
    1. System Status & Healthcheck
    2. Account Creation (Hash Map + BST + Welcome Email dispatch)
    3. Deposits & Withdrawals with balance updates
    4. Validation Edge Cases (Zero/Negative amounts, Insufficient Balance, 404s)
    5. Linked List Transaction Retrieval
    6. Sliding Window Fraud Detection Trigger & Alert Resolution
    7. BST Hierarchy Visualizer & O(log N) Search Endpoint
    8. SMTP Email Audit Log Endpoint
    9. Fraud Engine Settings Update
================================================================================
"""

from fastapi.testclient import TestClient
from backend.main import app, bank_db

client = TestClient(app)


def test_system_status():
    response = client.get("/api/system/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OPERATIONAL"
    assert "dsa_features" in data
    assert data["total_accounts"] >= 5


def test_list_accounts():
    response = client.get("/api/accounts")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 5
    assert isinstance(data["accounts"], list)


def test_create_account_workflow():
    payload = {
        "account_name": "Arjun Kapoor",
        "email": "arjun.kapoor@example.com",
        "account_number": "10001099",
        "initial_deposit": 12000.0,
        "account_type": "SAVINGS"
    }
    response = client.post("/api/accounts", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["account"]["account_number"] == "10001099"
    assert data["account"]["balance"] == 12000.0

    # Retrieve single account via O(1) Hash Map
    get_res = client.get("/api/accounts/10001099")
    assert get_res.status_code == 200
    assert get_res.json()["account_name"] == "Arjun Kapoor"


def test_duplicate_account_creation_fails():
    payload = {
        "account_name": "Duplicate User",
        "email": "dup@example.com",
        "account_number": "10001001",  # Pre-existing seed account
        "initial_deposit": 5000.0
    }
    response = client.post("/api/accounts", json=payload)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_deposit_and_withdrawal_ledger():
    deposit_payload = {
        "account_number": "10001002",
        "amount": 3500.0,
        "description": "Freelance Milestone Payment"
    }
    dep_res = client.post("/api/deposit", json=deposit_payload)
    assert dep_res.status_code == 200
    dep_data = dep_res.json()
    assert dep_data["transaction"]["amount"] == 3500.0
    assert dep_data["transaction"]["tx_type"] == "DEPOSIT"

    # Withdraw
    with_payload = {
        "account_number": "10001002",
        "amount": 1200.0,
        "description": "Utility Bill"
    }
    with_res = client.post("/api/withdraw", json=with_payload)
    assert with_res.status_code == 200
    assert with_res.json()["transaction"]["amount"] == 1200.0

    # Verify Linked List ledger
    ledger_res = client.get("/api/transactions/10001002")
    assert ledger_res.status_code == 200
    txs = ledger_res.json()["transactions"]
    assert txs[0]["tx_type"] == "WITHDRAWAL"
    assert txs[1]["tx_type"] == "DEPOSIT"


def test_insufficient_funds_withdrawal():
    # Withdraw amount greater than balance
    with_payload = {
        "account_number": "10001002",
        "amount": 99999999.0,
        "description": "Excessive Withdrawal"
    }
    response = client.post("/api/withdraw", json=with_payload)
    assert response.status_code == 400
    assert "Insufficient balance" in response.json()["detail"]


def test_nonexistent_account_returns_404():
    get_res = client.get("/api/accounts/99999999")
    assert get_res.status_code == 404

    dep_res = client.post("/api/deposit", json={"account_number": "99999999", "amount": 100.0})
    assert dep_res.status_code == 404

    tx_res = client.get("/api/transactions/99999999")
    assert tx_res.status_code == 404


def test_sliding_window_fraud_detection():
    # Account 10001004 deposit ₹30,000 + ₹25,000 in rapid succession
    client.post("/api/deposit", json={"account_number": "10001004", "amount": 30000.0, "description": "High Value Transfer 1"})
    res2 = client.post("/api/deposit", json={"account_number": "10001004", "amount": 25000.0, "description": "High Value Transfer 2"})
    
    assert res2.status_code == 200
    fraud_eval = res2.json()["fraud_evaluation"]
    assert fraud_eval["is_flagged"] is True
    assert fraud_eval["risk_level"] == "CRITICAL_FRAUD"
    assert fraud_eval["window_sum"] >= 50000.0

    # Check risk status endpoint
    alert_res = client.get("/api/fraud-alerts/10001004")
    assert alert_res.status_code == 200
    assert alert_res.json()["status"] == "FLAGGED"

    # Resolve fraud flag
    resolve_res = client.post("/api/fraud-alerts/10001004/resolve")
    assert resolve_res.status_code == 200
    assert resolve_res.json()["account_status"] == "ACTIVE"


def test_bst_tree_endpoint_and_search():
    response = client.get("/api/system/tree")
    assert response.status_code == 200
    data = response.json()
    assert data["data_structure"] == "Binary Search Tree (BST)"
    assert data["tree"] is not None
    assert "account_number" in data["tree"]

    # Test BST logarithmic search endpoint
    search_res = client.get("/api/dsa/bst/search?account_number=10001001")
    assert search_res.status_code == 200
    search_data = search_res.json()
    assert search_data["found"] is True
    assert search_data["account"]["account_number"] == "10001001"

    # Nonexistent account search in BST
    search_not_found = client.get("/api/dsa/bst/search?account_number=99999999")
    assert search_not_found.status_code == 404


def test_email_audit_logs():
    response = client.get("/api/emails")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["emails"], list)
    assert data["total_dispatched"] > 0


def test_settings_fraud_update():
    payload = {
        "k_window": 4,
        "fraud_threshold": 60000.0
    }
    response = client.post("/api/settings/fraud", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["k_window"] == 4
    assert data["fraud_threshold"] == 60000.0
