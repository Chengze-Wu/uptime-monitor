from app import db

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    monitor_id = db.Column(
        db.Integer,
        db.ForeignKey('monitors.id'),
        nullable=True
    )
    range_start = db.Column(db.DateTime, nullable=False)
    range_end = db.Column(db.DateTime, nullable=False)
    file_url = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'monitor_id': self.monitor_id,
            'range_start': self.range_start.isoformat() if self.range_start else None,
            'range_end': self.range_end.isoformat() if self.range_end else None,
            'file_url': self.file_url,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
