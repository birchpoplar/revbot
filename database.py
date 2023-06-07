from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from defs import Base  # Assuming models.py is in the same directory

engine = create_engine('postgresql://dev:revbotdev@localhost/myrevbot')
Session = sessionmaker(bind=engine)

def reset_and_init_db():
    # First reflect and drop all tables to delete contents of database
    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(bind=engine)

    # Then create all tables
    Base.metadata.create_all(engine)
