import datetime

from pydantic import BaseModel, Field


class NutritionData(BaseModel):
    date: datetime.date | None
    calories: int | None
    protein_g: int | None
    carbs_g: int | None
    fat_g: int | None
    bodyweight_kg: float | None
    steps: int | None
    notes: str | None


class WorkoutData(BaseModel):
    date: datetime.date | None

    exercise: str | None = Field(
        description="Name of exactly one exercise, e.g. Bench Press, Squat, Deadlift"
    )

    weight_kg: float | None = Field(
        description="Weight used for this exercise in kilograms"
    )

    reps_in_set_one: int | None = Field(
        description="Number of repetitions performed in the first set"
    )

    reps_in_set_two: int | None = Field(
        description="Number of repetitions performed in the second set"
    )

    reps_in_set_three: int | None = Field(
        description="Number of repetitions performed in the third set"
    )

    rest_in_reserve_min: int | None
    rest_in_reserve_max: int | None
    notes: str | None


class FitnessEntries(BaseModel):
    nutrition: list[NutritionData]
    workouts: list[WorkoutData]
