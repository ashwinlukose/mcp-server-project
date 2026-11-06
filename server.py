import httpx
from mcp.server.mcpserver import MCPServer

# Initialize the comprehensive MCP server
mcp = MCPServer("Live Map, Weather, and Travel MCP Server")

# ==================== 1. TOOLS (Actions & Computations) ====================

@mcp.tool()
async def get_live_location_coordinates(location_name: str) -> str:
    """Get real-world geographical coordinates for any city or address using OpenStreetMap."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": location_name, "format": "json", "limit": 1}
    headers = {"User-Agent": "MapServerMCPPortfolio/1.0"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            if not data:
                return f"No live geographic data found for '{location_name}'."

            result = data[0]
            return f"Location: {result.get('display_name')}\nLatitude: {result.get('lat')}\nLongitude: {result.get('lon')}"
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

            return (
                f"Current Weather Conditions:\n"
                f"- Temperature: {current.get('temperature_2m')} {units.get('temperature_2m', '°C')}\n"
                f"- Humidity: {current.get('relative_humidity_2m')} {units.get('relative_humidity_2m', '%')}\n"
                f"- Wind Speed: {current.get('wind_speed_10m')} {units.get('wind_speed_10m', 'km/h')}"
            )
        except Exception as e:
            return f"Error fetching live weather data: {str(e)}"

# ==================== 2. RESOURCES (Readable Data / URIs) ====================

@mcp.resource("location://favorite-cities")
def get_favorite_cities() -> str:
    """Expose a curated list of reference cities for travel and testing."""
    return (
        "Curated Reference Locations:\n"
        "1. Kaiserslautern, Germany (Primary Base)\n"
        "2. Frankfurt, Germany (Major Transport Hub)\n"
        "3. Berlin, Germany (Capital)\n"
        "4. Paris, France (International)"
    )

# ==================== 3. PROMPTS (Reusable Workflows) ====================

@mcp.prompt()
def travel_weather_briefing(destination: str) -> str:
    """Generate a structured workflow prompt to check a destination's coordinates and weather."""
    return (
        f"Please perform a complete travel weather briefing for {destination}:\n"
        f"1. Call the geocoding tool to get the exact latitude and longitude for {destination}.\n"
        f"2. Use those coordinates to fetch the live weather conditions.\n"
        f"3. Provide a concise summary of whether current weather conditions are suitable for outdoor walking."
    )

if __name__ == "__main__":
    mcp.run()