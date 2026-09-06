from typing import Dict
from datetime import date
from pydantic import BaseModel, Field, ConfigDict

class FXApiResponse(BaseModel):
    model_config = ConfigDict(strict=False)

    amount: float
    base: str
    start_date: date
    end_date: date
    rates: Dict[date, Dict[str,float]] = Field(
        ...,
        description="Map of date string to dictionary of currency codes and exchange rates"
    )