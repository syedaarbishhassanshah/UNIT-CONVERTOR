import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Advanced Unit Converter",
    page_icon="📏",
    layout="wide"
)

# Enhanced CSS
st.markdown("""
    <style>
    .stApp { max-width: 1200px; margin: 0 auto; }
    .stButton>button { 
        width: 100%; 
        background-color: #4285f4; 
        color: white;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #357abd;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .result-box { 
        background-color: #e8f0fe; 
        padding: 1.5rem; 
        border-radius: 8px;
        border-left: 4px solid #4285f4;
        margin: 1rem 0;
    }
    .category-title {
        color: #4285f4;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Enhanced conversion factors
CONVERSIONS = {
    'Length': {
        'meters': 1.0, 'kilometers': 0.001, 'centimeters': 100, 'millimeters': 1000,
        'inches': 39.3701, 'feet': 3.28084, 'yards': 1.09361, 'miles': 0.000621371,
        'nautical miles': 0.000539957
    },
    'Weight': {
        'kilograms': 1.0, 'grams': 1000, 'pounds': 2.20462, 'ounces': 35.274,
        'metric tons': 0.001, 'short tons': 0.00110231, 'long tons': 0.000984207
    },
    'Temperature': {'celsius': 'C', 'fahrenheit': 'F', 'kelvin': 'K', 'rankine': 'R'},
    'Volume': {
        'liters': 1.0, 'milliliters': 1000, 'cubic meters': 0.001,
        'gallons': 0.264172, 'cubic feet': 0.0353147, 'cubic inches': 61.0237
    },
    'Speed': {
        'meters per second': 1.0, 'kilometers per hour': 3.6, 'miles per hour': 2.23694,
        'feet per second': 3.28084, 'knots': 1.94384
    },
    'Pressure': {
        'pascals': 1.0, 'kilopascals': 0.001, 'bar': 0.00001,
        'atmosphere': 0.00000986923, 'psi': 0.000145038
    }
}

def convert_temperature(value, from_unit, to_unit):
    if from_unit == 'fahrenheit': celsius = (value - 32) * 5/9
    elif from_unit == 'kelvin': celsius = value - 273.15
    elif from_unit == 'rankine': celsius = (value - 491.67) * 5/9
    else: celsius = value
    
    if to_unit == 'fahrenheit': return (celsius * 9/5) + 32
    elif to_unit == 'kelvin': return celsius + 273.15
    elif to_unit == 'rankine': return (celsius * 9/5) + 491.67
    return celsius

def format_number(num, precision=6):
    if abs(num) < 0.000001 or abs(num) > 1000000:
        return f"{num:.{precision}e}"
    return f"{num:.{precision}f}"

def create_conversion_chart(values, from_unit, to_unit, category):
    df = pd.DataFrame({
        'Value': values,
        'Converted': [v * CONVERSIONS[category][to_unit] / CONVERSIONS[category][from_unit] for v in values]
    })
    fig = px.line(df, x='Value', y='Converted', 
                  title=f'Conversion Chart: {from_unit} to {to_unit}',
                  labels={'Value': from_unit, 'Converted': to_unit})
    return fig

def main():
    st.title("🚀 Advanced Unit Converter")
    
    # Sidebar with advanced options
    with st.sidebar:
        st.header("Advanced Options")
        show_history = st.checkbox("Show Conversion History", value=True)
        show_chart = st.checkbox("Show Conversion Chart", value=True)
        precision = st.slider("Result Precision", 2, 10, 6)
        st.markdown("---")
        st.markdown("### Quick Tips")
        st.markdown("""
        - Use the chart to visualize conversions
        - Enable history to track your conversions
        - Adjust precision for more accurate results
        """)

    # Main conversion interface
    col1, col2 = st.columns([1, 2])
    
    with col1:
        category = st.selectbox("Category", list(CONVERSIONS.keys()))
        from_unit = st.selectbox("From", list(CONVERSIONS[category].keys()), key="from")
        to_unit = st.selectbox("To", list(CONVERSIONS[category].keys()), key="to")
        value = st.number_input("Value", min_value=0.0, step=0.1, format="%.6f")
        
        if st.button("Convert", key="convert"):
            if category == 'Temperature':
                result = convert_temperature(value, from_unit, to_unit)
            else:
                base_value = value / CONVERSIONS[category][from_unit]
                result = base_value * CONVERSIONS[category][to_unit]
            
            st.markdown(f"""
            <div class="result-box">
                <h3>Result:</h3>
                <p>{format_number(value, precision)} {from_unit} = {format_number(result, precision)} {to_unit}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if show_history:
                history_data = {
                    "From": [f"{format_number(value, precision)} {from_unit}"],
                    "To": [f"{format_number(result, precision)} {to_unit}"],
                    "Category": [category],
                    "Time": [datetime.now().strftime("%H:%M:%S")]
                }
                st.dataframe(pd.DataFrame(history_data))
    
    with col2:
        if show_chart and category != 'Temperature':
            values = [i * value/10 for i in range(11)]
            fig = create_conversion_chart(values, from_unit, to_unit, category)
            st.plotly_chart(fig, use_container_width=True)
        elif show_chart and category == 'Temperature':
            st.info("Temperature conversion chart is not available due to non-linear conversion.")

if __name__ == "__main__":
    main() 