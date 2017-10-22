from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup_user import Base , User , Password
engine = create_engine('sqlite:///account.db')
Base.metadata.create_all(engine)
DBsession = sessionmaker(bind = engine)
session = DBsession()

user = User(name = "jaybe")
password = Password(password = "8888",user = user)
session.add(user)
session.add(password)
session.commit()
session.query(User).all()
