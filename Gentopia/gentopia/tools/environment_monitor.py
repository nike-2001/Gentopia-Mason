from typing import Optional, Type
from pydantic import BaseModel, Field
from gentopia.tools.basetool import BaseTool
import random

class EnvironmentalArgs(BaseModel):
    location: str = Field(..., description="The location for which environmental data is monitored.")
    temperature: Optional[float] = Field(None, description="Current temperature in Celsius.")
    air_quality_index: Optional[int] = Field(None, description="Current AQI (Air Quality Index).")
    soil_moisture: Optional[float] = Field(None, description="Current soil moisture level.")
    water_level: Optional[float] = Field(None, description="Current water level in the area.")

class EnvironmentalMonitoringAgent(BaseTool):
    """Agent that monitors environmental data and provides alerts and sustainability tips."""
    
    name = "environmental_monitoring_agent"
    description = ("An agent that monitors climate, air quality, and water levels, providing alerts and "
                   "sustainability suggestions.")
    args_schema: Optional[Type[BaseModel]] = EnvironmentalArgs

    sustainability_tips = [
        "Consider using renewable energy sources like solar panels to reduce your carbon footprint.",
        "Reduce water usage by fixing leaks and using efficient appliances.",
        "Plant more trees in your community to help combat air pollution.",
        "Support organizations that fight deforestation and promote sustainable agriculture."
    ]

    def _run(self, location: str, temperature: Optional[float] = None, 
             air_quality_index: Optional[int] = None, 
             soil_moisture: Optional[float] = None, 
             water_level: Optional[float] = None) -> str:
        try:
            # Analyze the data and generate alerts
            alerts = self._analyze_data(temperature, air_quality_index, soil_moisture, water_level)

            # If no alerts, provide a sustainability tip
            if not alerts:
                return f"No significant environmental risks detected in {location}. " + self._provide_sustainability_tip()
            else:
                return f"Environmental alerts for {location}: " + " | ".join(alerts) + " " + self._provide_sustainability_tip()

        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    async def _arun(self, location: str, temperature: Optional[float] = None, 
                    air_quality_index: Optional[int] = None, 
                    soil_moisture: Optional[float] = None, 
                    water_level: Optional[float] = None) -> str:
        """
        Asynchronous version of the tool.
        Since we haven't implemented async functionality, we call the synchronous version.
        """
        return self._run(location, temperature, air_quality_index, soil_moisture, water_level)

    def _analyze_data(self, temperature: Optional[float], 
                      air_quality_index: Optional[int], 
                      soil_moisture: Optional[float], 
                      water_level: Optional[float]) -> list:
        """Analyze environmental data and generate alerts."""
        alerts = []

        # Temperature Alert
        if temperature is not None and temperature > 35:
            alerts.append(f"High temperature detected: {temperature}°C. Stay hydrated and avoid prolonged outdoor activity.")

        # Air Quality Alert
        if air_quality_index is not None and air_quality_index > 100:
            alerts.append(f"Poor air quality detected: AQI = {air_quality_index}. Consider using air purifiers or wearing masks.")

        # Water Level Alert
        if water_level is not None and water_level > 5:
            alerts.append(f"Rising water levels detected: {water_level} meters. Flooding risk in the area. Stay alert!")

        return alerts

    def _provide_sustainability_tip(self) -> str:
        """Provide a random sustainability tip."""
        return random.choice(self.sustainability_tips)


# Example usage
if __name__ == "__main__":
    agent = EnvironmentalMonitoringAgent()
    
    # Example environmental data
    args = EnvironmentalArgs(
        location="New York",
        temperature=38,
        air_quality_index=150,
        soil_moisture=12.5,
        water_level=6
    )
    
    # Run the tool
    result = agent._run(
        location=args.location, 
        temperature=args.temperature, 
        air_quality_index=args.air_quality_index, 
        soil_moisture=args.soil_moisture, 
        water_level=args.water_level
    )
    
    print(result)
