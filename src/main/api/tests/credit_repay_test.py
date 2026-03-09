import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit


@pytest.mark.api
class TestCreditRepay:
    @pytest.mark.parametrize("amount, term_months", [(5000, 12)])
    def test_credit_repay(self, db_session: Session, amount: float, term_months: int, api_manager: ApiManager,
                            create_credit_user_request: CreateUserRequest):
        account = api_manager.user_steps.create_account(create_credit_user_request)

        credit_response = api_manager.user_steps.credit_account_request(
            create_user_request=create_credit_user_request,
            account_id=account.id,
            amount=amount,
            term_months=term_months
        )

        assert credit_response.balance == amount

        repay_response = api_manager.user_steps.credit_account_repay(
            create_user_request=create_credit_user_request,
            credit_id=credit_response.creditId,
            account_id=credit_response.id,
            amount=credit_response.amount
        )

        assert repay_response.creditId == credit_response.creditId
        assert repay_response.amountDeposited == credit_response.amount

        credit_from_db = Credit.get_credit_by_id(db_session, repay_response.creditId)

        assert credit_from_db is not None, "Кредит не найден в БД после погашения"
        assert credit_from_db.id == repay_response.creditId, "В БД найден неверный кредит"
        assert credit_from_db.balance == 0, "Баланс кредита после полного погашения не равен нулю"