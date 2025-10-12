from session import *
from main import *

with session_factory() as session:
    user = session.execute(select(User)).scalar_one()
    address = Address(user_id=user.id, street="SoftDev-street")
    session.add(address)
    for i in range(5):
        product = Product(name=f'newProduct-${i}')
        session.add(product)
        order = Order(date=datetime.now, user_id=user.id, address_id=address.id, product_id=product.id)

    session.commit()
