from dataclasses import dataclass
import os
from dotenv import load_dotenv


@dataclass
class EmailConfig:
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    email_from: str
    email_to: str
    email_subject: str = "Today's Young English Slang Digest"


def load_config() -> EmailConfig:
    load_dotenv()

    smtp_host = os.getenv("SMTP_HOST", "")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    email_from = os.getenv("EMAIL_FROM", "")
    email_to = os.getenv("EMAIL_TO", "")
    email_subject = os.getenv("EMAIL_SUBJECT", "Today's Young English Slang Digest")

    missing = [
        name for name, value in [
            ("SMTP_HOST", smtp_host),
            ("SMTP_USERNAME", smtp_username),
            ("SMTP_PASSWORD", smtp_password),
            ("EMAIL_FROM", email_from),
            ("EMAIL_TO", email_to),
        ]
        if not value
    ]

    if missing:
        raise ValueError(
            "Missing required environment variables: " + ", ".join(missing)
        )

    return EmailConfig(
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        smtp_username=smtp_username,
        smtp_password=smtp_password,
        email_from=email_from,
        email_to=email_to,
        email_subject=email_subject,
    )
