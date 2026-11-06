import httpx
from mcp.server.mcpserver import MCPServer

# Initialize the MCP server
mcp = MCPServer("Live Map and Weather MCP Server")

@mcp.tool()
async def get_live_location_coordinates(location_name: str) -> str:
    """Get real-world geographical coordinates for any city or address using OpenStreetMap."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_name,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "MapServerMCPPortfolio/1.0"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            if not data:
                return f"No live geographic data found for '{location_name}'."

            result = data[0]
            display_name = result.get("display_name")
            lat = result.get("lat")
            lon = result.get("lon")

            return f"Location: {display_name}\nLatitude: {lat}\nLongitude: {lon}"
        
        except Exception as e:
            return f"Error fetching live location data: {str(e)}"

@mcp.tool()
async def get_live_weather(latitude: float, longitude: float) -> str:
    """Get current live weather conditions for given latitude and longitude coordinates."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            current = data.get("current", {})
            units = data.get("current_units", {})

            temp = current.get("temperature_2m")
            temp_unit = units.get("temperature_2m", "°C")
            humidity = current.get("relative_humidity_2m")
            humidity_unit = units.get("relative_humidity_2m", "%")
            wind_speed = current.get("wind_speed_10m")
            wind_unit = units.get("wind_speed_10m", "km/h")

            return (
                f"Current Weather Conditions:\n"
                f"- Temperature: {temp} {temp_unit}\n"
                f"- Humidity: {humidity} {humidity_unit}\n"
                f"- Wind Speed: {wind_speed} {wind_unit}"
            )
        
        except Exception as e:
            return f"Error fetching live weather data: {str(e)}"

if __name__ == "__main__":
    mcp.run()