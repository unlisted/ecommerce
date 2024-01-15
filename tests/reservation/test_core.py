import pytest
from unittest.mock import patch
from sqlalchemy.orm import Session
from ecommerce.reservation.core import create_reservation, timeout_reservation, complete_reservation, cancel_reservation
from ecommerce.reservation.models import Reservation, ReservationStatus
from ecommerce.inventory.models import Item
from ecommerce.member.models import Member, Account
from ecommerce.inventory.core import create_new_item, update_available
from ecommerce.common.utils import id_str_to_uuid


@pytest.fixture(autouse=True)
def global_scheduler():
    with patch("ecommerce.reservation.core.Schedular", autospec=True, spec_set=True) as mock:
        yield mock


def test_create_and_timeout_reservation(db_session: Session, global_scheduler):
    item_id = create_new_item(db_session, "123", "test", 1000)
    update_available(db_session, item_id, 10)

    # need to patch this session because it's not passed in to the function.
    with patch("ecommerce.reservation.core.Session", autospec=True, spec_set=True) as mock:
        mock.return_value.__enter__.return_value = db_session
        global_scheduler.enter.side_effect = lambda *args, argument: timeout_reservation(argument[0])

        reservation_id = create_reservation(db_session, item_id)

    reservation: Reservation = db_session.get(Reservation, id_str_to_uuid(reservation_id))
    assert reservation.id.hex == reservation_id
    assert reservation.item_id.hex == item_id
    assert reservation.status == ReservationStatus.TIMED_OUT
    assert db_session.get(Item, item_id).item_stock.quantity_available == 10
    # assert False


def test_complete_reservation(db_session: Session):
    item_id: Item = create_new_item(db_session, "123", "test", 1000)
    update_available(db_session, item_id, 10)

    reservation_id = create_reservation(db_session, item_id)
    assert db_session.get(Item, item_id).item_stock.quantity_available == 9
    
    complete_reservation(db_session, reservation_id)

    
    assert db_session.get(Reservation, id_str_to_uuid(reservation_id)).status == ReservationStatus.COMPLETED


def test_complete_canceled_reservation(db_session: Session):
    item_id: Item = create_new_item(db_session, "123", "test", 1000)

    update_available(db_session, item_id, 10)

    reservation_id = create_reservation(db_session, item_id)
    cancel_reservation(db_session, reservation_id)

    with pytest.raises(ValueError):
        complete_reservation(db_session, reservation_id)