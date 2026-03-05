from app.extensions import db
import uuid


class Monitor(db.Model):
    __tablename__ = 'monitors'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(
        db.String(36),
        default=lambda: str(uuid.uuid4())
    )
    creator_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    owner_team_id = db.Column(
        db.Integer,
        db.ForeignKey('teams.id'),
        nullable=True
    )
    ownership_type = db.Column(
        db.String(20),
        nullable=False,
        default='personal'
    )
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.Text, nullable=False)
    check_interval = db.Column(db.Integer, default=300)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    check_results = db.relationship(
        'CheckResult',
        backref='monitor',
        lazy=True,
        cascade='all, delete-orphan'
    )
    ssl_certificates = db.relationship(
        'SSLCertificate',
        backref='monitor',
        lazy=True,
        cascade='all, delete-orphan'
    )
    notification_rules = db.relationship(
        'NotificationRule',
        backref='monitor',
        lazy=True,
        cascade='all, delete-orphan'
    )
    maintenance_windows = db.relationship(
        'MaintenanceWindow',
        backref='monitor',
        lazy=True,
        cascade='all, delete-orphan'
    )
    incidents = db.relationship(
        'Incident', 
        backref='monitor',
        lazy=True,
        cascade='all, delete-orphan'
    )
    reports = db.relationship('Report', backref='monitor', lazy=True)

    def to_dict(self):
        return {
            'id': self.public_id,
            'creator_id': self.creator_id,
            'owner_team_id': self.owner_team_id,
            'ownership_type': self.ownership_type,
            'name': self.name,
            'url': self.url,
            'check_interval': self.check_interval,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }