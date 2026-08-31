import gspread


class TrainingWorksheetProcessor:
    def process(self, worksheet: gspread.Worksheet) -> None:

        print(worksheet.title, " will be processed")
