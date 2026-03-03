from database import engine
from models import SQLModel, Property

def reset_and_init():
    print("\n\n===== Nuking the current database structure =====\n")
    SQLModel.metadata.drop_all(engine)

    print("\n\n===== Initializing the new database from models =====\n")
    SQLModel.metadata.create_all(engine)

    print("\n\n===== Phase 1 database is clean =====\n")

if __name__ == "__main__":
    reset_and_init()