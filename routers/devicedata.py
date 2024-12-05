from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse
from routers.dashboard import fetch_user_from_cookie

app = APIRouter()
html = Jinja2Templates(directory="Templates")

@app.get("/devicedata")
def devicedata(request: Request, current_user: dict = Depends(fetch_user_from_cookie)):
    # Check if the user is authenticated
    if not current_user:
        return RedirectResponse(url="/login?alert=true")
    # If authenticated, proceed with the usual logic
    user_role = current_user.get("role", "user")
    if user_role == "admin":
        return html.TemplateResponse("Devicedata.html", {"request": request, "role": user_role, "show_table": True})
    
    return html.TemplateResponse("Devicedata.html", {"request": request, "role": user_role, "show_table": False})

COOKIE_NAME = "access_token"  

@app.post("/logout")
async def logout(request: Request):
    try:
        response = JSONResponse(content={"message": "Logged out"})

        response.delete_cookie(COOKIE_NAME) 
        
        return response  

    except KeyError as exc:
        raise HTTPException(status_code=400, detail="Cookie name not found.") from exc
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception
