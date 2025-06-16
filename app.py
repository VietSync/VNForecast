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
    # Custom CSS for Apple Weather-like styling
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
    }
    .temp-display {
        text-align: center;
        padding: 2rem 0;
    }
    .main-temp {
        font-size: 5rem;
        font-weight: 100;
        margin: 0;
        color: #1a1a1a;
    }
    .condition-text {
        font-size: 1.5rem;
        font-weight: 300;
        color: #666;
        margin-top: 0.5rem;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .search-container {
        max-width: 400px;
        margin: 0 auto 2rem auto;
    }
    .stSelectbox > div > div {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        background: rgba(255, 255, 255, 0.9);
    }
    </style>
    """, unsafe_allow_html=True)
    

    
    # Header
    st.markdown('<div class="main-header">Vietnam Weather</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Real-time weather for all 63 provinces</div>', unsafe_allow_html=True)
    
    # Province selection with custom styling
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    selected_province = st.selectbox(
        "",
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
            
            # Main weather card
            st.markdown(f"""
            <div class="weather-card">
                <div style="text-align: center; color: #666; margin-bottom: 1rem;">
                    {location_info['name']}, {location_info['region']}
                </div>
                <div class="temp-display">
                    <img src="{get_weather_icon_url(current['condition']['icon'])}" width="120" style="margin-bottom: 1rem;">
                    <div class="main-temp">{current['temp_c']}°</div>
                    <div class="condition-text">{current['condition']['text']}</div>
                    <div style="color: #999; margin-top: 0.5rem;">H:{int(current['temp_c']) + 3}° L:{int(current['temp_c']) - 5}°</div>
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
            
            # Additional details in Apple style
            st.markdown(f"""
            <div style="margin-top: 2rem;">
                <div class="metric-card" style="text-align: left; padding: 1.5rem;">
                    <div style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">WEATHER DETAILS</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: 0.9rem;">
                        <div><strong>Cloud Cover:</strong> {current['cloud']}%</div>
                        <div><strong>Precipitation:</strong> {current['precip_mm']} mm</div>
                        <div><strong>Local Time:</strong> {location_info['localtime'].split()[1]}</div>
                        <div><strong>Timezone:</strong> {location_info['tz_id'].split('/')[-1]}</div>
                    </div>
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
