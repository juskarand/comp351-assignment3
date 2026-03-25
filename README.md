# Assignment 3 — LEGO Inventory Items API (Auth + Guards)

Assignment 3 extends Assignment 2 by adding an authentication and authorization layer (registration, login, JWT token management, and route guards) integrated into the LEGO Inventory Items API.

## Requirements
- Python 3.9+
- pip
- (Recommended) virtual environment (`venv`)

## Project Structure
assignment3/
main.py
database.py
models.py
schemas.py
auth.py
crud.py
requirements.txt
README.md
.env.example
.gitignore
templates/
static/

## Setup
```bash
# from the assignment3 folder
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Run
uvicorn main:app --reload

Swagger UI:
http://127.0.0.1:8000/docs

## Required Endpoints

-POST /api/register 
-POST /api/login 
-POST /api/logout 
-GET /api/me 
-GET /api/items
-GET /api/admin

## Testing

(Make sure the unvicorn is still running when testing these curl commands. Test them in a new tab inside the terminal. Then you can see the results in a more organized and cxlean manner.)

-Register: 
curl -i -X POST http://127.0.0.1:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","email":"u1@example.com","password":"password123"}'

-Login:
curl -i -c cookies.txt -X POST http://127.0.0.1:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"password123"}'

-Protected Routes:
curl -i -b cookies.txt http://127.0.0.1:8000/api/me
curl -i -b cookies.txt http://127.0.0.1:8000/api/items

-Authorization:
curl -i -b cookies.txt http://127.0.0.1:8000/api/admin

-Logout:
curl -i -b cookies.txt -c cookies.txt -X POST http://127.0.0.1:8000/api/logout
curl -i -b cookies.txt http://127.0.0.1:8000/api/me

## Security Design

-Password Security (bcrypt)

-JWT Token Management

-Token Storage Strategy (httpOnly cookie)

-CORS Configuration

## Route Gaurds
-Authentication Guard (401)

-Authorization Guard (403)

## Environment Variables

-JWT_SECRET_KEY
-ACCESS_TOKEN_EXPIRE_MINUTES
-COOKIE_SECURE
-DATABASE_URL



