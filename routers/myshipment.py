from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from config.config import Shipments  
from routers.Jwt_tokens import get_current_user
from routers.dashboard import fetch_user_from_cookie

app = APIRouter()
html = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/myshipment")
def my_shipments(request: Request, current_user: dict = Depends(fetch_user_from_cookie)):
    try:
        # current_user will be populated from the token
        if current_user is None:
            raise HTTPException(status_code=401, detail="Not authenticated")

        shipments = list(Shipments.find({"email": current_user["email"]}, {"_id": 0}))

        # If no shipments found for the user, raise a 404 error
        if not shipments:
            raise HTTPException(status_code=404, detail="No shipments found for this user.")

        return html.TemplateResponse("Myshipment.html", {"request": request, "shipments": shipments, "error_message": None})

    except HTTPException as http_error:
        return html.TemplateResponse("Myshipment.html", {"request": request, "shipments": [], "error_message": http_error.detail})
    except Exception as e:
        return html.TemplateResponse("Myshipment.html", {"request": request, "shipments": [], "error_message": str(e)})



COOKIE_NAME = "access_token"  
@app.post("/logout")
async def logout(request: Request):
    try:
        # Create a response object to handle logout and clear the cookie
        response = JSONResponse(content={"message": "Logged out"})
        
        response.delete_cookie(COOKIE_NAME, path="/",domain=None)
        
        return response  # Return the response indicating successful logout

    except KeyError as exc:
        raise HTTPException(status_code=400, detail="Cookie name not found.") from exc
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception
