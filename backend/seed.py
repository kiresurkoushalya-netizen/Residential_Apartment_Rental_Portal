from app import create_app
from extensions import db
from models import User, Tower, Unit, Amenity, Booking, TenantUnit, Payment
from werkzeug.security import generate_password_hash


def run_seed():
    app = create_app()

    with app.app_context():
        print("✅ Seeding started...")

        # Clear existing data (optional for dev)      
        TenantUnit.query.delete()
        Booking.query.delete()
        Unit.query.delete()
        Tower.query.delete()
        Amenity.query.delete()
        User.query.delete()

        db.session.commit()

        # -----------------------------
        # Create Admin
        # -----------------------------
        admin = User(
            name="Admin",
            email="admin@residential.com",
            phone="9999999999",
            role="admin",
            password_hash=generate_password_hash("admin123")
        )

        # -----------------------------
        # Create Tenants
        # -----------------------------
        tenant1 = User(
            name="Rahul",
            email="rahul@gmail.com",
            phone="8888888888",
            role="tenant",
            password_hash=generate_password_hash("123456")
        )
        tenant2 = User(
            name="Suresh",
            email="suresh@gmail.com",
            phone="7777777777",
            role="tenant",
            password_hash=generate_password_hash("123456")
        )

        db.session.add_all([admin, tenant1, tenant2])
        db.session.commit()

        # -----------------------------
        # Towers
        # -----------------------------
        tower_a = Tower(name="Tower A", floors=10)
        tower_b = Tower(name="Tower B", floors=12)
        db.session.add_all([tower_a, tower_b])
        db.session.commit()

        # -----------------------------
        # Units
        # -----------------------------
        units = [
            Unit(tower_id=tower_a.id, unit_no="A-101", floor=1, bhk="2BHK", rent=18000, status="available"),
            Unit(tower_id=tower_a.id, unit_no="A-102", floor=1, bhk="3BHK", rent=25000, status="available"),
            Unit(tower_id=tower_a.id, unit_no="A-201", floor=2, bhk="2BHK", rent=18500, status="occupied"),
            Unit(tower_id=tower_b.id, unit_no="B-101", floor=1, bhk="1BHK", rent=14000, status="available"),
            Unit(tower_id=tower_b.id, unit_no="B-202", floor=2, bhk="3BHK", rent=26000, status="occupied"),
        ]

        db.session.add_all(units)
        db.session.commit()

        # -----------------------------
        # Amenities
        # -----------------------------
        gym = Amenity(name="Gym", icon="gym")
        pool = Amenity(name="Swimming Pool", icon="pool")
        parking = Amenity(name="Parking", icon="parking")

        db.session.add_all([gym, pool, parking])
        db.session.commit()

        # -----------------------------
        # Assign TenantUnit occupancy
        # -----------------------------
        occ1 = TenantUnit(tenant_id=tenant1.id, unit_id=units[2].id, move_in_date=datetime(2025, 12, 1).date())
        occ2 = TenantUnit(tenant_id=tenant2.id, unit_id=units[4].id, move_in_date=datetime(2025, 11, 10).date())
        db.session.add_all([occ1, occ2])
        db.session.commit()

        

if __name__ == "__main__":
    run_seed()
