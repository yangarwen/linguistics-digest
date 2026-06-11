import smtplib
from email.message import EmailMessage
from typing import List

from .config import EmailConfig


def build_email_body(slang_items: List[dict], quote: dict) -> str:
    lines = ["Here is today’s classic English quote:", ""]
    lines.append(f"\"{quote['text']}\"")
    lines.append(f"— {quote['author']}")
    lines.append("")
    lines.append("Here are the latest young English slang terms for today:\n")
    for index, item in enumerate(slang_items, start=1):
        lines.append(f"{index}. {item['word']}: {item['definition']}\n")
    lines.append("Stay curious and enjoy learning new phrases!")
    return "\n".join(lines)


def build_html_body(slang_items: List[dict], quote: dict) -> str:
    rows = "".join(
        f"<li><strong>{item['word']}</strong>: {item['definition'].replace('\n', '<br>')}</li>"
        for item in slang_items
    )
    return f"""
<html>
  <body>
    <p><strong>Today's classic English quote</strong></p>
    <blockquote style="font-style:italic;">{quote['text']}</blockquote>
    <p>— {quote['author']}</p>
    <hr>
    <p>Here are the latest young English slang terms for today:</p>
    <ol>
      {rows}
    </ol>
    <p>Stay curious and enjoy learning new phrases!</p>
  </body>
</html>
"""


def send_email(config: EmailConfig, slang_items: List[dict], quote: dict) -> None:
    message = EmailMessage()
    message["Subject"] = config.email_subject
    message["From"] = config.email_from
    message["To"] = config.email_to
    message.set_content(build_email_body(slang_items, quote))
    message.add_alternative(build_html_body(slang_items, quote), subtype="html")

    with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=20) as smtp:
        smtp.starttls()
        smtp.login(config.smtp_username, config.smtp_password)
        smtp.send_message(message)
