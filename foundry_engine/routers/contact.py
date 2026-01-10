"""Contact form handling router for Foundry Engine."""

import logging
from typing import Any

import httpx
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr, ValidationError

from foundry_engine.config import MailProvider
from foundry_engine.mail.base import EmailMessage
from foundry_engine.mail.brevo import BrevoMailProvider
from foundry_engine.mail.mailgun import MailgunMailProvider
from foundry_engine.mail.smtp import SMTPMailProvider
from foundry_engine.security.csrf import validate_csrf_token
from foundry_engine.security.rate_limit import limiter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["contact"])


class ContactFormData(BaseModel):
    """Contact form data validation."""

    name: str
    email: EmailStr
    message: str


def get_mail_provider(request: Request) -> Any:
    """Get configured mail provider."""
    settings = request.app.state.settings
    site_config = request.app.state.site_config

    provider_type = settings.mail_provider

    if provider_type == MailProvider.BREVO:
        config = {
            "api_key": settings.brevo_api_key,
            "from_email": site_config.mail.from_email,
            "from_name": site_config.mail.from_name,
        }
        return BrevoMailProvider(config)

    elif provider_type == MailProvider.MAILGUN:
        config = {
            "api_key": settings.mailgun_api_key,
            "domain": settings.mailgun_domain,
            "api_base": settings.mailgun_api_base,
            "from_email": site_config.mail.from_email,
            "from_name": site_config.mail.from_name,
        }
        return MailgunMailProvider(config)

    elif provider_type == MailProvider.SMTP:
        config = {
            "host": settings.smtp_host,
            "port": settings.smtp_port,
            "username": settings.smtp_username,
            "password": settings.smtp_password,
            "use_tls": settings.smtp_use_tls,
            "from_email": site_config.mail.from_email,
            "from_name": site_config.mail.from_name,
        }
        return SMTPMailProvider(config)

    else:
        raise ValueError(f"Unsupported mail provider: {provider_type}")


async def verify_recaptcha(recaptcha_response: str, secret_key: str) -> bool:
    """Verify Google reCAPTCHA response."""
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {"secret": secret_key, "response": recaptcha_response}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data, timeout=5.0)
            result = response.json()
            return result.get("success", False)
    except Exception as e:
        logger.error(f"reCAPTCHA verification failed: {e}")
        return False


@router.post("/contact", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def handle_contact_form(
    request: Request,
    csrf_valid: bool = Depends(validate_csrf_token),
) -> str:
    """Handle contact form submission."""
    settings = request.app.state.settings
    site_config = request.app.state.site_config

    # Parse form data manually to handle any custom fields
    try:
        form_data_raw = await request.form()
        form_dict = dict(form_data_raw)

        # Extract required fields
        name = form_dict.get("name", "").strip()
        email = form_dict.get("email", "").strip()
        message = form_dict.get("message", "").strip()

        # Extract optional fields
        subject = form_dict.get("subject", "").strip()
        recaptcha_response = form_dict.get("g-recaptcha-response")

        # Log received form data for debugging
        logger.debug(
            f"Contact form received - name: {name}, email: {email}, "
            f"subject: {subject}, message length: {len(message)}, "
            f"all fields: {list(form_dict.keys())}"
        )

        # Validate required fields
        if not name:
            return '<div class="alert alert-error">Name is required.</div>'
        if not email:
            return '<div class="alert alert-error">Email is required.</div>'
        if not message:
            return '<div class="alert alert-error">Message is required.</div>'

    except Exception as e:
        logger.error(f"Error parsing form data: {e}", exc_info=True)
        return '<div class="alert alert-error">Invalid form data.</div>'

    # Validate form data
    try:
        form_data = ContactFormData(name=name, email=email, message=message)
    except ValidationError as e:
        logger.warning(f"Contact form validation error: {e.errors()}")
        # Return more specific error message
        error_details = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in e.errors()])
        return f'<div class="alert alert-error">Validation error: {error_details}</div>'

    # Verify reCAPTCHA if enabled
    if settings.recaptcha_secret_key and recaptcha_response:
        if not await verify_recaptcha(recaptcha_response, settings.recaptcha_secret_key):
            logger.warning("reCAPTCHA verification failed")
            return '<div class="alert alert-error">reCAPTCHA verification failed. Please try again.</div>'

    # Prepare email
    email_subject = f"Contact Form: {site_config.site.name}"
    if subject:
        email_subject = f"{email_subject} - {subject}"

    html_content = f"""
    <h2>New Contact Form Submission</h2>
    <p><strong>Name:</strong> {form_data.name}</p>
    <p><strong>Email:</strong> {form_data.email}</p>
    """
    if subject:
        html_content += f"<p><strong>Subject:</strong> {subject}</p>"
    html_content += f"""
    <p><strong>Message:</strong></p>
    <p>{form_data.message.replace(chr(10), '<br>')}</p>
    """

    text_content = f"""
    New Contact Form Submission

    Name: {form_data.name}
    Email: {form_data.email}
    """
    if subject:
        text_content += f"Subject: {subject}\n"
    text_content += f"""

    Message:
    {form_data.message}
    """

    email_message = EmailMessage(
        to=site_config.mail.contact_recipient,
        subject=email_subject,
        html_content=html_content,
        text_content=text_content,
        reply_to=form_data.email,
    )

    # Send email
    try:
        mail_provider = get_mail_provider(request)
        logger.debug(f"Sending email from {email_message.reply_to} to {site_config.mail.contact_recipient}")
        success = await mail_provider.send(email_message)

        if success:
            logger.info(f"Contact form submitted successfully from {form_data.email}")
            return '<div class="alert alert-success">Thank you! We\'ll be in touch soon.</div>'
        else:
            logger.error(
                f"Failed to send contact form email. "
                f"Provider: {settings.mail_provider}, "
                f"From: {site_config.mail.from_email}, "
                f"To: {site_config.mail.contact_recipient}"
            )
            return '<div class="alert alert-error">Sorry, something went wrong. Please try again later.</div>'

    except Exception as e:
        logger.error(f"Error processing contact form: {type(e).__name__}: {e}", exc_info=True)
        return '<div class="alert alert-error">Sorry, something went wrong. Please try again later.</div>'
