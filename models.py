import os
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

# Engine reads credentials from .env
_port = os.getenv('DB_PORT', '3306')
DATABASE_URL = (
    f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{_port}/{os.getenv('DB_NAME')}"
)
engine = db.create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token      = db.Column(db.String(255), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)


class Contact(Base):
    __tablename__ = 'contacts'

    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name    = db.Column(db.String(100), nullable=False)
    phone   = db.Column(db.String(15), nullable=False)