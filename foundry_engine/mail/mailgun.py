"""Mailgun email provider for Foundry Engine."""

import logging
from typing import Any

import httpx

from foundry_engine.mail.base import BaseMailProvider, EmailMessage

logger = logging.getLogger(__name__)


class MailgunMailProvider(BaseMailProvider):
    """Mailgun email provider implementation."""

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.domain = config.get("domain")
        self.api_base = config.get("api_base", "https://api.mailgun.net/v3")

    async def send(self, message: EmailMessage) -> bool:
        """Send email via Mailgun API."""
        if not self.api_key or not self.domain:
            logger.error("Mailgun API key or domain not configured")
            return False

        url = f"{self.api_base}/{self.domain}/messages"

        from_email = message.from_email or self.config.get("from_email")
        from_name = message.from_name or self.config.get("from_name")
        from_field = f"{from_name} <{from_email}>" if from_name else from_email

        data = {
            "from": from_field,
            "to": message.to,
            "subject": message.subject,
        }

        if message.html_content:
            data["html"] = message.html_content
        if message.text_content:
            data["text"] = message.text_content
        if message.reply_to:
            data["h:Reply-To"] = message.reply_to

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    auth=("api", self.api_key),
                    data=data,
                    timeout=10.0,
                )
                response.raise_for_status()
                logger.info(f"Email sent successfully via Mailgun to {message.to}")
                return True
        except httpx.HTTPError as e:
            logger.error(f"Failed to send email via Mailgun: {e}")
            return False

    async def verify_config(self) -> bool:
        """Verify Mailgun API configuration."""
        if not self.api_key or not self.domain:
            return False

        url = f"{self.api_base}/{self.domain}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    auth=("api", self.api_key),
                    timeout=5.0,
                )
                response.raise_for_status()
                return True
        except httpx.HTTPError:
            return False
