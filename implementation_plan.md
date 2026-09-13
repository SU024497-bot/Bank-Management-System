# Implementation Plan: Production-Ready Bank Management System with DSA Engine & SMTP Notifications

Build a modern, full-stack Bank Management System web application featuring an algorithmic core (Linked List Ledger, Sliding Window Fraud Detector, Binary Search Tree, Hash Map indexing), a FastAPI backend with asynchronous SMTP email dispatching & mock logger fallback, and a dashboard UI styled with a custom Purple-Indigo design system.

---

## 1. System Architecture & Color System

### Frontend UI/UX Design Palette
- **Primary Accent / Brand Buttons / Header**: `#6366F1` (Indigo)
- **Secondary Accent / Badges / Hover States**: `#8B5CF6` (Purple)
- **Main Page Background**: `#F3F4F6` (Soft Neutral Gray)
- **Cards & Containers**: `#FFFFFF` (Clean White with elevated drop shadows & glassmorphic highlights)
- **Typography & Dark Headers**: `#1E293B` (Dark Slate)
- **Fraud Alert Banner & Critical Warning**: `#EF4444` (Crimson Red with pulsing glow)
- **Success / Positive Indicators**: `#10B981` (Emerald Green)
- **Warning / Moderate Risk**: `#F59E0B` (Amber)

```
+---------------------------------------------------------------------------------------+
|  FRONTEND DASHBOARD (Single Page Application - Vanilla JS + CSS3 + HTML5)            |
|  - Top Bar: System Status, Active Account Picker, New Account CTA, Live Email Modal    |
|  - Dynamic Fraud Alert Banner (#EF4444) with real-time sliding window velocity gauge  |
|  - Account Overview Card (Balance in #6366F1, Account Tier, Quick Stats, Card Visual) |
|  - Quick Operations Panel (Deposit & Withdraw with instant balance update & remarks)  |
|  - Interactive Transaction Ledger (O(1) Head Prepend visualizer, Search, Filters)    |
|  - BST Account Hierarchy Visualizer (Interactive Tree diagram & sorted account list) |
|  - SMTP Real-time Email Dispatcher Logs (Drawer & Toast notifications)                |
+---------------------------------------------------------------------------------------+
                                        |  REST API (JSON)
                                        v
+---------------------------------------------------------------------------------------+
|  BACKEND ENGINE (FastAPI - Python 3.11)                                               |
|  1. HASH MAP INDEX: O(1) Instant account lookup and validation                        |
|  2. LINKED LIST LEDGER: O(1) prepend transaction history per account                  |
|  3. SLIDING WINDOW ENGINE: Real-time K-transaction velocity fraud detection threshold |
|  4. BINARY SEARCH TREE (BST): Sorted account hierarchy, tree search, range queries    |
|  5. SMTP NOTIFICATION SERVICE: Asynchronous email delivery with mock console fallback |
+---------------------------------------------------------------------------------------+
```

---

## 2. Proposed Changes & Component Breakdown

### Backend DSA Algorithmic Core (`backend/dsa/`)

#### [NEW] [linked_list.py](file:///d:/BANK%20MANAGEMENT%20SYSTEM/backend/dsa/linked_list.py)
- **Transaction Node**: Holds `tx_id`, `timestamp`, `tx_type` (DEPOSIT/WITHDRAW), `amount`, `balance_after`, `description`, `status`, and `next` pointer.
- **TransactionLinkedList**:
  - `prepend(tx_data)`: Adds a new transaction at the head in $O(1)$ time complexity.
  - `get_recent(limit)`: Retrieves recent transactions in $O(K)$ time for rendering or analysis.
  - `to_list()`: Iterates through the singly-linked list to return an ordered array of transactions.
  - `__len__()`: Tracks ledger length in $O(1)$ time via internal counter.

