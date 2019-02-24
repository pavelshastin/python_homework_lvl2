import types
import socket
import dis

class MetaServer(type):
    def __init__(self, clsname, bases, clsdict):

        for name, atr in clsdict.items():
            if type(atr) is not types.FunctionType:
                if isinstance(atr, socket.socket):
                    raise TypeError("You can't create sockets on class level")

            else:
                f_instr = dis.get_instructions(atr)

                for ins in f_instr:

                    if ins.opname == "LOAD_ATTR" and ins.argval == "connect":
                        print("Connect method in {}-function".format(name))
                        raise TypeError("The Server can't use connect-method of a socket")

                    elif ins.opname == "LOAD_GLOBAL" and ins.argval == "socket":
                        net_type = next(f_instr).argval
                        if net_type is not "AF_INET":
                            print("Connect method in {}-function".format(name))
                            raise TypeError("You need to create socket with AF_INET const")

                        stream = next(f_instr).argval
                        if stream is not "SOCK_STREAM":
                            print("Connect method in {}-function".format(name))
                            raise TypeError("You need to create socket with SOCK_STREAM const")

        for name, atr in clsdict.items():
            if type(atr) is types.FunctionType:
                print(name, atr)

        type.__init__(self, clsname, bases, clsdict)


