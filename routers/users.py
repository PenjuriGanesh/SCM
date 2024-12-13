from fastapi import APIRouter, Request, Depends, Form, HTTPException, Body
from fastapi.responses import RedirectResponse, JSONResponse
from config.config import User_details
from routers.dashboard import fetch_user_from_cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = APIRouter()
html = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/users")
def admin_page(request: Request, current_user: dict = Depends(fetch_user_from_cookie)):
    if current_user is None:
        return RedirectResponse(url="/login?alert=true")

    try:

        if current_user.get("role") == "admin":
            users = list(User_details.find({}, {"_id": 0}))  
        elif current_user.get("role") == "user":
            
            return html.TemplateResponse("Users.html", {"request": request, "user_details": [], "error_message": "You are a normal user and do not have access to this page."})
        else:
            return RedirectResponse(url="/dashboard?alert=unauthorized")

        
        return html.TemplateResponse("Users.html", {"request": request, "user_details": users})

    except Exception as e:
        return html.TemplateResponse("Users.html", {"request": request, "user_details": [], "error_message": str(e)})


@app.put("/update_user")
async def update_user(
    request: Request,
    data: dict = Body(...), 
    current_user: dict = Depends(fetch_user_from_cookie)
):
    if current_user is None:
        return JSONResponse(status_code=400, content={"detail": "User not logged in."})

    try:
        if current_user.get("role") != "admin":
            return JSONResponse(status_code=403, content={"detail": "Unauthorized."})

        user = data.get("user")
        role = data.get("role")

        
        user_to_update = User_details.find_one({"user": user})

        if user_to_update:
            
            result = User_details.update_one(
                {"user": user},  
                {"$set": {"role": role}}  
            )

            if result.matched_count > 0:
                return JSONResponse(status_code=200, content={"detail": "User updated successfully!"})
            else:
                return JSONResponse(status_code=404, content={"detail": "User not found or no changes made."})
        else:
            return JSONResponse(status_code=404, content={"detail": "User not found."})

    except Exception as e:
        
        return JSONResponse(status_code=500, content={"detail": str(e)})


COOKIE_NAME = "access_token"


@app.post("/logout")
async def logout(request: Request):
    try:
        
        response = JSONResponse(content={"message": "Logged out"})
        response.delete_cookie(COOKIE_NAME, path="/", domain=None)
        return response
    except KeyError as exc:
        raise HTTPException(status_code=400, detail="Cookie name not found.") from exc
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception))
