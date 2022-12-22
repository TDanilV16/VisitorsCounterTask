import datetime
from string import Template
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import statistics_counter

app = FastAPI()


@app.get("/")
async def root(request: Request):
    client_host = request.client.host
    today = statistics_counter.get_today_date()
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    weekday = statistics_counter.get_weekday(now.year, now.month, now.day)
    entity = (client_host, today, hour, minute, second, weekday)
    statistics_counter.write_in_table(entity)

    print(f"New visitor: {client_host}")

    res = (f"""
        <html>
            <head>
            </head>
            <body>
                <h1>{Template("Total visitors: $total_visits")
           .substitute(total_visits=statistics_counter.count_global())}</h1>
                <h1>{Template("Overall Unique visitors: $unique_visitors")
           .substitute(unique_visitors=statistics_counter.count_unique())}</h1> 
                <h1>{Template("Unique visitors for $today: $unique_visitors_for_today")
           .substitute(unique_visitors_for_today=statistics_counter.count_unique_for_today(), today=today)}</h1>
                <h1>{Template("Unique visitors for this month: $unique_visitors_for_this_month")
           .substitute(unique_visitors_for_this_month=statistics_counter.count_unique_for_month())}</h1>
                <h1>{Template("Unique visitors for this year: $unique_visitors_for_this_year")
           .substitute(unique_visitors_for_this_year=statistics_counter.count_unique_for_this_year())}</h1>
                <h1>{Template("All visitors for today $today: $today_visitors")
           .substitute(today_visitors=statistics_counter.count_for_today(), today=today)}</h1>
                <h1>{Template("All visitors for this month: $total_visits_for_month")
           .substitute(total_visits_for_month=statistics_counter.count_for_month())}</h1>
                <h1>{Template("All visitors for this year: $total_visits_for_year")
           .substitute(total_visits_for_year=statistics_counter.count_for_year())}</h1>
           <h1>{Template("All visitors for December: $total_visits_for_december")
           .substitute(total_visits_for_december=statistics_counter.count_visitors_for_month(12))}</h1>
           <h1>{Template("All visitors for Monday: $total_visits_for_monday")
           .substitute(total_visits_for_monday=statistics_counter.count_visitors_for_weekday("Monday"))}</h1>
           <h1>{Template("All visitors for 8 PM: $total_visits_for_hour")
           .substitute(total_visits_for_hour=statistics_counter.count_visitors_for_hour(20))}</h1>
            </body>
        </html>
        """)
    return HTMLResponse(content=res, status_code=200)

# uvicorn main:app --host 192.168.1.60  --port 80
