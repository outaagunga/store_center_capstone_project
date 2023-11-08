from app import app, db
from models import User, StorageUnit, Booking
from datetime import date, datetime


def seed_data():
    print("📚 Seeding data...")

    with app.app_context():  # Create an application context here
        # Create and add some Storage Units
        unit1 = StorageUnit(unit_name="Small Unit", price=50.0)
        unit2 = StorageUnit(unit_name="Medium Unit", price=100.0)
        unit3 = StorageUnit(unit_name="Large Unit", price=150.0)
        unit4 = StorageUnit(unit_name="X-Large Unit", price=200.0)
        unit5 = StorageUnit(unit_name="XX-Large Unit", price=250.0)
        unit6 = StorageUnit(
            unit_name="Small Climate-Controlled Unit", price=75.0)
        unit7 = StorageUnit(
            unit_name="Medium Climate-Controlled Unit", price=125.0)
        unit8 = StorageUnit(
            unit_name="Large Climate-Controlled Unit", price=175.0)

        db.session.add(unit1)
        db.session.add(unit2)
        db.session.add(unit3)
        db.session.add(unit4)
        db.session.add(unit5)
        db.session .add(unit6)
        db.session .add(unit7)
        db.session.add(unit8)

        # Commit the Storage Unit data
        db.session.commit()

        # Create and add some Users
        user1 = User(username="admin", email="admin@example.com",
                     password="admin123", admin=True, role="admin")
        user2 = User(username="user1", email="user1@example.com",
                     password="user123", admin=False, role="client")
        user3 = User(username="user2", email="user2@example.com",
                     password="user123", admin=False, role="client")
        user4 = User(username="user3", email="user3@example.com",
                     password="user123", admin=False, role="client")
        user5 = User(username="user4", email="user4@example.com",
                     password="user123", admin=False, role="client")
        user6 = User(username="user5", email="user5@example.com",
                     password="user123", admin=False, role="client")
        user7 = User(username="user6", email="user6@example.com",
                     password="user123", admin=False, role="client")

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(user4)
        db.session.add(user5)
        db.session.add(user6)
        db.session.add(user7)

        # Commit the User data
        db.session.commit()

        # Create and add some Bookings
        booking1 = Booking(user_id=user2.id, storage_unit_id=unit1.id, start_date=date(
            2023, 10, 1), end_date=date(2023, 11, 1), pickup_requested=False, delivery_requested=True)
        booking2 = Booking(user_id=user3.id, storage_unit_id=unit2.id, start_date=date(
            2023, 10, 15), end_date=date(2023, 11, 15), pickup_requested=True, delivery_requested=False)
        booking3 = Booking(user_id=user4.id, storage_unit_id=unit3.id, start_date=date(
            2023, 11, 1), end_date=date(2023, 12, 1), pickup_requested=False, delivery_requested=True)
        booking4 = Booking(user_id=user5.id, storage_unit_id=unit4.id, start_date=date(
            2023, 11, 15), end_date=date(2023, 12, 15), pickup_requested=True, delivery_requested=False)
        booking5 = Booking(user_id=user6.id, storage_unit_id=unit5.id, start_date=date(
            2023, 12, 1), end_date=date(2024, 1, 1), pickup_requested=False, delivery_requested=True)
        booking6 = Booking(user_id=user7.id, storage_unit_id=unit6.id, start_date=date(
            2023, 12, 15), end_date=date(2024, 1, 15), pickup_requested=True, delivery_requested=False)

        db.session.add(booking1)
        db.session.add(booking2)
        db.session.add(booking3)
        db.session.add(booking4)
        db.session.add(booking5)
        db.session.add(booking6)

        # Commit the Booking data
        db.session.commit()
        print("📚 Data seeded successfully!")


if __name__ == "__main__":
    seed_data()
    print("📚 Done seeding!")
