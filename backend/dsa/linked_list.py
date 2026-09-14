"""
================================================================================
CORE DSA MODULE: TRANSACTION HISTORY LEDGER (LINKED LIST)
================================================================================
Concept:
    A custom Singly Linked List data structure specifically designed for
    financial transaction ledgers.
    
Time Complexity:
    - Prepend (Insert new transaction at head): O(1) constant time
    - Retrieve top K recent transactions: O(K) time
    - Full ledger traversal: O(N) linear time
    - Ledger length check: O(1) via internal size counter
    
Space Complexity:
    - O(N) where N is the total number of recorded transactions.
================================================================================
"""

from datetime import datetime
from typing import Optional, List, Dict, Any


class TransactionNode:
    """
    Represents an individual node in the Transaction Linked List.
    Each node encapsulates the financial record and a pointer to the previous transaction.
    """
    def __init__(
        self,
        tx_id: str,
        tx_type: str,          # "DEPOSIT", "WITHDRAWAL", "INITIAL_DEPOSIT"
        amount: float,
        balance_after: float,
        description: str = "",
        timestamp: Optional[str] = None,
        status: str = "COMPLETED",  # "COMPLETED", "FLAGGED", "FAILED"
        is_fraud_flagged: bool = False
    ):
        self.tx_id: str = tx_id
        self.tx_type: str = tx_type.upper()
        self.amount: float = float(amount)
        self.balance_after: float = float(balance_after)
        self.description: str = description or f"{self.tx_type.capitalize()} of ₹{amount:,.2f}"
        self.timestamp: str = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status: str = status
        self.is_fraud_flagged: bool = is_fraud_flagged
        
        # Pointer to next node in the linked chain (representing the preceding transaction)
        self.next: Optional["TransactionNode"] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize node data to a clean dictionary format."""
        return {
            "tx_id": self.tx_id,
            "tx_type": self.tx_type,
            "amount": self.amount,
            "balance_after": self.balance_after,
            "description": self.description,
            "timestamp": self.timestamp,
            "status": self.status,
            "is_fraud_flagged": self.is_fraud_flagged,
        }


class TransactionLinkedList:
    """
    Singly Linked List maintaining an chronological transaction ledger.
    New transactions are always PREPENDED at the HEAD in O(1) time complexity,
    ensuring the most recent transactions are accessed immediately without
    array shifting overhead.
    """
    def __init__(self):
        self.head: Optional[TransactionNode] = None
        self._size: int = 0

    def prepend(
        self,
        tx_id: str,
        tx_type: str,
        amount: float,
        balance_after: float,
        description: str = "",
        status: str = "COMPLETED",
        is_fraud_flagged: bool = False,
        timestamp: Optional[str] = None
    ) -> TransactionNode:
        """
        DSA OPERATION: O(1) Prepend
        Inserts a new transaction node at the head of the linked list.
        """
        new_node = TransactionNode(
            tx_id=tx_id,
            tx_type=tx_type,
            amount=amount,
            balance_after=balance_after,
            description=description,
            timestamp=timestamp,
            status=status,
            is_fraud_flagged=is_fraud_flagged
        )
        
        # New node points to current head
        new_node.next = self.head
        
        # Head pointer moves to the new node
        self.head = new_node
        self._size += 1
        
        return new_node

    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Traverses the linked list from head downwards to fetch the top K recent transactions.
        Time Complexity: O(min(limit, N))
        """
        results: List[Dict[str, Any]] = []
        current = self.head
        count = 0
        
        while current and count < limit:
            results.append(current.to_dict())
            current = current.next
            count += 1
            
        return results

    def to_list(self) -> List[Dict[str, Any]]:
        """
        Full traversal: converts the entire linked list to a list of dicts.
        Time Complexity: O(N)
        """
        results: List[Dict[str, Any]] = []
        current = self.head
        while current:
            results.append(current.to_dict())
            current = current.next
        return results

    def find_by_id(self, tx_id: str) -> Optional[TransactionNode]:
        """
        Linear search across the linked list to find a transaction by its unique ID.
        Time Complexity: O(N)
        """
        current = self.head
        while current:
            if current.tx_id == tx_id:
                return current
            current = current.next
        return None

    def get_sliding_window_amounts(self, k: int = 3) -> List[float]:
        """
        Extracts the amounts of the last K transactions from the head for algorithmic analysis.
        Time Complexity: O(K)
        """
        amounts: List[float] = []
        current = self.head
        count = 0
        while current and count < k:
            amounts.append(current.amount)
            current = current.next
            count += 1
        return amounts

    def __len__(self) -> int:
        """Returns the number of transactions recorded in O(1) time."""
        return self._size

    def is_empty(self) -> bool:
        """Returns True if the transaction ledger has no entries."""
        return self.head is None
