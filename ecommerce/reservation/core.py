from sqlalchemy.orm import Session as OrmSession
from .models import Reservation, ReservationStatus
from ecommerce.inventory.models import Item
from ecommerce.common.utils import id_str_to_uuid
from ecommerce.common.global_sched import Schedular
from ecommerce.common.db import Session


def create_reservation(db_session: OrmSession, item_id: str) -> str:
    """Creates a new reservation for an item. A simple scheduled event is also created as a side-efffect.
    The event triggers 15 minutes in the future and attempts the delete the reservation. If the reservation
    has already been completed or canceled then the event does nothing.

    Args:
        db_session (OrmSession): The database session.
        item_id (str): The item id.

    Returns:
        str: The hex string of the reservation id.
    """

    item = db_session.get(Item, item_id)
    if item is None:
        raise ValueError("Item not found")

    if item.item_stock.quantity_available == 0:
        raise ValueError("Item quantity == 0")

    item.item_stock.quantity_available -= 1

    reservation = Reservation(item=item)
    db_session.add(reservation)

    db_session.commit()

    # run scheduled task in thread to delete reservation after 15 seconds
    Schedular.enter(15 * 1000, 1, timeout_reservation, argument=(reservation.id.hex,))

    return reservation.id.hex


def cancel_reservation(db_session: OrmSession, reservation_id: str) -> None:
    """Cancels a reservation.

    Args:
        db_session (OrmSession): The database session.
        reservation_id (str): The reservation id.
    """
    reservation = db_session.get(Reservation, id_str_to_uuid(reservation_id))
    if reservation is None:
        raise ValueError("Reservation not found")

    reservation.status = ReservationStatus.CANCELED
    reservation.item.item_stock.quantity_available += 1
    db_session.commit()


def timeout_reservation(reserversaion_id: str) -> None:
    with Session() as db_session:
        reservation = db_session.get(Reservation, id_str_to_uuid(reserversaion_id))
        if reservation is None:
            raise ValueError("Reservation not found")
        if reservation.status != ReservationStatus.ACTIVE:
            return
        reservation.status = ReservationStatus.TIMED_OUT
        reservation.item.item_stock.quantity_available += 1
        db_session.commit()


def complete_reservation(db_session: OrmSession, reservation_id: str) -> None:
    """Completes a reservation, reduces item quantity by 1.

    Args:
        reservation_id (str): The hex of reservation id UUID.

    Raises:
        ValueError:
    """
    reservation = db_session.get(Reservation, id_str_to_uuid(reservation_id))
    if reservation is None:
        raise ValueError("Reservation not found")

    if reservation.status != ReservationStatus.ACTIVE:
        raise ValueError("Reservation not active")

    if reservation.item.item_stock.quantity_available == 0:
        raise ValueError("Item quantity == 0")

    reservation.status = ReservationStatus.COMPLETED
    db_session.commit()
