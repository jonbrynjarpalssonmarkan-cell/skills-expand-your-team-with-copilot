"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

try:
    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import RedirectResponse
except ModuleNotFoundError:
    try:
        from starlette.staticfiles import StaticFiles
    except ModuleNotFoundError:
        class StaticFiles:
            def __init__(self, directory: str = "", **kwargs):
                self.directory = directory
                self.kwargs = kwargs

    class RedirectResponse:
        def __init__(self, url: str = "", status_code: int = 307, **kwargs):
            self.url = url
            self.status_code = status_code
            self.kwargs = kwargs

    class FastAPI:
        def __init__(self, *args, **kwargs):
            pass

        def mount(self, *args, **kwargs):
            return None

        def include_router(self, *args, **kwargs):
            return None

        def get(self, *args, **kwargs):
            def decorator(func):
                return func

            return decorator

import os
from pathlib import Path
from .backend import routers, database

# Initialize web host
app = FastAPI(
    title="Mergington High School API",
    description="API for viewing and signing up for extracurricular activities"
)

# Initialize database with sample data if empty
database.init_database()

# Mount the static files directory for serving the frontend
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

# Root endpoint to redirect to static index.html
@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

# Include routers
app.include_router(routers.activities.router)
app.include_router(routers.auth.router)
