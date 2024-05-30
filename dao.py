import psycopg2
import sys
import utils
from service import session
from db import cur, conn
from models import Todo, TodoType
from service import login
from colorama import Fore
from typing import Dict


def choose_todo_type() -> TodoType:
    todo_type_dict: Dict[str, TodoType] = {'1': TodoType.Optional.value, '2': TodoType.Personal.value,
                                           '3': TodoType.Shopping.value, }  # dict of todo types
    choice_todo_type: str = input(Fore.LIGHTWHITE_EX + """Enter your todo type:\nAny button-Optional
    \n2-Personal\n3-Shopping\n ....""" + Fore.RESET)
    todo_type: TodoType = todo_type_dict.get(choice_todo_type)
    return todo_type


def create_todo() -> utils:
    if session.check_session():
        title: str = input(Fore.LIGHTWHITE_EX + "Enter your todo title: " + Fore.RESET)
        todo_type: TodoType = choose_todo_type()

        user_id: int = session.user.id
        todo: Todo = Todo(title, user_id, todo_type)
        try:
            cur.execute("""INSERT INTO todos(title, todo_type, user_id) VALUES (%s,%s,%s)""",
                        (todo.title, todo.todo_type, todo.user_id))
            conn.commit()
            return utils.ResponseData('Todo Created')
        except psycopg2.Error as e:
            conn.rollback()
            return utils.BadRequest('Error', str(e))


def delete_todo() -> utils:
    if session.check_session():
        todo_id_to_delete: str = input(Fore.LIGHTWHITE_EX + "Please enter todo id to delete: " + Fore.RESET)
        if todo_id_to_delete:
            try:
                cur.execute("""DELETE FROM todos WHERE id=%s""", (todo_id_to_delete,))
                conn.commit()
                return utils.ResponseData('Todo Deleted')
            except psycopg2.Error as e:
                conn.rollback()
                return utils.BadRequest('Error', str(e))


def update_todo() -> utils:
    if session.check_session():
        todo_id_to_update: str = input(Fore.LIGHTWHITE_EX + "Please enter todo id to update: " + Fore.RESET)
        if todo_id_to_update:
            try:
                cur.execute("""SELECT * FROM todos where id = %s""", (todo_id_to_update,))
                todo_data: tuple = cur.fetchone()
                if not todo_data:
                    utils.BadRequest('Todo Not Found')
                else:
                    title: str = input(Fore.LIGHTWHITE_EX + "Enter your todo title: " + Fore.RESET)
                    todo_type: TodoType = choose_todo_type()
                    user_id: int = session.user.id
                    todo: Todo = Todo(title, user_id, todo_type)
                    cur.execute("UPDATE todos SET title = %s, todo_type = %s, user_id = %s WHERE id = %s",
                                (todo.title, todo.todo_type, todo.user_id, todo_id_to_update))
                    conn.commit()
                    utils.ResponseData('Todo Updated')
            except psycopg2.Error as e:
                conn.rollback()
                return utils.BadRequest('Error', str(e))
        else:
            utils.BadRequest('Todo Not Found')


def show_todos() -> utils:
    if session.check_session():
        try:
            cur.execute("""SELECT * FROM todos where user_id = %s""", (session.user.id,))
            user_todo_data: tuple = cur.fetchall()
            if not user_todo_data:
                utils.BadRequest('Todo Not Found')
            list(map(print, user_todo_data))
        except psycopg2.Error as e:
            conn.rollback()
            return utils.BadRequest('Error', str(e))


def login_menu() -> str:
    print(Fore.LIGHTWHITE_EX + """Please choose option which you want:
    1. Create todo
    2. Show todos
    3. Update todo
    4. Delete todo
    0. Exit""" + Fore.RESET)
    return input(Fore.LIGHTCYAN_EX + '.....' + Fore.RESET)


def choice_run() -> None:
    while True:
        choice = login_menu()
        options_db = {
            '1': create_todo,
            '2': show_todos,
            '3': update_todo,
            '4': delete_todo,
            '0': lambda: sys.exit(Fore.LIGHTGREEN_EX + "Thanks for using" + Fore.RESET)
        }
        chosen_option = options_db.get(choice)
        if chosen_option:
            chosen_option()
        else:
            utils.BadRequest('Invalid option')


def run() -> None:
    while True:
        if not session.check_session():
            choice = input(Fore.LIGHTWHITE_EX + "Welcome to our website.\n1."
                                                " To login\n0. Exit\n.... " + Fore.RESET)
            if choice == '1':
                login_result = login()
                if isinstance(login_result, utils.BadRequest):
                    pass

                else:
                    choice_run()
            elif choice == '0':
                utils.ResponseData("Thank you for using our website")
                break
            else:
                utils.BadRequest('Invalid option')


run()
