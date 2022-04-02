from db import db
from flask import request, url_for
from requests import Response, post

MAILGUN_DOMAIN = "sandboxe8c60dc8add04d689d81a59b032e5cc4.mailgun.org"
MAILGUN_API_KEY = "bedc25ef79c15a3be0bbeccd8fa8d095-62916a6c-5d8ec552"
FROM_TITLE = "Store REST API"
FROM_EMAIL = "postmaster@sandboxe8c60dc8add04d689d81a59b032e5cc4.mailgun.org"


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def send_confirmation_email(self) -> Response:
        link = request.url_root[:-1] + url_for("userconfirm", user_id=self.id)

        return post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"{FROM_TITLE} <{FROM_EMAIL}>",
                "to": [self.email],
                "subject": "Registration Confirmation",
                "text": f"Please click the link to confirm your registration {link}",
            },
        )

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
