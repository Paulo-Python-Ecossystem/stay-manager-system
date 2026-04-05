#!/bin/sh

echo "Waiting for PostgreSQL to start..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Navigate to django app folder
cd /app/stay_manager_system

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Seeding basic test data
echo "Seeding basic test data (roles and superuser)..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
from hotel_auth.models.permission import Role
from hotel_auth.models.user import Account

User = get_user_model()

# Create standard Roles if they don't exist
admin_role, _ = Role.objects.get_or_create(label='Admin', defaults={'description': 'System Administrator', 'is_staff': True})
receptionist_role, _ = Role.objects.get_or_create(label='Receptionist', defaults={'description': 'Hotel Front Desk', 'is_staff': True})
guest_role, _ = Role.objects.get_or_create(label='Guest', defaults={'description': 'Regular Customer', 'is_staff': False})

if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@staymanager.com', 'admin123')
    Account.objects.create(user=user, role=admin_role)
    print("Sucessfully created test Superuser 'admin' with password 'admin123'")
else:
    print("Superuser already exists.")

from hotel.models.property import Hotel
from hotel.models.room import RoomType, Room
from hotel.models.guest import Guest

# Create a demo Guest account
if not User.objects.filter(username='johndoe').exists():
    guest_user = User.objects.create_user('johndoe', 'johndoe@example.com', 'guest123')
    Account.objects.create(user=guest_user, role=guest_role)
    Guest.objects.create(
        user=guest_user,
        first_name="John",
        last_name="Doe",
        email="johndoe@example.com",
        phone="555-9999",
        identification_type="PASSPORT",
        identification_number="A12345678"
    )
    print("Successfully created test Guest 'johndoe' with password 'guest123'")

# Create a demo Hotel if it doesn't exist
hotel, created = Hotel.objects.get_or_create(
    name="Grand Plaza Hotel",
    defaults={
        "address": "123 Main Avenue, Downtown",
        "description": "Luxurious stay in the city center",
        "phone": "555-0100",
        "email": "contact@grandplaza.com",
    }
)

if created:
    print("Created demo Hotel: Grand Plaza Hotel")

    # Create Room Types
    suite, _ = RoomType.objects.get_or_create(
        name="Presidential Suite",
        defaults={"description": "Top floor suite", "capacity": 4, "base_price": 500.00}
    )
    standard, _ = RoomType.objects.get_or_create(
        name="Standard Double",
        defaults={"description": "Standard room with double bed", "capacity": 2, "base_price": 100.00}
    )

    # Create some rooms
    Room.objects.get_or_create(hotel=hotel, room_type=suite, room_number="1001", defaults={"floor": 10})
    Room.objects.get_or_create(hotel=hotel, room_type=standard, room_number="101", defaults={"floor": 1})
    Room.objects.get_or_create(hotel=hotel, room_type=standard, room_number="102", defaults={"floor": 1})
    Room.objects.get_or_create(hotel=hotel, room_type=standard, room_number="103", defaults={"floor": 1})
    print("Created demo Room Types and Rooms for the hotel.")
EOF

# Load the normal startup command array
exec "$@"
