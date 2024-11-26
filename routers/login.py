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
    return html.TemplateResponse("Login.html", {"request": request})


@app.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        # Check if the user exists in the database
        user_data = User_details.find_one({"user": form_data.username})
        
        if user_data:
            # Verify password
            if pwd_cxt.verify(form_data.password, user_data["password"]):
                # Create JWT token for the user
                token = create_access_token(data={
                    "username": user_data["user"],
                    "email": user_data["email"],
                    "role": user_data["role"]
                })
                
                response_content = {
                    "access_token": token,
                    "username": user_data["user"],
                    "email": user_data["email"],
                    "role": user_data["role"]
                }
                response = JSONResponse(content=response_content, status_code=200)
                response.set_cookie(
                    key="access_token",
                    value=f"Bearer {token}",
                    httponly=True
                )
                return response
            else:
                raise HTTPException(status_code=401, detail="Password is incorrect")
        else:
            raise HTTPException(status_code=401, detail="Username not found")
    except HTTPException as http_exception:
        return JSONResponse(content={"detail": http_exception.detail}, status_code=http_exception.status_code)
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
