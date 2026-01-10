"""Brevo (formerly Sendinblue) email provider for Foundry Engine."""

import logging
from typing import Any

import httpx

from foundry_engine.mail.base import BaseMailProvider, EmailMessage

logger = logging.getLogger(__name__)


class BrevoMailProvider(BaseMailProvider):
    """Brevo email provider implementation."""

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.api_url = "https://api.brevo.com/v3/smtp/email"

    async def send(self, message: EmailMessage) -> bool:
        """Send email via Brevo API."""
        if not self.api_key:
            logger.error("Brevo API key not configured")
            return False

        headers = {
            "accept": "application/json",
            "api-key": self.api_key,
            "content-type": "application/json",
        }

        sender = {"email": message.from_email or self.config.get("from_email")}
        if message.from_name or self.config.get("from_name"):
            sender["name"] = message.from_name or self.config.get("from_name")

        payload = {
            "sender": sender,
            "to": [{"email": message.to}],
            "subject": message.subject,
        }

        if message.html_content:
            payload["htmlContent"] = message.html_content
        if message.text_content:
            payload["textContent"] = message.text_content
        if message.reply_to:
            payload["replyTo"] = {"email": message.reply_to}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, headers=headers, json=payload, timeout=10.0)
                response.raise_for_status()
                logger.info(f"Email sent successfully via Brevo to {message.to}")
                return True
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Brevo API error {e.response.status_code}: {e.response.text}. "
                f"Payload: {payload}"
            )
            return False
        except httpx.HTTPError as e:
            logger.error(f"Failed to send email via Brevo: {e}")
            return False

    async def verify_config(self) -> bool:
        """Verify Brevo API configuration."""
        if not self.api_key:
            return False

        headers = {
            "accept": "application/json",
            "api-key": self.api_key,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.brevo.com/v3/account", headers=headers, timeout=5.0
                )
                response.raise_for_status()
                return True
        except httpx.HTTPError:
            return False
