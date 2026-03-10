import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.create_user_request import CreateUserRequest
from dataclasses import dataclass


@pytest.fixture
def create_credit_user_account_request(api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest):
    return api_manager.user_steps.create_account(create_credit_user_request)


@pytest.fixture
def create_account_request(api_manager: ApiManager, create_user_request: CreateUserRequest):
    return api_manager.user_steps.create_account(create_user_request)


@dataclass
class TransferAccountsRequest:
    first_account: any
    second_account: any
    deposit_amount: float


@pytest.fixture
def transfer_accounts_request(api_manager: ApiManager, create_user_request: CreateUserRequest):
    first_account = api_manager.user_steps.create_account(create_user_request)
    second_account = api_manager.user_steps.create_account(create_user_request)
    deposit_amount = 1000.5

    api_manager.user_steps.deposit_account(
        create_user_request=create_user_request,
        account_id=first_account.id,
        amount=deposit_amount
    )

    return TransferAccountsRequest(first_account=first_account, second_account=second_account, deposit_amount=deposit_amount)
