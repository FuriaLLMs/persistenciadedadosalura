from database import engine, Base
import models

def reset_database():
    print("Resetting database...")
    # Dropping all tables to ensure schema consistency with new relationships
    Base.metadata.drop_all(bind=engine)
    print("Tables dropped.")
    
    # Creating tables again
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    reset_database()
