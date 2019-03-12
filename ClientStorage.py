from sqlalchemy import create_engine, func, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class ContactList(Base):
    __tablename__ = "contact_list"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True)

    def __init__(self, user_id):
        self.user_id = user_id


class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=func.now())
    _from = Column(String)
    _to = Column(String)
    mess = Column(String)


    def __init__(self, _from, _to, mess):
        self._from = _from
        self._to = _to
        self.mess = mess


class ClientStorage:

    def __init__(self, name):
        eng = create_engine("sqlite:///clients_dbs/client_{}.sqlite".format(name),
                            connect_args={'check_same_thread': False})

        Session = sessionmaker()
        Session.configure(bind=eng)
        self.session = Session()

        Base.metadata.create_all(eng)


    def add_message(self, _from, _to, mess):
        self.session.add(Messages(_from, _to, mess))
        self.session.commit()


    def get_messages(self, num):
        return self.session.query(Messages).order_by(desc(Messages.id)).limit(num).all()


    def add_contact(self, user_id):
        try:
            self.session.query(ContactList).filter(ContactList.user_id == user_id).one()
            return False
        except:
            self.session.add(ContactList(user_id))
            self.session.commit()
            return True


    def del_contact(self, user_id):
        try:
            user = self.session.query(ContactList).filter(ContactList.iser_id == user_id).one()
            self.session.delete(user)
            self.session.commit()
            return True
        except:
            return False


    def get_contacts(self):
        q = self.session.query(ContactList).all()
        return [r.user_id for r in q]