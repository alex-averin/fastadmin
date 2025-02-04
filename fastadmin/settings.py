from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Settings"""

    model_config = SettingsConfigDict(
        env_nested_delimiter="__", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # This value is the prefix you used for mounting FastAdmin app for FastAPI.
    ADMIN_PREFIX: str = Field("admin")

    # This value is the site name on sign-in page and on header.
    ADMIN_SITE_NAME: str = Field("FastAdmin")

    # This value is the logo path on sign-in page.
    ADMIN_SITE_SIGN_IN_LOGO: str = Field("/admin/static/images/sign-in-logo.svg")

    # This value is the logo path on header.
    ADMIN_SITE_HEADER_LOGO: str = Field("/admin/static/images/header-logo.svg")

    # This value is the favicon path.
    ADMIN_SITE_FAVICON: str = Field("/admin/static/images/favicon.png")

    # This value is the primary color for FastAdmin.
    ADMIN_PRIMARY_COLOR: str = Field("#009485")

    # This value is the session id key to store session id in http only cookies.
    ADMIN_SESSION_ID_KEY: str = Field("admin_session_id")

    # This value is the expired_at period (in sec) for session id.
    ADMIN_SESSION_EXPIRED_AT: int = Field(144000)  # in sec

    # This value is the date format for JS widgets.
    ADMIN_DATE_FORMAT: str = Field("YYYY-MM-DD")

    # This value is the datetime format for JS widgets.
    ADMIN_DATETIME_FORMAT: str = Field("YYYY-MM-DD HH:mm")

    # This value is the time format for JS widgets.
    ADMIN_TIME_FORMAT: str = Field("HH:mm:ss")

    # This value is the name for User db/orm model class for authentication.
    ADMIN_USER_MODEL: str = Field(...)

    # This value is the username field for User db/orm model for authentication.
    ADMIN_USER_MODEL_USERNAME_FIELD: str = Field(...)

    # This value is the key to securing signed data - it is vital you keep this secure,
    # or attackers could use it to generate their own signed values.
    ADMIN_SECRET_KEY: str = Field(...)


settings = Settings()
