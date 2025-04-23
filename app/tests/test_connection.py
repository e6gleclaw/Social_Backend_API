from app.core.database import engine
from sqlalchemy import text

def test_connection():
    try:
        with engine.connect() as conn:
            # Test the connection
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            
            # Check if database exists
            result = conn.execute(text("SHOW DATABASES"))
            databases = [row[0] for row in result]
            if 'social_db' in databases:
                print("✅ Database 'social_db' exists")
            else:
                print("❌ Database 'social_db' does not exist")
                
            # Check if we can create tables
            try:
                conn.execute(text("CREATE TABLE IF NOT EXISTS test_table (id INT)"))
                conn.execute(text("DROP TABLE test_table"))
                print("✅ Can create and drop tables")
            except Exception as e:
                print(f"❌ Cannot create tables: {str(e)}")
                
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Make sure MySQL service is running")
        print("2. Verify your MySQL credentials in .env file")
        print("3. Check if port 3306 is open")
        print("4. Try connecting with MySQL Workbench or command line")

if __name__ == "__main__":
    test_connection() 