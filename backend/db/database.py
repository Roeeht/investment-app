from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DB_URL as DB_URL

print(f" Attempting database connection...")
print(f"📍 Database URL: {DB_URL[:50]}...")  # Show first 50 chars for security

try:
    engine = create_engine(
        DB_URL,
        pool_size=5,
        max_overflow=0,
        pool_pre_ping=True,
    )
    
    # Test the connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
        
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base = declarative_base()
    
    # Dependency for getting DB session
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    print("✅ Database setup complete!")
    
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("⚠️  Server will run without database functionality")
    # Create dummy objects so imports don't fail
    engine = None
    SessionLocal = None
    Base = declarative_base()
    
    def get_db():
        raise Exception("Database not available")