#### [NEW] [sliding_window.py](file:///d:/BANK%20MANAGEMENT%20SYSTEM/backend/dsa/sliding_window.py)
- **SlidingWindowFraudDetector**:
  - Fixed-size or time-bounded sliding window maintaining the last $K$ transactions (default $K=3$).
  - Evaluates cumulative transaction sum within the window against threshold (e.g. ₹50,000).
  - Calculates velocity metrics: total window volume, average transaction size, time delta between operations.
  - Returns `FraudEvaluationResult(is_flagged: bool, window_sum: float, threshold: float, risk_score: int, reason: str)`.

#### [NEW] [bst.py](file:///d:/BANK%20MANAGEMENT%20SYSTEM/backend/dsa/bst.py)
- **AccountBSTNode**: Contains `account_number`, `account_name`, `balance`, `left`, `right`.
- **AccountBST**:
  - `insert(account)`: Inserts account maintaining BST invariant by account number in $O(\log N)$ average time.
  - `search(account_number)`: Traverses tree in $O(\log N)$ time.
  - `inorder_traversal()`: Returns sorted account list by account number.
  - `get_tree_structure()`: Exports nested hierarchical tree JSON representation for frontend visual tree rendering.

#### [NEW] [account_store.py](file:///d:/BANK%20MANAGEMENT%20SYSTEM/backend/dsa/account_store.py)
- **BankDatabase**:
  - In-memory Hash Map / Dictionary (`dict[str, BankAccount]`) for instant $O(1)$ primary key lookups.
  - Integrated with `AccountBST` for tree operations and `TransactionLinkedList` per account.
  - Pre-seeded with realistic demo accounts for instant testing out-of-the-box.

---

### Backend SMTP Email Module (`backend/services/`)

#### [NEW] [smtp_service.py](file:///d:/BANK%20MANAGEMENT%20SYSTEM/backend/services/smtp_service.py)
- Supports dual mode:
  1. **Real SMTP Dispatcher**: Connects to SMTP server (e.g., Gmail, SendGrid, Mailgun) using credentials from `.env` or configuration.
  2. **Mock SMTP Fallback & Live Event Logger**: Emits formatted console output and persists in an in-memory event bus/queue for frontend live visualization.
- Email Templates (Rich HTML + Plaintext):
  - `send_welcome_email(account)`: Welcome letter with account details, safety guidelines.
  - `send_transaction_email(account, tx_details)`: Credit/Debit instant transaction receipt.
  - `send_security_alert_email(account, fraud_details)`: High-priority security warning with flagged window sum and instructions.

---

### Backend REST API (`backend/`)

#### [NEW] [main.py](file:///d:/BANK%20MANAGEMENT%20SYSTEM/backend/main.py)
- REST Endpoints:
  - `POST /api/accounts`: Create new account -> Insert into Hash Map & BST -> Send Welcome Email.
  - `GET /api/accounts`: List all accounts (BST in-order).
  - `GET /api/accounts/{acc_num}`: Get single account details ($O(1)$ Hash Map lookup).
  - `POST /api/deposit`: Deposit money -> Prepend to Linked List ($O(1)$) -> Run Sliding Window -> Send Credit/Alert Email.
  - `POST /api/withdraw`: Withdraw money -> Validate balance -> Prepend to Linked List ($O(1)$) -> Run Sliding Window -> Send Debit/Alert Email.
  - `GET /api/transactions/{acc_num}`: Retrieve Linked List ledger.
  - `GET /api/fraud-alerts/{acc_num}`: Get current fraud risk status and sliding window metrics.
  - `POST /api/fraud-alerts/{acc_num}/resolve`: Clear fraud flag upon verification.
  - `GET /api/system/tree`: BST structure for frontend tree rendering.
  - `GET /api/emails`: Audit log of sent emails.
  - `POST /api/settings/smtp`: Configure live SMTP settings dynamically.
- Serves static frontend files and OpenAPI docs (`/docs`).

#### [NEW] [config.py](file:///d:/BANK%20MANAGEMENT%20SYSTEM/backend/config.py)
- Application configuration, default fraud detection parameters ($K=3$, limit ₹50,000), SMTP settings.

---

### Frontend UI/UX (`frontend/`)

