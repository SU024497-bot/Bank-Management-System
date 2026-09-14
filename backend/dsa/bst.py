"""
================================================================================
CORE DSA MODULE: BINARY SEARCH TREE (BST) ACCOUNT INDEX & HIERARCHY
================================================================================
Concept:
    A Binary Search Tree (BST) data structure used to maintain an ordered
    hierarchy of bank accounts based on Account Number (key).
    
Algorithmic Properties:
    - Invariant: For every node N, all keys in left subtree < N.key,
                 all keys in right subtree > N.key.
    - Average Time Complexity:
        * Search: O(log N)
        * Insert: O(log N)
        * In-Order Traversal: O(N) -> yields perfectly sorted account roster
    - Worst-case Time: O(N) (unbalanced)
    - Space Complexity: O(N) for tree nodes.
================================================================================
"""

from typing import Optional, List, Dict, Any


class BSTNode:
    """Represents a node in the Account Binary Search Tree."""
    def __init__(self, account_number: str, account_name: str, email: str, balance: float, created_at: str):
        self.account_number: str = account_number
        self.account_name: str = account_name
        self.email: str = email
        self.balance: float = float(balance)
        self.created_at: str = created_at
        
        # Pointers to subtrees
        self.left: Optional["BSTNode"] = None
        self.right: Optional["BSTNode"] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "account_number": self.account_number,
            "account_name": self.account_name,
            "email": self.email,
            "balance": self.balance,
            "created_at": self.created_at,
        }


class AccountBST:
    """
    Binary Search Tree maintaining accounts sorted by Account Number.
    Enables logarithmic search, sorted sequential reporting, and hierarchical visualization.
    """
    def __init__(self):
        self.root: Optional[BSTNode] = None
        self._size: int = 0

    def insert(
        self,
        account_number: str,
        account_name: str,
        email: str,
        balance: float,
        created_at: str
    ) -> BSTNode:
        """
        DSA INSERTION: Inserts an account into the BST maintaining ordering invariant.
        Time Complexity: O(log N) average, O(N) worst case.
        """
        new_node = BSTNode(
            account_number=account_number,
            account_name=account_name,
            email=email,
            balance=balance,
            created_at=created_at
        )
        
        if self.root is None:
            self.root = new_node
            self._size += 1
            return new_node
            
        current = self.root
        while True:
            if account_number < current.account_number:
                if current.left is None:
                    current.left = new_node
                    self._size += 1
                    return new_node
                current = current.left
            elif account_number > current.account_number:
                if current.right is None:
                    current.right = new_node
                    self._size += 1
                    return new_node
                current = current.right
            else:
                # Key already exists: update existing node values
                current.account_name = account_name
                current.email = email
                current.balance = balance
                return current

    def search(self, account_number: str) -> Optional[BSTNode]:
        """
        DSA SEARCH: Traverses tree by comparing search key with node keys.
        Time Complexity: O(log N) average.
        """
        current = self.root
        while current:
            if account_number == current.account_number:
                return current
            elif account_number < current.account_number:
                current = current.left
            else:
                current = current.right
        return None

    def update_balance(self, account_number: str, new_balance: float) -> bool:
        """Finds node and updates its balance in O(log N) time."""
        node = self.search(account_number)
        if node:
            node.balance = round(float(new_balance), 2)
            return True
        return False

    def inorder_traversal(self) -> List[Dict[str, Any]]:
        """
        DSA IN-ORDER TRAVERSAL (Left -> Root -> Right):
        Produces accounts sorted in ascending order by Account Number.
        Time Complexity: O(N)
        """
        result: List[Dict[str, Any]] = []
        
        def _inorder(node: Optional[BSTNode]):
            if not node:
                return
            _inorder(node.left)
            result.append(node.to_dict())
            _inorder(node.right)

        _inorder(self.root)
        return result

    def get_tree_structure(self) -> Optional[Dict[str, Any]]:
        """
        Generates a hierarchical nested JSON structure of the BST for frontend tree rendering.
        """
        if not self.root:
            return None

        def _serialize_node(node: Optional[BSTNode]) -> Optional[Dict[str, Any]]:
            if not node:
                return None
            return {
                "name": f"ACC #{node.account_number}",
                "account_number": node.account_number,
                "account_name": node.account_name,
                "balance": node.balance,
                "children": [
                    child for child in [
                        _serialize_node(node.left),
                        _serialize_node(node.right)
                    ] if child is not None
                ]
            }

        return _serialize_node(self.root)

    def __len__(self) -> int:
        return self._size
