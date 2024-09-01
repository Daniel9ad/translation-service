from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi.templating import Jinja2Templates
import schemas
import crud
import models
from database import get_db, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

template = Jinja2Templates(directory="templates")

@app.get('/index', response_class=HTMLResponse)
def index(request: Request):
    return template.TemplateResponse("index2.html", {"request": request})

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post('/translate', response_model=schemas.TaskResponse)
def tanslate(request: schemas.TranslationRequest):
    task = crud.create_translation_task(get_db.db, request.text, request.lanaguages)
    Background_tasks.add_task(perform_translation, task.id, request.text, request.lanaguages, get_db.db)
    return { "task_id": {task.id} }