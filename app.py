import streamlit as st
import requests
import os
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Vietnam Weather Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load environment variables
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "your_api_key_here")

# Vietnamese provinces with coordinates for WeatherAPI
VIETNAMESE_PROVINCES = {
    "An Giang": "An Giang, Vietnam",
    "Bà Rịa - Vũng Tàu": "Ba Ria, Vietnam",
    "Bạc Liêu": "Bac Lieu, Vietnam",
    "Bắc Giang": "Bac Giang, Vietnam",
    "Bắc Kạn": "Bac Kan, Vietnam",
    "Bắc Ninh": "Bac Ninh, Vietnam",
    "Bến Tre": "Ben Tre, Vietnam",
    "Bình Dương": "Binh Duong, Vietnam",
    "Bình Định": "Binh Dinh, Vietnam",
    "Bình Phước": "Binh Phuoc, Vietnam",
    "Bình Thuận": "Binh Thuan, Vietnam",
    "Cà Mau": "Ca Mau, Vietnam",
    "Cần Thơ": "Can Tho, Vietnam",
    "Cao Bằng": "Cao Bang, Vietnam",
    "Đà Nẵng": "Da Nang, Vietnam",
    "Đắk Lắk": "Dak Lak, Vietnam",
    "Đắk Nông": "Dak Nong, Vietnam",
    "Điện Biên": "Dien Bien, Vietnam",
    "Đồng Nai": "Dong Nai, Vietnam",
    "Đồng Tháp": "Dong Thap, Vietnam",
    "Gia Lai": "Gia Lai, Vietnam",
    "Hà Giang": "Ha Giang, Vietnam",
    "Hà Nam": "Ha Nam, Vietnam",
    "Hà Nội": "Hanoi, Vietnam",
    "Hà Tĩnh": "Ha Tinh, Vietnam",
    "Hải Dương": "Hai Duong, Vietnam",
    "Hải Phòng": "Hai Phong, Vietnam",
    "Hậu Giang": "Hau Giang, Vietnam",
    "Hòa Bình": "Hoa Binh, Vietnam",
    "Hưng Yên": "Hung Yen, Vietnam",
    "Khánh Hòa": "Khanh Hoa, Vietnam",
    "Kiên Giang": "Kien Giang, Vietnam",
    "Kon Tum": "Kon Tum, Vietnam",
    "Lai Châu": "Lai Chau, Vietnam",
    "Lâm Đồng": "Lam Dong, Vietnam",
    "Lạng Sơn": "Lang Son, Vietnam",
    "Lào Cai": "Lao Cai, Vietnam",
    "Long An": "Long An, Vietnam",
    "Nam Định": "Nam Dinh, Vietnam",
    "Nghệ An": "Nghe An, Vietnam",
    "Ninh Bình": "Ninh Binh, Vietnam",
    "Ninh Thuận": "Ninh Thuan, Vietnam",
    "Phú Thọ": "Phu Tho, Vietnam",
    "Phú Yên": "Phu Yen, Vietnam",
    "Quảng Bình": "Quang Binh, Vietnam",
    "Quảng Nam": "Quang Nam, Vietnam",
    "Quảng Ngãi": "Quang Ngai, Vietnam",
    "Quảng Ninh": "Quang Ninh, Vietnam",
    "Quảng Trị": "Quang Tri, Vietnam",
    "Sóc Trăng": "Soc Trang, Vietnam",
    "Sơn La": "Son La, Vietnam",
    "Tây Ninh": "Tay Ninh, Vietnam",
    "Thái Bình": "Thai Binh, Vietnam",
    "Thái Nguyên": "Thai Nguyen, Vietnam",
    "Thanh Hóa": "Thanh Hoa, Vietnam",
    "Thừa Thiên Huế": "Hue, Vietnam",
    "Tiền Giang": "Tien Giang, Vietnam",
    "TP. Hồ Chí Minh": "Ho Chi Minh City, Vietnam",
    "Trà Vinh": "Tra Vinh, Vietnam",
    "Tuyên Quang": "Tuyen Quang, Vietnam",
    "Vĩnh Long": "Vinh Long, Vietnam",
    "Vĩnh Phúc": "Vinh Phuc, Vietnam",
    "Yên Bái": "Yen Bai, Vietnam"
}

def get_weather_data(location):
    """Fetch current weather data from WeatherAPI.com"""
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}&aqi=yes"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

def get_forecast_data(location, days=3):
    """Fetch forecast data from WeatherAPI.com"""
    try:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days={days}&aqi=no&alerts=yes"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching forecast data: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

