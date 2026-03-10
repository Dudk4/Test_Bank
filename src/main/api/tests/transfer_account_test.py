import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestTransferAccount:
    @pytest.mark.parametrize("transfer_amount", [500.75])
    def test_transfer_account(self, db_session: Session, transfer_amount: float, api_manager: ApiManager,
                              create_user_request: CreateUserRequest, transfer_accounts_request):
        transfer_response = api_manager.user_steps.transfer_account(
            create_user_request=create_user_request,
            from_account_id=transfer_accounts_request.first_account.id,
            to_account_id=transfer_accounts_request.second_account.id,
            amount=transfer_amount
        )

        assert transfer_response.fromAccountIdBalance == transfer_accounts_request.deposit_amount - transfer_amount

        second_account_db = Account.get_account_by_id(db_session, transfer_accounts_request.second_account.id)

        assert second_account_db.balance == transfer_amount, \
            "Баланс второго аккаунта в БД некорректен после перевода"
