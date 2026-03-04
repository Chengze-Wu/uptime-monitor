from app import db


class SSLCertificate(db.Model):
    __tablename__ = 'ssl_certificates'

    id = db.Column(db.Integer, primary_key=True)
    monitor_id = db.Column(
        db.Integer,
        db.ForeignKey('monitors.id'),
        nullable=False
    )
    checked_at = db.Column(db.DateTime, server_default=db.func.now())
    is_valid = db.Column(db.Boolean, nullable=False)
    expires_at = db.Column(db.DateTime)
    days_remaining = db.Column(db.Integer)
    issuer = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'monitor_id': self.monitor_id,
            'checked_at': self.checked_at.isoformat() if self.checked_at else None,
            'is_valid': self.is_valid,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'days_remaining': self.days_remaining,
            'issuer': self.issuer
        }
