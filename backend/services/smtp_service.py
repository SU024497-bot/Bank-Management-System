"""
================================================================================
SMTP NOTIFICATION ENGINE & EMAIL DISPATCHER SERVICE
================================================================================
Features:
    1. Real SMTP delivery via aiosmtplib / smtplib with TLS support.
    2. Fallback Mock Console Logger with colorized terminal formatting.
    3. In-memory Live Mailbox Audit Stream for real-time Frontend visualization.
    4. Production-grade HTML/CSS responsive email templates:
       - Welcome Email (Onboarding)
       - Transaction Receipt (Credit / Debit)
       - High-Priority Security Alert (Sliding Window Velocity Breach)
================================================================================
"""

import asyncio
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import smtplib
from typing import Dict, List, Optional, Any
import uuid

import aiosmtplib

from ..config import settings

logger = logging.getLogger("smtp_service")
logging.basicConfig(level=logging.INFO)


class EmailRecord:
    """Represents a logged email message in the system audit stream."""
    def __init__(
        self,
        to_email: str,
        subject: str,
        body_html: str,
        body_text: str,
        email_type: str,  # "WELCOME", "TRANSACTION", "SECURITY_ALERT"
        status: str = "DELIVERED",
        account_number: str = "",
        delivery_mode: str = "MOCK_CONSOLE",
        error_message: Optional[str] = None
    ):
        self.email_id: str = f"EML-{uuid.uuid4().hex[:8].upper()}"
        self.to_email: str = to_email
        self.subject: str = subject
        self.body_html: str = body_html
        self.body_text: str = body_text
        self.email_type: str = email_type
        self.status: str = status
        self.account_number: str = account_number
        self.delivery_mode: str = delivery_mode
        self.error_message: Optional[str] = error_message
        self.sent_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "email_id": self.email_id,
            "to_email": self.to_email,
            "subject": self.subject,
            "body_html": self.body_html,
            "body_text": self.body_text,
            "email_type": self.email_type,
            "status": self.status,
            "account_number": self.account_number,
            "delivery_mode": self.delivery_mode,
            "error_message": self.error_message,
            "sent_at": self.sent_at,
        }


