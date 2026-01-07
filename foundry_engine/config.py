"""Configuration management for Foundry Engine using Pydantic."""

from enum import Enum
from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Application environment."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"


class MailProvider(str, Enum):
    """Supported email providers."""

    BREVO = "brevo"
    MAILGUN = "mailgun"
    SMTP = "smtp"


class NavigationType(str, Enum):
    """Supported navigation types."""

    TOP_RIBBON = "top_ribbon"
    HAMBURGER = "hamburger"
    SIDEBAR = "sidebar"


class FoundrySettings(BaseSettings):
    """Application-wide settings from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    # Application
    foundry_env: Environment = Environment.DEVELOPMENT
    foundry_site_path: Path = Field(default=Path("./sites/example_site"))
    foundry_host: str = "0.0.0.0"
    foundry_port: int = 8000

    # Security
    secret_key: str = Field(..., min_length=32)
    allowed_hosts: str = "localhost,127.0.0.1"
    cors_origins: str = ""
    jwt_secret_key: Optional[str] = None
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 10
    rate_limit_per_hour: int = 100

    # Email
    mail_provider: MailProvider = MailProvider.BREVO
    mail_from_email: str = "noreply@example.com"
    mail_from_name: str = "Example Site"

    # Brevo
    brevo_api_key: Optional[str] = None

    # Mailgun
    mailgun_api_key: Optional[str] = None
    mailgun_domain: Optional[str] = None
    mailgun_api_base: str = "https://api.mailgun.net/v3"

    # SMTP
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_use_tls: bool = True

    # reCAPTCHA
    recaptcha_site_key: Optional[str] = None
    recaptcha_secret_key: Optional[str] = None

    # Logging
    log_level: str = "INFO"

    @property
    def allowed_hosts_list(self) -> list[str]:
        """Parse allowed hosts string into list."""
        return [host.strip() for host in self.allowed_hosts.split(",") if host.strip()]

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins string into list."""
        if not self.cors_origins:
            return []
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


class NavItemConfig(BaseModel):
    """Navigation item configuration."""

    text: str
    url: str
    icon: Optional[str] = None
    children: Optional[list["NavItemConfig"]] = None


class NavigationConfig(BaseModel):
    """Navigation configuration."""

    type: NavigationType
    logo: Optional[str] = None
    logo_alt: Optional[str] = None
    items: list[NavItemConfig]
    sticky: bool = True
    mobile_breakpoint: int = 768


class SecurityConfig(BaseModel):
    """Site-specific security configuration."""

    allowed_hosts: list[str]
    cors_origins: list[str] = Field(default_factory=list)
    jwt_enabled: bool = False
    csrf_enabled: bool = True


class MailConfig(BaseModel):
    """Site-specific mail configuration."""

    provider: MailProvider
    from_email: str
    from_name: Optional[str] = None
    contact_recipient: str


class SiteInfo(BaseModel):
    """Basic site information."""

    name: str
    domain: str
    description: Optional[str] = None
    favicon: Optional[str] = None
    og_image: Optional[str] = None


class SiteConfig(BaseModel):
    """Complete site configuration from config.yaml."""

    site: SiteInfo
    security: SecurityConfig
    navigation: NavigationConfig
    mail: MailConfig
    pages: list[str]
    theme_css: str = "theme/custom.css"


class SectionFieldConfig(BaseModel):
    """Configuration for a contact form field."""

    name: str
    type: str = "text"  # text, email, tel, textarea, select, checkbox, radio
    label: Optional[str] = None
    placeholder: Optional[str] = None
    required: bool = False
    options: Optional[list[str]] = None  # For select, radio
    validation: Optional[dict[str, Any]] = None


class SectionConfig(BaseModel):
    """Configuration for a page section."""

    type: str
    content: Optional[str] = None  # Path to markdown file
    config: dict[str, Any] = Field(default_factory=dict)

    @field_validator("config", mode="before")
    @classmethod
    def ensure_dict(cls, v: Any) -> dict[str, Any]:
        """Ensure config is a dictionary."""
        if v is None:
            return {}
        return v


class PageConfig(BaseModel):
    """Page configuration from YAML."""

    page: "PageInfo"
    sections: list[SectionConfig]


class PageInfo(BaseModel):
    """Page metadata."""

    slug: str
    title: str
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    protected: bool = False  # Requires JWT authentication


def load_site_config(site_path: Path) -> SiteConfig:
    """Load site configuration from YAML file."""
    config_file = site_path / "config.yaml"
    if not config_file.exists():
        raise FileNotFoundError(f"Site config not found: {config_file}")

    with open(config_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return SiteConfig.model_validate(data)


def load_page_config(site_path: Path, page_slug: str) -> PageConfig:
    """Load page configuration from YAML file."""
    page_file = site_path / "content" / "pages" / f"{page_slug}.yaml"
    if not page_file.exists():
        raise FileNotFoundError(f"Page config not found: {page_file}")

    with open(page_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return PageConfig.model_validate(data)
