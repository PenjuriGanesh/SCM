from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from config.config import Shipments  
from routers.dashboard import fetch_user_from_cookie

app = APIRouter()
html = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/myshipment")
def my_shipments(request: Request, current_user: dict = Depends(fetch_user_from_cookie)):
    if current_user is None:
        return RedirectResponse(url="/login?alert=true")

    try:
        # Fetch shipments for the authenticated user
        shipments = list(Shipments.find({"email": current_user["email"]}, {"_id": 0}))

        # If no shipments found, render with a message
        if not shipments:
            return html.TemplateResponse("Myshipment.html", {"request": request, "shipments": [], "error_message": "No shipments found for this user."})

        # Render shipments data
        return html.TemplateResponse("Myshipment.html", {"request": request, "shipments": shipments, "error_message": None})

    except Exception as e:
        return html.TemplateResponse("Myshipment.html", {"request": request, "shipments": [], "error_message": str(e)})

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
