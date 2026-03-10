import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreditRequest:
    @pytest.mark.parametrize("amount, term_months", [(5000, 12)])
    def test_credit_request(self, db_session: Session, amount: float, term_months: int, api_manager: ApiManager,
                            create_credit_user_request: CreateUserRequest, create_credit_user_account_request):
        response = api_manager.user_steps.credit_account_request(
            create_user_request=create_credit_user_request,
            account_id=create_credit_user_account_request.id,
            amount=amount,
            term_months=term_months
        )

        assert response.balance == amount

        credit_from_db = Credit.get_credit_by_id(db_session, response.creditId)

        assert credit_from_db.id == response.creditId, "Кредит не создан, id кредита нет в БД"
        assert credit_from_db.amount == response.amount, "Кредит в БД создался с неверной суммой"
