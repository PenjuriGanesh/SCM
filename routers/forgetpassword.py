from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app=APIRouter()
html=Jinja2Templates(directory="Templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/forgetpassword")
def forget(request: Request):
    return html.TemplateResponse("Forget_password.html",{"request" : request})