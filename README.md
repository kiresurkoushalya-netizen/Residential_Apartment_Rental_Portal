# residential-apartment-portal
Rental-Apartment application 

Required Software
1. Node.js 20 LTS

2. Angular CLI

Run below commoand for Angular
npm install -g @angular/cli

3. Python 3.11+

4. PostgreSQL 15+

5. Docker Desktop

6. VS Code for code editing 

7. Postman


Open the terminal for  Residential_Apartment_Rental_Portal

Run below command

1. docker-compose down -v
2. docker-compose up --build

Now backend API ready with DB.

Runbelow command for UI

Open the bash in frontend project and open bash and run below command

1. ng serve

now UI also ready in http://localhost:4200/

Run below command in bash for creating the all table

docker exec -it apartment_backend python -c "from app import app; from extensions import db; app.app_context().push(); db.create_all(); print('✅Tables created')"


Open Bash in backend and run below command for demo user

docker compose exec backend flask shell

Paste the below code

from app import app
from extensions import db
from models.user import User
from werkzeug.security import generate_password_hash

with app.app_context():
    if not User.query.filter_by(email="user@gmail.com").first():
        u = User(
            name="User",
            email="user@gmail.com",
            phone="9999999999",
            password_hash=generate_password_hash("User@123"),
            role="tenant"
        )
        
        db.session.add(u)
        db.session.commit()
        print("✅ User inserted")


with app.app_context():
    if not User.query.filter_by(email="admin@gmail.com").first():
        admin = User(
            name="Admin",
            email="admin@gmail.com",
            phone="9999999999",
            password_hash=generate_password_hash("Admin@123"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin inserted")
    else:
        print("ℹ️ Admin already exists")
        
Database Verification & SQL Queries

Step 1: Access PostgreSQL Database

Run the below command to connect to PostgreSQL running inside Docker container:

docker exec -it apartment_postgres psql -U postgres -d apartment_db

Step 2: List All Tables

Run the below command to check all created tables:

\dt







