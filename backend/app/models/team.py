from app.extensions import db
import uuid

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(
        db.String(36),
        default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    users = db.relationship('User', backref='team', lazy=True)
    monitors = db.relationship('Monitor', backref='owner_team', lazy=True)