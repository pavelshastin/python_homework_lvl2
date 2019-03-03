from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class ContactList(Base):
    __tablename__ = "contact_list"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)

    def __init__(self, user_id):
        self.user_id = user_id


class MessageHistory(Base):
    __tablename__ = "message_history"

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=func.now())
    user_id = Column(String, ForeignKey('contact_list.id'))
    mess = Column(String)


    def __init__(self, time, user_id, mess):
        self.time = time
        self.user_id = user_id
        self.mess = mess


class ClientStorage:

    def __init__(self, name):
        eng = create_engine("sqlite:///client_{}.sqlite".format(name))

        Session = sessionmaker()
        Session.configure(bind=eng)
        self.session = Session()

        Base.metadata.create_all(eng)


    def add_message(self, dt, user_id, mess):
        self.session.add(MessageHistory(dt, user_id, mess))
        self.session.commit()

    def add_contact(self, user_id):
        self.session.add(ContactList(user_id))
        self.session.commit()

    def del_contact(self, user_id):
        user = self.session.query(ContactList).filter(ContactList.iser_id == user_id).one()
        self.session.delete(user)
        self.session.commit()

    def get_contacts(self):

        return self.session.query(ContactList).all()