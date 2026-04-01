from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReserveRecord:
    date: str
    national_days: float
    private_days: float
    cooperative_days: float
    total_days: float
    source_pdf: str
    fetched_at: str

    @staticmethod
    def create(
        date: str,
        national_days: float,
        private_days: float,
        cooperative_days: float,
        source_pdf: str,
    ) -> "ReserveRecord":
        return ReserveRecord(
            date=date,
            national_days=national_days,
            private_days=private_days,
            cooperative_days=cooperative_days,
            total_days=national_days + private_days + cooperative_days,
            source_pdf=source_pdf,
            fetched_at=datetime.now().isoformat(),
        )

    def to_dict(self) -> dict:
        return {
            "date": self.date,
            "national_days": self.national_days,
            "private_days": self.private_days,
            "cooperative_days": self.cooperative_days,
            "total_days": self.total_days,
            "source_pdf": self.source_pdf,
            "fetched_at": self.fetched_at,
        }

    def to_api_response(self) -> dict:
        return {
            "date": self.date,
            "national_days": self.national_days,
            "private_days": self.private_days,
            "cooperative_days": self.cooperative_days,
            "total_days": self.total_days,
        }
