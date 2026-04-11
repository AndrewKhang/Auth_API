import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Connet database
def get_connection(use_db=True):
    config = {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD")
    }   
    if use_db:
        config["database"] = os.getenv("DB_NAME")
    return mysql.connector.connect(**config)

# 2. create database, table
def init_db():
    db = get_connection(use_db=False)  # chưa có database nên False
    cursor = db.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS auth_db")
        cursor.execute("USE auth_db")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        print("Table ready!")
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS refresh_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(255) NOT NULL,
    expires_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
     )
     """)
        print("Refresh token table ready!")
        db.commit()
        print("Database ready!")
    finally:
        cursor.close()
        db.close()

# 3. insert user
def create_user(username: str, hashed_password: str):
    db = get_connection()  
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_password)
        )
        db.commit()
    except Exception as e:
        print(f"[ERROR] create_user() failed: {str(e)}")
        raise
    finally:
        cursor.close()
        db.close()
        
def get_user(username: str):
    db = get_connection()  
    cursor = db.cursor(dictionary=True)
    try:
       cursor.execute("SELECT * FROM users WHERE username = %s", (username,)) 
       result = cursor.fetchone()  
       if not result:
         return None
       else:
             return result
    except Exception as e:
     print(f"[ERROR] get_user() failed: {str(e)}")
     raise
    finally:
        cursor.close() 
        db.close()

def save_refresh_token(user_id: int, token: str, expires_at):
    db = get_connection()  
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "INSERT INTO refresh_tokens (user_id, token, expires_at ) VALUES (%s, %s, %s)",
            (user_id, token, expires_at )
        )
        db.commit()
    except Exception as e:
        print(f"[ERROR] save_refresh_token() failed: {str(e)}")
        raise
    finally:
        cursor.close()
        db.close()

def get_refresh_token(token: str):
    db = get_connection()  
    cursor = db.cursor(dictionary=True)
    try:
       cursor.execute("SELECT * FROM refresh_tokens WHERE token = %s", (token,)) 
       result = cursor.fetchone()  
       if not result:
         return None
       else:
             return result
    except Exception as e:
     print(f"[ERROR] get_refresh_token() failed: {str(e)}")
     raise
    finally:
        cursor.close() 
        db.close()
        
def delete_refresh_tokens(user_id: int):
    db = get_connection()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM refresh_tokens WHERE user_id = %s", (user_id,))
        db.commit()
    except Exception as e:
        print(f"[ERROR] delete_refresh_tokens() failed: {str(e)}")
        raise
    finally:
        cursor.close()
        db.close()