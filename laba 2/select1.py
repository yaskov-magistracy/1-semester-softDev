from session import *
from main import *

query = (select(User).options(selectinload(User.addresses)))

with session_factory() as session:
    print(session.execute(query).scalars().all())