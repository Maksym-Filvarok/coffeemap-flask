from datetime import datetime, timezone

from app import db


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(120), nullable=False)
    short_description = db.Column(db.String(180), nullable=False)
    full_description = db.Column(db.Text, nullable=False)

    city = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    price_level = db.Column(db.String(10), nullable=False)

    tags = db.Column(db.String(255), nullable=False)

    image_url = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    contact_url = db.Column(db.String(500), nullable=True)

    is_featured = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]