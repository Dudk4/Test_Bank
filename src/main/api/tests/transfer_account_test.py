import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestTransferAccount:
    @pytest.mark.parametrize("deposit_amount, transfer_amount", [(1000.5, 500.75)])
    def test_transfer_account(self, db_session: Session, deposit_amount: float, transfer_amount: float,
                              api_manager: ApiManager, create_user_request: CreateUserRequest):
        first_account = api_manager.user_steps.create_account(create_user_request)
        second_account = api_manager.user_steps.create_account(create_user_request)

        deposit_response = api_manager.user_steps.deposit_account(
            create_user_request=create_user_request,
            account_id=first_account.id,
            amount=deposit_amount
        )

        assert deposit_response.id == first_account.id
        assert deposit_response.balance == deposit_amount

        transfer_response = api_manager.user_steps.transfer_account(
            create_user_request=create_user_request,
            from_account_id=first_account.id,
            to_account_id=second_account.id,
            amount=transfer_amount
        )

        assert transfer_response.fromAccountId == first_account.id
        assert transfer_response.toAccountId == second_account.id
        assert transfer_response.fromAccountIdBalance == deposit_amount - transfer_amount

        first_account_db = Account.get_account_by_id(db_session, first_account.id)
        second_account_db = Account.get_account_by_id(db_session, second_account.id)

        assert first_account_db.id == first_account.id, "Первый аккаунт не создан, id аккаунта нет в БД"
        assert second_account_db.id == second_account.id, "Второй аккаунт не создан, id аккаунта нет в БД"
        assert first_account_db.balance == transfer_response.fromAccountIdBalance, \
            "Баланс первого аккаунта в БД некорректен после перевода"
        assert second_account_db.balance == transfer_amount, \
            "Баланс второго аккаунта в БД некорректен после перевода"
