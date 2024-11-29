from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from routers.dashboard import fetch_user_from_cookie

app = APIRouter()
html = Jinja2Templates(directory="Templates")

@app.get("/devicedata")
def devicedata(request: Request, current_user: dict = Depends(fetch_user_from_cookie)):
    # print(current_user)
    # Check the user's role
    user_role = current_user.get("role")

    if user_role == "admin":
        # If the user is an admin, return device data page
        return html.TemplateResponse("Devicedata.html", {"request": request, "role": user_role, "show_table": True})
    elif user_role == "user":
        # If the user is a regular user, return the page but hide the table
        return html.TemplateResponse("Devicedata.html", {"request": request, "role": user_role, "show_table": False})

    # Pass user role to the template, no need for anything specific here for this case
    return html.TemplateResponse("Devicedata.html", {"request": request, "role": user_role, "show_table": False})

COOKIE_NAME = "access_token"  

@app.post("/logout")
async def logout(request: Request):
    try:
        # Create a response object to handle logout and clear the cookie
        response = JSONResponse(content={"message": "Logged out"})
        
        response.delete_cookie(COOKIE_NAME, path="/", domain=None) 
        
        return response  # Return the response indicating successful logout

    except KeyError as exc:
        raise HTTPException(status_code=400, detail="Cookie name not found.") from exc
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception
