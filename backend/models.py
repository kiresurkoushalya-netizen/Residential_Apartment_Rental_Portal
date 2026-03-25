from extensions import db

unit_amenities = db.Table(
    'unit_amenities',
    db.Column('unit_id', db.Integer, db.ForeignKey('unit.id')),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenity.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default="user")

class Tower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    location = db.Column(db.String(100))

class Amenity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    tower_id = db.Column(db.Integer, db.ForeignKey('tower.id'))
    unit_no = db.Column(db.String(20))   # ✅ FIX NAME

    floor = db.Column(db.Integer)
    bhk = db.Column(db.String(10))

    rent = db.Column(db.Float)
    status = db.Column(db.String(20), default="available")

    # ✅ ADD THIS
    furnishing_type = db.Column(db.String(50))

    # ✅ RELATIONSHIPS
    tower = db.relationship('Tower')

    amenities = db.relationship(
        'Amenity',
        secondary=unit_amenities,
        lazy='subquery'
    )

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    status = db.Column(db.String(20), default="pending")