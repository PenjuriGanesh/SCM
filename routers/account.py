from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from routers.dashboard import fetch_user_from_cookie

# Initialize the FastAPI router and templates
app = APIRouter()
html = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/account")
async def account(request: Request, user: dict = Depends(fetch_user_from_cookie)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found or not authenticated")
    print("hello :",user)
    # Extract the username and email (or other details you want to show)
    username = user.get("user") 
    email = user.get("email")        

    if not username:
        raise HTTPException(status_code=404, detail="User's username not found")

    # Pass the username and email to the template
    return html.TemplateResponse("Account.html", {"request": request, "username": username, "email": email})
 

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
