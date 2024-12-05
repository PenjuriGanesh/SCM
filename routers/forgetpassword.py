from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from config.config import User_details

app = APIRouter()
html = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/forgetpassword")
def forget(request: Request, message: str = None):
    
    return html.TemplateResponse("Forget_password.html", {"request": request, "message": message})

@app.post("/forgetpassword")
def handle_forget_password(request: Request):
    form_data =  request.form() 
    email = form_data.get("email")
    
    user = User_details.find_one({"email": email})
    # print(user)
    
    if user:
        print(message)
        message = "Password reset link has been sent to your email."
    else:
        # If user not found, show this message
        message = "Email not found. Please check your email or register first."

    # Return the page with the appropriate message
    return html.TemplateResponse("Forget_password.html", {"request": request, "message": message})
