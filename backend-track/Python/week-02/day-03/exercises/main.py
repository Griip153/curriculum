# Day 7 - FastAPI skeleton (SOLVED - the logging middleware, /health, and the
# router mount are worked together in the session; the rest of the CRUD lives
# in routers/students.py, where TODOs mark the "Your turn" assignment steps.
#
# Run: uvicorn main:app --reload
# Docs: http://localhost:8000/docs

import time
from fastapi import FastAPI, Request

from routers import students

app = FastAPI(title="Students API")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    print(f"{request.method} {request.url.path} - {response.status_code} ({duration:.3f}s)")
    return response


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(students.router, prefix="/students", tags=["students"])
