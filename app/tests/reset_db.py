from app.core.database import Base, engine
from sqlalchemy import text

def reset_database():
    # Drop all tables
    with engine.connect() as conn:
        # Disable foreign key checks
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        
        # Get all tables in the database
        result = conn.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        
        # Drop each table
        for table in tables:
            conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
        
        # Re-enable foreign key checks
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        conn.commit()
    
    # Create all tables with new schema
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables reset successfully!")

if __name__ == "__main__":
    reset_database() 