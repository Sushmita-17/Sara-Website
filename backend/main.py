import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from .api import auth, routes, admin, payment

app = FastAPI(title="Sara Foods API", version="2.0.0")

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(routes.router, prefix="/api")
app.include_router(admin.router, prefix="/api/admin")
app.include_router(payment.router, prefix="/api")

# Serve frontend (MUST be last)
# Local run: repo root has /build or /frontend
# Docker run: Dockerfile copies /build or /frontend into the image
repo_build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "build"))
repo_frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
docker_build_dir = "/build"
docker_frontend_dir = "/frontend"

if os.path.isdir(repo_build_dir):
    app.mount("/", StaticFiles(directory=repo_build_dir, html=True), name="static")
elif os.path.isdir(repo_frontend_dir):
    app.mount("/", StaticFiles(directory=repo_frontend_dir, html=True), name="static")
elif os.path.isdir(docker_build_dir):
    app.mount("/", StaticFiles(directory=docker_build_dir, html=True), name="static")
elif os.path.isdir(docker_frontend_dir):
    app.mount("/", StaticFiles(directory=docker_frontend_dir, html=True), name="static")
else:
    # Don’t crash the app if frontend/build isn’t present; API can still run
    print(f"[WARN] Static files directory not found. tried: {repo_build_dir}, {repo_frontend_dir}, {docker_build_dir}, and {docker_frontend_dir}")



if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
