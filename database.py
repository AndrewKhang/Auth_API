
from models import Base, engine, Session, User, RefreshToken, Contact



# create database, table
def init_db():
    Base.metadata.create_all(engine)

# insert user
def create_user(username: str, hashed_password: str):
    session = Session()
    try:
        user = User(username=username,password=hashed_password)
        session.add(user)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    
        
def get_user(username: str):
    session = Session()
    try: 
       result = session.query(User).filter(User.username == username).first()
       if not result:
         return None
       else:
             return result
    except:
        session.rollback()
        raise
    finally:
        session.close()

def save_refresh_token(user_id: int, token: str, expires_at):
    session = Session()
    try:
        token = RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
        session.add(token)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def get_refresh_token(token: str):
    session = Session()
    try: 
       result = session.query(RefreshToken).filter(RefreshToken.token == token).first()
       if not result:
         return None
       else:
         return result
    except:
        session.rollback()
        raise
    finally:
        session.close()

        
def delete_refresh_tokens(user_id: int):
    session = Session()
    try: 
     session.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
     session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        
def add_contact(user_id: int, name: str, phone: str):
    session = Session()
    try:
        contact = Contact(user_id=user_id, name=name, phone = phone )
        session.add(contact)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        
def get_contacts(user_id: int):
    session = Session()
    try: 
       result = session.query(Contact).filter(Contact.user_id == user_id).all()
       if not result:
         return None
       else:
             return result
    except:
        session.rollback()
        raise
    finally:
        session.close()
        
def delete_contact(user_id: int, name: str):
    session = Session()
    try: 
     session.query(Contact).filter(Contact.user_id == user_id, Contact.name == name).delete()
     session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        
def find_contact(user_id: int, name: str):
    session = Session()
    try: 
       result = session.query(Contact).filter(Contact.user_id == user_id,Contact.name == name).first()
       if not result:
         return None
       else:
         return result
    except:
        session.rollback()
        raise
    finally:
        session.close()