from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.foundation.requesters.crud_requester import CrudRequester


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def deposit_account(self, create_user_request: CreateUserRequest, account_id: int, amount: float):
        deposit_account_request = DepositAccountRequest(accountId=account_id, amount=amount)
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(deposit_account_request)
        return response

    def deposit_account_invalid(self, create_user_request: CreateUserRequest, account_id: int, amount: float):
        deposit_account_request = DepositAccountRequest(accountId=account_id, amount=amount)
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(deposit_account_request)

    def credit_account_request(
            self, create_user_request: CreateUserRequest, account_id: int, amount: float, term_months: int
    ):
        credit_account_request = CreditRequestRequest(accountId=account_id, amount=amount, termMonths=term_months)
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_ACCOUNT_REQUEST,
            ResponseSpecs.request_created()
        ).post(credit_account_request)
        return response

    def credit_account_repay(
            self, create_user_request: CreateUserRequest, credit_id: int, account_id: int, amount: float
    ):
        credit_account_repay = CreditRepayRequest(
            creditId=credit_id,
            accountId=account_id,
            amount=amount
        )

        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_ACCOUNT_REPAY,
            ResponseSpecs.request_ok()
        ).post(credit_account_repay)
        return response

    def transfer_account(
            self, create_user_request: CreateUserRequest, from_account_id: int, to_account_id: int, amount: float
    ):
        transfer_account_request = TransferAccountRequest(
            fromAccountId=from_account_id,
            toAccountId=to_account_id,
            amount=amount
        )

        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(transfer_account_request)
        return response
