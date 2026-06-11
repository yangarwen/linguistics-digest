import time

import schedule

from slang_digest.collector import get_daily_quote, get_trending_slang
from slang_digest.config import load_config
from slang_digest.mailer import send_email


def send_daily_digest() -> None:
    config = load_config()
    slang_items = get_trending_slang(count=6)
    quote = get_daily_quote()
    send_email(config, slang_items, quote)
    print(f"Sent daily slang digest to {config.email_to}.")


if __name__ == "__main__":
    schedule_time = "08:00"
    schedule.every().day.at(schedule_time).do(send_daily_digest)
    print(f"Scheduler started. Daily digest will send at {schedule_time}.")

    while True:
        schedule.run_pending()
        time.sleep(30)
