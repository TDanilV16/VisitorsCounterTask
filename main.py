from fastapi import FastAPI, Request
import threading
import statistics_counter

app = FastAPI()

lock = threading.Lock()


@app.get("/")
async def root(request: Request):

    with lock:
        client_host = request.client.host
        total_visits = statistics_counter.count_global()

    print(f"New visitor: {client_host}")
    return f"""Total visitors: {total_visits}"""
