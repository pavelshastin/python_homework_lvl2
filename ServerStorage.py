from sqlalchemy import create_engine, func, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import sessionmaker
import json

Base = declarative_base()


class Clients(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    info = Column(String)

    def __init__(self, user_id, info):
        self.user_id = user_id
        self.info = info

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
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

    user_id = Column(Integer, primary_key=True)
    contacts = Column(String)


class ServerStorage:

    def __init__(self):
        eng = create_engine("sqlite:///server.sqlite")

        Session = sessionmaker()
        Session.configure(bind=eng)
        self.session = Session()

        Base.metadata.create_all(eng)

    def get_user(self, user_id):
        pass

    def add_user(self, user_id, info):
        user = Clients(user_id, info)
        self.session.add(user)
        self.session.commit()



    def get_messages(self, user_id):
        pass

    def get_messages_to_user(self, user_id, _to):
        pass


    def get_contacts(self, user_id):
        try:
            user = self.session.query(Clients).filter(Clients.user_id == user_id).one()
            conts_str = self.session.query(Contacts).filter(Contacts.user_id == user.id)

            conts_list = conts_str.split(",")

            return self.session.query(Clients).filter(Clients.id in conts_list).all()

        except:
            pass


    def add_contact(self, user_id, contact):
        print("add_contact", user_id, contact)
        print(self.session.query(Clients).all())
        user = self.session.query(Clients).filter(Clients.user_id == user_id).one()
        print("user", user)
        cont = self.session.query(Clients).filter(Clients.user_id == contact).one()

        print("Add_contact", user, cont)
        conts = self.session.query(Contacts).filter(Contacts.user_id == user.id).one()
        conts = conts + cont.id + ","

        print("conts", conts)
        self.session.query(Contacts).filter(Contacts.user_id == user.id).update({'contacts': conts})
        self.session.commit()

        return True