#### [NEW] [index.html](file:///d:/BANK%20MANAGEMENT%20SYSTEM/frontend/index.html)
- Semantic HTML5 structure with modern responsive layout:
  - Header: Logo, Live System Status pill, Active Account selector dropdown, "Open New Account" button, "Email Stream" toggle button.
  - Critical Fraud Alert Banner (`#EF4444`) with animated icon and "Verify & Resolve" button.
  - Main Dashboard Grid:
    - Left Column:
      - Account Overview Card with Indigo `#6366F1` balance banner, account details, copyable account number, account risk badge.
      - Deposit & Withdrawal Panel with segmented tab toggle, preset quick buttons (₹1,000, ₹5,000, ₹10,000, ₹25,000, ₹50,000), remarks field, and instant balance preview.
      - Sliding Window Fraud Monitor Card showing real-time window fill (e.g. 2/3 transactions), cumulative sum vs ₹50,000 threshold bar, and risk radar.
    - Right Column:
      - Interactive Transaction Ledger Table with live updates, type badges (Credit in `#10B981`, Debit in `#8B5CF6`), transaction timestamps, and expandable details.
      - DSA Engine Visualizer Tab:
        - **Linked List View**: Visual representation of nodes with head pointer and `O(1)` prepend visual cue.
        - **BST Visualizer**: Interactive hierarchical account tree with node highlighting on search.
  - Modals:
    - "Open Account" Modal with form validation.
    - "Email Logs / Dispatcher" Drawer showing sent HTML email receipts with search and copy functionality.
    - "Settings & Fraud Thresholds" Modal to customize window size $K$ and monetary limits.

#### [NEW] [style.css](file:///d:/BANK%20MANAGEMENT%20SYSTEM/frontend/style.css)
- Custom CSS utilizing Google Font ('Plus Jakarta Sans' & 'JetBrains Mono').
- Custom theme variables:
  - `--primary: #6366F1`
  - `--secondary: #8B5CF6`
  - `--bg-main: #F3F4F6`
  - `--card-bg: #FFFFFF`
  - `--text-dark: #1E293B`
  - `--danger: #EF4444`
  - Glassmorphic card styling, smooth micro-interactions, ripple effects, pulsing danger states, and crisp typography.

#### [NEW] [app.js](file:///d:/BANK%20MANAGEMENT%20SYSTEM/frontend/app.js)
- Modular frontend controller:
  - Account state management & auto-refresh.
  - Real-time API integration with error handling and optimistic UI updates.
  - Interactive Linked List and BST renderer (SVG / DOM nodes).
  - Toast notification system for transactions and security events.
  - Real-time email log polling and preview modal.

---

## 3. Verification Plan

### Automated Backend Tests
- Create [test_dsa.py](file:///d:/BANK%20MANAGEMENT%20SYSTEM/tests/test_dsa.py) to test:
  1. `TransactionLinkedList`: Verify $O(1)$ prepend, head update, length tracking, and order preservation.
  2. `SlidingWindowFraudDetector`: Test normal transactions, boundary conditions, and fraud trigger when window sum exceeds ₹50,000.
  3. `AccountBST`: Verify binary search tree insertion, search, and in-order sorted traversal.
  4. `FastAPI Endpoints`: Test `/api/accounts`, `/api/deposit`, `/api/withdraw`, `/api/transactions`, `/api/fraud-alerts` with `TestClient`.

### Manual & Interactive Browser Verification
- Start the backend server on `http://127.0.0.1:8000`.
- Use browser subagent to interactively verify:
  1. Loading dashboard and inspecting initial seeded accounts.
  2. Creating a new account with custom initial deposit and verifying welcome email generation.
  3. Performing a normal deposit and withdrawal, verifying real-time balance update and transaction ledger prepend.
  4. Performing rapid high-value transactions (e.g., ₹20,000 + ₹20,000 + ₹15,000) to trigger the Sliding Window fraud detection.
  5. Verifying the `#EF4444` Fraud Alert banner lights up with siren/pulsing indicator and security email is dispatched.
  6. Testing the BST and Linked List visualizer tabs.
  7. Opening Email Dispatcher drawer and inspecting formatted HTML emails.
