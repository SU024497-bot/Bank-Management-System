"""
================================================================================
CORE DSA INTEGRATION: BANK ACCOUNT MODEL & IN-MEMORY DATABASE STORE
================================================================================
Combines:
    1. HASH MAP (dict): O(1) Instant Primary Key Lookup & Authentication
    2. LINKED LIST: O(1) Head Prepend Chronological Transaction Ledger
    3. SLIDING WINDOW: Real-time K-operation Velocity Fraud Detection Engine
    4. BINARY SEARCH TREE (BST): Logarithmic Search & Sorted Account Hierarchy
================================================================================
"""

from datetime import datetime
import uuid
from typing import Dict, List, Optional, Any

from .linked_list import TransactionLinkedList, TransactionNode
from .sliding_window import SlidingWindowFraudDetector, FraudEvaluationResult
from .bst import AccountBST


class BankAccount:
    """
    Represents an individual bank account combining multiple DSA structures.
    """
    def __init__(
        self,
        account_number: str,
        account_name: str,
        email: str,
        initial_deposit: float = 0.0,
        phone: str = "+91 98765 43210",
        account_type: str = "SAVINGS",
        created_at: Optional[str] = None,
        k_window: int = 3,
        fraud_threshold: float = 50000.0
    ):
        self.account_number: str = str(account_number).strip()
        self.account_name: str = account_name.strip()
        self.email: str = email.strip()
        self.phone: str = phone
        self.account_type: str = account_type.upper()
        self.balance: float = round(float(initial_deposit), 2)
        self.created_at: str = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status: str = "ACTIVE"  # "ACTIVE", "FLAGGED", "LOCKED"
        
        # 1. CORE DSA: Custom Linked List for Transaction Ledger
        self.transaction_ledger: TransactionLinkedList = TransactionLinkedList()
        
        # 2. CORE DSA: Sliding Window Engine for Real-Time Fraud Detection
        self.fraud_detector: SlidingWindowFraudDetector = SlidingWindowFraudDetector(
            k_window=k_window,
            volume_threshold=fraud_threshold
        )
        
        # Record initial deposit if present
        if initial_deposit > 0:
            tx_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
            self.transaction_ledger.prepend(
                tx_id=tx_id,
                tx_type="INITIAL_DEPOSIT",
                amount=initial_deposit,
                balance_after=self.balance,
                description="Account Opening Initial Deposit",
                timestamp=self.created_at
            )

    def deposit(self, amount: float, description: str = "") -> Dict[str, Any]:
        """
        Executes deposit:
        1. Updates balance
        2. Prepends to Linked List in O(1)
        3. Evaluates Sliding Window fraud detection
        """
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Deposit amount must be strictly positive.")
            
        self.balance = round(self.balance + amount, 2)
        tx_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        
        # DSA: Sliding Window Fraud Evaluation
        fraud_eval: FraudEvaluationResult = self.fraud_detector.evaluate_new_transaction(amount, "DEPOSIT")
        
        if fraud_eval.is_flagged:
            self.status = "FLAGGED"
            tx_status = "FLAGGED"
        else:
            tx_status = "COMPLETED"
            
        # DSA: O(1) Prepend to Linked List Ledger
        node: TransactionNode = self.transaction_ledger.prepend(
            tx_id=tx_id,
            tx_type="DEPOSIT",
            amount=amount,
            balance_after=self.balance,
            description=description or f"Funds deposited into account",
            status=tx_status,
            is_fraud_flagged=fraud_eval.is_flagged
        )
        
        return {
            "transaction": node.to_dict(),
            "fraud_evaluation": fraud_eval.to_dict(),
            "current_balance": self.balance
        }

    def withdraw(self, amount: float, description: str = "") -> Dict[str, Any]:
        """
        Executes withdrawal:
        1. Validates sufficient balance
        2. Deducts balance
        3. Prepends to Linked List in O(1)
        4. Evaluates Sliding Window fraud detection
        """
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Withdrawal amount must be strictly positive.")
        if amount > self.balance:
            raise ValueError(f"Insufficient balance. Current balance is ₹{self.balance:,.2f}.")

        self.balance = round(self.balance - amount, 2)
        tx_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        
        # DSA: Sliding Window Fraud Evaluation
        fraud_eval: FraudEvaluationResult = self.fraud_detector.evaluate_new_transaction(amount, "WITHDRAWAL")
        
        if fraud_eval.is_flagged:
            self.status = "FLAGGED"
            tx_status = "FLAGGED"
        else:
            tx_status = "COMPLETED"
            
        # DSA: O(1) Prepend to Linked List Ledger
        node: TransactionNode = self.transaction_ledger.prepend(
            tx_id=tx_id,
            tx_type="WITHDRAWAL",
            amount=amount,
            balance_after=self.balance,
            description=description or f"Funds withdrawn from account",
            status=tx_status,
            is_fraud_flagged=fraud_eval.is_flagged
        )
        
        return {
            "transaction": node.to_dict(),
            "fraud_evaluation": fraud_eval.to_dict(),
            "current_balance": self.balance
        }

    def resolve_fraud(self) -> None:
        """Clears fraud risk status."""
        self.fraud_detector.resolve_fraud_flag()
        self.status = "ACTIVE"

    def to_dict(self, include_recent_tx: bool = True) -> Dict[str, Any]:
        """Convert account state to dictionary."""
        fraud_metrics = self.fraud_detector.get_current_metrics()
        return {
            "account_number": self.account_number,
            "account_name": self.account_name,
            "email": self.email,
            "phone": self.phone,
            "account_type": self.account_type,
            "balance": self.balance,
            "status": self.status,
            "created_at": self.created_at,
            "total_transactions": len(self.transaction_ledger),
            "fraud_metrics": fraud_metrics,
            "recent_transactions": self.transaction_ledger.get_recent(10) if include_recent_tx else []
        }


