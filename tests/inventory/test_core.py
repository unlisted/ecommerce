from sqlalchemy import select

from ecommerce.inventory.core import create_new_item, update_available
from ecommerce.inventory.models import Item, ItemStock
from ecommerce.common.utils import id_str_to_uuid



def test_create_item(db_session):
    create_new_item(db_session, "123", "test", 1000)

    results = db_session.execute(select(Item)).scalars().all()
    assert len(results) == 1
    assert results[0].sku_number == "123"
    assert results[0].description == "test"
    assert results[0].unit_cost_cents == 1000
    assert results[0].item_stock.quantity_available == 0


def test_update_available(db_session):
    item_id = create_new_item(db_session, "123", "test", 1000)

    assert db_session.get(Item, item_id).id.hex == item_id
    assert db_session.execute(select(ItemStock)).scalars().all()[0].quantity_available == 0
    
    update_available(db_session, item_id, 10)

    assert db_session.execute(select(ItemStock)).scalars().all()[0].quantity_available == 10
