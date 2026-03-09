import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestDepositAccount:
    @pytest.mark.parametrize("amount", [1000.5])
    def test_deposit_account_valid(self, db_session: Session, amount: float, api_manager: ApiManager, create_user_request: CreateUserRequest):
        account = api_manager.user_steps.create_account(create_user_request)

        response = api_manager.user_steps.deposit_account(
            create_user_request=create_user_request,
            account_id=account.id,
            amount=amount
        )

        assert response.id == account.id
        assert response.balance == amount

        account_from_db = Account.get_account_by_id(db_session, account.id)

        assert account_from_db.id == account.id, "Аккаунт не создан, id аккаунта нет в БД"
        assert account_from_db.balance == amount, "Пополнение баланса аккаунта не произошло в БД"

    @pytest.mark.parametrize(
        "amount",
        [
            999.99,
            9000.01
        ]
    )
    def test_deposit_account_invalid(self, db_session: Session, amount: float, api_manager: ApiManager,
                                     create_user_request: CreateUserRequest):
        account = api_manager.user_steps.create_account(create_user_request)

        api_manager.user_steps.deposit_account_invalid(
            create_user_request=create_user_request,
            account_id=account.id,
            amount=amount
        )

        account_from_db = Account.get_account_by_id(db_session, account.id)

        assert account_from_db.id == account.id, "Аккаунт не создан, id аккаунта нет в БД"
        assert account_from_db.balance == 0, "Произошло пополнение баланса аккаунта в БД"