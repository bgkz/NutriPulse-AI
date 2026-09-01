from datetime import datetime
from typing import Any


class WorksheetProcessor:
    
    
    
    
    
    @staticmethod
    def _parse_date(value: Any):
        return datetime.strptime(  # noqa: DTZ007
            f"{value}.2026",
            "%d.%m.%Y",
        ).date()
