from subprocess import Popen
import os
CREATE_NEW_CONSOLE = None

if os.name == "nt":
    from subprocess import CREATE_NEW_CONSOLE


while True:

    inp = input("Start subprocess (s), cancel (x), quit (q): ")

    if inp == "q":
        break

    if inp == "s":
        p_list = []

        users = [("Pavel", "Password"), ("Alex", "Password"), ("Me", "Password"),
                 ("Sveta", "Password"), ("Girl", "Password"), ("Pavel_2", "Password")].__iter__()

        for _ in range(3):
            user = next(users)
            p_list.append(Popen(["python3", "client.py", "-w", "-un",  user[0], "-pw", user[1]],
                                CREATE_NEW_CONSOLE, shell=True))

        for _ in range(3):
            user = next(users)
            p_list.append(Popen(["python3", "client.py", "-r", "-un",  user[0], "-pw", user[1]],
                                CREATE_NEW_CONSOLE, shell=True))


    if inp == "x":
        for p in p_list:
            p.kill()
        p_list.clear()