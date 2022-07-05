from fastapi import FastAPI
from routers import record, comp, upload_files
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(record.router)
app.include_router(comp.router)
app.include_router(upload_files.router)


origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
