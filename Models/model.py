from pydantic import BaseModel
from datetime import datetime


class Signup_details(BaseModel):
    user:str
    email: str
    password: str
    role: str

class Signup(BaseModel):
    user: str
    email: str
    role: str
    password: str
    created_at: datetime = datetime.now()   

class ShipmentData(BaseModel):
    shipment_number: int
    route_details: str
    device: int
    po_number: int
    ndc_number: int
    serial_number: int
    container_number: int
    goods_type: str
    expected_delivery_date: str
    delivery_number: int
    batch_id: int
    shipment_description: str

class DeviceData(BaseModel):
    Battery_Level: float
    Device_Id: int
    First_Sensor_temperature: float
    Route_From: str
    Route_To: str