def get_weather_icon_url(icon_code):
    """Get weather icon URL from WeatherAPI"""
    return f"https:{icon_code}" if icon_code.startswith('//') else icon_code

def format_time(time_str):
    """Format time string to 12-hour format"""
    try:
        time_obj = datetime.strptime(time_str, "%I:%M %p")
        return time_obj.strftime("%I:%M %p")
    except:
        return time_str

def get_weather_gradient(condition, temp_c):
    """Get dynamic background gradient based on weather condition and temperature"""
    condition_lower = condition.lower()
    
    # Temperature-based color intensity
    temp_intensity = min(max((temp_c - 10) / 30, 0), 1)  # 0-1 scale based on temp
    
    if any(word in condition_lower for word in ['sunny', 'clear']):
        if temp_c > 25:
            return "linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF6B35 100%)"
        else:
            return "linear-gradient(135deg, #87CEEB 0%, #FFD700 50%, #FFA500 100%)"
    elif any(word in condition_lower for word in ['rain', 'drizzle', 'shower']):
        return "linear-gradient(135deg, #4682B4 0%, #5F9EA0 50%, #708090 100%)"
    elif any(word in condition_lower for word in ['cloud', 'overcast']):
        return "linear-gradient(135deg, #B0C4DE 0%, #D3D3D3 50%, #A9A9A9 100%)"
    elif any(word in condition_lower for word in ['fog', 'mist']):
        return "linear-gradient(135deg, #F5F5F5 0%, #E0E0E0 50%, #D3D3D3 100%)"
    elif any(word in condition_lower for word in ['snow']):
        return "linear-gradient(135deg, #F0F8FF 0%, #E6E6FA 50%, #D8BFD8 100%)"
    elif any(word in condition_lower for word in ['thunder', 'storm']):
        return "linear-gradient(135deg, #2F4F4F 0%, #696969 50%, #808080 100%)"
    else:
        # Default gradient based on temperature
        if temp_c > 30:
            return "linear-gradient(135deg, #FF6B35 0%, #F7931E 50%, #FFD700 100%)"
        elif temp_c > 20:
            return "linear-gradient(135deg, #87CEEB 0%, #98FB98 50%, #FFD700 100%)"
        else:
            return "linear-gradient(135deg, #B0E0E6 0%, #87CEEB 50%, #ADD8E6 100%)"

def get_weather_animation(condition):
    """Get CSS animation based on weather condition"""
    condition_lower = condition.lower()
    
    if any(word in condition_lower for word in ['sunny', 'clear']):
        return """
        @keyframes sunGlow {
            0%, 100% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.8); }
            50% { box-shadow: 0 0 40px rgba(255, 215, 0, 1), 0 0 60px rgba(255, 165, 0, 0.8); }
        }
        .weather-animation { animation: sunGlow 3s ease-in-out infinite; }
        """
    elif any(word in condition_lower for word in ['rain', 'drizzle']):
        return """
        @keyframes rainDrop {
            0% { transform: translateY(-10px); opacity: 0; }
            50% { opacity: 1; }
            100% { transform: translateY(10px); opacity: 0; }
        }
        .weather-animation::before {
            content: '💧 💧 💧';
            position: absolute;
            top: -20px;
            left: 50%;
            transform: translateX(-50%);
            animation: rainDrop 2s ease-in-out infinite;
        }
        """
    elif any(word in condition_lower for word in ['cloud']):
        return """
        @keyframes cloudFloat {
            0%, 100% { transform: translateX(-5px); }
            50% { transform: translateX(5px); }
        }
        .weather-animation { animation: cloudFloat 4s ease-in-out infinite; }
        """
    elif any(word in condition_lower for word in ['thunder', 'storm']):
        return """
        @keyframes lightning {
            0%, 90%, 100% { opacity: 1; }
            95% { opacity: 0.7; box-shadow: 0 0 50px rgba(255, 255, 255, 0.9); }
        }
        .weather-animation { animation: lightning 3s ease-in-out infinite; }
        """
    else:
        return """
        @keyframes gentle {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        .weather-animation { animation: gentle 4s ease-in-out infinite; }
        """

