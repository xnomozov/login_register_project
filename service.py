from db import cur, conn
from models import User
from sessions import Session
import utils
from colorama import Fore

session: Session = Session()


def get_data(parameter: str, input_atr: str | int) -> tuple:
    cur.execute(f"""SELECT * FROM users where {parameter} = %s """, (input_atr,))
    return cur.fetchone()


def login() -> utils:
    if session.check_session():
        return utils.BadRequest('You already logged in', status_code=401)
    username: str = input(Fore.LIGHTWHITE_EX + "Enter your username please: " + Fore.RESET)
    password: str = input(Fore.LIGHTWHITE_EX + "Enter your password please: " + Fore.RESET)
    data_user: tuple = get_data(parameter='username', input_atr=username)
    if not data_user:
        return utils.BadRequest('Wrong password or username')
    _user = User(user_id=data_user[0], username=data_user[1], password=data_user[2], role=data_user[3],
                 status=data_user[4],
                 login_try_count=data_user[5])

    if password != _user.password:
        update_count_query = """update users set login_try_count = login_try_count + 1 where username = %s;"""
        cur.execute(update_count_query, (_user.username,))
        conn.commit()
        return utils.BadRequest('Wrong password or username', status_code=401)

    if _user.login_try_count > 3:
        return utils.BadRequest('You are blocked', status_code=401)

    session.add_session(_user)
    print("Welcome to profile😊")
