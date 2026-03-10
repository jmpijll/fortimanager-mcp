"""Configuration management for FortiManager MCP server."""

import logging
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # FortiManager Connection
    FORTIMANAGER_HOST: str = Field(
        ...,
        description="FortiManager hostname or IP address",
    )

    FORTIMANAGER_API_TOKEN: str | None = Field(
        default=None,
        description="FortiManager API token for authentication",
    )

    FORTIMANAGER_USERNAME: str | None = Field(
        default=None,
        description="FortiManager username (for session-based auth)",
    )

    FORTIMANAGER_PASSWORD: str | None = Field(
        default=None,
        description="FortiManager password (for session-based auth)",
    )

    # FortiCloud OAuth
    FORTICLOUD_AUTH: bool = Field(
        default=False,
        description="Use FortiCloud OAuth flow for authentication",
    )

    FORTICLOUD_CLIENT_ID: str = Field(
        default="FortiManager",
        description="FortiCloud OAuth client_id ('FortiManager' or 'FortiAnalyzer')",
    )

    FORTIMANAGER_VERIFY_SSL: bool = Field(
        default=True,
        description="Verify SSL certificates",
    )

    FORTIMANAGER_TIMEOUT: int = Field(
        default=30,
        ge=1,
        le=300,
        description="Request timeout in seconds",
    )

    FORTIMANAGER_MAX_RETRIES: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Maximum number of retry attempts",
    )

    # MCP Server Settings
    MCP_SERVER_HOST: str = Field(
        default="0.0.0.0",
        description="MCP server bind address",
    )

    MCP_SERVER_PORT: int = Field(
        default=8000,
        ge=1,
        le=65535,
        description="MCP server port",
    )

    # MCP Server Mode
    MCP_SERVER_MODE: Literal["http", "stdio", "auto"] = Field(
        default="auto",
        description="Server mode: 'http' for Docker/web, 'stdio' for Claude Desktop, 'auto' to detect",
    )

    # Tool Loading Mode
    FMG_TOOL_MODE: Literal["full", "dynamic"] = Field(
        default="full",
        description="Tool loading mode: 'full' loads all tools, 'dynamic' loads meta-tools only",
    )

    # Logging Configuration
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level",
    )

    LOG_FILE: Path | None = Field(
        default=None,
        description="Log file path (if file logging enabled)",
    )

    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log message format",
    )

    # Testing Configuration
    TEST_ADOM: str = Field(
        default="root",
        description="ADOM to use for integration tests",
    )

    TEST_DEVICE: str | None = Field(
        default=None,
        description="Device name for device-specific tests",
    )

    TEST_SKIP_WRITE_TESTS: bool = Field(
        default=False,
        description="Skip write operations in tests",
    )

    @field_validator("FORTIMANAGER_HOST")
    @classmethod
    def validate_host(cls, v: str) -> str:
        """Validate FortiManager host."""
        if not v:
            raise ValueError("FORTIMANAGER_HOST cannot be empty")
        # Remove protocol if present
        v = v.replace("https://", "").replace("http://", "")
        # Remove trailing slash
        v = v.rstrip("/")
        return v

    @field_validator("LOG_FILE")
    @classmethod
    def validate_log_file(cls, v: Path | None) -> Path | None:
        """Ensure log directory exists."""
        if v is not None:
            v.parent.mkdir(parents=True, exist_ok=True)
        return v

    @property
    def has_token_auth(self) -> bool:
        """Check if API token authentication is configured."""
        return self.FORTIMANAGER_API_TOKEN is not None

    @property
    def has_session_auth(self) -> bool:
        """Check if session-based authentication is configured."""
        return (
            self.FORTIMANAGER_USERNAME is not None
            and self.FORTIMANAGER_PASSWORD is not None
        )

    @property
    def has_forticloud_auth(self) -> bool:
        """Check if FortiCloud OAuth authentication is configured."""
        return (
            self.FORTICLOUD_AUTH
            and self.FORTIMANAGER_USERNAME is not None
            and self.FORTIMANAGER_PASSWORD is not None
        )

    @property
    def base_url(self) -> str:
        """Get FortiManager base URL."""
        return f"https://{self.FORTIMANAGER_HOST}/jsonrpc"

    def configure_logging(self) -> None:
        """Configure application logging based on settings."""
        # Set log level
        log_level = getattr(logging, self.LOG_LEVEL)
        
        # Configure root logger
        logging.basicConfig(
            level=log_level,
            format=self.LOG_FORMAT,
            handlers=self._get_log_handlers(),
        )

        # Set httpx logging to WARNING to reduce noise
        logging.getLogger("httpx").setLevel(logging.WARNING)

    def _get_log_handlers(self) -> list[logging.Handler]:
        """Get configured log handlers."""
        handlers: list[logging.Handler] = []

        # Console handler (always enabled)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, self.LOG_LEVEL))
        console_handler.setFormatter(logging.Formatter(self.LOG_FORMAT))
        handlers.append(console_handler)

        # File handler (if configured)
        if self.LOG_FILE:
            file_handler = logging.FileHandler(self.LOG_FILE)
            file_handler.setLevel(getattr(logging, self.LOG_LEVEL))
            file_handler.setFormatter(logging.Formatter(self.LOG_FORMAT))
            handlers.append(file_handler)

        return handlers


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings instance with configuration from environment

    Raises:
        ValidationError: If required settings are missing or invalid
    """
    return Settings()

