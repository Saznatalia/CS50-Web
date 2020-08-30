import os 

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, text


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Create table users if it doesn't exist
db.execute(text("CREATE TABLE IF NOT EXISTS users (user_id SERIAL, user_name VARCHAR NOT NULL, password VARCHAR NOT NULL)"))
db.commit()

# Create reviews table if it doesn't exist
db.execute(text("CREATE TABLE IF NOT EXISTS reviews (id SERIAL PRIMARY KEY, review TEXT, isbn VARCHAR NOT NULL, rate SMALLINT NOT NULL, user_id INT NOT NULL, UNIQUE (user_id, isbn))"))
db.commit()