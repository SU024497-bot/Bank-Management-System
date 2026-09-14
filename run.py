"""
================================================================================
APEX BANK MANAGEMENT SYSTEM - APPLICATION LAUNCHER
================================================================================
Usage:
    py -3.11 run.py
================================================================================
"""

import os
import sys
import uvicorn

# Ensure current directory is in Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.config import settings

if __name__ == "__main__":
    host = settings.HOST
    port = settings.PORT

    print("=" * 75)
    print("   APEX NATIONAL BANK — ENTERPRISE CORE BANKING PORTAL")
    print("   Theme: Classic Corporate Banking (Deep Navy / Slate / Cool Grey)")
    print("   DSA Engines: Singly Linked List + Sliding Window (K=3) + BST + Hash Map")
    print("   SMTP Delivery: Real SMTP / Non-Blocking Mock Audit Stream")
    print("=" * 75)
    print(f"   Localhost URL:     http://localhost:{port}")
    print(f"   Local IP URL:      http://127.0.0.1:{port}")
    print(f"   API Documentation: http://localhost:{port}/docs")
    print(f"   Alt Docs URL:      http://127.0.0.1:{port}/docs")
    print("=" * 75)

    uvicorn.run(
        "backend.main:app",
        host=host,
        port=port,
        reload=True
    )
