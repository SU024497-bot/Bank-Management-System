"""
================================================================================
UNIT TESTS: CORE DSA ALGORITHMIC ENGINE
================================================================================
Tests:
    1. TransactionLinkedList (O(1) Prepend, Node Chaining, Recents, Length)
    2. SlidingWindowFraudDetector (K=3 Window sum, threshold breach, flags)
    3. AccountBST (Insertion, logarithmic search, in-order sorted traversal)
    4. BankDatabaseStore (Hash Map O(1) integration + BST + Linked List)
================================================================================
"""

import unittest
from backend.dsa.linked_list import TransactionLinkedList, TransactionNode
from backend.dsa.sliding_window import SlidingWindowFraudDetector
from backend.dsa.bst import AccountBST
from backend.dsa.account_store import BankDatabaseStore


class TestTransactionLinkedList(unittest.TestCase):
    def setUp(self):
        self.ledger = TransactionLinkedList()

    def test_empty_list(self):
        self.assertTrue(self.ledger.is_empty())
        self.assertEqual(len(self.ledger), 0)
        self.assertIsNone(self.ledger.head)

    def test_prepend_and_order(self):
        # Insert 3 transactions
        self.ledger.prepend(
            tx_id="TX-1", tx_type="INITIAL_DEPOSIT", amount=1000.0, balance_after=1000.0
        )
        self.ledger.prepend(
            tx_id="TX-2", tx_type="DEPOSIT", amount=500.0, balance_after=1500.0
        )
        self.ledger.prepend(
            tx_id="TX-3", tx_type="WITHDRAWAL", amount=200.0, balance_after=1300.0
        )

        # Total size must be 3
        self.assertEqual(len(self.ledger), 3)

        # Head must be the most recent transaction (TX-3) -> O(1) insertion
        self.assertEqual(self.ledger.head.tx_id, "TX-3")
        self.assertEqual(self.ledger.head.amount, 200.0)

        # Traversal order must be TX-3 -> TX-2 -> TX-1
        recent = self.ledger.get_recent(limit=3)
        self.assertEqual([tx["tx_id"] for tx in recent], ["TX-3", "TX-2", "TX-1"])

    def test_find_by_id(self):
        self.ledger.prepend("TX-A", "DEPOSIT", 100.0, 100.0)
        self.ledger.prepend("TX-B", "DEPOSIT", 200.0, 300.0)

        found = self.ledger.find_by_id("TX-A")
        self.assertIsNotNone(found)
        self.assertEqual(found.amount, 100.0)

        not_found = self.ledger.find_by_id("TX-NONEXISTENT")
        self.assertIsNone(not_found)


class TestSlidingWindowFraudDetector(unittest.TestCase):
    def setUp(self):
        # K = 3, Threshold = ₹50,000.00
        self.detector = SlidingWindowFraudDetector(k_window=3, volume_threshold=50000.0)

    def test_normal_velocity_safe(self):
        r1 = self.detector.evaluate_new_transaction(5000.0)
        self.assertFalse(r1.is_flagged)
        self.assertEqual(r1.risk_level, "SAFE")
        self.assertEqual(r1.window_sum, 5000.0)

        r2 = self.detector.evaluate_new_transaction(10000.0)
        self.assertFalse(r2.is_flagged)
        self.assertEqual(r2.window_sum, 15000.0)

    def test_threshold_breach_triggers_fraud(self):
        # 3 transactions: 20k + 20k + 15k = 55k > 50k threshold
        self.detector.evaluate_new_transaction(20000.0)
        self.detector.evaluate_new_transaction(20000.0)
        r3 = self.detector.evaluate_new_transaction(15000.0)

        self.assertTrue(r3.is_flagged)
        self.assertEqual(r3.risk_level, "CRITICAL_FRAUD")
        self.assertEqual(r3.window_sum, 55000.0)
        self.assertTrue(self.detector.is_account_flagged)

    def test_sliding_window_eviction(self):
        # Insert 10k, 10k, 10k -> sum = 30k
        self.detector.evaluate_new_transaction(10000.0)
        self.detector.evaluate_new_transaction(10000.0)
        self.detector.evaluate_new_transaction(10000.0)
        self.assertEqual(self.detector.get_current_metrics()["window_sum"], 30000.0)

        # Insert 5k -> oldest 10k evicted -> sum = 10k + 10k + 5k = 25k
        self.detector.evaluate_new_transaction(5000.0)
        metrics = self.detector.get_current_metrics()
        self.assertEqual(metrics["window_sum"], 25000.0)
        self.assertEqual(metrics["window_count"], 3)


class TestAccountBST(unittest.TestCase):
    def setUp(self):
        self.bst = AccountBST()

    def test_insert_and_search(self):
        self.bst.insert("10001005", "User E", "e@bank.com", 5000.0, "2026-01-01")
        self.bst.insert("10001002", "User B", "b@bank.com", 2000.0, "2026-01-01")
        self.bst.insert("10001008", "User H", "h@bank.com", 8000.0, "2026-01-01")

        node = self.bst.search("10001002")
        self.assertIsNotNone(node)
        self.assertEqual(node.account_name, "User B")

        not_found = self.bst.search("10009999")
        self.assertIsNone(not_found)

    def test_inorder_sorted_traversal(self):
        keys = ["10001009", "10001001", "10001005", "10001003"]
        for k in keys:
            self.bst.insert(k, f"Name {k}", f"{k}@bank.com", 1000.0, "2026-01-01")

        inorder = self.bst.inorder_traversal()
        extracted_keys = [item["account_number"] for item in inorder]
        self.assertEqual(extracted_keys, ["10001001", "10001003", "10001005", "10001009"])


class TestBankDatabaseStore(unittest.TestCase):
    def test_account_creation_and_hashmap_lookup(self):
        db = BankDatabaseStore()
        acc = db.create_account(
            account_name="Test User",
            email="test@example.com",
            account_number="99990001",
            initial_deposit=10000.0
        )
        
        # O(1) Hash Map retrieval
        fetched = db.get_account_by_number("99990001")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.account_name, "Test User")
        self.assertEqual(fetched.balance, 10000.0)

        # BST retrieval
        bst_node = db.search_bst("99990001")
        self.assertIsNotNone(bst_node)
        self.assertEqual(bst_node["account_name"], "Test User")


if __name__ == "__main__":
    unittest.main()
