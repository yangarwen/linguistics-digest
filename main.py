from slang_digest.collector import get_trending_slang
from slang_digest.config import load_config
from slang_digest.mailer import send_email


def main() -> None:
    config = load_config()
    slang_items = get_trending_slang(count=6)
    send_email(config, slang_items)
    print(f"Email sent to {config.email_to} with {len(slang_items)} slang terms.")


if __name__ == "__main__":
    main()
