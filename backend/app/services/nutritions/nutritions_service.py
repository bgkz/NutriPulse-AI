from app.models.nutritions_entry import NutritionsEntry
from app.repositories.nutritions.nutritions_repository import NutritionRepository


class NutritionsService:
    def __init__(self, nutrition_repo: NutritionRepository):
        self.nutrition_repo = nutrition_repo

    def add(self, nutrition_entry: NutritionsEntry) -> NutritionsEntry:
        return self.nutrition_repo.add(nutrition_entry)
