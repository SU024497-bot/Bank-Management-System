"""
================================================================================
APEX BANK MANAGEMENT SYSTEM - FASTAPI BACKEND API ENGINE
================================================================================
Integrates:
    - Core DSA Algorithmic Engine (Linked List, Sliding Window, BST, Hash Map)
    - Asynchronous SMTP Email Dispatcher & Mock Fallback Logger
    - Full REST Endpoints with Pydantic validation & CORS support
    - Static single-page dashboard serving
================================================================================
"""

import os
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, status, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr, Field

from .config import settings
from .dsa.account_store import BankDatabaseStore, BankAccount
from .services.smtp_service import smtp_service

# Initialize FastAPI App
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-Ready Bank Management System with Core DSA Algorithms & SMTP Notifications"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Central In-Memory Bank Database Store
# Combines:
# 1. Hash Map: O(1) Instant account lookup
# 2. Linked List: O(1) Transaction ledger head prepend
# 3. Sliding Window: Real-time fraud detection
# 4. BST: Logarithmic search and sorted hierarchy
bank_db = BankDatabaseStore()


# ==============================================================================
# PYDANTIC REQUEST / RESPONSE SCHEMAS
# ==============================================================================

class AccountCreateRequest(BaseModel):
    account_name: str = Field(..., min_length=2, max_length=100, json_schema_extra={"example": "Vikram Sharma"})
    email: EmailStr = Field(..., json_schema_extra={"example": "vikram@example.com"})
    account_number: Optional[str] = Field(None, min_length=4, max_length=20, json_schema_extra={"example": "10001009"})
    initial_deposit: float = Field(0.0, ge=0.0, json_schema_extra={"example": 25000.0})
    phone: Optional[str] = Field("+91 98765 43210", json_schema_extra={"example": "+91 98765 43210"})
    account_type: Optional[str] = Field("SAVINGS", json_schema_extra={"example": "SAVINGS"})


class TransactionRequest(BaseModel):
    account_number: str = Field(..., json_schema_extra={"example": "10001001"})
    amount: float = Field(..., gt=0, json_schema_extra={"example": 5000.0})
    description: Optional[str] = Field("", max_length=200, json_schema_extra={"example": "Vendor Payment"})


class FraudThresholdUpdateRequest(BaseModel):
    k_window: Optional[int] = Field(None, ge=1, le=20, json_schema_extra={"example": 3})
    fraud_threshold: Optional[float] = Field(None, ge=100.0, json_schema_extra={"example": 50000.0})


class SMTPSettingsUpdateRequest(BaseModel):
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    mock_mode: Optional[bool] = None


# ==============================================================================
# REST API ENDPOINTS
# ==============================================================================

@app.get("/api/system/status", tags=["System"])
async def get_system_status():
    """Returns system health, total accounts, transaction volume, and DSA engine stats."""
    all_accs = list(bank_db.accounts_hash_map.values())
    total_tx = sum(len(acc.transaction_ledger) for acc in all_accs)
    flagged_accs = sum(1 for acc in all_accs if acc.status == "FLAGGED")
    total_deposits = sum(acc.balance for acc in all_accs)
    
    return {
        "status": "OPERATIONAL",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "total_accounts": len(all_accs),
        "total_transactions": total_tx,
        "total_deposits": round(total_deposits, 2),
        "flagged_accounts_count": flagged_accs,
        "dsa_features": {
            "transaction_ledger": "Custom Singly Linked List (O(1) Prepend)",
            "fraud_detection": f"Sliding Window Engine (K={settings.DEFAULT_SLIDING_WINDOW_K}, Limit=₹{settings.DEFAULT_FRAUD_THRESHOLD:,.2f})",
            "account_index": "Hash Map O(1) + Binary Search Tree O(log N)"
        },
        "smtp_mode": "REAL_SMTP" if smtp_service._is_real_smtp_configured() else "MOCK_CONSOLE"
    }


