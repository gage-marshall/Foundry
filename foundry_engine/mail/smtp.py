"""SMTP email provider for Foundry Engine."""

import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

import aiosmtplib

from foundry_engine.mail.base import BaseMailProvider, EmailMessage

logger = logging.getLogger(__name__)


class SMTPMailProvider(BaseMailProvider):
    """SMTP email provider implementation."""

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.host = config.get("host")
        self.port = config.get("port", 587)
        self.username = config.get("username")
        self.password = config.get("password")
        self.use_tls = config.get("use_tls", True)

    async def send(self, message: EmailMessage) -> bool:
        """Send email via SMTP."""
        if not self.host or not self.username or not self.password:
            logger.error("SMTP configuration incomplete")
            return False

        from_email = message.from_email or self.config.get("from_email")
        from_name = message.from_name or self.config.get("from_name")

        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = message.subject
        msg["From"] = f"{from_name} <{from_email}>" if from_name else from_email
        msg["To"] = message.to
        if message.reply_to:
            msg["Reply-To"] = message.reply_to

        # Add text and HTML parts
        if message.text_content:
            msg.attach(MIMEText(message.text_content, "plain"))
        if message.html_content:
            msg.attach(MIMEText(message.html_content, "html"))

        try:
            await aiosmtplib.send(
                msg,
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                use_tls=self.use_tls,
                timeout=10.0,
            )
            logger.info(f"Email sent successfully via SMTP to {message.to}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email via SMTP: {e}")
            return False

    async def verify_config(self) -> bool:
        """Verify SMTP configuration."""
        if not self.host or not self.username or not self.password:
            return False

        try:
            smtp = aiosmtplib.SMTP(
                hostname=self.host,
                port=self.port,
                use_tls=self.use_tls,
                timeout=5.0,
            )
            await smtp.connect()
            await smtp.login(self.username, self.password)
            await smtp.quit()
            return True
        except Exception:
            return False
