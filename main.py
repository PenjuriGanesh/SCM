from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routers import signup, home, login ,forgetpassword ,dashboard ,account, newshipment , devicedata,myshipment




app = FastAPI()
templates = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(home.app)
app.include_router(signup.app)
app.include_router(forgetpassword.app)
app.include_router(login.app)
app.include_router(dashboard.app)
app.include_router(account.app)
app.include_router(myshipment.app)
app.include_router(newshipment.app)
app.include_router(devicedata.app)

