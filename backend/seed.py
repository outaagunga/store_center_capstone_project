from models.dbconfig import db 
from models.users import User 
from models.storageUnit import StorageUnit 
from models.category import Category 
from models.product import Product 
from models.booking import Booking 
from models.payment import Payment 
from models.review import Review 
from models.pickupDelivery import PickUpDelivery 
from models.category import ProductCategory
from models.product import Product
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app import create_app

def create_users():
    users = []
    
    
    admin = User(
        first_name="John",
        last_name="Doe",
        username="johndoe",
        email="vitamax@gmail.com",
        user_type="admin",
        profile_image_url="",
    )
    admin.set_password("adminpass")
    users.append(admin)
    

    client1 = User(
        first_name="Jane",
        last_name="Smith",
        username="janesmith",
        email="janeth@example.com",
        user_type="client",
        profile_image_url="",
    )
    client1.set_password("clientpass1")
    users.append(client1)
   
    
    client2 = User(
        first_name="Algorand",
        last_name="Mager",
        username="mageralgo",
        email="mager@meta-verse.com",
        user_type="client",
        profile_image_url="",
    )
    client2.set_password("clientpass2")
    users.append(client2)

    
    client3 = User(
        first_name="Sophia",
        last_name="Wambui",
        username="Wambusophie",
        email="sophie@outlook.com",
        user_type="client",
        profile_image_url="",
    )
    client3.set_password("clientpass3")
    users.append(client3)
    
    
    client4 = User(
        first_name="Bill",
        last_name="Joseph",
        username="billjoseph",
        email="billjoseph@yahoo.com",
        user_type="client",
        profile_image_url="",
    )
    client4.set_password("clientpass4")
    users.append(client4)

    employee1 = User(
        first_name="Will",
        last_name="Turner",
        username="willturner",
        email="employee@example.com",
        user_type="employee",
        profile_image_url="",
    )
    employee1.set_password("employeepass")
    users.append(employee1)
    
    
    employee2 = User(
        first_name="Meek",
        last_name="Mill",
        username="meekmill",
        email="meekmill@yahoo.com",
        user_type="employee",
        profile_image_url="",
    )
    employee2.set_password("employeepass1") 
    users.append(employee2)

    db.session.add_all(users)
    db.session.commit()


def create_storage_units():
    sizes = ['Small', 'Medium', 'Large', 'Extra Large']
    for i, size in enumerate(sizes, 1):
        unit = StorageUnit(
            size=size,
            price=i * 50,
            availability_status="available"
        )
        db.session.add(unit)
    db.session.commit()


def create_categories():
    for category in ProductCategory:
        cat = Category(name=category)
        db.session.add(cat)
    db.session.commit()


def create_products():
    products = []
    
    product1 = Product(
        name="Electronics",
        description="The package is  20 box of TVs, 15 boxes 12000wts subwoofer, 5 150ltrs Samsung, LG, Von  refrigerators.",
        image_url="",
        quantity=35,
        weight=100,
        category_id=1
    )
    products.append(product1)
    
    
    product2 = Product(
        name="Vegetables, Fruits",
        description="The is a package of vegetables including sukumawiki(10kg), a package of  watermelone(15kgs), mangoes(5kg), kiwi(8kgs) and mboga(12kg) .",
        image_url="",
        quantity= 5,
        weight=100,
        category_id=2
    )
    products.append(product2)
    
    product3 = Product(
        name="Men and women fashion clothing bales",
        description="The is a 200kg package with two 50kg of pair of trousers, sweat-pants and t-shirts, and two 50kg package of women wares .",
        image_url="",
        quantity=4,
        weight=100,
        category_id=3
    )
    products.append(product3)
    
    db.session.add_all(products)
    db.session.commit()


def create_bookings():
    bookings = []
    
    booking1 = Booking(
        client_id=2,
        storage_unit_id=1,
        start_date=datetime.strptime("2023-10-27", "%Y-%m-%d").date(),
        end_date=datetime.strptime("2023-11-05", "%Y-%m-%d").date(),
        product_id=1
    )
    bookings.append(booking1)
    
    booking2 = Booking(
        client_id=1,
        storage_unit_id=3,
        start_date=datetime.strptime("2023-11-01", "%Y-%m-%d").date(),
        end_date=datetime.strptime("2023-11-03", "%Y-%m-%d").date(),
        product_id=2
    )
    bookings.append(booking2)
    
    booking3 = Booking(
        client_id=3,
        storage_unit_id=12,
        start_date=datetime.strptime("2023-10-13", "%Y-%m-%d").date(),
        end_date=datetime.strptime("2023-11-05", "%Y-%m-%d").date(),
        product_id=3
    )
    bookings.append(booking3)
    
    
    db.session.add_all(bookings)
    db.session.commit()


def create_payments():
    payments = []
    
    payment1 = Payment(
        transaction_id="txn12345",
        amount=50000,
        method="MPESA",
        status="completed",
        client_id=1
    )
    payments.append(payment1)
    
    payment2 = Payment(
        transaction_id="txn12345",
        amount=8000,
        method="MPESA",
        status="completed",
        client_id=2
    )
    payments.append(payment2)
    
    payment3 = Payment(
        transaction_id="txn12345",
        amount=100000,
        method="MPESA",
        status="completed",
        client_id=3
    )
    payments.append(payment3)
    
    db.session.add_all(payments)
    db.session.commit()


def create_reviews():
    reviews = []
    
    review1 = Review(
        client_id=2,
        rating=4,
        comment="Great service!",
        date_submitted=datetime.strptime("2023-10-25", "%Y-%m-%d").date()
    )
    reviews.append(review1)
    
    review2 = Review(
        client_id=1,
        rating=5,
        comment="Impressive!",
        date_submitted=datetime.strptime("2023-08-15", "%Y-%m-%d").date()
    )
    reviews.append(review2)
    
    
    review3 = Review(
        client_id=3,
        rating=4,
        comment="Great service!",
        date_submitted=datetime.strptime("2023-10-01", "%Y-%m-%d").date()
    )
    
    reviews.append(review3)

    db.session.add_all(reviews)
    db.session.commit()


def create_pickups():
    pickups = []
    
    pickup1 = PickUpDelivery(
        client_id=2,
        service_type="pickup",
        date=datetime.strptime("2023-11-03", "%Y-%m-%d").date(),
        address="123 Main St",
        status="pending"
    )
    pickups.append(pickup1)
    
    pickup2 = PickUpDelivery(
        client_id=3,
        service_type="pickup",
        date=datetime.strptime("2023-11-05", "%Y-%m-%d").date(),
        address="123 Main St",
        status="pending"
    )
    pickups.append(pickup2)

    pickup3 = PickUpDelivery(
        client_id=1,
        service_type="pickup",
        date=datetime.strptime("2023-11-05", "%Y-%m-%d").date(),
        address="123 Main St",
        status="pending"
    )
    pickups.append(pickup3)
    
    db.session.add_all(pickups)
    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        try:
            create_users()
            create_storage_units()
            create_categories()
            create_products()
            create_bookings()
            create_payments()
            create_reviews()
            create_pickups()
            print("Data seeded successfully.")
        except IntegrityError:
            db.session.rollback()
            print("Data already exists in the database.")