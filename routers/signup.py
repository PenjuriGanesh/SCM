from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import logging
from config.config import User_details
from Models.model import Signup
from fastapi.staticfiles import StaticFiles
import re  # For regex validation
from passlib.context import CryptContext
app = APIRouter()



# Initialize collection and template renderer
html = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/signup", response_class=HTMLResponse)
def sign(request: Request):
    # Render the signup page with no error message initially
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
            return html.TemplateResponse("sign_up.html", {"request": request, "error_message": "Username already used"})
        
        if existing_email:
            return html.TemplateResponse("sign_up.html", {"request": request, "error_message": "Email already used"})

        if password != confirm:
            return html.TemplateResponse("sign_up.html", {"request": request, "error_message": "Passwords do not match"})

        if not password[0].isupper():
            return html.TemplateResponse("sign_up.html", {"request": request, "error_message": "Password should start with a capital letter"})

        if len(password) < 7:
            return html.TemplateResponse("sign_up.html", {"request": request, "error_message": "Password should be at least 7 characters long"})

        if not any(char.isdigit() for char in password):
            return html.TemplateResponse("sign_up.html", {"request": request, "error_message": "Password should contain at least one digit"})

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return html.TemplateResponse("sign_up.html", {"request": request, "error_message": "Password should contain at least one special character"})
        
        pw = pwd_cxt.hash(password)
        signupData=Signup(user=username, email=email,role=role,password=pw)
        User_details.insert_one(dict(signupData)) 


        return RedirectResponse(url='/login', status_code=303)

    except Exception as e:
    
        return html.TemplateResponse("sign_up.html", {"request": request, "error_message": f"Internal Server Error: {str(e)}"})
