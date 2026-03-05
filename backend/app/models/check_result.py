from app.extensions import db
import uuid


class CheckResult(db.Model):
    __tablename__ = 'check_results'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(
        db.String(36),
        default=lambda: str(uuid.uuid4())
    )
    monitor_id = db.Column(
        db.Integer,
        db.ForeignKey('monitors.id'),
        nullable=False
    )
    checked_at = db.Column(db.DateTime, server_default=db.func.now())
    is_up = db.Column(db.Boolean, nullable=False)
    status_code = db.Column(db.Integer)
    response_time_ms = db.Column(db.Integer)
    error_message = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.public_id,
            'monitor_id': self.monitor_id,
            'checked_at': self.checked_at.isoformat() if self.checked_at else None,
            'is_up': self.is_up,
            'status_code': self.status_code,
            'response_time_ms': self.response_time_ms,
            'error_message': self.error_message
        }
