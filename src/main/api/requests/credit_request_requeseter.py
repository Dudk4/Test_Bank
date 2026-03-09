import requests
from requests import Response
from src.main.api.models.credit_request_response import CreditRequestResponse
from src.main.api.requests.requester import Requester
from src.main.api.models.credit_request_request import CreditRequestRequest


class CreditRequestRequester(Requester):
    def post(self, credit_request: CreditRequestRequest) -> CreditRequestResponse | Response:
        url = f"{self.base_url}/credit/request"
        response = requests.post(
            url=url,
            json=credit_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        return CreditRequestResponse(**response.json())
