"""Contact form section for Foundry Engine."""

from typing import Any

from foundry_engine.sections.base import BaseSection


class ContactSection(BaseSection):
    """Contact form section."""

    section_type = "contact"
    template_name = "sections/contact.html"

    def get_context(self) -> dict[str, Any]:
        """Get context for contact section."""
        fields = self.config.get("fields", [])

        # Default fields if none provided
        if not fields:
            fields = [
                {"name": "name", "type": "text", "label": "Name", "required": True},
                {"name": "email", "type": "email", "label": "Email", "required": True},
                {"name": "message", "type": "textarea", "label": "Message", "required": True},
            ]

        return {
            "content": self.get_rendered_content(),
            "fields": fields,
            "submit_text": self.config.get("submit_text", "Send Message"),
            "success_message": self.config.get("success_message", "Thank you! We'll be in touch soon."),
            "error_message": self.config.get("error_message", "Sorry, something went wrong. Please try again."),
            "recaptcha": self.config.get("recaptcha", False),
            "csrf_token": self.config.get("csrf_token"),
            "recaptcha_site_key": self.config.get("recaptcha_site_key"),
        }
