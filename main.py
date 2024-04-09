import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
import requests



from models import Course, Discussion

load_dotenv()

app = FastAPI()

access_token = lambda: os.getenv("ACCESS_TOKEN")

# api/v1/courses/:course_id/discussion_topics

base_url: str = "https://dixietech.instructure.com/api/v1"


headers: dict[str, str] = {
    "Authorization":  f"Bearer {access_token()}"
}


@app.get("/courses")
async def get_courses() -> list[Course]:
   response = requests.get(url=f"{base_url}/courses", headers=headers)
   response_json_data = response.json()
   return [Course(**object) for object in response_json_data]

@app.get("/courses/{course_id}")
async def get_course(course_id: int) -> Course:
    response = requests.get(url=f"{base_url}/courses", headers=headers)
    response_json_data = response.json()
    courses = [Course(**object) for object in response_json_data]
    try:
        course = [course for course in courses if course.id == course_id][0]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with Course ID: {course_id} not found.")
    return course

@app.get("/discussions")
async def get_discussions(course_id: int) -> list:
    response = requests.get(url=f"{base_url}/courses/{course_id}/discussion_topics", headers=headers)
    response_json = response.json()
    return [Discussion(**discussion) for discussion in response_json]

