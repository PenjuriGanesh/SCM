from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from routers.dashboard import fetch_user_from_cookie

# Initialize the FastAPI router and templates
app = APIRouter()
html = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/account")
async def account(request: Request, user: dict = Depends(fetch_user_from_cookie)):
    if not user:
        return RedirectResponse(url="/login?alert=true")

    # Extract username and email from the user data
    username = user.get("user") 
    email = user.get("email")

    return html.TemplateResponse(
        "Account.html", {"request": request, "username": username, "email": email}
    )

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
