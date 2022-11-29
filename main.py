import datetime

from fastapi import FastAPI, Request
import threading
import statistics_counter

app = FastAPI()

lock = threading.Lock()


@app.get("/")
async def root(request: Request):

    with lock:
        client_host = request.client.host
        today = datetime.date.today().strftime("%d/%m/%y")

        entity = (client_host, today)
        statistics_counter.write_in_table(entity)

        total_visits = statistics_counter.count_global()
        today_visitors = statistics_counter.count_for_today()
        unique_visitors = statistics_counter.count_unique()

    print(f"New visitor: {client_host}")
    return f"""Total visitors: {total_visits} For today {today}: {today_visitors} Unique visitors: {unique_visitors}"""
