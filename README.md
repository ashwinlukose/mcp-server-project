# Live Map, Weather, and Travel MCP Server

A comprehensive [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server built with Python. It demonstrates all three core MCP primitives — **Tools**, **Resources**, and **Prompts** — providing real-time geocoding, live weather forecasts, curated location data, and structured travel workflow templates for AI clients (such as Claude Desktop, Antigravity, Cursor, and the MCP Inspector).

---

## Features & MCP Capabilities

This server implements the complete trio of MCP primitives:

1. 🛠️ **Tools (Actions & Computations)**
   - **`get_live_location_coordinates`**: Resolves any address or city to geographical coordinates (latitude and longitude) using the [OpenStreetMap Nominatim API](https://nominatim.openstreetmap.org/).
   - **`get_live_weather`**: Fetches real-time temperature, relative humidity, and wind speed for any coordinate pair using the [Open-Meteo API](https://open-meteo.com/).

2. 📄 **Resources (Readable Context & Data)**
   - **`location://favorite-cities`**: Exposes a curated list of reference locations (base locations, transport hubs, and capitals) that AI agents can inspect and read directly as contextual data.

3. 💬 **Prompts (Reusable Workflow Templates)**
   - **`travel_weather_briefing`**: Provides a standardized, step-by-step workflow prompt that guides the AI to geocode a given destination, fetch current weather, and provide outdoor suitability advice.

4. 🔑 **No API Keys Required**
   - Both OpenStreetMap Nominatim and Open-Meteo provide free-tier access without requiring registration or API tokens.

---

## Prerequisites

- **Python**: 3.10 or higher
- **Virtual Environment**: Recommended (`venv` or `uv`)

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ashwinlukose/mcp-server-project.git
   cd mcp-server-project
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(or `pip install mcp httpx`)*

---

## Project Structure

```text
mcp-server/
├── server.py          # MCP server (Tools, Resources, and Prompts)
├── requirements.txt   # Project dependencies
├── README.md          # Project documentation
└── venv/              # Python virtual environment (ignored in git)
```

---

## MCP Primitives Reference

### 1. Tools

#### `get_live_location_coordinates`
Looks up coordinates for an address or city.
- **Parameters**:
  - `location_name` (*string*, required): Name of the city, region, or address (e.g., `"Berlin"`, `"1600 Amphitheatre Parkway, Mountain View, CA"`).
- **Returns**: Formatted text containing display name, latitude, and longitude.

#### `get_live_weather`
Retrieves current weather conditions for given coordinates.
- **Parameters**:
  - `latitude` (*float*, required): Latitude coordinate (e.g., `52.5200`).
  - `longitude` (*float*, required): Longitude coordinate (e.g., `13.4050`).
- **Returns**: Formatted text containing temperature, relative humidity, and wind speed with units.

---

### 2. Resources

#### `location://favorite-cities`
- **URI**: `location://favorite-cities`
- **Description**: Exposes a curated list of reference locations (e.g., Kaiserslautern, Frankfurt, Berlin, Paris) for testing and travel context.
- **Format**: Plain text / Markdown list.

---

### 3. Prompts

#### `travel_weather_briefing`
- **Name**: `travel_weather_briefing`
- **Arguments**:
  - `destination` (*string*, required): Destination city or location name to analyze.
- **Description**: Generates an instruction template directing the LLM to:
  1. Call `get_live_location_coordinates` for the destination.
  2. Call `get_live_weather` using the retrieved coordinates.
  3. Synthesize a concise summary assessing whether weather conditions are suitable for outdoor activities.

---

## Running the Server

### Direct Execution (stdio)

Run the server script using your virtual environment's Python:

```bash
python server.py
```

### Testing with MCP Inspector

You can test and inspect tools, resources, and prompts interactively using the official MCP Inspector:

```bash
npx @modelcontextprotocol/inspector /absolute/path/to/venv/bin/python /absolute/path/to/server.py
```

Inside the Inspector UI:
- Under **Tools**: test `get_live_location_coordinates` and `get_live_weather`.
- Under **Resources**: view and read `location://favorite-cities`.
- Under **Prompts**: execute `travel_weather_briefing` with a custom destination.

---

## Client Configuration

To connect this server to an MCP host, add it to your client configuration file.

### Claude Desktop Configuration

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "live-map-weather": {
      "command": "/Users/ashwinlukose/Developer/stuff/mcp-server/venv/bin/python",
      "args": [
        "/Users/ashwinlukose/Developer/stuff/mcp-server/server.py"
      ]
    }
  }
}
```

> **Note**: Replace `/Users/ashwinlukose/Developer/stuff/mcp-server/...` with your actual system paths.

---

## External APIs & Usage Policies

- **OpenStreetMap Nominatim**: Subject to the [Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/) (includes custom `User-Agent` header, max 1 request/second).
- **Open-Meteo**: Free for non-commercial and open use. See [Open-Meteo Terms](https://open-meteo.com/en/terms).
