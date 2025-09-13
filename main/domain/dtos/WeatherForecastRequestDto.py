from pydantic import BaseModel, Field

from main.domain.validations.StringValidations import NonBlankStr

class WeatherForecastRequestDto(BaseModel):
    location: NonBlankStr = Field(..., example="São Paulo")
    datetime: NonBlankStr = Field(..., example="2025-09-12T20")