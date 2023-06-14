from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://dev:revbotdev@localhost/myrevbot', echo=True)
Session = sessionmaker(bind=engine)

from revbot.models import Base, Customer, Contract, RevenueSegment, Invoice 

def reset_and_init_db():
    # First reflect and drop all tables to delete contents of database
    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(bind=engine)

    # Then create all tables
    Base.metadata.create_all(engine)

def create_session():
    return Session()

def remove_session(session):
    session.close()