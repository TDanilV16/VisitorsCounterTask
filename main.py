import datetime
from string import Template
from uuid import UUID, uuid4

from fastapi import HTTPException, FastAPI, Response, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.session_verifier import SessionVerifier
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

import statistics_counter

router = FastAPI()
cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password):
    return pwd_context.hash(password)


class SessionData(BaseModel):
    username: str
    user_pass: str
    session_id : str

    def get_inf(self):
        data = {
            'auth_': False,
            'username:': None,
            'user_pass': ''
        }
        if self.username:
            data = {
                'auth_': True,
                'username:': self.username,
                'user_pass': self.user_pass,
                'session_id': self.session_id
            }
        return data


backend = InMemoryBackend[UUID, SessionData]()


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
            self,
            *,
            identifier: str,
            auto_error: bool,
            backend: InMemoryBackend[UUID, SessionData],
            auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


@router.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return templates.TemplateResponse("login_exception_handler.html", {"request": request})

verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=RedirectResponse)
async def root(response: Response):
    return RedirectResponse("/login", status_code=303, headers=response.headers)


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=RedirectResponse)
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    session = uuid4()
    data = SessionData(username=username,
                       user_pass=get_password_hash(password),
                       session_id=str(session))

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    return RedirectResponse("/statistics", status_code=303, headers=response.headers)


@router.get("/statistics", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def send(session_data: SessionData = Depends(verifier)):
    client_host = session_data.session_id
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


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request, response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return templates.TemplateResponse("logout.html", {"request": request})

# uvicorn main:app --host 192.168.1.60  --port 80
