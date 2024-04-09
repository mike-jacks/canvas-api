import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
import requests



from models import Course, Discussion, DiscussionEntry, Submission

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

@app.post("/discussions/entries")
async def create_discussion_entry(course_id: int, topic_id: int, data: DiscussionEntry) -> None:
    response = requests.post(f"{base_url}/courses/{course_id}/discussion_topics/{topic_id}/entries", data=data.model_dump(), headers=headers)
    r_json = response.json()
    return

@app.get("/discussions/entries")
async def get_discussion_entries(course_id: int, topic_id: int, per_page: int):
    response = requests.get(f"{base_url}/courses/{course_id}/discussion_topics/{topic_id}/entries?per_page={per_page}", headers=headers)
    r_json = response.json()
    return r_json

@app.put("/discussion/entries")
async def update_discussion_entrie(course_id: int, topic_id: int, entry_id: int, data: DiscussionEntry) -> None:
    response = requests.put(f"{base_url}/courses/{course_id}/discussion_topics/{topic_id}/entries/{entry_id}", headers=headers, data=data.model_dump())
    r_json = response.json()
    return


@app.get("/courses/{course_id}/assignments")
async def get_course_assignments(course_id: int, per_page: int = 10, assignment_name: str = "") -> list | dict:
    response = requests.get(f"{base_url}/courses/{course_id}/assignments?per_page={per_page}", headers=headers)
    r_json = response.json()
    if assignment_name == "":
        return [{"assignment_id":assignment["id"], "name":assignment["name"]} for assignment in r_json]
    try:
        assignment = [assignment for assignment in r_json if assignment["name"] == assignment_name][0]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Assignment {assignment_name} not found.")
    return assignment

@app.post("/courses/{course_id}/assignments/{assignment_id}/submit") 
async def post_course_assignment(course_id: int, assignment_id: int, submission: Submission):
    data =  {"comment[text_comment]": submission.comment, "submission[submission_type]": submission.type, "submission[url]": submission.url}
    response = requests.post(f"{base_url}/courses/{course_id}/assignments/{assignment_id}/submissions", headers=headers, data=data)
    return response.json()