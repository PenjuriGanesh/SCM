from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from Models.model import Signup
from config.config import User_details
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
import re

app = APIRouter()
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
app.mount("/static", StaticFiles(directory= "static"), name = "static")
html = Jinja2Templates(directory="Templates")


@app.get("/signup", response_class=HTMLResponse)
def sign(request: Request):
    return html.TemplateResponse("sign_up.html", {"request": request, "error_message": None})
@app.post("/signup", response_class=HTMLResponse)
def sign(request: Request, username: str = Form(...), email: str = Form(...), role: str = Form("user"),
         password: str = Form(...), confirm: str = Form(...)):
    try:
        # Check for existing user or email
        existing_user = User_details.find_one({"user": username})  
        existing_email = User_details.find_one({"email": email})

        # Validation checks and corresponding error messages
        if existing_user:
            return html.TemplateResponse("sign_up.html", {"request": request, "error_message": "Username already used", "username": username, "email": email, "role": role})

        if existing_email:
            return html.TemplateResponse("sign_up.html", {"request": request, "error_message": "Email already used", "username": username, "email": email, "role": role})

        if password != confirm:
            return html.TemplateResponse("sign_up.html", {"request": request, "error_message": "Passwords do not match", "username": username, "email": email, "role": role})

        if not any(char.isdigit() for char in password):
            return html.TemplateResponse("sign_up.html", {"request": request, "error_message": "Password should contain at least one digit", "username": username, "email": email, "role": role})

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return html.TemplateResponse("sign_up.html", {"request": request, "error_message": "Password should contain at least one special character", "username": username, "email": email, "role": role})

        if len(password) < 7:
            return html.TemplateResponse("sign_up.html", {"request": request, "error_message": "Password should be at least 7 characters long", "username": username, "email": email, "role": role})
        

        # Hash the password
        pw = pwd_cxt.hash(password)
        signupData = Signup(user=username, email=email, role=role, password=pw)
        User_details.insert_one(dict(signupData)) 

        # Redirect to login page
        return RedirectResponse(url='/login', status_code=303)

    except Exception as e:
        # If an error occurs, show it to the user
        return html.TemplateResponse("sign_up.html", {"request": request, "error_message": f"Internal Server Error: {str(e)}", "username": username, "email": email, "role": role})
