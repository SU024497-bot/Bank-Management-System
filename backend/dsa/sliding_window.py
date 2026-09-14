"""
================================================================================
CORE DSA MODULE: REAL-TIME FRAUD DETECTION (SLIDING WINDOW ALGORITHM)
================================================================================
Concept:
    A dynamic Sliding Window algorithmic engine that inspects transaction
    velocity and cumulative financial volume over a moving window of the last
    'K' operations.
    
Algorithmic Properties:
    - Window Size: K operations (default K=3)
    - Threshold: Cumulative volume limit (default ₹50,000.00)
    - Time Complexity: O(K) per evaluation using Linked List head traversal or
      O(1) amortized queue maintenance.
    - Space Complexity: O(K) auxiliary buffer for the active evaluation frame.
================================================================================
"""

from collections import deque
from datetime import datetime
from typing import List, Dict, Any, Optional


class FraudEvaluationResult:
    """Encapsulates the structured outcome of a sliding window evaluation."""
    def __init__(
        self,
        is_flagged: bool,
        risk_level: str,          # "SAFE", "MODERATE", "CRITICAL_FRAUD"
        window_size: int,
        window_count: int,
        window_sum: float,
        threshold: float,
        threshold_percentage: float,
        recent_amounts: List[float],
        reason: str,
        timestamp: Optional[str] = None
    ):
        self.is_flagged: bool = is_flagged
        self.risk_level: risk_level = risk_level
        self.window_size: int = window_size
        self.window_count: int = window_count
        self.window_sum: float = round(window_sum, 2)
        self.threshold: float = round(threshold, 2)
        self.threshold_percentage: float = round(threshold_percentage, 1)
        self.recent_amounts: List[float] = recent_amounts
        self.reason: str = reason
        self.timestamp: str = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_flagged": self.is_flagged,
            "risk_level": self.risk_level,
            "window_size": self.window_size,
            "window_count": self.window_count,
            "window_sum": self.window_sum,
            "threshold": self.threshold,
            "threshold_percentage": self.threshold_percentage,
            "recent_amounts": self.recent_amounts,
            "reason": self.reason,
            "timestamp": self.timestamp,
        }


class SlidingWindowFraudDetector:
    """
    Sliding Window algorithmic engine for real-time anomaly and velocity fraud detection.
    Maintains a rolling queue of the most recent K transactions for each bank account.
    """
    def __init__(self, k_window: int = 3, volume_threshold: float = 50000.0):
        self.k_window: int = max(1, int(k_window))
        self.volume_threshold: float = float(volume_threshold)
        
        # Sliding window buffer storing recent transaction amounts
        self._window: deque = deque(maxlen=self.k_window)
        self._running_sum: float = 0.0
        
        # State tracking
        self.is_account_flagged: bool = False
        self.last_evaluation: Optional[FraudEvaluationResult] = None
        self.alert_history: List[Dict[str, Any]] = []

    def evaluate_new_transaction(self, amount: float, tx_type: str = "DEPOSIT") -> FraudEvaluationResult:
        """
        DSA SLIDING WINDOW EVALUATION:
        Adds a new incoming transaction to the sliding window, shifts out old operations
        if the buffer exceeds K, and calculates whether the current window sum breaches
        the security threshold.
        
        Time Complexity: O(1) amortized sliding window update.
        """
        amount = float(amount)
        
        # If the window is already full, subtract the element that will be evicted
        if len(self._window) == self.k_window:
            evicted_amount = self._window[0]
            self._running_sum -= evicted_amount
            
        # Append new transaction amount to sliding window
        self._window.append(amount)
        self._running_sum += amount
        
        # Calculate algorithmic metrics
        window_count = len(self._window)
        current_sum = round(self._running_sum, 2)
        pct_of_threshold = (current_sum / self.volume_threshold) * 100.0
        recent_amounts_list = list(self._window)
        
        # Fraud Condition: Window sum exceeds threshold across the last K operations
        is_breached = current_sum >= self.volume_threshold
        
        if is_breached:
            risk_level = "CRITICAL_FRAUD"
            reason = (
                f"Suspicious high velocity! Cumulative volume of ₹{current_sum:,.2f} across "
                f"last {window_count} transaction(s) exceeds security threshold of ₹{self.volume_threshold:,.2f}."
            )
            self.is_account_flagged = True
        elif pct_of_threshold >= 75.0:
            risk_level = "MODERATE"
            reason = (
                f"Approaching velocity limit ({pct_of_threshold:.1f}%). Window volume at ₹{current_sum:,.2f}."
            )
        else:
            risk_level = "SAFE"
            reason = "Normal velocity within acceptable financial parameters."

        result = FraudEvaluationResult(
            is_flagged=self.is_account_flagged,
            risk_level=risk_level,
            window_size=self.k_window,
            window_count=window_count,
            window_sum=current_sum,
            threshold=self.volume_threshold,
            threshold_percentage=pct_of_threshold,
            recent_amounts=recent_amounts_list,
            reason=reason
        )
        
        self.last_evaluation = result
        if is_breached:
            self.alert_history.append(result.to_dict())
            
        return result

    def get_current_metrics(self) -> Dict[str, Any]:
        """Returns the current state of the sliding window for dashboard monitoring."""
        current_sum = round(self._running_sum, 2)
        pct = (current_sum / self.volume_threshold) * 100.0 if self.volume_threshold > 0 else 0
        return {
            "is_flagged": self.is_account_flagged,
            "risk_level": "CRITICAL_FRAUD" if self.is_account_flagged else ("MODERATE" if pct >= 75 else "SAFE"),
            "window_size": self.k_window,
            "window_count": len(self._window),
            "window_sum": current_sum,
            "threshold": self.volume_threshold,
            "threshold_percentage": round(pct, 1),
            "window_amounts": list(self._window),
            "alert_count": len(self.alert_history)
        }

    def resolve_fraud_flag(self) -> None:
        """Clears the flagged state after security verification or admin resolution."""
        self.is_account_flagged = False
        if self.last_evaluation:
            self.last_evaluation.is_flagged = False

    def update_parameters(self, k_window: Optional[int] = None, volume_threshold: Optional[float] = None) -> None:
        """Dynamically adjusts sliding window size or volume threshold."""
        if k_window is not None and k_window > 0:
            self.k_window = int(k_window)
            old_items = list(self._window)
            self._window = deque(old_items[-self.k_window:], maxlen=self.k_window)
            self._running_sum = sum(self._window)
        if volume_threshold is not None and volume_threshold > 0:
            self.volume_threshold = float(volume_threshold)
