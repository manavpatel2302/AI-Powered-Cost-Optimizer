import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# --- Page Configuration ---
st.set_page_config(page_title="Cost Optimizer AI", layout="wide")

# --- Sample Data Function ---
def get_sample_data():
    """Creates a sample DataFrame for demonstration."""
    data = {
        'component_id': [f'CMP-{100+i}' for i in range(20)],
        'material_type': np.random.choice(['Aluminum', 'Steel', 'Titanium', 'Polymer'], 20),
        'volume_cm3': np.random.uniform(50, 500, 20),
        'component_count': np.random.randint(5, 50, 20),
        'machining_hours': np.random.uniform(1, 20, 20),
        'supplier': np.random.choice(['Supplier A', 'Supplier B', 'Supplier C'], 20),
        'cost_usd': np.zeros(20) # We will predict this
    }
    df = pd.DataFrame(data)
    # Create a plausible cost based on features
    df['cost_usd'] = (df['volume_cm3'] * 2.5 + 
                      df['component_count'] * 15 + 
                      df['machining_hours'] * 80 + 
                      df['material_type'].map({'Aluminum': 50, 'Steel': 150, 'Titanium': 600, 'Polymer': 20}) +
                      np.random.uniform(-50, 50, 20) # noise
                     ).round(2)
    return df

# --- Model Training Function ---
@st.cache_data
def train_model(df, feature_cols, target_col):
    """Trains an XGBoost model and returns the model, predictions, and metrics."""
    # Prepare data (One-Hot Encoding for categorical features)
    X = pd.get_dummies(df[feature_cols], drop_first=True)
    y = df[target_col]

    # Add any missing columns from training to the dataset if needed
    # This handles cases where uploaded data might have different categories
    # In a real app, you would save and load column lists. For this demo, we refit.
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    
    # Generate predictions and metrics
    predictions = model.predict(X)
    rmse = np.sqrt(mean_squared_error(y, predictions))
    feature_importance = pd.DataFrame({'feature': X.columns, 'importance': model.feature_importances_}).sort_values('importance', ascending=False)
    
    return model, predictions, rmse, feature_importance


# --- Main App UI ---
st.title("🧠 Extreme AI Cost Optimizer for R&D")
st.markdown("Use an AI model to predict costs, analyze drivers, and get optimization suggestions. **Load sample data or upload your own.**")

df = None
data_source = st.radio("Choose a data source:", ("Upload your own file", "Use sample data"), horizontal=True)

if data_source == "Upload your own file":
    uploaded_file = st.file_uploader("📁 Upload your file (.csv or .xlsx)", type=["csv", "xlsx"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
else:
    st.info("👇 Sample manufacturing data loaded below. You can now configure the model.")
    df = get_sample_data()

# --- This block runs once data is loaded ---
if df is not None:
    st.success("✅ Data loaded successfully!")
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    st.markdown("---")
    st.header("🤖 Configure AI Model")
    
    # --- Feature Selection ---
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("Select columns that influence the cost.")
        # Attempt to pre-select columns that are not the target or an ID
        default_features = [col for col in df.columns if col.lower() not in ['cost_usd', 'cost', 'component_id', 'id']]
        feature_cols = st.multiselect("Feature Columns (Input)", options=df.columns, default=default_features)
    with col2:
        st.markdown("Select the column you want to predict.")
        # Attempt to find a default cost column
        try:
            cost_col_index = [c.lower() for c in df.columns].index('cost_usd')
        except ValueError:
            cost_col_index = len(df.columns)-1 # Default to last column if not found
        target_col = st.selectbox("Target Column (Output)", options=df.columns, index=cost_col_index)

    # --- Model Training and Prediction ---
    if st.button("🚀 Run AI Cost Analysis", type="primary"):
        if not feature_cols or not target_col:
            st.warning("Please select at least one feature and a target column.")
        else:
            with st.spinner("AI is analyzing the data... This may take a moment."):
                model, predictions, rmse, feature_importance = train_model(df, feature_cols, target_col)
                df['predicted_cost'] = predictions.round(2)
                df['cost_difference'] = (df['predicted_cost'] - df[target_col]).round(2)
                
                st.markdown("---")
                st.header("📊 AI Analysis Results")
                
                st.metric("Model Prediction Accuracy (RMSE)", f"${rmse:,.2f}", help=f"Root Mean Squared Error. A lower value is better. On average, the model's predictions are off by this amount.")
                
                st.subheader("📈 Feature Importance")
                st.markdown("Which factors have the biggest impact on cost?")
                st.bar_chart(feature_importance.set_index('feature'))

                st.subheader("💰 Predicted vs. Actual Costs")
                st.dataframe(df[['component_id', target_col, 'predicted_cost', 'cost_difference']].head(10))

                st.subheader("🛠️ AI-Driven Recommendations")
                highest_cost_component = df.loc[df[target_col].idxmax()]
                st.markdown(f"- **Focus on Component `{highest_cost_component['component_id']}`**: It is the most expensive item at **${highest_cost_component[target_col]:,.2f}**.")
                
                # Recommendation based on top feature
                top_feature = feature_importance.iloc[0]['feature']
                st.markdown(f"- **Investigate `{top_feature}`**: This is the primary driver of cost. Look for ways to optimize it (e.g., if it's `material_type`, explore cheaper alternatives; if it's `machining_hours`, improve process efficiency).")

                st.success("✅ Analysis complete!")