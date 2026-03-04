from app import db


class MaintenanceWindow(db.Model):
    __tablename__ = 'maintenance_windows'

    id = db.Column(db.Integer, primary_key=True)
    monitor_id = db.Column(
        db.Integer,
        db.ForeignKey('monitors.id'),
        nullable=False
    )
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'monitor_id': self.monitor_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
