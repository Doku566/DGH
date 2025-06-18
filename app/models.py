from . import db # Assuming db is defined in app/__init__.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import login_manager # Import login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256)) # Increased length for stronger hashes
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    hardware_assigned = db.relationship('Hardware', backref='assigned_to', lazy=True)
    updates_made = db.relationship('UpdateHistory', backref='updater', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Hardware(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False) # e.g., Laptop, Desktop, Monitor, Printer
    serial_number = db.Column(db.String(100), unique=True, nullable=True)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    purchase_date = db.Column(db.DateTime, nullable=True)
    warranty_expiry_date = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(100), nullable=True) # e.g., "Oficina A", "Sala de Servidores"
    status = db.Column(db.String(50), default='En almacén') # e.g., "En uso", "En almacén", "En reparación", "De baja"
    description = db.Column(db.Text, nullable=True)

    assigned_to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # Relationship to UpdateHistory
    update_history = db.relationship('UpdateHistory', backref='hardware_item', lazy=True,
                                     primaryjoin="and_(UpdateHistory.item_id==Hardware.id, UpdateHistory.item_type=='Hardware')")

    def __repr__(self):
        return f'<Hardware {self.name} ({self.serial_number})>'

class Software(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(50), nullable=True)
    license_key = db.Column(db.String(255), nullable=True) # Increased length
    registration_date = db.Column(db.DateTime, default=datetime.utcnow) # Added for consistency
    purchase_date = db.Column(db.DateTime, nullable=True)
    expiry_date = db.Column(db.DateTime, nullable=True) # For subscription licenses
    seats = db.Column(db.Integer, default=1) # Number of licensed seats
    installation_location = db.Column(db.String(100), nullable=True) # e.g., "Servidor App", "Estaciones de Trabajo Marketing"
    supplier = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)

    # Relationship to UpdateHistory
    update_history = db.relationship('UpdateHistory', backref='software_item', lazy=True,
                                     primaryjoin="and_(UpdateHistory.item_id==Software.id, UpdateHistory.item_type=='Software')")

    def __repr__(self):
        return f'<Software {self.name} {self.version}>'

class UpdateHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, nullable=False) # ID of the Hardware or Software item
    item_type = db.Column(db.String(50), nullable=False) # "Hardware" or "Software"
    field_changed = db.Column(db.String(50), nullable=False)
    old_value = db.Column(db.Text, nullable=True)
    new_value = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    updated_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # To handle generic relationship (though SQLAlchemy doesn't directly support it like Django's GenericForeignKey)
    # We'll rely on item_id and item_type to query the correct table.
    # For backrefs, they are defined in Hardware and Software models.

    def __repr__(self):
        return f'<UpdateHistory ID:{self.id} for {self.item_type} ID:{self.item_id} Field: {self.field_changed}>'

# Required by Flask-Login
@login_manager.user_loader # login_manager should be imported from app/__init__ or passed here
def load_user(user_id):
    return User.query.get(int(user_id))
