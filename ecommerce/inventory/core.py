from sqlalchemy.orm import Session
from .models import Item, ItemStock
from ecommerce.common.utils import id_str_to_uuid


# use this to create and initialize new items
def create_new_item(
    db_session: Session, sku_number: str, description: str, unit_cost_cents: int
) -> str:
    """Creates a new item in inventory and initializes inventory stock.

    Args:
        db_session (Session): The database session.
        sku_number (str): The item sku number.
        description (str): A text description of the item.
        unit_cost_cents (int): The unit cost of the item in cents.

    Returns:
        str: hex string of the item id.
    """
    item = Item(
        sku_number=sku_number,
        description=description,
        unit_cost_cents=unit_cost_cents,
        item_stock=ItemStock(),
    )
    db_session.add(item)
    db_session.commit()

    return item.id.hex


# use this function to update the quantity available of an item
def update_available(db_session: Session, item_id: str, quantity: int) -> int:
    """Updates the quantity available of an item.

    Args:
        db_session (Session): The database session.
        item_id (str): The item id.
        quantity (int): The quantity to update by.

    Returns:
        int: The available quantity of the item.
    """
    item = db_session.get(Item, item_id)
    if item is None:
        raise ValueError("Item not found")

    item.item_stock.quantity_available += quantity
    db_session.commit()

    return item.item_stock.quantity_available
