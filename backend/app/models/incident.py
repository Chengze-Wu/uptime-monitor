from app import db


class Incident(db.Model):
    __tablename__ = 'incidents'

    id = db.Column(db.Integer, primary_key=True)
    monitor_id = db.Column(
        db.Integer,
        db.ForeignKey('monitors.id'),
        nullable=False
    )
    started_at = db.Column(db.DateTime, server_default=db.func.now())
    resolved_at = db.Column(db.DateTime)
    description = db.Column(db.Text)
    is_resolved = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'monitor_id': self.monitor_id,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'description': self.description,
            'is_resolved': self.is_resolved
        }