from typing import ClassVar

from sqlalchemy.orm import Session

from app.models.nutrition_entry import NutritionEntry
from app.repositories.nutrition_repository import NutritionRepository
from exceptions.repository_exceptions import RepositoryNotFoundError


class RepositoryFactory:
    _repositories: ClassVar[dict[type, type]] = {
        NutritionEntry: NutritionRepository,
    }

    @classmethod
    def get_repository(cls, model_type: type, db: Session):
        repository_class = cls._repositories.get(model_type)

        if repository_class is None:
            raise RepositoryNotFoundError(
                f"No repository registered for model: {model_type.__name__}"
            )

        return repository_class(db=db)
