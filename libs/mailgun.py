from typing import List
from requests import Response, post


class Mailgun:
    MAILGUN_DOMAIN = "sandboxe8c60dc8add04d689d81a59b032e5cc4.mailgun.org"
    MAILGUN_API_KEY = "bedc25ef79c15a3be0bbeccd8fa8d095-62916a6c-5d8ec552"

    FROM_TITLE = "Store REST API"
    FROM_EMAIL = "postmaster@sandboxe8c60dc8add04d689d81a59b032e5cc4.mailgun.org"

    @classmethod
    def send_email(
        cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:
        return post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )
