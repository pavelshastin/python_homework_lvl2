

class Chat:

    def __init__(self, name):
        self.__name = name.upper()
        self.__users = {}
        self.__messages = []



    def add_user(self, name):
        if name in self.__users:
            raise ValueError("There is a person with given account")
        else:
            self.__users.update({name.title(): 0})


    def remove_user(self, name):
        if name in self.__users:
            del self.__users[name]
        else:
            raise Exception("There is NO person with given account")


    def get_messages(self, to_whom):
        #Giving only last messages
        last = self.__users[to_whom]
        self.__users[to_whom] = len(self.__messages)
        return self.__messages[last:]


    def add_message(self, msg, from_whom):
        if self.__verify_user(from_whom):
            self.__messages.append((from_whom, msg))
        else:
            raise Exception("There is no such account")


    def get_all_msgs(self):
        return self.__messages

    @property
    def name(self):
        return self.__name


    def __verify_user(self, user):
        if user in self.__users:
            return True
        else:
            return False


    def __msg_to_db(self):
        pass



