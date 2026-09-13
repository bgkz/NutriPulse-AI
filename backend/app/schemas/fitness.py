import datetime

from pydantic import BaseModel


class NutritionEntry(BaseModel):
    date: datetime.date | None
    calories: int | None
    protein_g: float | None
    carbs_g: float | None
    fat_g: float | None
    bodyweight_kg: float | None
    steps: int | None
    notes: str | None


class WorkoutEntry(BaseModel):
    date: datetime.date | None
    exercise: str | None
    weight_kg: float | None
    repititions: list[int] | None
    rest_in_reserve_min: int | None
    rest_in_reserve_max: int | None
    notes: str | None


class FitnessEntries(BaseModel):
    nutrition: list[NutritionEntry]
    workouts: list[WorkoutEntry]
