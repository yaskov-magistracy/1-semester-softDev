from session import *
from main import *

with session_factory() as session:
    user = User(login="123", email="321")
    session.add(user)
    session.commit()