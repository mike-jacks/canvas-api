from enum import Enum

from pydantic import BaseModel

class SubmissionType(str, Enum):
    online_text_entry = "online_text_entry"
    online_url = "online_url"
    online_upload = "online_upload"
    media_recording = "media_recording"
    basic_lti_launch = "basic_lti_launch"
    student_annotation = "student_annotation"

class Course(BaseModel):
    id: int
    name: str
class Discussion(BaseModel):
    id: int
    title: str
    discussion_type: str
    user_name: str

class DiscussionEntry(BaseModel):
    message: str

class Submission(BaseModel):
    comment: str
    type: SubmissionType = SubmissionType.online_url
    url: str