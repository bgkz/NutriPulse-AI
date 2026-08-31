from datetime import date, datetime

import gspread

from app.models.nutrition_entry import NutritionEntry


class NutritionWorksheetProcessor:
    def process(self, worksheet: gspread.Worksheet) -> NutritionEntry:
        print(worksheet.title, " will be processed")
        for rows in worksheet.get_all_records():
            (
                nutrition_date,
                training,
                steps,
                calories,
                protein,
                fat,
                carbs,
                weight,
                notes,
            ) = rows.values()

            nutrition_date = datetime.strptime(  # noqa: DTZ007
                f"{nutrition_date}.2026",
                "%d.%m.%Y",
            ).date()

            print(training)
            print(type(training))

            nutrition_entry = NutritionEntry()
            nutrition_entry.nutrition_date = nutrition_date
