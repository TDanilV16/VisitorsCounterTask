import sqlite3 as sql
import datetime as dt

months = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

weekDays = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}


def get_today_date():
    return dt.date.today().strftime("%d/%m/%y")


def get_weekday(year, month, day):
    wd = dt.date(year, month, day).weekday()
    return weekDays[wd]


def get_month_name(month):
    return months[month]


def write_in_table(entities):
    db = sql.connect("data.sqlite")

    cursor = db.cursor()

    cursor \
        .execute("INSERT INTO Visitors VALUES(?, ?, ?, ?, ?, ?)", entities)

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
    today = get_today_date()
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    cursor \
        .execute("SELECT * FROM Visitors WHERE date = ?;", (today,))
    count = len(cursor.fetchall())
    db.close()

    return count


def count_for_month():
    today = get_today_date()
    month = today.split('/')[1]
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    string = f'/{month}/'
    cursor \
        .execute("SELECT * FROM Visitors WHERE instr(date, ?)", (string,))
    count = len(cursor.fetchall())

    return count


def count_for_year():
    today = get_today_date()
    year = today.split('/')[2]
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    string = f'/{year}'
    cursor \
        .execute("SELECT * FROM Visitors WHERE instr(date, ?)", (string,))
    count = len(cursor.fetchall())

    return count


def count_unique():
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    cursor \
        .execute("SELECT DISTINCT ip FROM Visitors")
    count = len(cursor.fetchall())
    db.close()

    return count


def count_unique_for_today():
    today = get_today_date()
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    cursor \
        .execute("SELECT DISTINCT ip FROM Visitors WHERE date = ?", (today,))
    count = len(cursor.fetchall())
    db.close()

    return count


def count_unique_for_month():
    today = get_today_date()
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    month = today.split('/')[1]
    year = today.split('/')[2]
    string = f'/{month}/{year}'
    cursor \
        .execute("SELECT DISTINCT ip FROM Visitors WHERE instr(date, ?)", (string,))
    count = len(cursor.fetchall())

    return count


def count_unique_for_this_year():
    today = get_today_date()
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    year = today.split('/')[2]
    string = f'/{year}'
    cursor \
        .execute("SELECT DISTINCT ip FROM Visitors WHERE instr(date, ?)", (string,))
    count = len(cursor.fetchall())

    return count


def count_visitors_for_month(month):
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    string = f'/{month}/'
    cursor \
        .execute("SELECT * FROM Visitors WHERE instr(date, ?)", (string,))
    count = len(cursor.fetchall())

    return count


def count_visitors_for_weekday(weekday):
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    cursor \
        .execute("SELECT * FROM Visitors WHERE weekday = ?", (weekday, ))

    count = len(cursor.fetchall())

    return count


def count_visitors_for_hour(hour):
    db = sql.connect("data.sqlite")
    cursor = db.cursor()
    cursor \
        .execute("Select * FROM Visitors WHERE hour = ?", (hour, ))

    count = len(cursor.fetchall())

    return count
