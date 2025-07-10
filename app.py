import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cost Optimizer AI", layout="wide")

st.title("🧠 AI-Powered Cost Optimization for R&D")
st.markdown("Upload your design data to receive cost insights, material efficiency analysis, and design suggestions.")

# --- File Upload Section ---
uploaded_file = st.file_uploader("📁 Upload your file (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully!")
        st.subheader("🔍 Uploaded Data Preview")
        st.dataframe(df.head())

        # --- Mocked AI Insights ---
        st.subheader("📊 Optimization Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Cost Reduction Potential", "28.5%")
        col2.metric("Material Efficiency", "18.3%")
        col3.metric("Durability Score", "87/100")

        st.markdown("## 🛠️ AI-Recommended Designs")
        designs = [
            {
                "ID": "VAH-2245",
                "Description": "Feed Mixing Chamber",
                "Cost": "$2,150",
                "Durability": "88/100",
                "Materials": "Polymer, Stainless Steel",
                "Score": "94.7"
            },
            {
                "ID": "VAH-2246",
                "Description": "Cooling Fan Assembly",
                "Cost": "$1,780",
                "Durability": "85/100",
                "Materials": "Aluminum, PVC",
                "Score": "92.1"
            },
            {
                "ID": "VAH-2247",
                "Description": "Vibration Control Base",
                "Cost": "$980",
                "Durability": "90/100",
                "Materials": "Rubber, Steel",
                "Score": "95.2"
            }
        ]

        design_df = pd.DataFrame(designs)
        st.dataframe(design_df)

        st.markdown("## ✅ Design Recommendations")
        recommendations = [
            "🔁 Replace stainless steel with aluminum where feasible.",
            "💨 Improve chamber airflow by 15% to enhance cooling efficiency.",
            "⚙️ Reduce motor RPM by 5% to save energy without performance loss."
        ]
        for rec in recommendations:
            st.markdown(f"- {rec}")

    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
else:
    st.info("Please upload a .csv or .xlsx file to begin.")
