from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

import database
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Корневая старница
@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

# Страница создания нового пользователя
@app.get("/create-profile", response_class=HTMLResponse)
async def create_profile_get(request: Request):
    return templates.TemplateResponse(
        request=request, name="new-profile.html"
    )

# Страница создания нового пользователя
@app.post("/create-profile", response_class=HTMLResponse)
async def create_profile(request: Request, username: str = Form(...),
                         email: str = Form(...), surname: str = Form(...), 
                         name: str = Form(...), patronymic: str = Form(None)):
    database.insert_user(username, email, name, surname, patronymic)
    return templates.TemplateResponse(
        request=request, name="new-profile.html"
    )

# Страница просмотра профилей слушателей
@app.get("/view-profiles", response_class=HTMLResponse)
async def view_profiles(request: Request):
    return templates.TemplateResponse(
            request=request, name="profiles.html"
    )

# Страница просмотра всех курсов на платформе
@app.get("/view-courses", response_class=HTMLResponse)
async def view_courses(request: Request):
    return templates.TemplateResponse(
            request=request, name="all-courses.html"
    )

# Сервисная страница получения всех профилей пользователей
@app.get("/profiles", response_class=HTMLResponse)
async def get_profiles(request: Request):
    result = []
    for user in database.get_all_users():
        result.append(user.to_json())
    return json.dumps(result)


# Страница просмотра курсов, на которые записан конкретный слушатель
@app.get("/add-course/{user_id}", response_class=HTMLResponse)
async def add_courses(request: Request, user_id: int):
    user = database.get_user_by_id(user_id)
    return templates.TemplateResponse(
        request=request, name="courses.html", context={"user" : user.to_json()}
    )

# Сервисная страница просмотра курсов на которые записан конкретный пользователь
@app.get("/list-courses/{user_id}", response_class=HTMLResponse)
async def list_courses_of_user(request: Request, user_id: int):
    courses = database.get_courses_by_user_id(user_id)
    
    result = []
    for course in courses:
        result.append(course.to_json())
    return json.dumps(result)


# Сервисная страница просмотра всех курсов
@app.get("/courses", response_class=HTMLResponse)
async def get_courses(request: Request):
    result = []
    for course in database.get_all_courses():
        result.append(course.to_json())
    return json.dumps(result)


# Страница создания нового курса
@app.get("/create-course", response_class=HTMLResponse)
async def create_course_get(request: Request):
    return templates.TemplateResponse(
        request=request, name="new-course.html"
    )

# Сервисная страница создания нового курса
@app.post("/create-course", response_class=HTMLResponse)
async def create_course_post(request: Request, title: str = Form(...), description: str = Form(...)):
    database.insert_course(title, description)
    return templates.TemplateResponse(
        request=request, name="new-course.html"
    )

# Сервисная страница добавления курса слушателю
@app.post("/add-education", response_class=HTMLResponse)
async def add_education(request: Request):
    body = await request.json()
    database.insert_education(body["user_id"], body["course_id"])


# Сервисная страница удаления курса у слушателя
@app.post("/rm-education", response_class=HTMLResponse)
async def delete_education(request: Request):
    body = await request.json()
    print(body)
    database.delete_education(int(body["user_id"]), int(body["course_id"]))


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
