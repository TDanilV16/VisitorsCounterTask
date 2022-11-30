import sqlite3 as sql
import datetime as dt


def write_in_table(entities):
    db = sql.connect("data.sqlite")

    cursor = db.cursor()

    cursor\
        .execute("INSERT INTO Visitors VALUES(?, ?)", entities)

    db.commit()

    db.close()


def count_global():
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Visitors")
    total = len(cursor.fetchall())
    db.close()

    return total


def count_for_today():
    today = dt.date.today().strftime("%d/%m/%y")
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    cursor\
        .execute("SELECT * FROM Visitors WHERE date = ?;", (today,))
    count = len(cursor.fetchall())
    db.close()

    return count


def count_for_month():
    today = dt.date.today().strftime("%d/%m/%y")
    month = today.split('/')[1]
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    string = f'/{month}/'
    cursor\
        .execute("SELECT * FROM Visitors WHERE instr(date, ?)", (string, ))
    count = len(cursor.fetchall())

    return count


def count_for_year():
    today = dt.date.today().strftime("%d/%m/%y")
    year = today.split('/')[2]
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    string = f'/{year}'
    cursor\
        .execute("SELECT * FROM Visitors WHERE instr(date, ?)", (string,))
    count = len(cursor.fetchall())

    return count


def count_unique():
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    cursor\
        .execute("SELECT DISTINCT ip FROM Visitors")
    count = len(cursor.fetchall())
    db.close()

    return count


def count_unique_for_today():
    today = dt.date.today().strftime("%d/%m/%y")
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    cursor\
        .execute("SELECT DISTINCT ip FROM Visitors WHERE date = ?;", (today,))
    count = len(cursor.fetchall())
    db.close()

    return count


def count_unique_for_month():
    today = dt.date.today().strftime("%d/%m/%y")
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    month = today.split('/')[1]
    string = f'/{month}/'
    cursor\
        .execute("SELECT DISTINCT ip FROM Visitors WHERE instr(date, ?)", (string,))
    count = len(cursor.fetchall())

    return count


def count_unique_for_this_year():
    today = dt.date.today().strftime("%d/%m/%y")
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    year = today.split('/')[2]
    string = f'/{year}'
    cursor\
        .execute("SELECT DISTINCT ip FROM Visitors WHERE instr(date, ?)", (string,))
    count = len(cursor.fetchall())

    return count