@app.post("/api/accounts", status_code=status.HTTP_201_CREATED, tags=["Accounts"])
async def create_account(req: AccountCreateRequest, background_tasks: BackgroundTasks):
    """
    POST /api/accounts:
    1. Indexes new account in Hash Map O(1) and BST O(log N).
    2. Initializes empty Linked List for transactions.
    3. Asynchronously sends Onboarding Welcome Email.
    """
    try:
        acc = bank_db.create_account(
            account_name=req.account_name,
            email=req.email,
            account_number=req.account_number,
            initial_deposit=req.initial_deposit,
            phone=req.phone or "+91 98765 43210",
            account_type=req.account_type or "SAVINGS",
            k_window=settings.DEFAULT_SLIDING_WINDOW_K,
            fraud_threshold=settings.DEFAULT_FRAUD_THRESHOLD
        )
        
        # Dispatch Welcome Email via Background Tasks
        background_tasks.add_task(
            smtp_service.send_welcome_email,
            account_name=acc.account_name,
            account_number=acc.account_number,
            email=acc.email,
            initial_balance=acc.balance
        )
        
        return {
            "message": "Account successfully created and indexed into Hash Map & BST.",
            "account": acc.to_dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/api/accounts", tags=["Accounts"])
async def list_accounts():
    """
    GET /api/accounts:
    Returns all registered accounts in sorted order utilizing BST In-Order Traversal.
    """
    return {
        "count": len(bank_db.accounts_hash_map),
        "accounts": bank_db.list_all_accounts()
    }


@app.get("/api/accounts/{acc_num}", tags=["Accounts"])
async def get_account(acc_num: str):
    """
    GET /api/accounts/{acc_num}:
    Instant O(1) account lookup using primary Hash Map index.
    """
    acc = bank_db.get_account_by_number(acc_num)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bank account #{acc_num} not found in Hash Map index."
        )
    return acc.to_dict()


@app.post("/api/deposit", tags=["Transactions"])
async def deposit_funds(req: TransactionRequest, background_tasks: BackgroundTasks):
    """
    POST /api/deposit:
    1. O(1) Hash Map lookup.
    2. Updates balance and prepends new node to custom Linked List in O(1).
    3. Runs Sliding Window fraud detection across last K operations.
    4. Dispatches instant Credit Email & Security Alert Email if threshold breached.
    """
    acc = bank_db.get_account_by_number(req.account_number)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account #{req.account_number} does not exist."
        )

    try:
        result = acc.deposit(req.amount, req.description)
        bank_db.sync_bst_balance(acc.account_number)
        
        tx_data = result["transaction"]
        fraud_eval = result["fraud_evaluation"]

        # Send Credit Email Notification
        background_tasks.add_task(
            smtp_service.send_transaction_email,
            account_name=acc.account_name,
            account_number=acc.account_number,
            email=acc.email,
            tx_type="DEPOSIT",
            amount=req.amount,
            balance_after=result["current_balance"],
            tx_id=tx_data["tx_id"],
            description=tx_data["description"]
        )

        # If Sliding Window algorithm flagged fraud, send high-priority security alert
        if fraud_eval["is_flagged"]:
            background_tasks.add_task(
                smtp_service.send_security_alert_email,
                account_name=acc.account_name,
                account_number=acc.account_number,
                email=acc.email,
                window_sum=fraud_eval["window_sum"],
                threshold=fraud_eval["threshold"],
                window_size=fraud_eval["window_size"],
                reason=fraud_eval["reason"]
            )

        return {
            "message": "Deposit successful.",
            "transaction": tx_data,
            "fraud_evaluation": fraud_eval,
            "new_balance": result["current_balance"],
            "account_status": acc.status
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/api/withdraw", tags=["Transactions"])
async def withdraw_funds(req: TransactionRequest, background_tasks: BackgroundTasks):
    """
    POST /api/withdraw:
    1. O(1) Hash Map lookup and balance verification.
    2. Deducts amount and prepends to custom Linked List in O(1).
    3. Runs Sliding Window fraud detection across last K operations.
    4. Dispatches instant Debit Email & Security Alert Email if threshold breached.
    """
    acc = bank_db.get_account_by_number(req.account_number)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account #{req.account_number} does not exist."
        )

    try:
        result = acc.withdraw(req.amount, req.description)
        bank_db.sync_bst_balance(acc.account_number)

        tx_data = result["transaction"]
        fraud_eval = result["fraud_evaluation"]

        # Send Debit Email Notification
        background_tasks.add_task(
            smtp_service.send_transaction_email,
            account_name=acc.account_name,
            account_number=acc.account_number,
            email=acc.email,
            tx_type="WITHDRAWAL",
            amount=req.amount,
            balance_after=result["current_balance"],
            tx_id=tx_data["tx_id"],
            description=tx_data["description"]
        )

        # If Sliding Window algorithm flagged fraud, send high-priority security alert
        if fraud_eval["is_flagged"]:
            background_tasks.add_task(
                smtp_service.send_security_alert_email,
                account_name=acc.account_name,
                account_number=acc.account_number,
                email=acc.email,
                window_sum=fraud_eval["window_sum"],
                threshold=fraud_eval["threshold"],
                window_size=fraud_eval["window_size"],
                reason=fraud_eval["reason"]
            )

        return {
            "message": "Withdrawal successful.",
            "transaction": tx_data,
            "fraud_evaluation": fraud_eval,
            "new_balance": result["current_balance"],
            "account_status": acc.status
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/api/transactions/{acc_num}", tags=["Transactions"])
async def get_transaction_history(acc_num: str, limit: Optional[int] = Query(50, ge=1, le=500)):
    """
    GET /api/transactions/{acc_num}:
    Traverses the custom Singly Linked List ledger from head downwards.
    """
    acc = bank_db.get_account_by_number(acc_num)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account #{acc_num} does not exist."
        )

    transactions = acc.transaction_ledger.get_recent(limit)
    return {
        "account_number": acc_num,
        "total_records": len(acc.transaction_ledger),
        "returned_count": len(transactions),
        "data_structure": "Custom Singly Linked List (O(1) Prepend)",
        "transactions": transactions
    }


