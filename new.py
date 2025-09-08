import streamlit as st
import pandas as pd
import numpy as np # For generating mock data

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

        # --- Check for Biomedical Data Pattern (simple check for demonstration) ---
        is_biomedical_data = False
        if 'Biocompatibility_Score' in df.columns and 'Compliance_Standard' in df.columns:
            is_biomedical_data = True

        if is_biomedical_data:
            st.subheader("🔬 Biomedical Industry Cost Optimization Insights")
            col1, col2, col3 = st.columns(3)
            col1.metric("Biomedical Cost Reduction Potential", "15.2%")
            col2.metric("Biocompatibility Improvement", "12.5%")
            col3.metric("Regulatory Compliance Score", "95/100")

            st.markdown("## 🏥 AI-Recommended Biomedical Designs")
            biomed_designs = [
                {
                    "ID": "BMD-001",
                    "Component": "Surgical Instrument Handle",
                    "Cost": "$120",
                    "Biocompatibility": "92/100",
                    "Materials": "Medical-grade Polymer, Titanium",
                    "Optimization_Score": "91.5"
                },
                {
                    "ID": "BMD-002",
                    "Component": "Implantable Sensor Casing",
                    "Cost": "$450",
                    "Biocompatibility": "95/100",
                    "Materials": "PEEK, Platinum",
                    "Optimization_Score": "94.0"
                },
                {
                    "ID": "BMD-003",
                    "Component": "Drug Delivery Micro-pump",
                    "Cost": "$780",
                    "Biocompatibility": "90/100",
                    "Materials": "Silicone, Stainless Steel (316L)",
                    "Optimization_Score": "90.2"
                }
            ]
            biomed_design_df = pd.DataFrame(biomed_designs)
            st.dataframe(biomed_design_df)

            st.markdown("## ✨ Biomedical Design Recommendations")
            biomed_recommendations = [
                "🔄 Explore PEEK alternatives for implantable devices to reduce cost while maintaining biocompatibility.",
                "🧪 Optimize sterilization protocols for heat-sensitive materials to prevent degradation and extend lifespan.",
                "🔬 Conduct further in-vitro and in-vivo testing for novel material combinations to accelerate regulatory approval."
            ]
            for rec in biomed_recommendations:
                st.markdown(f"- {rec}")

        else: # Original industrial R&D insights
            # --- Mocked AI Insights ---
            st.subheader("📊 Optimization Summary (General R&D)")
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

# --- How to use for Biomedical Industry (Instructions/Example) ---
st.markdown("---")
st.subheader("💡 How to use for Biomedical Industry Data:")
st.markdown("""
To see a demonstration with biomedical data, you can create a sample CSV or Excel file with the following (or similar) columns:
`Device_ID`, `Component`, `Material`, `Manufacturing_Cost`, `Biocompatibility_Score`, `Sterilization_Method`, `Failure_Rate`, `Compliance_Standard`.""")

