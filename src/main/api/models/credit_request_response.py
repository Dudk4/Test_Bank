from typing import Optional, Union
from src.main.api.models.base_model import BaseModel


class CreditRequestResponse(BaseModel):
    id: int
    amount: Optional[Union[int, float]]
    termMonths: int
    balance: Optional[Union[int, float]]
    creditId: int