from slang_digest.collector import get_daily_quote, get_trending_slang
from slang_digest.config import load_config
from slang_digest.mailer import send_email


def main() -> None:
    config = load_config()
    slang_items = get_trending_slang(count=6)
    quote = get_daily_quote()
    send_email(config, slang_items, quote)
    print(f"Email sent to {config.email_to} with {len(slang_items)} slang terms and one quote.")


if __name__ == "__main__":
    main()
