from database import SessionLocal
from app.models.user import User
from app.models.ticket import Ticket
from app.models.booking import Resource, Booking, ResourceTypeEnum

db = SessionLocal()

resources = [
    Resource(name="Lab 204", resource_type=ResourceTypeEnum.LAB, location="Block A"),
    Resource(name="Room 101", resource_type=ResourceTypeEnum.ROOM, location="Block B"),
    Resource(name="Basketball Court", resource_type=ResourceTypeEnum.SPORTS_FACILITY, location="Sports Complex"),
]

for r in resources:
    db.add(r)

db.commit()
print("Resources seeded successfully.")
db.close()
