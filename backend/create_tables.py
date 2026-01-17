from app import create_app
from extensions import db

# ✅ import all models so SQLAlchemy registers them
from models.user import User
from models.tower import Tower
from models.unit import Unit
from models.booking import Booking
from models.amenity import Amenity
from models.tenantUnit import TenantUnit

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tables created successfully")
