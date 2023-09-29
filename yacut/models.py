from datetime import datetime

from yacut import db, BASE_URL
from yacut.settings import MAX_LENGTH, MAX_LINK


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LINK))
    short = db.Column(db.String(MAX_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return dict(
            url=self.original,
            short_link=BASE_URL + self.short,
        )

    def from_dict(self, data: dict) -> None:
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])