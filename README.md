# 🌦️ weather-dash

> A beautiful terminal weather dashboard built with Python.

Get real-time weather and a 3-day forecast for any city — right in your terminal, with color-coded temperatures, wind direction arrows, moon phases, and more.

---

## ✨ Features

- 🌡️ **Current conditions** — temperature, feels-like, humidity, UV index, pressure, visibility
- 📅 **3-day forecast** — high/low temps, sunrise/sunset, moon phase
- 🎨 **Color-coded output** — temperature changes color from icy blue to blazing red
- 💨 **Wind direction arrows** — visual compass arrows for wind direction
- ⚡ **No API key needed** — uses the free [wttr.in](https://wttr.in) service

---

## 🖥️ Preview

```
╭─────────────────────────────────────────╮
│  Current Weather — London               │
│                                         │
│  🌧️  11°C  feels like 9°C              │
│                                         │
│  📍 London, United Kingdom              │
│  🌤  Overcast                           │
│                                         │
│  💧 Humidity:    82%                    │
│  💨 Wind:        ↙ 15 km/h (SW)        │
│  👁  Visibility:  10 km                 │
│  📊 Pressure:    1012 hPa               │
│  ☀️  UV Index:    1                     │
╰─────────────────────────────────────────╯
```

---

## 🚀 Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/weather-dash.git
cd weather-dash
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## 🔧 Usage

```bash
# Default city (London)
python weather_dash.py

# Specify a city
python weather_dash.py Tokyo
python weather_dash.py "New York"
python weather_dash.py Paris
```

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `requests` | Fetch weather data from wttr.in |
| `rich` | Beautiful terminal formatting & colors |

Install them with:
```bash
pip install requests rich
```

---

## 🌍 How It Works

weather-dash queries [wttr.in](https://wttr.in)'s free JSON API — no account or API key required. The response is parsed and rendered using the [Rich](https://github.com/Textualize/rich) library for beautiful terminal output.

---

## 📁 Project Structure

```
weather-dash/
├── weather_dash.py     # Main script
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🤝 Contributing

Pull requests are welcome! Feel free to open an issue for bugs or feature ideas.

---

## 📄 License

MIT License — free to use and modify.

---

<p align="center">Made with ☕ and Python</p>
