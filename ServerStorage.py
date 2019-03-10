from sqlalchemy import create_engine, func, update, not_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, ForeignKeyConstraint
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.schema import ForeignKeyConstraint
import json

Base = declarative_base()


class Clients(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True)
    password = Column(String)
    cont_rel = relationship("Contacts")

    def __init__(self, user_id, pswd):
        self.user_id = user_id
        self.password = pswd


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
    user_id = Column(String)
    contact = Column(String)

    __table_args__ = (
        ForeignKeyConstraint([user_id, contact], ['clients.user_id', 'clients.user_id']),

    )

    def __init__(self, user_id, contact):
        self.user_id = user_id
        self.contact = contact


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
        try:
            q = self.session.query(Clients).filter(Clients.user_id == user_id).one()

            return False
        except:
            user = Clients(user_id, info)
            self.session.add(user)
            self.session.commit()

            return True


    def authenticate(self, user_id, pswd):
        try:

            q = self.session.query(Clients).filter(Clients.user_id == user_id).one()

            if q.password != pswd:
                return False

            return True
        except:

            return False


    def get_users_all(self):
        try:
            q = self.session.query(Clients).all()

            return [row.user_id for row in q]
        except:
            return False


    def get_messages(self, user_id):
        pass

    def get_messages_to_user(self, user_id, _to):
        pass


    def get_contacts(self, user_id):
        try:
            q = self.session.query(Contacts).all()
            return [row.user_id for row in q]
        except:

            return False


    def get_potencials(self, user_id):
        # try:
        contacts = self.session.query(Contacts).all()
        contacts = [r.user_id for r in contacts]
        contacts.append(user_id)

        potencials = self.session.query(Clients).filter(not_(Clients.user_id.in_(contacts))).all()

        return [row.user_id for row in potencials]
        # except:
        #     return False



    def add_contact(self, user_id, contact):
        print("Add_contact", user_id, contact)

        contact = Contacts(user_id, contact)
        self.session.add(contact)
        self.session.commit()

        return True


    def del_contact(self, user_id, contact):

        try:
            contact = self.session.query(Contacts).filter(and_(Contacts.user_id == user_id,
                                                               Contacts.contact == contact)).one()
            self.session.delete(contact)
            self.session.commit()
            return True

        except:
            return False
