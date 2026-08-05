"""Transactional email delivery (SMTP). Falls back to logging when SMTP is not configured."""

from __future__ import annotations

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config import settings

logger = logging.getLogger(__name__)


def email_is_configured() -> bool:
    return settings.email_is_configured()


def send_email(
    to: str,
    subject: str,
    body_text: str,
    body_html: str | None = None,
) -> bool:
    """
    Send an email via SMTP. Returns True on success.
    When SMTP is not configured, logs the message and returns False.
    """
    recipient_hash = hash(to) % 10_000

    if not email_is_configured():
        logger.warning(
            "email_not_configured recipient_hash=%s subject=%s (SMTP not configured; message not sent)",
            recipient_hash,
            subject,
        )
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.email_from
    msg["To"] = to
    msg.attach(MIMEText(body_text, "plain", "utf-8"))
    if body_html:
        msg.attach(MIMEText(body_html, "html", "utf-8"))

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=30) as server:
            if settings.smtp_use_tls:
                server.starttls()
            if settings.smtp_user and settings.smtp_password:
                server.login(settings.smtp_user, settings.smtp_password)
            server.sendmail(settings.email_from, [to], msg.as_string())
        logger.info("email_sent recipient_hash=%s subject=%s", recipient_hash, subject)
        return True
    except Exception as e:
        logger.exception(
            "email_send_failed recipient_hash=%s subject=%s err=%s",
            recipient_hash,
            subject,
            e,
        )
        return False


def send_password_reset_email(to: str, reset_token: str) -> bool:
    base = settings.frontend_url.rstrip("/")
    link = f"{base}/reset-password?token={reset_token}"
    subject = "Reset your Iskonnect password"
    text = (
        "You requested a password reset for your Iskonnect account.\n\n"
        f"Open this link to set a new password (valid for 1 hour):\n{link}\n\n"
        "If you did not request this, you can ignore this email."
    )
    html = (
        f"<p>You requested a password reset for your Iskonnect account.</p>"
        f'<p><a href="{link}">Reset your password</a> (link valid for 1 hour)</p>'
        "<p>If you did not request this, you can ignore this email.</p>"
    )
    return send_email(to, subject, text, html)


def send_email_verification_email(to: str, verify_token: str) -> bool:
    base = settings.frontend_url.rstrip("/")
    link = f"{base}/verify-email?token={verify_token}"
    subject = "Verify your Iskonnect email"
    text = (
        "Welcome to Iskonnect!\n\n"
        f"Verify your email address:\n{link}\n\n"
        "This link expires in 7 days."
    )
    html = (
        "<p>Welcome to Iskonnect!</p>"
        f'<p><a href="{link}">Verify your email address</a> (expires in 7 days)</p>'
    )
    return send_email(to, subject, text, html)
