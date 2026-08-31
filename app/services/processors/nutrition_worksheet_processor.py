import re
from datetime import datetime
from typing import Any

import gspread

from app.models.nutrition_entry import NutritionEntry
from app.services.processors.worksheet_processor import WorksheetProcessor


class NutritionWorksheetProcessor:
    model_type = NutritionEntry

    def process(
        self,
        worksheet: gspread.Worksheet,
    ) -> list[NutritionEntry]:
        nutrition_entries: list[NutritionEntry] = []

        for row in worksheet.get_all_records():
            (
                nutrition_date,
                training,
                cardio,
                calories,
                protein,
                fat,
                carbs,
                weight,
                notes,
            ) = row.values()

            parsed_date = WorksheetProcessor._parse_date(nutrition_date)

            steps = self._parse_steps(cardio)

            cardio_training = self._remove_steps_from_cardio(cardio)

            parsed_training = self._merge_training(
                training=training,
                cardio_training=cardio_training,
            )

            nutrition_entry = NutritionEntry(
                nutrition_date=parsed_date,
                training=parsed_training,
                steps=steps,
                calories=self._parse_int(calories),
                protein=self._parse_int(protein),
                fat=self._parse_int(fat),
                carbs=self._parse_int(carbs),
                weight=self._parse_float(weight),
                notes=self._parse_optional_string(notes),
            )

            nutrition_entries.append(nutrition_entry)

        return nutrition_entries


    @staticmethod
    def _parse_steps(value: Any) -> int | None:
        if value in ("", None):
            return None

        text = str(value).strip().lower()

        # Fall: Sheet enthält einfach "8000"
        if text.isdigit():
            return int(text)

        # Fälle:
        # "10k Schritte"
        # "4.5k Schritte"
        # "9.5k Schritte"
        # "Push + 10k Schritte + Laufband"
        match = re.search(
            r"(\d+(?:[.,]\d+)?)\s*k\s*(?:schritte|sxhritte|schrigte)?",
            text,
        )

        if match:
            number = float(match.group(1).replace(",", "."))

            return int(number * 1000)

        return None

    @staticmethod
    def _remove_steps_from_cardio(value: Any) -> str | None:
        if value in ("", None):
            return None

        text = str(value).strip()

        # "10k Schritte", "4.5k Schritte" usw. entfernen
        text = re.sub(
            r"\d+(?:[.,]\d+)?\s*k\s*(?:schritte|sxhritte|schrigte)?",
            "",
            text,
            flags=re.IGNORECASE,
        )

        # Reine Schrittzahlen wie "8000"
        if text.strip().isdigit():
            return None

        # Überbleibsel aufräumen
        text = re.sub(r"\s*\+\s*\+", "+", text)
        text = re.sub(r"^[\s,+]+", "", text)
        text = re.sub(r"[\s,+)]+$", "", text)
        text = text.strip()

        return text or None

    @staticmethod
    def _merge_training(
        training: Any,
        cardio_training: str | None,
    ) -> str | None:
        training_text = str(training).strip() if training not in ("", None) else None

        if not training_text:
            return cardio_training

        if not cardio_training:
            return training_text

        # Beispiel:
        # training = "Push"
        # cardio = "Push + 10min laufband"
        #
        # -> nicht "Push + Push + 10min laufband"
        if training_text.lower() in cardio_training.lower():
            return cardio_training

        return f"{training_text} + {cardio_training}"

    @staticmethod
    def _parse_int(value: Any) -> int | None:
        if value in ("", None):
            return None

        # z.B.
        # "2600 schätzungsweise"
        # "3000 (geschätzt)"
        # "über 2600 geschätzt"
        match = re.search(r"\d+", str(value))

        if match is None:
            return None

        return int(match.group())

    @staticmethod
    def _parse_float(value: Any) -> float | None:
        if value in ("", None):
            return None

        try:
            return float(str(value).replace(",", "."))
        except ValueError:
            return None

    @staticmethod
    def _parse_optional_string(value: Any) -> str | None:
        if value in ("", None):
            return None

        return str(value).strip()
