from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from config.config import Shipments  
from fastapi.security import OAuth2PasswordBearer
from routers.Jwt_tokens import oauth2_scheme, decode_token
from Models.model import ShipmentData 
app = APIRouter()
html = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@app.get("/newshipment")
def newship(request: Request):      
    return html.TemplateResponse("NewShipment.html", {"request": request})
@app.post("/newshipment_user")
def newshipment(
    request: Request,
    shipment_number: int = Form(...),
    container_number: int = Form(...),
    goods_number: int = Form(...),
    route_details: str = Form(...),
    goods_type: str = Form(...),
    device_id: int = Form(...),
    expected_delivery_date: str = Form(...),
    po_number: int = Form(...),
    delivery_number: int = Form(...),
    ndc_number: int = Form(...),
    batch_id: int = Form(...),
    shipment_description: str = Form(...),
    token: str = Depends(oauth2_scheme)
):
    print(device_id)
    try:
        # Check if any field is empty
        if any(value == "" for value in [
            shipment_number, container_number, goods_number, route_details, goods_type, 
            device_id, expected_delivery_date, po_number, delivery_number, ndc_number, 
            batch_id, shipment_description
        ]):
            print('in the if')
            raise HTTPException(status_code=400, detail="All fields must be filled")

        # Check if shipment_number has exactly 7 characters
        if len(str(shipment_number)) != 7:  # Convert to string to check length
            print('in the length')
            raise HTTPException(status_code=400, detail="Shipment number must be 7 characters")
        
        # Check if the shipment number already exists in the database
        existing_data = Shipments.find_one({"shipment_number": shipment_number}, {"_id": 0})
        if existing_data:
            print('in the existing')
            raise HTTPException(status_code=400, detail="Shipment number already exists")

        # Decode token to get user email (extracting the token after 'Bearer ')
        decoded_token = decode_token(token)
        # print("decoded_token",decoded_token)

        # Prepare data for inserting into the database
        shipment_data = {
            "user": decoded_token["username"],
            "email": decoded_token["email"],
            'shipment_number': shipment_number,
            "container_number": container_number,
            "route_details": route_details,
            "goods_type": goods_type,
            "device": device_id,
            "expected_delivery": expected_delivery_date,
            "po_number": po_number,
            "delivery_number": delivery_number,
            "ndc_number": ndc_number,
            "batch_id": batch_id,
            "serial_number": goods_number,  # Assuming this is the goods serial number
            "shipment_description": shipment_description
        }

        # Insert shipment data into the database
        Shipments.insert_one(shipment_data)

        # Return a success message as a JSON response
        return JSONResponse(content={"message": "Shipment Created Successfully"}, status_code=200)

    except HTTPException as http_error:
        # Handle HTTP exceptions (e.g., missing fields, invalid shipment number)
        return JSONResponse(content={"error_message": http_error.detail}, status_code=http_error.status_code)
    except Exception as e:
        # Handle other exceptions (e.g., database issues)
        return JSONResponse(content={"detail": str(e)}, status_code=500)


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