# User Authentication API

A REST API for user authentication and contact management built with FastAPI, SQLAlchemy, and MySQL.

## Tech Stack
- Python 3.13
- FastAPI
- SQLAlchemy ORM
- MySQL
- JWT (PyJWT)
- bcrypt
- python-dotenv
- Docker

## How to run

### With Docker (recommended)
1. Clone the repo
2. Run:
```bash
docker-compose up --build
```
3. Open `http://localhost:8000/docs`

### Without Docker
1. Create `.env` file:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=auth_db
SECRET_KEY=your_secret_key
```
2. Activate virtual environment:
```bash
source venv/Scripts/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the server:
```bash
uvicorn main:app --reload
```
5. Open `http://127.0.0.1:8000/docs`

## Endpoints

### Auth
- `POST /register` → register new user
- `POST /login` → login, returns access token + refresh token
- `GET /profile` → get user profile (requires token)
- `POST /refresh` → get new access token using refresh token
- `POST /logout` → logout, invalidates refresh token

### Contacts
- `GET /contacts` → list all contacts (requires token)
- `GET /contacts/{name}` → find contact by name (requires token)
- `POST /contacts` → add contact (requires token)
- `DELETE /contacts/{name}` → delete contact (requires token)

## Security
- Passwords hashed with bcrypt
- JWT access token (1 hour expiry)
- Refresh token (7 days expiry, stored in database)
- Refresh token deleted on logout and re-login
- Phone number validation (7-15 digits)
