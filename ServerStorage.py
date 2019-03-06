from sqlalchemy import create_engine, func, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import ForeignKeyConstraint
import json

Base = declarative_base()


class Clients(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True)
    info = Column(String)

    def __init__(self, user_id, info):
        self.user_id = user_id
        self.info = info


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, default=func.now())
    _from = Column(String)
    _from_ip = Column(String)
    _to = Column(String)
    _to_ip = Column(String)
    message = Column(String)

    def __init__(self, _from, _from_ip, _to, _to_ip, message):
        self._from = _from
        self._from_ip = _from_ip
        self._to = _to
        self._to_ip = _to_ip
        self.message = message

class Contacts(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("clients.user_id"))
    contacts = Column(String, ForeignKey("clients.user_id"))


class ServerStorage:

    def __init__(self):
        eng = create_engine("sqlite:///server.sqlite", connect_args={'check_same_thread': False})

        Session = sessionmaker()
        Session.configure(bind=eng)
        self.session = Session()

        Base.metadata.create_all(eng)

    def get_user(self, user_id):
        pass

    def add_user(self, user_id, info):
        if self.session.query(Clients).filter(Clients.user_id == user_id).one():
            return False

        user = Clients(user_id, info)
        self.session.add(user)
        self.session.commit()




    def get_messages(self, user_id):
        pass

    def get_messages_to_user(self, user_id, _to):
        pass


    def get_contacts(self, user_id):
        try:
            q = self.session.query(Contacts).filter(Contacts.user_id == user_id).all()

            if len(q) == 0:

                rows = self.session.query(Clients).all()

                return [row.user_id for row in rows]

            return [row.user_id for row in q]
        except:
            pass


    def add_contact(self, user_id, contact):
        print("Add_contact", user_id, contact)
        contact = Contacts(user_id, contact)
        self.session.add(contact)
        self.session.commit()

        print("Query", self.session.query(Contacts).all())

        return True
