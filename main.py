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

        unique_visitors_for_today = \
            statistics_counter.count_unique_for_today()
        total_visits_for_month = \
            statistics_counter.count_for_month()
        total_visits_for_year = \
            statistics_counter.count_for_year()
        unique_visitors_for_this_month = \
            statistics_counter.count_unique_for_month()
        unique_visitors_for_this_year = \
            statistics_counter.count_unique_for_this_year()

    print(f"New visitor: {client_host}")
    return f"""
    Total visitors: {total_visits} 
    Overall Unique visitors: {unique_visitors} 
    Unique visitors for today: {unique_visitors_for_today}  
    Unique visitors for this month: {unique_visitors_for_this_month} 
    Unique visitors for this year: {unique_visitors_for_this_year} 
    All visitors for today {today}: {today_visitors} 
    All visitors for this month: {total_visits_for_month} 
    All visitors for this year: {total_visits_for_year} 
    """

# uvicorn main:app --host 192.168.1.60  --port 80
