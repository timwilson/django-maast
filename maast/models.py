from datetime import date
from pydantic import BaseModel, HttpUrl


class Gender(BaseModel):
    id: int
    abbrev: str
    name: str


class ScoringMethod(BaseModel):
    id: int
    name: str
    description: str | None


class EventType(BaseModel):
    id: int
    name: str
    description: str | None


class Person(BaseModel):
    id: int
    first_name: str
    last_name: str
    name_suffix: str | None
    nickname: str | None
    slug: str
    is_deceased: bool
    full_name: str


class Location(BaseModel):
    id: int
    name: str
    slug: str
    address1: str | None
    address2: str | None
    city: str
    state: str
    postal_code: str | None
    url: str | None
    name_and_location: str


class Organization(BaseModel):
    id: int
    name: str
    slug: str
    abbreviation: str
    url: HttpUrl | None


class AgeDivision(BaseModel):
    id: int
    name: str
    slug: str
    abbreviation: str | None
    description: str | None
    is_retired: bool
    organization_id: int


class EquipmentClass(BaseModel):
    id: int
    name: str
    slug: str
    abbreviation: str | None
    description: str | None
    organization_id: int
    is_retired: bool


class Round(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None
    organization_id: int
    distance_unit: str
    is_retired: bool
    in_out: str


class EventRound(BaseModel):
    id: int
    event_date: date | None
    event_id: int
    round_id: int


class Event(BaseModel):
    id: int
    name: str
    slug: str
    start_date: date | None
    end_date: date | None
    location_id: int
    scoring_method_id: int
    event_type_id: int | None
    event_date: str
    location: Location


class Finish(BaseModel):
    id: int
    person_id: int
    event_id: int
    age_division_id: int
    equipment_class_id: int
    gender_id: int
    place: int | None
    person: Person
    event: Event
    age_division: AgeDivision
    equipment_class: EquipmentClass
    gender: Gender


class Score(BaseModel):
    id: int
    score: int
    x_count: int | None
    person_id: int
    event_round_id: int
    age_division_id: int
    equipment_class_id: int
    gender_id: int
    event_id: int
    round_id: int
    pretty_score: str
    possible_multiday_score: bool
    event: Event
    person: Person
    event_round: EventRound
    round: Round
    age_division: AgeDivision
    equipment_class: EquipmentClass
    gender: Gender
    rank: int


class Record(BaseModel):
    id: int
    score: int
    x_count: int | None
    person_id: int
    event_round_id: int
    age_division_id: int
    equipment_class_id: int
    gender_id: int
    event_id: int
    round_id: int
    pretty_score: str
    possible_multiday_score: bool
    event: Event
    person: Person
    event_round: EventRound
    round: Round
    age_division: AgeDivision
    equipment_class: EquipmentClass
    gender: Gender

    def template_representation(self):
        return {
            "age_division": self.age_division.name,
            "gender": self.gender.name,
            "equipment_class": self.equipment_class.name,
            "full_name": self.person.full_name,
            "person_slug": self.person.slug,
            "score": self.pretty_score,
            "event_id": self.event.id,
            "event_date": self.event.event_date,
            "event_name": self.event.name,
            "event_location": self.event.location.name_and_location,
        }
