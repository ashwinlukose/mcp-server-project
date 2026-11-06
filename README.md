# Live Map & Weather MCP Server

A Model Context Protocol (MCP) server that provides real-time geographic location lookups and live weather data for AI assistants and MCP-compatible clients (such as Claude Desktop, Antigravity, Cursor, and the MCP Inspector).

---

## Features

- **Geocoding Tool (`get_live_location_coordinates`)**:
  - Resolves any city, place, or street address to geographical coordinates (latitude and longitude) using the [OpenStreetMap Nominatim API](https://nominatim.openstreetmap.org/).
  - Returns the full display name along with latitude and longitude.

- **Weather Tool (`get_live_weather`)**:
  - Fetches current, real-time meteorological conditions for given coordinates using the [Open-Meteo Forecast API](https://open-meteo.com/).
  - Returns current temperature, relative humidity, and wind speed with appropriate units.

- **No API Keys Required**:
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
├── server.py          # MCP server implementation and tool definitions
├── requirements.txt   # Project dependencies
├── README.md          # Project documentation
└── venv/              # Python virtual environment (ignored in git)
```

---

## Available Tools

### 1. `get_live_location_coordinates`
Looks up coordinates for an address or city.

- **Parameters**:
  - `location_name` (*string*, required): Name of the city, region, or address (e.g., `"Berlin"`, `"1600 Amphitheatre Parkway, Mountain View, CA"`).
- **Output**:
  - Location display name, latitude, and longitude.

### 2. `get_live_weather`
Retrieves current weather conditions for given coordinates.

- **Parameters**:
  - `latitude` (*float*, required): Latitude coordinate (e.g., `52.5200`).
  - `longitude` (*float*, required): Longitude coordinate (e.g., `13.4050`).
- **Output**:
  - Current temperature (e.g., `°C`), relative humidity (`%`), and wind speed (`km/h`).

---

## Running the Server

### Direct Execution (stdio)

Run the server script using your virtual environment's Python:

```bash
python server.py
```

### Testing with MCP Inspector

You can test and inspect the tools interactively using the official MCP Inspector:

```bash
npx @modelcontextprotocol/inspector /absolute/path/to/venv/bin/python /absolute/path/to/server.py
```

---

## Client Configuration

To connect this server to an MCP host, add it to your client's configuration file.

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

> **Note**: Update paths above with your absolute system paths.

---

## External APIs & Usage Policies

- **OpenStreetMap Nominatim**: Subject to the [Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/) (includes custom `User-Agent` header, max 1 request/second).
- **Open-Meteo**: Free for non-commercial and open use. See [Open-Meteo Terms](https://open-meteo.com/en/terms).
