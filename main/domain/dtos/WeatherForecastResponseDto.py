from pydantic import BaseModel, Field

class WeatherForecastResponseDto(BaseModel):
    temperature_2m: float = Field(..., example=23.5)
    relative_humidity_2m: float = Field(..., example=78.0)
    precipitation: float = Field(..., example=0.0)
    wind_gusts_10m: float = Field(..., example=15.0)
    pm10: float = Field(..., example=12.0)
    pm2_5: float = Field(..., example=8.0)
    us_aqi: int = Field(..., example=42)
    ozone: float = Field(..., example=0.030)