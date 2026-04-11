# User Authentication API

A REST API for user authentication built with FastAPI and MySQL.

## Tech Stack
- Python
- FastAPI
- MySQL (XAMPP)
- JWT (PyJWT)
- bcrypt
- python-dotenv

## How to run
1. Start XAMPP (Apache + MySQL)
2. Create `.env` file:
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=auth_db
SECRET_KEY=your_secret_key
3. Activate virtual environment:
```bash
source venv/Scripts/activate
```
4. Run the server:
```bash
uvicorn main:app --reload
```
5. Open `http://127.0.0.1:8000/docs`

## Endpoints
- `POST /register` → register new user
- `POST /login` → login, returns JWT access token + refresh token
- `GET /profile` → get user profile (requires token)
- `POST /refresh` → get new access token using refresh token
- `POST /logout` → logout, invalidates refresh token

## Security
- Passwords hashed with bcrypt
- JWT access token (1 hour expiry)
- Refresh token (7 days expiry, stored in database)
- Refresh token deleted on logout and re-login