"""Base mail provider interface for Foundry Engine."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class EmailMessage:
    """Email message structure."""

    def __init__(
        self,
        to: str,
        subject: str,
        html_content: Optional[str] = None,
        text_content: Optional[str] = None,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
    ) -> None:
        self.to = to
        self.subject = subject
        self.html_content = html_content
        self.text_content = text_content
        self.from_email = from_email
        self.from_name = from_name
        self.reply_to = reply_to


class BaseMailProvider(ABC):
    """Base class for email providers."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize mail provider with configuration."""
        self.config = config

    @abstractmethod
    async def send(self, message: EmailMessage) -> bool:
        """
        Send an email message.

        Args:
            message: EmailMessage instance to send

        Returns:
            True if sent successfully, False otherwise
        """
        pass

    @abstractmethod
    async def verify_config(self) -> bool:
        """
        Verify provider configuration is valid.

        Returns:
            True if configuration is valid, False otherwise
        """
        pass