class SMTPService:
    """
    Central email dispatcher coordinating live SMTP connections and fallback logging.
    """
    def __init__(self):
        self.email_history: List[EmailRecord] = []

    def _is_real_smtp_configured(self) -> bool:
        """Returns True if real SMTP server credentials have been provided."""
        return bool(settings.SMTP_USER and settings.SMTP_PASSWORD and not settings.MOCK_SMTP_MODE)

    async def _dispatch_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        plain_text: str,
        email_type: str,
        account_number: str = ""
    ) -> EmailRecord:
        """
        Dispatches email asynchronously via real SMTP server or mock fallback logger.
        """
        delivery_mode = "REAL_SMTP" if self._is_real_smtp_configured() else "MOCK_CONSOLE"
        status = "DELIVERED"
        error_msg = None

        if delivery_mode == "REAL_SMTP":
            try:
                message = MIMEMultipart("alternative")
                message["Subject"] = subject
                message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
                message["To"] = to_email
                
                message.attach(MIMEText(plain_text, "plain"))
                message.attach(MIMEText(html_content, "html"))

                await aiosmtplib.send(
                    message,
                    hostname=settings.SMTP_HOST,
                    port=settings.SMTP_PORT,
                    username=settings.SMTP_USER,
                    password=settings.SMTP_PASSWORD,
                    start_tls=settings.SMTP_USE_TLS
                )
                logger.info(f" [SMTP REAL] Successfully dispatched '{subject}' to {to_email}")
            except Exception as exc:
                logger.error(f" [SMTP ERROR] Failed to send real email: {exc}. Falling back to mock log.")
                delivery_mode = "MOCK_FALLBACK (SMTP Failed)"
                status = "MOCK_FALLBACK"
                error_msg = str(exc)
        else:
            # Mock Console Logger Format
            print("\n" + "=" * 70)
            print(" [MOCK SMTP CONSOLE LOG] -> Email Dispatch Simulation")
            print(f" To: {to_email} | Account: {account_number}")
            print(f" Subject: {subject}")
            print(f" Type: {email_type} | Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 70)
            # Safe ascii fallback for console display
            safe_text = plain_text.encode('ascii', 'replace').decode('ascii')
            print(safe_text.strip())
            print("=" * 70 + "\n")

        # Record into audit stream (newest first)
        record = EmailRecord(
            to_email=to_email,
            subject=subject,
            body_html=html_content,
            body_text=plain_text,
            email_type=email_type,
            status=status,
            account_number=account_number,
            delivery_mode=delivery_mode,
            error_message=error_msg
        )
        self.email_history.insert(0, record)
        return record

    async def send_welcome_email(
        self,
        account_name: str,
        account_number: str,
        email: str,
        initial_balance: float
    ) -> EmailRecord:
        """Generates and dispatches onboarding welcome email."""
        subject = f" Welcome to Apex National Bank - Account #{account_number}"
        
        plain_text = f"""
Dear {account_name},

Welcome to Apex National Bank! Your account has been successfully opened.

Account Summary:
- Account Holder: {account_name}
- Account Number: {account_number}
- Starting Balance: ₹{initial_balance:,.2f}
- Date: {datetime.now().strftime('%d %B %Y, %I:%M %p')}

Security Tip:
Never share your banking PIN, OTP, or passwords with anyone. Our 24/7 AI-driven Sliding Window fraud detection engine continuously monitors your account.

Warm regards,
Apex National Bank Team
support@apexbank.internal
"""

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #F8FAFC; margin: 0; padding: 24px; color: #0F172A; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #FFFFFF; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #E2E8F0; }}
    .header {{ background-color: #0F172A; color: #FFFFFF; padding: 24px 30px; text-align: left; border-bottom: 3px solid #1E3A8A; }}
    .header-logo {{ font-size: 20px; font-weight: 700; letter-spacing: 0.5px; margin: 0; }}
    .header-subtitle {{ font-size: 12px; color: #94A3B8; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }}
    .content {{ padding: 30px; color: #334155; line-height: 1.6; font-size: 14px; }}
    .card {{ background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 4px; padding: 18px 20px; margin: 20px 0; }}
    .badge {{ display: inline-block; background: #E0E7FF; color: #1E3A8A; font-weight: 700; padding: 3px 10px; border-radius: 3px; font-size: 11px; text-transform: uppercase; }}
    .balance-box {{ font-size: 24px; font-weight: 700; color: #0F172A; margin-top: 6px; font-family: 'Consolas', monospace; }}
    .footer {{ background: #F1F5F9; padding: 20px 30px; font-size: 12px; color: #64748B; border-top: 1px solid #E2E8F0; line-height: 1.5; }}
    .info-callout {{ background: #F0FDF4; border-left: 3px solid #16A34A; padding: 12px 16px; font-size: 13px; color: #166534; margin-top: 20px; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="header-logo">APEX NATIONAL BANK</div>
      <div class="header-subtitle">Enterprise Banking & Wealth Management</div>
    </div>
    <div class="content">
      <h2 style="color: #0F172A; margin-top: 0; font-size: 18px; font-weight: 700;">Account Opening Confirmation</h2>
      <p>Dear <strong>{account_name}</strong>,</p>
      <p>We are pleased to inform you that your bank account with Apex National Bank has been successfully established and is fully operational.</p>
      
      <div class="card">
        <span class="badge">Active & Verified</span>
        <div style="margin-top: 12px; font-size: 12px; color: #64748B; text-transform: uppercase; font-weight: 600;">Account Number</div>
        <div style="font-size: 18px; font-weight: 700; color: #0F172A; font-family: 'Consolas', monospace;">{account_number}</div>
        
        <div style="margin-top: 14px; font-size: 12px; color: #64748B; text-transform: uppercase; font-weight: 600;">Opening Available Balance</div>
        <div class="balance-box">₹{initial_balance:,.2f}</div>
      </div>

      <div class="info-callout">
        <strong>Security Notice:</strong> Your account is protected by real-time algorithmic fraud detection and 24/7 velocity monitoring. Never share your credentials or OTP with anyone.
      </div>
    </div>
    <div class="footer">
      <strong>Confidentiality Notice:</strong> This is an official automated notification from Apex National Bank. If you did not request this account, please contact our Security Operations Desk immediately at security@apexbank.internal.<br>
      © 2026 Apex National Bank. All rights reserved.
    </div>
  </div>
</body>
</html>
"""
        return await self._dispatch_email(email, subject, html_content, plain_text, "WELCOME", account_number)

    async def send_transaction_email(
        self,
        account_name: str,
        account_number: str,
        email: str,
        tx_type: str,
        amount: float,
        balance_after: float,
        tx_id: str,
        description: str
    ) -> EmailRecord:
        """Dispatches instant Credit/Debit transaction receipt email."""
        is_credit = tx_type.upper() in ("DEPOSIT", "CREDIT", "INITIAL_DEPOSIT")
        type_label = "CREDITED" if is_credit else "DEBITED"
        theme_color = "#16A34A" if is_credit else "#0F172A"
        badge_bg = "#DCFCE7" if is_credit else "#F1F5F9"
        badge_color = "#15803D" if is_credit else "#334155"
        symbol = "+" if is_credit else "-"
        
        subject = f"[{type_label}] ₹{amount:,.2f} on Account #{account_number} | {tx_id}"
        
        plain_text = f"""
Dear {account_name},

Your account #{account_number} has been {type_label.lower()} with ₹{amount:,.2f}.

Transaction Details:
- Transaction ID: {tx_id}
- Type: {tx_type.upper()}
- Amount: {symbol}₹{amount:,.2f}
- Description: {description}
- Clear Balance: ₹{balance_after:,.2f}
- Timestamp: {datetime.now().strftime('%d %b %Y, %I:%M:%S %p')}

If you did not authorize this transaction, contact our security desk immediately at support@apexbank.internal.

Apex National Bank
"""

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #F8FAFC; margin: 0; padding: 24px; color: #0F172A; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #FFFFFF; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #E2E8F0; }}
    .header {{ background: #0F172A; color: #FFFFFF; padding: 20px 30px; text-align: left; border-bottom: 3px solid #1E3A8A; }}
    .header-logo {{ font-size: 18px; font-weight: 700; letter-spacing: 0.5px; }}
    .header-subtitle {{ font-size: 12px; color: #94A3B8; margin-top: 2px; }}
    .content {{ padding: 28px 30px; color: #334155; font-size: 14px; }}
    .receipt-header {{ text-align: center; padding: 10px 0 18px 0; border-bottom: 1px solid #E2E8F0; }}
    .badge {{ display: inline-block; background: {badge_bg}; color: {badge_color}; font-weight: 700; padding: 4px 12px; border-radius: 3px; font-size: 12px; text-transform: uppercase; }}
    .amount-display {{ font-size: 28px; font-weight: 800; color: {theme_color}; margin: 8px 0; font-family: 'Consolas', monospace; }}
    .receipt-card {{ background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 4px; padding: 16px 20px; margin: 20px 0; }}
    .footer {{ background: #F1F5F9; padding: 18px 30px; text-align: left; font-size: 12px; color: #64748B; border-top: 1px solid #E2E8F0; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="header-logo">APEX NATIONAL BANK</div>
      <div class="header-subtitle">Official Transaction Statement</div>
    </div>
    <div class="content">
      <div class="receipt-header">
        <span class="badge">{type_label} TRANSACTION</span>
        <div class="amount-display">{symbol}₹{amount:,.2f}</div>
        <p style="color: #64748B; margin: 0; font-size: 13px;">{description}</p>
      </div>
      
      <div class="receipt-card">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
          <tr>
            <td style="padding: 7px 0; color: #64748B;">Account Holder</td>
            <td style="padding: 7px 0; text-align: right; font-weight: 600; color: #0F172A;">{account_name}</td>
          </tr>
          <tr>
            <td style="padding: 7px 0; color: #64748B;">Account Number</td>
            <td style="padding: 7px 0; text-align: right; font-weight: 600; font-family: 'Consolas', monospace; color: #0F172A;">{account_number}</td>
          </tr>
          <tr>
            <td style="padding: 7px 0; color: #64748B;">Transaction ID</td>
            <td style="padding: 7px 0; text-align: right; font-family: 'Consolas', monospace; font-weight: 600; color: #0F172A;">{tx_id}</td>
          </tr>
          <tr>
            <td style="padding: 7px 0; color: #64748B;">Value Date</td>
            <td style="padding: 7px 0; text-align: right; color: #0F172A;">{datetime.now().strftime('%d %b %Y, %I:%M %p')}</td>
          </tr>
          <tr style="border-top: 1px solid #CBD5E1;">
            <td style="padding: 10px 0 0 0; color: #0F172A; font-weight: 700;">Available Balance</td>
            <td style="padding: 10px 0 0 0; text-align: right; font-weight: 700; color: #0F172A; font-size: 15px; font-family: 'Consolas', monospace;">₹{balance_after:,.2f}</td>
          </tr>
        </table>
      </div>

      <p style="font-size: 12px; color: #64748B; text-align: center; margin-top: 16px;">
        Ledger Record: Linked List Node inserted in O(1) constant time.
      </p>
    </div>
    <div class="footer">
      For disputes or inquiries, contact our 24/7 banking desk at support@apexbank.internal.
    </div>
  </div>
</body>
</html>
"""
        return await self._dispatch_email(email, subject, html_content, plain_text, "TRANSACTION", account_number)

    async def send_security_alert_email(
        self,
        account_name: str,
        account_number: str,
        email: str,
        window_sum: float,
        threshold: float,
        window_size: int,
        reason: str
    ) -> EmailRecord:
        """Dispatches high-priority Security Alert when Sliding Window detects potential fraud."""
        subject = f"SECURITY ALERT: High-Velocity Transaction Breach on Account #{account_number}"
        
        plain_text = f"""
!!! SECURITY ALERT - IMMEDIATE ATTENTION REQUIRED !!!

Dear {account_name},

Our Real-Time Algorithmic Fraud Engine has flagged abnormal velocity activity on your account #{account_number}.

Sliding Window Fraud Metrics:
- Algorithmic Engine: Sliding Window Anomaly Detection (K={window_size})
- Window Volume Sum: ₹{window_sum:,.2f}
- Security Threshold Limit: ₹{threshold:,.2f}
- Violation Reason: {reason}
- Action Taken: Account flagged for administrative verification.

If this was you, you can verify and resolve this security hold via your dashboard or call our emergency desk at +91 (800) 555-APEX immediately.

Security Operations Division
Apex National Bank
"""

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #F8FAFC; margin: 0; padding: 24px; color: #0F172A; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #FFFFFF; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #E2E8F0; }}
    .header {{ background: #991B1B; color: #FFFFFF; padding: 22px 30px; text-align: left; border-bottom: 3px solid #7F1D1D; }}
    .header-logo {{ font-size: 18px; font-weight: 700; letter-spacing: 0.5px; }}
    .header-subtitle {{ font-size: 12px; color: #FCA5A5; margin-top: 2px; text-transform: uppercase; }}
    .content {{ padding: 28px 30px; color: #334155; font-size: 14px; line-height: 1.6; }}
    .alert-box {{ background: #FEF2F2; border: 1px solid #FECACA; border-radius: 4px; padding: 16px 20px; margin: 20px 0; }}
    .footer {{ background: #F1F5F9; padding: 18px 30px; text-align: left; font-size: 12px; color: #64748B; border-top: 1px solid #E2E8F0; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="header-logo">APEX NATIONAL BANK - RISK OPERATIONS</div>
      <div class="header-subtitle">Security Alert: Velocity Threshold Exceeded</div>
    </div>
    <div class="content">
      <h3 style="color: #991B1B; margin-top: 0; font-size: 16px;">Automated Risk Flag Notification</h3>
      <p>Dear <strong>{account_name}</strong>,</p>
      <p>
        Our real-time Sliding Window Fraud Detection Engine has detected a burst of high-volume financial activity exceeding authorized safety thresholds.
      </p>
      
      <div class="alert-box">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
          <tr>
            <td style="padding: 6px 0; color: #7F1D1D;">Account Number</td>
            <td style="padding: 6px 0; text-align: right; font-weight: 700; font-family: 'Consolas', monospace; color: #0F172A;">{account_number}</td>
          </tr>
          <tr>
            <td style="padding: 6px 0; color: #7F1D1D;">Window Size (K)</td>
            <td style="padding: 6px 0; text-align: right; font-weight: 600; color: #0F172A;">Last {window_size} Operations</td>
          </tr>
          <tr>
            <td style="padding: 6px 0; color: #7F1D1D;">Cumulative Window Volume</td>
            <td style="padding: 6px 0; text-align: right; font-weight: 800; color: #DC2626; font-size: 15px; font-family: 'Consolas', monospace;">₹{window_sum:,.2f}</td>
          </tr>
          <tr>
            <td style="padding: 6px 0; color: #7F1D1D;">Safety Threshold Limit</td>
            <td style="padding: 6px 0; text-align: right; font-weight: 600; font-family: 'Consolas', monospace; color: #0F172A;">₹{threshold:,.2f}</td>
          </tr>
          <tr style="border-top: 1px solid #FECACA;">
            <td colspan="2" style="padding: 10px 0 0 0; color: #991B1B; font-size: 13px;">
              <strong>Trigger Reason:</strong> {reason}
            </td>
          </tr>
        </table>
      </div>

      <div style="background: #FFFBEB; border: 1px solid #FDE68A; padding: 12px 16px; border-radius: 4px; font-size: 13px; color: #92400E;">
        <strong>Recommended Action:</strong> If you authorized these transactions, log into the banking portal to verify and clear the hold. For unauthorized transactions, contact the fraud desk immediately.
      </div>
    </div>
    <div class="footer">
      Apex National Bank Risk & Security Operations • Emergency Hotline: 1800-APEX-FRAUD
    </div>
  </div>
</body>
</html>
"""
        return await self._dispatch_email(email, subject, html_content, plain_text, "SECURITY_ALERT", account_number)

    def get_email_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Returns the recent in-memory email audit history."""
        return [record.to_dict() for record in self.email_history[:limit]]


# Singleton instance
smtp_service = SMTPService()