@app.get("/api/fraud-alerts/{acc_num}", tags=["Fraud Detection"])
async def get_fraud_status(acc_num: str):
    """
    GET /api/fraud-alerts/{acc_num}:
    Returns sliding window metrics, recent amounts within window, and risk status.
    """
    acc = bank_db.get_account_by_number(acc_num)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account #{acc_num} does not exist."
        )

    metrics = acc.fraud_detector.get_current_metrics()
    return {
        "account_number": acc_num,
        "status": acc.status,
        "algorithm": "Sliding Window K-Operation Volume Aggregator",
        "metrics": metrics,
        "last_evaluation": acc.fraud_detector.last_evaluation.to_dict() if acc.fraud_detector.last_evaluation else None,
        "alert_history": acc.fraud_detector.alert_history
    }


@app.post("/api/fraud-alerts/{acc_num}/resolve", tags=["Fraud Detection"])
async def resolve_fraud_status(acc_num: str):
    """
    POST /api/fraud-alerts/{acc_num}/resolve:
    Resolves active security alert and clears the fraud flag.
    """
    acc = bank_db.get_account_by_number(acc_num)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account #{acc_num} does not exist."
        )

    acc.resolve_fraud()
    return {
        "message": f"Fraud flag cleared and account #{acc_num} restored to ACTIVE status.",
        "account_status": acc.status
    }


@app.get("/api/system/tree", tags=["DSA Visualizer"])
async def get_bst_tree():
    """
    GET /api/system/tree:
    Returns the full hierarchical Binary Search Tree structure for visualization.
    """
    tree_data = bank_db.get_tree_visualization()
    return {
        "data_structure": "Binary Search Tree (BST)",
        "total_nodes": len(bank_db.bst_index),
        "tree": tree_data
    }


@app.get("/api/dsa/bst/search", tags=["DSA Visualizer"])
async def search_bst_endpoint(account_number: str = Query(..., min_length=1)):
    """
    GET /api/dsa/bst/search:
    Executes an O(log N) search on the Account Binary Search Tree.
    """
    node_data = bank_db.search_bst(account_number)
    if not node_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account #{account_number} not found in BST index."
        )
    return {
        "found": True,
        "algorithm": "Binary Search Tree O(log N) Search",
        "account": node_data
    }


@app.get("/api/emails", tags=["SMTP Emails"])
async def get_email_logs(limit: int = Query(30, ge=1, le=100)):
    """
    GET /api/emails:
    Fetches the live stream audit log of dispatched HTML/Plaintext emails.
    """
    return {
        "total_dispatched": len(smtp_service.email_history),
        "emails": smtp_service.get_email_logs(limit)
    }


@app.post("/api/settings/fraud", tags=["Settings"])
async def update_fraud_settings(req: FraudThresholdUpdateRequest):
    """Dynamically updates sliding window parameter K and threshold for all accounts."""
    if req.k_window:
        settings.DEFAULT_SLIDING_WINDOW_K = req.k_window
    if req.fraud_threshold:
        settings.DEFAULT_FRAUD_THRESHOLD = req.fraud_threshold

    for acc in bank_db.accounts_hash_map.values():
        acc.fraud_detector.update_parameters(req.k_window, req.fraud_threshold)

    return {
        "message": "Fraud detection parameters updated successfully across all accounts.",
        "k_window": settings.DEFAULT_SLIDING_WINDOW_K,
        "fraud_threshold": settings.DEFAULT_FRAUD_THRESHOLD
    }


# ==============================================================================
# STATIC FRONTEND MOUNTING & SPA ROUTING
# ==============================================================================

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/", tags=["UI"])
    async def serve_index():
        """Serves the main Frontend single page dashboard."""
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
