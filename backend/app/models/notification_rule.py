from app.extensions import db
from sqlalchemy.dialects.postgresql import ARRAY
import uuid


class NotificationRule(db.Model):
    __tablename__ = 'notification_rules'

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
    notify_email = db.Column(db.String(255), nullable=False)
    notify_on_down = db.Column(db.Boolean, default=True)
    notify_on_recovery = db.Column(db.Boolean, default=True)
    ssl_warning_days = db.Column(ARRAY(db.Integer), default=[30, 7, 1])
    consecutive_failures = db.Column(db.Integer, default=3)

    def to_dict(self):
        return {
            'id': self.public_id,
            'monitor_id': self.monitor_id,
            'notify_email': self.notify_email,
            'notify_on_down': self.notify_on_down,
            'notify_on_recovery': self.notify_on_recovery,
            'ssl_warning_days': self.ssl_warning_days,
            'consecutive_failures': self.consecutive_failures
        }
