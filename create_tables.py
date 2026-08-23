from database import Base, engine
from app.models.user import User
from app.models.ticket import Ticket

Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
