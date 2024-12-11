from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from routers.Jwt_tokens import create_access_token
from config.config import User_details

app = APIRouter()
html = Jinja2Templates(directory="Templates")

# Password context for hashing and verifying passwords
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/login")
def login(request: Request):
    return html.TemplateResponse("Login.html", {"request": request, "error_message": None})


@app.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        # Check if the user exists in the database
        user_data = User_details.find_one({"user": form_data.username})
        
        if not user_data:
            # If the username is not found
            return JSONResponse(content={"detail": "Username not found."}, status_code=404)
        
        # Verify password if username exists
        if not pwd_cxt.verify(form_data.password, user_data["password"]):
            # If the password doesn't match
            return JSONResponse(content={"detail": "Incorrect password."}, status_code=401)
        
        # If authentication is successful, create JWT token
        token = create_access_token(data={
            "username": user_data["user"],
            "email": user_data["email"],
            "role": user_data["role"]
        })
        
        response_content = {  # Structure the response data
            "access_token": token,
            "username": user_data["user"],
            "email": user_data["email"],
            "role": user_data["role"]
        }
        
        response = JSONResponse(content=response_content, status_code=200)
        response.set_cookie(
            key="access_token",
            value=f"Bearer {token}",
            httponly=True,    # Prevent access via JavaScript (XSS protection)
            samesite="Strict" # Protect against CSRF(Cross-Site Request Forgery)
        )
        return response
        
    except HTTPException as http_exception:
        return JSONResponse(content={"detail": http_exception.detail}, status_code=http_exception.status_code)
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
