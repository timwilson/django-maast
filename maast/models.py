from pydantic import BaseModel


class Record(BaseModel):
    age_division: str
    gender: str
    equipment_class: str
    full_name: str
    person_slug: str
    score: str
    event_id: int
    event_date: str
    event_name: str
    event_location: str
