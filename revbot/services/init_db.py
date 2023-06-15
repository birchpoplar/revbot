from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session

def create_engine_and_session(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True, connect_args={'sslmode':'require'})
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)

    from revbot.models import Base, Customer, Contract, RevenueSegment, Invoice 

    def reset_and_init_db():
        # First reflect and drop all tables to delete contents of database
        meta = MetaData()
        meta.reflect(bind=engine)
        meta.drop_all(bind=engine)

        # Then create all tables
        Base.metadata.create_all(engine)
 
    return reset_and_init_db, Session