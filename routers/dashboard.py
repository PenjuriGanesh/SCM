from fastapi import APIRouter, Depends,HTTPException,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from Models.model import Signup
from fastapi.responses import JSONResponse,RedirectResponse
from routers.Jwt_tokens import decode_token

app=APIRouter()
html=Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory= "static"), name = "static")


def fetch_user_from_cookie(request: Request) -> Signup:
    token = request.cookies.get("access_token")
    # print("tokentoken",token)
    user = decode_token(token)
    return user

@app.get("/dashboard")
def dashboard(request: Request, current_user: dict = Depends(fetch_user_from_cookie)):
    if current_user is None:
        # Redirect to login with alert parameter
        return RedirectResponse(url="/login?alert=true")
    
    # If authenticated, render the dashboard page
    return html.TemplateResponse("Dashboard.html", {"request": request})
COOKIE_NAME = "access_token"  
@app.post("/logout")
async def logout(request: Request):
    try:
        # Create a response object to handle logout and clear the cookie
        response = JSONResponse(content={"message": "Logged out"})
        
        response.delete_cookie(COOKIE_NAME)  # Clear the 'access_token' cookie
        
        return response  # Return the response indicating successful logout

    except KeyError as exc:
        raise HTTPException(status_code=400, detail="Cookie name not found.") from exc
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception
