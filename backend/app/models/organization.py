from app.extensions import db
import uuid


class Organization(db.Model):
    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(
        db.String(36),
        default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String(255), nullable=False)
    logo_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )
