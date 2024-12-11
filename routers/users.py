from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from config.config import User_details  # Import User_details from config
from routers.dashboard import fetch_user_from_cookie

app = APIRouter()
html = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/users")
def admin_page(request: Request, current_user: dict = Depends(fetch_user_from_cookie)):
    if current_user is None:
        return RedirectResponse(url="/login?alert=true")

    try:
        # Fetch all user details from User_details collection
        if current_user.get("role") == "admin":
            users = list(User_details.find({}, {"_id": 0}))  # Fetch all fields except _id
        else:
            # If the current user is not an admin, restrict access
            return RedirectResponse(url="/dashboard?alert=unauthorized")

        # Pass the fetched data to the template
        return html.TemplateResponse(
            "Users.html",
            {"request": request, "user_details": users},
        )

    except Exception as e:
        return html.TemplateResponse(
            "Users.html",
            {"request": request, "user_details": [], "error_message": str(e)},
        )

COOKIE_NAME = "access_token"
@app.post("/logout")
async def logout(request: Request):
    try:
        # Create a response object to handle logout and clear the cookie
        response = RedirectResponse(url="/login?alert=loggedout")
        response.delete_cookie(COOKIE_NAME, path="/", domain=None)
        return response

    except KeyError as exc:
        raise HTTPException(status_code=400, detail="Cookie name not found.") from exc
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception
