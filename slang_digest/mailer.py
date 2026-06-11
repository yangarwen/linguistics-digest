import re
import smtplib
from email.message import EmailMessage
from typing import List

from .config import EmailConfig

bad_words: List[str] = []

def build_email_body(slang_items: List[dict], quote: dict) -> str:
    lines = ["Here is today’s classic English quote:", ""]
    lines.append(f"\"{_sanitize(quote['text'])}\"")
    lines.append(f"— {_sanitize(quote['author'])}")
    lines.append("")
    lines.append("Here are the latest young English slang terms for today:\n")
    for index, item in enumerate(slang_items, start=1):
        lines.append(f"{index}. {_sanitize(item['word'])}: {_sanitize(item['definition'])}\n")
    lines.append("Stay curious and enjoy learning new phrases!")
    return "\n".join(lines)

def build_html_body(slang_items: List[dict], quote: dict) -> str:
    rows = "".join(
        f"<li><strong>{_sanitize(item['word'])}</strong>: {_sanitize(item['definition']).replace('\n', '<br>')}</li>"
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

def _sanitize(text: str) -> str:
    """Replace whole-word matches of any term in `bad_words` with asterisks.

    The replacement preserves the length of the original word so layout
    is not dramatically altered.
    """
    pattern = re.compile(r"\b({})\b".format('|'.join(map(re.escape, bad_words))), flags=re.IGNORECASE)
    return pattern.sub(lambda m: '*' * len(m.group()), text)

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
