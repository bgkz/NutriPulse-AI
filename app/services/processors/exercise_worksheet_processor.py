import re
from datetime import date, datetime

import gspread

from app.models.exercise_sets_entry import ExerciseSetsEntry


class ExerciseWorksheetProcessor:
    model_type = ExerciseSetsEntry
    EXERCISE_COLUMNS = (
        "Bankdrücken",
        "Schulterdrücken",
        "Kniebeuge",
        "Klimmzüge",
        "Kreuzheben",
    )

    def process(
        self,
        worksheet: gspread.Worksheet,
    ) -> list[ExerciseSetsEntry]:

        exercise_sets: list[ExerciseSetsEntry] = []

        for row in worksheet.get_all_records():
            exercise_date = self._parse_date(row["Datum"])

            for exercise_name in self.EXERCISE_COLUMNS:
                value = row.get(exercise_name)

                if not value:
                    continue

                parsed_sets = self._parse_exercise(
                    exercise_date=exercise_date,
                    exercise_name=exercise_name,
                    value=str(value),
                )

                exercise_sets.extend(parsed_sets)

        return exercise_sets

    @staticmethod
    def _parse_date(value: object) -> date:
        text = str(value).strip()

        formats = (
            "%d.%m.%Y",
            "%d.%m.%y",
            "%d.%m",
        )

        for date_format in formats:
            try:
                parsed_date = datetime.strptime(
                    text,
                    date_format,
                ).date()

                if date_format == "%d.%m":
                    parsed_date = parsed_date.replace(year=2026)

                return parsed_date

            except ValueError:
                continue

        raise ValueError(f"Unsupported date format: {value!r}")

    @staticmethod
    def _parse_exercise(
        exercise_date: date,
        exercise_name: str,
        value: str,
    ) -> list[ExerciseSetsEntry]:

        rir = ExerciseWorksheetProcessor._parse_rir(value)

        cleaned = re.sub(
            r"\([^)]*\)",
            "",
            value,
        ).strip()

        matches = re.findall(
            r"(\d+(?:[.,]\d+)?)\s*kg\s+(\d+(?:/\d+)*)",
            cleaned,
            flags=re.IGNORECASE,
        )

        result: list[ExerciseSetsEntry] = []

        for weight_text, reps_text in matches:
            weight = float(weight_text.replace(",", "."))

            repetitions = [int(rep) for rep in reps_text.split("/")]

            for reps in repetitions:
                entry = ExerciseSetsEntry(
                    exercise_date=exercise_date,
                    exercise_name=exercise_name,
                    weight=weight,
                    repetitions=reps,
                    reps_in_reserve=rir,
                )

                result.append(entry)

        return result

    @staticmethod
    def _parse_rir(value: str) -> int | None:
        match = re.search(
            r"(?:RIR\s*(\d+)|(\d+)\s*RIR)",
            value,
            flags=re.IGNORECASE,
        )

        if match is None:
            return None

        return int(match.group(1) or match.group(2))
