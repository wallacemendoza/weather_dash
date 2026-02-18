"""
weather_dash.py — Terminal Weather Dashboard
Fetches real-time weather and displays it with rich terminal styling.
"""

import sys
import argparse
import requests
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.rule import Rule
from rich import box

console = Console()

# Weather condition → emoji map
CONDITION_ICONS = {
    "clear": "☀️",
    "sunny": "☀️",
    "cloud": "☁️",
    "overcast": "🌥️",
    "mist": "🌫️",
    "fog": "🌫️",
    "drizzle": "🌦️",
    "rain": "🌧️",
    "thunder": "⛈️",
    "snow": "❄️",
    "sleet": "🌨️",
    "blizzard": "🌨️",
    "hail": "🌩️",
    "wind": "💨️",
}

WIND_DIRECTIONS = {
    "N": "↑", "NNE": "↗", "NE": "↗", "ENE": "→",
    "E": "→", "ESE": "↘", "SE": "↘", "SSE": "↓",
    "S": "↓", "SSW": "↙", "SW": "↙", "WSW": "←",
    "W": "←", "WNW": "↖", "NW": "↖", "NNW": "↑",
}

def get_condition_icon(description: str) -> str:
    desc = description.lower()
    for key, icon in CONDITION_ICONS.items():
        if key in desc:
            return icon
    return "🌡️"

def temp_color(temp_c: float) -> str:
    if temp_c <= 0:
        return "bold cyan"
    elif temp_c <= 10:
        return "bold blue"
    elif temp_c <= 20:
        return "bold green"
    elif temp_c <= 30:
        return "bold yellow"
    else:
        return "bold red"

def fetch_weather(city: str) -> dict:
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        console.print("[bold red]❌  No internet connection.[/bold red]")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        console.print(f"[bold red]❌  HTTP Error: {e}[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]❌  Error fetching weather: {e}[/bold red]")
        sys.exit(1)

def build_current_panel(data: dict, city: str) -> Panel:
    current = data["current_condition"][0]
    nearest = data["nearest_area"][0]

    area = nearest["areaName"][0]["value"]
    country = nearest["country"][0]["value"]
    location_str = f"{area}, {country}"

    temp_c = int(current["temp_C"])
    feels_c = int(current["FeelsLikeC"])
    humidity = current["humidity"]
    desc = current["weatherDesc"][0]["value"]
    wind_kmph = current["windspeedKmph"]
    wind_dir = current["winddir16Point"]
    visibility = current["visibility"]
    uv_index = current["uvIndex"]
    pressure = current["pressure"]

    icon = get_condition_icon(desc)
    color = temp_color(temp_c)
    wind_arrow = WIND_DIRECTIONS.get(wind_dir, "?")

    content = Text()
    content.append(f"\n  {icon}  ", style="bold")
    content.append(f"{temp_c}°C", style=color + " bold")
    content.append(f"  feels like {feels_c}°C\n", style="dim")
    content.append(f"\n  📍 {location_str}\n", style="white")
    content.append(f"  🌤  {desc}\n\n", style="italic white")
    content.append(f"  💧 Humidity:    {humidity}%\n", style="cyan")
    content.append(f"  💨 Wind:        {wind_arrow} {wind_kmph} km/h ({wind_dir})\n", style="cyan")
    content.append(f"  👁  Visibility:  {visibility} km\n", style="cyan")
    content.append(f"  📊 Pressure:    {pressure} hPa\n", style="cyan")
    content.append(f"  ☀️  UV Index:    {uv_index}\n", style="cyan")

    return Panel(
        content,
        title=f"[bold white]Current Weather — {city.title()}[/bold white]",
        border_style="bright_blue",
        box=box.ROUNDED,
        padding=(0, 1),
    )

def build_forecast_panels(data: dict) -> list:
    panels = []
    weather_days = data["weather"][:3]
    day_names = ["📅 Today", "📅 Tomorrow", "📅 Day After"]

    for i, day in enumerate(weather_days):
        date = day["date"]
        max_c = int(day["maxtempC"])
        min_c = int(day["mintempC"])
        sunrise = day["astronomy"][0]["sunrise"]
        sunset = day["astronomy"][0]["sunset"]
        moon = day["astronomy"][0]["moon_phase"]

        hourly = day["hourly"]
        mid = hourly[len(hourly) // 2]
        desc = mid["weatherDesc"][0]["value"]
        icon = get_condition_icon(desc)

        content = Text()
        content.append(f"\n  {icon}  {desc}\n", style="italic")
        content.append(f"\n  🌡️  {max_c}°C  /  {min_c}°C\n", style=temp_color(max_c))
        content.append(f"\n  🌅 {sunrise}   🌇 {sunset}\n", style="yellow")
        content.append(f"  🌙 {moon}\n", style="dim white")

        panels.append(Panel(
            content,
            title=f"[bold]{day_names[i]}[/bold]  [dim]{date}[/dim]",
            border_style="blue",
            box=box.SIMPLE_HEAVY,
            padding=(0, 1),
        ))

    return panels

def display_weather(city: str):
    console.print()
    with console.status(f"[bold blue]Fetching weather for [cyan]{city}[/cyan]...[/bold blue]"):
        data = fetch_weather(city)

    console.print(Rule("[bold bright_blue]🌍  Weather Dashboard[/bold bright_blue]", style="bright_blue"))
    console.print()
    console.print(build_current_panel(data, city))
    console.print()
    console.print(Rule("[bold blue]3-Day Forecast[/bold blue]", style="blue"))
    console.print()
    forecast_panels = build_forecast_panels(data)
    console.print(Columns(forecast_panels, equal=True, expand=True))
    console.print()
    console.print(Rule(style="dim"))
    console.print("[dim]Data from wttr.in  •  weather-dash[/dim]\n")

def main():
    parser = argparse.ArgumentParser(
        description="🌦️  weather-dash — Terminal Weather Dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n  python weather_dash.py London\n  python weather_dash.py \"New York\"\n  python weather_dash.py Tokyo"
    )
    parser.add_argument("city", nargs="?", default="London", help="City name (default: London)")
    args = parser.parse_args()

    display_weather(args.city)

if __name__ == "__main__":
    main()
