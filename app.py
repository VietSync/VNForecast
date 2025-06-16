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
    """Fetch weather data from WeatherAPI.com"""
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}&aqi=no"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {str(e)}")
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

def main():
    # Header
    st.title("🌤️ Vietnam Weather Dashboard")
    st.markdown("*Real-time weather information for all 63 Vietnamese provinces*")
    
    # Theme toggle
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🌙 Toggle Theme"):
            st.rerun()
    
    # Province selection
    st.markdown("### Select a Province")
    selected_province = st.selectbox(
        "Choose a Vietnamese province:",
        options=list(VIETNAMESE_PROVINCES.keys()),
        index=None,
        placeholder="Type to search for a province...",
        help="Search and select from all 63 Vietnamese provinces"
    )
    
    if selected_province:
        location = VIETNAMESE_PROVINCES[selected_province]
        
        # Fetch weather data
        with st.spinner(f"Getting weather data for {selected_province}..."):
            weather_data = get_weather_data(location)
        
        if weather_data:
            current = weather_data['current']
            location_info = weather_data['location']
            
            # Location header
            st.markdown(f"## 📍 {location_info['name']}, {location_info['region']}")
            st.markdown(f"*Last updated: {current['last_updated']}*")
            
            # Main temperature display
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown(f"""
                <div style="text-align: center; padding: 20px;">
                    <img src="{get_weather_icon_url(current['condition']['icon'])}" width="100">
                    <h1 style="font-size: 4rem; margin: 10px 0;">{current['temp_c']}°C</h1>
                    <h3 style="margin: 5px 0;">{current['condition']['text']}</h3>
                </div>
                """, unsafe_allow_html=True)
            
            # Weather metrics
            st.markdown("### Weather Details")
            
            # First row of metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="🌡️ Feels Like",
                    value=f"{current['feelslike_c']}°C"
                )
            
            with col2:
                st.metric(
                    label="💧 Humidity",
                    value=f"{current['humidity']}%"
                )
            
            with col3:
                st.metric(
                    label="💨 Wind Speed",
                    value=f"{current['wind_kph']} km/h"
                )
            
            with col4:
                st.metric(
                    label="🧭 Wind Direction",
                    value=current['wind_dir']
                )
            
            # Second row of metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="🌊 Pressure",
                    value=f"{current['pressure_mb']} mb"
                )
            
            with col2:
                st.metric(
                    label="👁️ Visibility",
                    value=f"{current['vis_km']} km"
                )
            
            with col3:
                st.metric(
                    label="☀️ UV Index",
                    value=f"{current['uv']}"
                )
            
            with col4:
                st.metric(
                    label="🌡️ Dew Point",
                    value=f"{current.get('dewpoint_c', 'N/A')}°C" if 'dewpoint_c' in current else "N/A"
                )
            
            # Additional information
            st.markdown("### Additional Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(f"""
                **🌍 Location Details:**
                - **Country:** {location_info['country']}
                - **Region:** {location_info['region']}
                - **Timezone:** {location_info['tz_id']}
                - **Local Time:** {location_info['localtime']}
                """)
            
            with col2:
                st.info(f"""
                **🌤️ Current Conditions:**
                - **Weather:** {current['condition']['text']}
                - **Cloud Cover:** {current['cloud']}%
                - **Precipitation:** {current['precip_mm']} mm
                - **Wind Gust:** {current.get('gust_kph', 'N/A')} km/h
                """)
            
            # Weather summary card
            st.markdown("### Weather Summary")
            summary_text = f"""
            Currently in **{selected_province}**, it's **{current['condition']['text'].lower()}** 
            with a temperature of **{current['temp_c']}°C** (feels like {current['feelslike_c']}°C). 
            The humidity is at **{current['humidity']}%** with winds blowing at **{current['wind_kph']} km/h** 
            from the **{current['wind_dir']}**. The visibility is **{current['vis_km']} km** 
            and the UV index is **{current['uv']}**.
            """
            st.success(summary_text)
            
        else:
            st.error("Unable to fetch weather data. Please check your internet connection and try again.")
    
    else:
        # Welcome message when no province is selected
        st.markdown("### Welcome to Vietnam Weather Dashboard")
        st.info("""
        👆 **Select a province above** to view current weather conditions.
        
        **Features:**
        - 🔍 Search from all 63 Vietnamese provinces
        - 🌡️ Current temperature and feels-like temperature
        - 💧 Humidity and atmospheric pressure
        - 💨 Wind speed and direction
        - ☀️ UV index and visibility
        - 🌤️ Weather conditions with icons
        - 📍 Location and timezone information
        
        **Data Source:** WeatherAPI.com - providing accurate, real-time weather data.
        """)
        
        # Display some provinces as examples
        st.markdown("### Popular Provinces")
        col1, col2, col3 = st.columns(3)
        
        popular_provinces = ["Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng"]
        for i, province in enumerate(popular_provinces):
            with [col1, col2, col3][i]:
                if st.button(f"📍 {province}", key=f"popular_{i}"):
                    st.session_state.selected_province = province
                    st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🌤️ Vietnam Weather Dashboard | Powered by WeatherAPI.com</p>
        <p>Real-time weather data for all 63 Vietnamese provinces</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
