import requests
from requests import Response
from src.main.api.models.transactions_response import TransactionsResponse
from src.main.api.requests.requester import GetRequester


class TransactionsRequester(GetRequester):
    def get(self, get_id) -> TransactionsResponse | Response:
        url = f"{self.base_url}/account/transactions/{get_id}"
        response = requests.get(
            url=url,
            headers=self.headers
        )
        self.response_spec(response)
        return TransactionsResponse(**response.json())