class BankDatabaseStore:
    """
    Central database repository that coordinates:
    - O(1) Hash Map indexing by account_number
    - Logarithmic BST structure for hierarchy and ordered search
    """
    def __init__(self):
        # 1. DSA Hash Map for O(1) instant account lookups
        self.accounts_hash_map: Dict[str, BankAccount] = {}
        
        # 2. DSA Binary Search Tree for sorted account hierarchy
        self.bst_index: AccountBST = AccountBST()
        
        # Pre-seed with demo accounts
        self._seed_demo_accounts()

    def create_account(
        self,
        account_name: str,
        email: str,
        account_number: Optional[str] = None,
        initial_deposit: float = 0.0,
        phone: str = "+91 98765 43210",
        account_type: str = "SAVINGS",
        k_window: int = 3,
        fraud_threshold: float = 50000.0
    ) -> BankAccount:
        """
        Creates new account and indexes into both Hash Map O(1) and BST O(log N).
        """
        if not account_number:
            # Generate deterministic 8-digit unique account number
            base_num = 10001000 + len(self.accounts_hash_map) + 1
            account_number = str(base_num)
        else:
            account_number = str(account_number).strip()

        if account_number in self.accounts_hash_map:
            raise ValueError(f"Account number {account_number} already exists.")

        account = BankAccount(
            account_number=account_number,
            account_name=account_name,
            email=email,
            initial_deposit=initial_deposit,
            phone=phone,
            account_type=account_type,
            k_window=k_window,
            fraud_threshold=fraud_threshold
        )
        
        # Index in Hash Map O(1)
        self.accounts_hash_map[account_number] = account
        
        # Index in BST O(log N)
        self.bst_index.insert(
            account_number=account.account_number,
            account_name=account.account_name,
            email=account.email,
            balance=account.balance,
            created_at=account.created_at
        )
        
        return account

    def get_account_by_number(self, account_number: str) -> Optional[BankAccount]:
        """
        DSA HASH MAP LOOKUP: Instant O(1) retrieval by primary key.
        """
        return self.accounts_hash_map.get(str(account_number).strip())

    def search_bst(self, account_number: str) -> Optional[Dict[str, Any]]:
        """
        DSA BST SEARCH: O(log N) lookup in the Binary Search Tree.
        """
        node = self.bst_index.search(str(account_number).strip())
        return node.to_dict() if node else None

    def list_all_accounts(self) -> List[Dict[str, Any]]:
        """
        Returns all accounts sorted by account number via BST In-Order Traversal.
        """
        sorted_nodes = self.bst_index.inorder_traversal()
        # Merge with full account state from Hash Map
        return [
            self.accounts_hash_map[node["account_number"]].to_dict(include_recent_tx=False)
            for node in sorted_nodes
            if node["account_number"] in self.accounts_hash_map
        ]

    def get_tree_visualization(self) -> Optional[Dict[str, Any]]:
        """Returns JSON tree structure for frontend visualizer."""
        return self.bst_index.get_tree_structure()

    def sync_bst_balance(self, account_number: str) -> None:
        """Synchronizes balance updates into BST node."""
        acc = self.get_account_by_number(account_number)
        if acc:
            self.bst_index.update_balance(account_number, acc.balance)

    def _seed_demo_accounts(self) -> None:
        """Seeds realistic bank accounts for out-of-the-box demonstration."""
        seed_data = [
            ("Vikram Sharma", "vikram.sharma@example.com", "10001001", 75000.0, "SAVINGS"),
            ("Priya Patel", "priya.patel@example.com", "10001002", 42500.0, "SAVINGS"),
            ("Aditya Verma", "aditya.verma@example.com", "10001003", 115000.0, "CURRENT"),
            ("Ananya Rao", "ananya.rao@example.com", "10001004", 28000.0, "SAVINGS"),
            ("Rajesh Malhotra", "rajesh.m@example.com", "10001005", 95000.0, "SALARY")
        ]
        
        for name, email, acc_num, balance, acc_type in seed_data:
            acc = self.create_account(
                account_name=name,
                email=email,
                account_number=acc_num,
                initial_deposit=balance,
                account_type=acc_type
            )
            # Add a couple of realistic transaction history entries
            if acc_num == "10001001":
                acc.deposit(5000.0, "Client Consultancy Fee")
                acc.withdraw(2500.0, "Office Supplies & Software")
                self.sync_bst_balance(acc_num)
            elif acc_num == "10001003":
                acc.deposit(15000.0, "Invoice #4092 Settlement")
                self.sync_bst_balance(acc_num)
