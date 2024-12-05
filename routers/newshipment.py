from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from config.config import Shipments  
from routers.Jwt_tokens import oauth2_scheme, decode_token
from Models.model import ShipmentData 
app = APIRouter()
html = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/newshipment")
def newship(request: Request):      
    return html.TemplateResponse("NewShipment.html", {"request": request})
@app.post("/newshipment_user")
def newshipment(
    request: Request, 
    shipment_details:ShipmentData ,
    token: str = Depends(oauth2_scheme)
):
    try:
        
        if any(value == "" for value in [
            shipment_details.shipment_number, shipment_details.container_number, shipment_details.goods_number, shipment_details.route_details, shipment_details.goods_type, 
            shipment_details.device_id, shipment_details.expected_delivery_date, shipment_details.po_number, shipment_details.delivery_number, shipment_details.ndc_number, 
            shipment_details.batch_id, shipment_details.shipment_description
        ]):
    
            raise HTTPException(status_code=400, detail="All fields must be filled")

        # Check if the shipment number already exists in the database
        existing_data = Shipments.find_one({"shipment_number": shipment_details.shipment_number}, {"_id": 0})
        if existing_data:
            
            raise HTTPException(status_code=400, detail="Shipment number already exists")

        
        decoded_token = decode_token(token)
        # print("decoded_token",decoded_token)

        # Prepare data for inserting into the database
        shipment_data = {
            "user": decoded_token["user"],
            "email": decoded_token["email"],
            'shipment_number': shipment_details.shipment_number,
            "container_number": shipment_details.container_number,
            "route_details": shipment_details.route_details,
            "goods_type": shipment_details.goods_type,
            "device": shipment_details.device_id,
            "expected_delivery": shipment_details.expected_delivery_date,
            "po_number": shipment_details.po_number,
            "delivery_number": shipment_details.delivery_number,
            "ndc_number": shipment_details.ndc_number,
            "batch_id": shipment_details.batch_id,
            "serial_number": shipment_details.goods_number,  # Assuming this is the goods serial number
            "shipment_description": shipment_details.shipment_description
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
        # print(e)
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
