from typing import ClassVar

from app.services.processors.exercise_worksheet_processor import (
    ExerciseWorksheetProcessor,
)
from app.services.processors.nutrition_worksheet_processor import (
    NutritionWorksheetProcessor,
)
from exceptions.processors_exceptions import (
    WorksheetProcessorNotFoundError,
)


class WorksheetProcessorFactory:
    _processors: ClassVar[dict[str, type]] = {
        "Nutrition": NutritionWorksheetProcessor,
        "Training": ExerciseWorksheetProcessor,
    }

    @classmethod
    def get_processor(cls, worksheet_name: str):
        """
        Return the processor for a worksheet.

        Raises:
            WorksheetProcessorNotFoundError:
                If no processor is registered for the worksheet.
        """
        processor_class = cls._processors.get(worksheet_name)

        if processor_class is None:
            raise WorksheetProcessorNotFoundError(
                f"No processor registered for worksheet: {worksheet_name}"
            )

        return processor_class()
