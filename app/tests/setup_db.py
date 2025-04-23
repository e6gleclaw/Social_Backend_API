from sqlalchemy import create_engine, text
from app.core.database import Base
import pymysql

def setup_database():
    # Database connection details
    DB_URL = "mysql+pymysql://root:allthebest@localhost:3306"
    DB_NAME = "social_db"
    
    try:
        # Connect to MySQL server (without specifying database)
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='allthebest',
            port=3306
        )
        
        with conn.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print(f"✅ Database {DB_NAME} created/verified")
            
            # Select the database
            cursor.execute(f"USE {DB_NAME}")
            
            # Create engine with the specific database
            engine = create_engine(f"{DB_URL}/{DB_NAME}")
            
            # Create all tables
            Base.metadata.create_all(bind=engine)
            print("✅ All tables created successfully")
            
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database() 