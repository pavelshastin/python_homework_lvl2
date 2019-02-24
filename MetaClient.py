import dis
import types
import socket


class MetaClient(type):
    def __init__(self, clsname, bases, clsdict):

        for name, atr in clsdict.items():
            if type(atr) is not types.FunctionType:
                if isinstance(atr, socket.socket):
                    raise TypeError("You can't create socket on class level")
            else:
                f_instr = dis.get_instructions(atr)

                for ins in f_instr:
                    if ins.opname == "LOAD_ATTR" and ins.argval == "accept":
                        print(".accept in {}-function".format(name))
                        raise TypeError("You can't use accept method on client side")

                    elif ins.opname == "LOAD_ATTR" and ins.argval == "listen":
                        print(".listen in {}-function".format(name))
                        raise TypeError("You can't use listen method on client side")

                    elif ins.opname == "LOAD_GLOBAL" and ins.argval == "socket":
                        net_type = next(f_instr).argval
                        if net_type != "AF_INET":
                            print("NOT AF_INET in {}-function".format(name))
                            raise TypeError("You need to create socket with AF_INET const")

                        stream = next(f_instr).argval
                        if stream != "SOCK_STREAM":
                            print("NOT SOCK_STREAM in {}-function".format(name))
                            raise TypeError("You need to create socket with SOCK_STREAM const")

        type.__init__(self, clsname, bases, clsdict)