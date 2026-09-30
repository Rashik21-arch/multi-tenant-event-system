from pydantic import BaseModel


class MockPaymentRequest(BaseModel):
    success: bool = True


class PaymentResponse(BaseModel):
    reservation_id: int
    payment_status: str
    reservation_status: str
    message: str