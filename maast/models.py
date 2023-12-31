"""
These Pydantic models mirror and database models in the MAAST API
application at https://github.com/timwilson/maast-api
"""

from datetime import date
from typing import Dict, Any

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
    family_name: str | None
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
    score_date: str


def make_date(event_name: str) -> date | None:
    """Make a date object when an event has no start_date given by taking the year from the event name."""
    try:
        year = int(event_name[:4])
    except ValueError:
        return None
    return date(year, 1, 1)


def trim_event_name(event_name: str) -> str:
    """If the event name starts with a year, trim off the year and return the rest of the string."""
    if event_name[:4].isdigit():
        return event_name[4:]
    else:
        return event_name


class Event(BaseModel):
    id: int
    name: str
    slug: str
    start_date: date | None
    end_date: date | None
    location_id: int
    has_scores: bool
    scoring_method_id: int
    event_type_id: int | None
    event_date: str
    location: Location

    def template_representation(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": trim_event_name(self.name),
            "start_date": self.start_date if self.start_date else make_date(self.name),
            "has_scores": self.has_scores,
        }


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

    def template_representation(self) -> Dict[str, Any]:
        return {
            "division": f"{self.age_division.name} {self.gender.name} {self.equipment_class.name}",
            "place": self.place,
            "start_date": self.event.start_date,
            "event_date": self.event.event_date,
            "event_id": self.event.id,
            "event_name": self.event.name,
            "has_scores": self.event.has_scores,
            "event_location": self.event.location.name_and_location,
        }


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
    rank: int | None

    def template_representation(self) -> Dict[str, Any]:
        return {
            "rank": self.rank if self.rank is not None else "",
            "person": self.person.full_name,
            "person_slug": self.person.slug,
            "round_id": self.round.id,
            "round": self.round.name,
            "division": f"{self.age_division.name} {self.gender.name} {self.equipment_class.name}",
            "age_division": self.age_division.name,
            "gender": self.gender.name,
            "equipment_class": self.equipment_class.name,
            "score_date": self.event_round.score_date,
            "is_multiday_score": 1
            if self.possible_multiday_score
            else 0,  # DataTables javascript doesn't like capitalized True or False.
            "pretty_score": self.pretty_score,
            "score": self.score,
            "x_count": self.x_count if self.x_count is not None else 0,
            "event_id": self.event.id,
            "event_date": self.event.event_date,
            "event_name": self.event.name,
            "event_location": self.event.location.name_and_location,
        }


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

    def template_representation(self) -> Dict[str, Any]:
        return {
            "round": self.round.name,
            "round_id": self.round.id,
            "age_division": self.age_division.name,
            "gender": self.gender.name,
            "equipment_class": self.equipment_class.name,
            "division": f"{self.age_division.name} {self.gender.name} {self.equipment_class.name}",
            "full_name": self.person.full_name,
            "person_slug": self.person.slug,
            "score": self.pretty_score,
            "score_date": self.event_round.score_date,
            "is_multiday_score": 1
            if self.possible_multiday_score
            else 0,  # DataTables javascript doesn't like capitalized True or False.
            "event_id": self.event.id,
            "event_date": self.event.event_date,
            "event_name": self.event.name,
            "event_location": self.event.location.name_and_location,
        }
