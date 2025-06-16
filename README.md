# 🌤️ Vietnam Weather Dashboard

A beautiful, Apple Weather-inspired Streamlit dashboard providing real-time weather information for all 63 Vietnamese provinces. Built with modern UI/UX principles and powered by WeatherAPI.com.

![Vietnam Weather Dashboard](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![WeatherAPI](https://img.shields.io/badge/WeatherAPI-00A8CC?style=for-the-badge&logo=weather&logoColor=white)

## ✨ Features

- **🔍 Smart Province Search**: Type-ahead searchable dropdown with all 63 Vietnamese provinces
- **🎨 Dynamic Weather Animations**: Weather-specific background gradients and animations
  - Sunny conditions: Golden gradients with glowing sun effects
  - Rainy weather: Blue gradients with animated raindrops
  - Cloudy skies: Floating cloud animations
  - Stormy weather: Lightning effects and dark themes
- **🌡️ Comprehensive Weather Data**: 
  - Current temperature with dynamic color-coded backgrounds
  - Feels-like temperature and comfort indices
  - Humidity, pressure, and atmospheric conditions
  - Wind speed, direction, gusts, and wind chill
  - UV index and visibility metrics
  - Dew point and heat index calculations
- **🌍 Air Quality Monitoring**: Real-time AQI data with color-coded health indicators
- **⏰ 24-Hour Forecast**: Scrollable hourly weather predictions with precipitation chances
- **📅 3-Day Extended Forecast**: Daily weather outlook with detailed conditions
- **⚠️ Weather Alerts**: Automatic severe weather warnings and advisories
- **📍 Location Intelligence**: Detailed location data with timezone information
- **📱 Mobile Responsive**: Fully optimized for all device sizes with touch-friendly interface
- **🎭 Apple Weather UI**: Glassmorphism cards, smooth animations, and premium typography
- **⚡ Real-time Data**: Live weather updates from WeatherAPI.com with comprehensive coverage

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- WeatherAPI.com API key (free tier available)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/vietnam-weather-dashboard.git
   cd vietnam-weather-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file and add your WeatherAPI key
   ```

4. **Run the application**
   ```bash
   streamlit run app.py

   NOTES: Streamlit port is 8501,Normal Port IS 5000
   