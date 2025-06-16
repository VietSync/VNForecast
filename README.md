# 🌤️ Vietnam Weather Dashboard

A beautiful, Apple Weather-inspired Streamlit dashboard providing real-time weather information for all 63 Vietnamese provinces. Built with modern UI/UX principles and powered by WeatherAPI.com.

![Vietnam Weather Dashboard](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![WeatherAPI](https://img.shields.io/badge/WeatherAPI-00A8CC?style=for-the-badge&logo=weather&logoColor=white)

## ✨ Features

- **🔍 Smart Province Search**: Type-ahead searchable dropdown with all 63 Vietnamese provinces
- **🌡️ Comprehensive Weather Data**: 
  - Current temperature and "feels like" temperature
  - Humidity and atmospheric pressure
  - Wind speed, direction, and gusts
  - UV index and visibility
  - Weather conditions with icons
- **📍 Location Information**: Detailed location data with timezone
- **🎨 Clean Interface**: Apple Weather-inspired design with metric cards
- **📱 Mobile Responsive**: Optimized for all device sizes
- **🌙 Theme Support**: Built-in light/dark theme toggle
- **⚡ Real-time Data**: Live weather updates from WeatherAPI.com

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
   