def main():
    # Enhanced CSS for Apple Weather-like styling with animations
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        font-size: 2.5rem;
        font-weight: 300;
        color: #1a1a1a;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .weather-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    .dynamic-weather-card {
        border-radius: 25px;
        padding: 3rem 2rem;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
        transition: all 0.5s ease;
    }
    .temp-display {
        text-align: center;
        padding: 2rem 0;
        position: relative;
    }
    .main-temp {
        font-size: 5rem;
        font-weight: 100;
        margin: 0;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    .condition-text {
        font-size: 1.5rem;
        font-weight: 300;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .location-text {
        font-size: 1.2rem;
        font-weight: 400;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.2rem;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    .search-container {
        max-width: 400px;
        margin: 0 auto 2rem auto;
    }
    .stSelectbox > div > div {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        background: rgba(255, 255, 255, 0.9);
        transition: all 0.3s ease;
    }
    .hourly-forecast {
        display: flex;
        overflow-x: auto;
        gap: 1rem;
        padding: 1rem 0;
        scrollbar-width: none;
        -ms-overflow-style: none;
    }
    .hourly-forecast::-webkit-scrollbar {
        display: none;
    }
    .hourly-item {
        min-width: 80px;
        text-align: center;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 1rem 0.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    .weather-icon-large {
        width: 120px;
        height: 120px;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
        transition: transform 0.3s ease;
    }
    .weather-icon-large:hover {
        transform: scale(1.1);
    }
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .main-header { font-size: 2rem; padding: 1rem 0 0.5rem 0; }
        .main-temp { font-size: 3.5rem; }
        .condition-text { font-size: 1.2rem; }
        .weather-icon-large { width: 80px; height: 80px; }
        .dynamic-weather-card { padding: 2rem 1rem; margin: 1rem 0; }
        .metric-card { padding: 1rem; margin: 0.3rem 0; }
        .hourly-item { min-width: 70px; padding: 0.8rem 0.3rem; }
        .search-container { max-width: 100%; padding: 0 1rem; }
    }
    
    @media (max-width: 480px) {
        .main-temp { font-size: 3rem; }
        .metric-card { font-size: 0.9rem; }
        .hourly-forecast { gap: 0.5rem; }
        .hourly-item { min-width: 60px; }
    }
    </style>
    """, unsafe_allow_html=True)
    

    
    # Header
    st.markdown('<div class="main-header">Vietnam Weather</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Real-time weather for all 63 provinces</div>', unsafe_allow_html=True)
    
    # Province selection with custom styling
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    selected_province = st.selectbox(
        "Search provinces",
        options=list(VIETNAMESE_PROVINCES.keys()),
        index=None,
        placeholder="Search for a province...",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if selected_province:
        location = VIETNAMESE_PROVINCES[selected_province]
        
        # Fetch weather data
        with st.spinner(f"Getting weather data for {selected_province}..."):
            weather_data = get_weather_data(location)
        
        if weather_data:
            current = weather_data['current']
            location_info = weather_data['location']
            
            # Get dynamic styling based on weather
            gradient = get_weather_gradient(current['condition']['text'], current['temp_c'])
            animation_css = get_weather_animation(current['condition']['text'])
            
            # Add weather-specific animation CSS
            st.markdown(f"<style>{animation_css}</style>", unsafe_allow_html=True)
            
            # Dynamic animated weather card
            st.markdown(f"""
            <div class="dynamic-weather-card weather-animation fade-in" style="background: {gradient};">
                <div class="location-text">
                    {location_info['name']}, {location_info['region']}
                </div>
                <div class="temp-display">
                    <img src="{get_weather_icon_url(current['condition']['icon'])}" class="weather-icon-large" style="margin-bottom: 1rem;">
                    <div class="main-temp">{current['temp_c']}°</div>
                    <div class="condition-text">{current['condition']['text']}</div>
                    <div style="color: rgba(255, 255, 255, 0.7); margin-top: 0.5rem; font-size: 1rem;">
                        H:{int(current['temp_c']) + 3}° L:{int(current['temp_c']) - 5}°
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Apple-style metrics grid
            st.markdown("""
            <div style="margin: 2rem 0;">
            """, unsafe_allow_html=True)
            
            # First row of metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;">FEELS LIKE</div>
                    <div style="font-size: 2rem; font-weight: 300;">{current['feelslike_c']}°</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;">HUMIDITY</div>
                    <div style="font-size: 2rem; font-weight: 300;">{current['humidity']}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;">WIND</div>
                    <div style="font-size: 2rem; font-weight: 300;">{current['wind_kph']}</div>
                    <div style="color: #999; font-size: 0.8rem;">km/h {current['wind_dir']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Second row of metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;">PRESSURE</div>
                    <div style="font-size: 2rem; font-weight: 300;">{current['pressure_mb']}</div>
                    <div style="color: #999; font-size: 0.8rem;">mb</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;">VISIBILITY</div>
                    <div style="font-size: 2rem; font-weight: 300;">{current['vis_km']}</div>
                    <div style="color: #999; font-size: 0.8rem;">km</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;">UV INDEX</div>
                    <div style="font-size: 2rem; font-weight: 300;">{current['uv']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Air Quality and Extended Weather Info
            col1, col2 = st.columns(2)
            
            with col1:
                # Air Quality (if available)
                if 'air_quality' in current:
                    aqi = current['air_quality']
                    aqi_value = aqi.get('us-epa-index', 0)
                    aqi_levels = ["Good", "Moderate", "Unhealthy for Sensitive", "Unhealthy", "Very Unhealthy", "Hazardous"]
                    aqi_level = aqi_levels[min(aqi_value - 1, 5)] if aqi_value > 0 else "N/A"
                    aqi_colors = ["#00E400", "#FFFF00", "#FF7E00", "#FF0000", "#8F3F97", "#7E0023"]
                    aqi_color = aqi_colors[min(aqi_value - 1, 5)] if aqi_value > 0 else "#999"
                    
                    st.markdown(f"""
                    <div class="metric-card" style="text-align: left; padding: 1.5rem;">
                        <div style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">AIR QUALITY</div>
                        <div style="font-size: 2rem; font-weight: 300; color: {aqi_color}; margin-bottom: 0.5rem;">{aqi_value}</div>
                        <div style="color: {aqi_color}; font-weight: 500;">{aqi_level}</div>
                        <div style="margin-top: 1rem; font-size: 0.8rem; color: #666;">
                            CO: {aqi.get('co', 0):.1f} μg/m³<br>
                            NO₂: {aqi.get('no2', 0):.1f} μg/m³<br>
                            PM2.5: {aqi.get('pm2_5', 0):.1f} μg/m³
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="metric-card" style="text-align: left; padding: 1.5rem;">
                        <div style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">WEATHER DETAILS</div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: 0.9rem;">
                            <div><strong>Cloud Cover:</strong> {current['cloud']}%</div>
                            <div><strong>Precipitation:</strong> {current['precip_mm']} mm</div>
                            <div><strong>Local Time:</strong> {location_info['localtime'].split()[1]}</div>
                            <div><strong>Timezone:</strong> {location_info['tz_id'].split('/')[-1]}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                # Extended weather metrics
                st.markdown(f"""
                <div class="metric-card" style="text-align: left; padding: 1.5rem;">
                    <div style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">COMFORT INDEX</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: 0.9rem;">
                        <div><strong>Heat Index:</strong> {current['feelslike_c']}°C</div>
                        <div><strong>Wind Chill:</strong> {current['windchill_c'] if 'windchill_c' in current else 'N/A'}</div>
                        <div><strong>Wind Gust:</strong> {current.get('gust_kph', 'N/A')} km/h</div>
                        <div><strong>Dew Point:</strong> {current.get('dewpoint_c', 'N/A')}°C</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Fetch and display hourly forecast
            st.markdown('<div style="margin-top: 2rem;"><div style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">24-HOUR FORECAST</div></div>', unsafe_allow_html=True)
            
            with st.spinner("Loading hourly forecast..."):
                forecast_data = get_forecast_data(location, days=2)
            
            if forecast_data and 'forecast' in forecast_data:
                # Get today and tomorrow's hourly data
                today_hours = forecast_data['forecast']['forecastday'][0]['hour']
                current_hour = int(location_info['localtime'].split()[1].split(':')[0])
                
                # Show next 12 hours starting from current hour
                hourly_items = []
                for i in range(12):
                    hour_index = (current_hour + i) % 24
                    if i < (24 - current_hour):
                        hour_data = today_hours[hour_index]
                        time_label = "Now" if i == 0 else f"{hour_index:02d}:00"
                    else:
                        # Tomorrow's data
                        if len(forecast_data['forecast']['forecastday']) > 1:
                            tomorrow_hours = forecast_data['forecast']['forecastday'][1]['hour']
                            hour_data = tomorrow_hours[hour_index]
                            time_label = f"{hour_index:02d}:00"
                        else:
                            continue
                    
                    hourly_items.append(f"""
                    <div class="hourly-item">
                        <div style="font-size: 0.8rem; color: #666; margin-bottom: 0.5rem;">{time_label}</div>
                        <img src="{get_weather_icon_url(hour_data['condition']['icon'])}" width="40" style="margin: 0.5rem 0;">
                        <div style="font-weight: 500;">{hour_data['temp_c']}°</div>
                        <div style="font-size: 0.7rem; color: #999; margin-top: 0.3rem;">{hour_data['chance_of_rain']}%</div>
                    </div>
                    """)
                
                st.markdown(f"""
                <div class="hourly-forecast">
                    {''.join(hourly_items)}
                </div>
                """, unsafe_allow_html=True)
                
                # Weather alerts (if any)
                if 'alerts' in forecast_data and forecast_data['alerts']['alert']:
                    st.markdown('<div style="margin-top: 2rem;"><div style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">WEATHER ALERTS</div></div>', unsafe_allow_html=True)
                    
                    for alert in forecast_data['alerts']['alert']:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%); 
                                    color: white; padding: 1.5rem; border-radius: 15px; margin: 1rem 0;
                                    box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);">
                            <div style="font-weight: 600; margin-bottom: 0.5rem;">⚠️ {alert['headline']}</div>
                            <div style="font-size: 0.9rem; opacity: 0.9;">{alert['desc']}</div>
                            <div style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.8;">
                                Effective: {alert['effective']} - {alert['expires']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # 3-Day Forecast
            if forecast_data and 'forecast' in forecast_data:
                st.markdown('<div style="margin-top: 2rem;"><div style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">3-DAY FORECAST</div></div>', unsafe_allow_html=True)
                
                forecast_days = forecast_data['forecast']['forecastday']
                
                for i, day in enumerate(forecast_days):
                    date_obj = datetime.strptime(day['date'], '%Y-%m-%d')
                    day_name = "Today" if i == 0 else date_obj.strftime('%A')
                    date_str = date_obj.strftime('%b %d')
                    
                    day_data = day['day']
                    
                    # Calculate rain probability from hourly data
                    avg_rain_chance = sum([hour['chance_of_rain'] for hour in day['hour']]) / 24
                    
                    st.markdown(f"""
                    <div class="metric-card" style="padding: 1.5rem; margin: 0.5rem 0;">
                        <div style="display: flex; align-items: center; justify-content: space-between;">
                            <div style="flex: 1;">
                                <div style="font-weight: 500; margin-bottom: 0.2rem;">{day_name}</div>
                                <div style="color: #666; font-size: 0.9rem;">{date_str}</div>
                            </div>
                            <div style="flex: 1; text-align: center;">
                                <img src="{get_weather_icon_url(day_data['condition']['icon'])}" width="50">
                                <div style="font-size: 0.8rem; color: #666; margin-top: 0.2rem;">{avg_rain_chance:.0f}%</div>
                            </div>
                            <div style="flex: 1; text-align: right;">
                                <div style="font-weight: 500;">{day_data['maxtemp_c']:.0f}°</div>
                                <div style="color: #666;">{day_data['mintemp_c']:.0f}°</div>
                            </div>
                        </div>
                        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #eee; font-size: 0.8rem; color: #666;">
                            {day_data['condition']['text']} • UV Index: {day_data['uv']} • Max Wind: {day_data['maxwind_kph']} km/h
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
        else:
            st.error("Unable to fetch weather data. Please check your internet connection and try again.")
    
    else:
        # Welcome message with Apple-style design
        st.markdown("""
        <div class="weather-card" style="text-align: center; margin-top: 3rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🌤️</div>
            <div style="font-size: 1.5rem; font-weight: 300; margin-bottom: 1rem; color: #666;">
                Select a province above to view current weather conditions
            </div>
            <div style="font-size: 1rem; color: #999; line-height: 1.6;">
                Real-time weather data for all 63 Vietnamese provinces<br>
                Powered by WeatherAPI.com
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick access to popular cities
        st.markdown("""
        <div style="margin-top: 2rem;">
            <div style="text-align: center; color: #666; margin-bottom: 1rem; font-size: 0.9rem;">POPULAR DESTINATIONS</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        popular_provinces = ["Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng"]
        
        for i, province in enumerate(popular_provinces):
            with [col1, col2, col3][i]:
                if st.button(province, key=f"popular_{i}", use_container_width=True):
                    st.session_state.selected_province = province
                    st.rerun()
    
    # Footer with minimal styling
    st.markdown("""
    <div style="text-align: center; color: #ccc; padding: 3rem 0 1rem 0; font-size: 0.8rem;">
        Vietnam Weather Dashboard
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
