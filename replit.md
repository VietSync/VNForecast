# Vietnam Weather Dashboard

## Overview

A modern, Apple Weather-inspired Streamlit dashboard that provides real-time weather information for all 63 Vietnamese provinces. The application features a clean, responsive interface with comprehensive weather data including temperature, humidity, wind conditions, and more. Built with Python and Streamlit, it integrates with WeatherAPI.com for live weather data.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for web application framework
- **UI Design**: Apple Weather-inspired interface with metric cards
- **Responsive Design**: Mobile-optimized layout using Streamlit's wide layout configuration
- **Theme Support**: Light/dark theme toggle capabilities
- **Search Interface**: Type-ahead searchable dropdown for province selection

### Backend Architecture
- **Runtime**: Python 3.11+
- **Web Framework**: Streamlit server handling HTTP requests and responses
- **API Integration**: Direct HTTP requests to WeatherAPI.com using the requests library
- **Data Processing**: Real-time weather data parsing and formatting
- **Environment Management**: Environment variable configuration for API keys

### Data Storage Solutions
- **Configuration Storage**: Environment variables for API keys and settings
- **Static Data**: Hardcoded dictionary of Vietnamese provinces with location mappings
- **No Database**: Application operates as a stateless service with no persistent data storage

## Key Components

### Core Application (`app.py`)
- Main Streamlit application entry point
- Weather data fetching and processing logic
- UI rendering and user interaction handling
- Province search and selection functionality

### Configuration Management
- **Environment Variables**: `.env` file for sensitive configuration (API keys)
- **Streamlit Config**: `.streamlit/config.toml` for server and theme settings
- **Project Config**: `pyproject.toml` for Python project dependencies

### Province Data Structure
- Comprehensive mapping of all 63 Vietnamese provinces
- Location-specific queries optimized for WeatherAPI.com
- Standardized naming conventions for API compatibility

## Data Flow

1. **User Input**: User selects a Vietnamese province from searchable dropdown
2. **API Request**: Application constructs weather API request with province location
3. **Data Retrieval**: HTTP request sent to WeatherAPI.com with authentication
4. **Data Processing**: JSON response parsed and formatted for display
5. **UI Update**: Streamlit updates interface with weather metrics and information
6. **Real-time Updates**: Fresh data fetched on each province selection

## External Dependencies

### Third-Party Services
- **WeatherAPI.com**: Primary weather data provider
  - Free tier available with API key registration
  - Provides current weather, forecasts, and location data
  - Rate limiting considerations for free tier usage

### Python Libraries
- **Streamlit (>=1.45.1)**: Web application framework and UI components
- **Requests (>=2.32.4)**: HTTP client for API communication
- **Standard Library**: datetime, json, os for core functionality

## Deployment Strategy

### Replit Deployment
- **Target**: Autoscale deployment on Replit platform
- **Runtime**: Python 3.11 with Nix package management
- **Port Configuration**: Streamlit server running on port 5000
- **Process Management**: Direct streamlit command execution

### Environment Setup
- **Development**: Local development with virtual environment support
- **Production**: Environment variables managed through Replit secrets
- **Configuration**: Headless server mode for cloud deployment

### Scalability Considerations
- Stateless application design supports horizontal scaling
- API rate limiting may require caching implementation for high traffic
- No database dependencies simplify deployment and scaling

## Changelog

```
Changelog:
- June 16, 2025. Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```