# 🏛️ Apex National Bank — Enterprise Core Banking Portal

A full-stack, production-grade enterprise bank management system featuring a **Classic Corporate Banking** interface, a **FastAPI** backend engine, real-time **SMTP notification stream**, and **Core DSA Algorithmic logic** (Singly Linked List ledger, Sliding Window velocity fraud detection, Binary Search Tree hierarchy, and Hash Map indexing).

---

## 🎨 Design System & Color Palette (Classic Corporate Banking)
- **Primary Brand / Header / Active States**: `#0F172A` (Deep Navy Blue)
- **Institutional Accent**: `#1E3A8A` / `#2563EB` (Royal Corporate Blue)
- **Secondary Surfaces / Cards**: `#FFFFFF` (Crisp White with 1px `#E2E8F0` borders)
- **Page Background**: `#F1F5F9` (Enterprise Cool Grey)
- **Typography**: `Inter` / `Segoe UI` (Sans-serif) & `JetBrains Mono` (Monospace Financials)
- **Success / Credit**: `#16A34A` (Standard Banking Green)
- **Warning**: `#D97706` (Professional Amber)
- **Critical Risk Alert**: `#DC2626` (Crimson Red)

---

## 🧠 Core DSA Algorithmic Engine

### 1. Singly Linked List (`backend/dsa/linked_list.py`)
- **Use Case**: Chronological Financial Transaction Ledger.
- **Complexity**: $O(1)$ constant-time prepending at the `head`.
- **Properties**: Every transaction node links to the preceding transaction (`node.next`), enabling instantaneous record insertion without array-shifting overhead.

### 2. Sliding Window Algorithm (`backend/dsa/sliding_window.py`)
- **Use Case**: Real-Time Anomaly & Velocity Fraud Detection.
- **Complexity**: $O(1)$ amortized maintenance over rolling queue buffer.
- **Logic**: Inspects cumulative volume across the last $K$ operations (default $K=3$).
- **Trigger**: If the transaction sum in the sliding window breaches the threshold (default ₹50,000.00), the account is immediately flagged as `CRITICAL_FRAUD`, lights up the security banner, and dispatches a high-priority security statement email.

### 3. Binary Search Tree (BST) (`backend/dsa/bst.py`)
- **Use Case**: Account Hierarchy, Logarithmic Search, and In-Order Sorted Reporting.
- **Complexity**: $O(\log N)$ average search and insertion, $O(N)$ In-Order traversal.
- **Visualization**: Interactive nested tree hierarchy rendered dynamically with search node highlighting.

### 4. Hash Map Indexing (`backend/dsa/account_store.py`)
- **Use Case**: Instantaneous $O(1)$ account lookup and primary key authentication.

---

## 📧 Real-Time SMTP Email Engine (`backend/services/smtp_service.py`)
- **Welcome Statements**: Sent automatically upon account creation.
- **Transaction Receipts**: Sent for every Credit/Debit operation with clean enterprise HTML styling.
- **Security Alert Notices**: High-priority alert dispatched when Sliding Window flags fraud.
- **Dual Mode**: Supports real SMTP servers (Gmail, SendGrid, etc.) and a non-blocking in-memory audit log stream.

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
py -3.11 -m pip install -r requirements.txt
```

### 2. Start Application Server
```bash
py -3.11 run.py
```
- Localhost URL: **`http://localhost:8000`**
- Local IP URL:  **`http://127.0.0.1:8000`**
- OpenAPI Docs:  **`http://localhost:8000/docs`** (or `http://127.0.0.1:8000/docs`)

### 3. Run Automated Test Suite
```bash
py -3.11 -m pytest tests/ -v
```

---

## 📡 REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/system/status` | System health, AUM deposits, account count, and DSA engine stats |
| `POST` | `/api/accounts` | Create new bank account ($O(1)$ Hash Map + $O(\log N)$ BST) |
| `GET` | `/api/accounts` | List all accounts (BST in-order sorted traversal) |
| `GET` | `/api/accounts/{acc_num}` | Get account details ($O(1)$ Hash Map lookup) |
| `POST` | `/api/deposit` | Deposit funds, prepend to Linked List ($O(1)$), run Sliding Window |
| `POST` | `/api/withdraw` | Withdraw funds, validate balance, prepend to Linked List ($O(1)$) |
| `GET` | `/api/transactions/{acc_num}` | Retrieve Linked List transaction ledger |
| `GET` | `/api/fraud-alerts/{acc_num}` | Get account risk status & sliding window metrics |
| `POST` | `/api/fraud-alerts/{acc_num}/resolve` | Resolve/clear active fraud alert |
| `GET` | `/api/system/tree` | Hierarchical BST structure for interactive visualizer |
| `GET` | `/api/dsa/bst/search` | Direct logarithmic $O(\log N)$ search on BST index |
| `GET` | `/api/emails` | Outbound email audit stream |
| `POST` | `/api/settings/fraud` | Adjust Sliding Window size $K$ and volume threshold |
