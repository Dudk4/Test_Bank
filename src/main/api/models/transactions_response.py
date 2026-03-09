from typing import Optional, List
from src.main.api.models.base_model import BaseModel


class Transactions(BaseModel):
    transactionId: int
    type: str
    amount: float
    fromAccountId: int
    toAccountId: int
    createdAt: str
    creditId: Optional[int] = None

class TransactionsResponse(BaseModel):
        id: int
        number: str
        balance: float
        transactions: List[Transactions]
