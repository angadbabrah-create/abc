import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Excel Forecast Readiness Checker", layout="wide")

st.title("📊 Excel Forecast Readiness Checker")

st.write("""
Upload an Excel file (.xlsx or .xls).

The app will:
- Detect numerical columns
- Create histograms
- Calculate Mean and Median
- Check whether Mean and Median are close
- Suggest whether the column may be suitable for forecasting
""")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:

    try:
        df = pd.read_excel(uploaded_file)

        st.subheader("Data Preview")
        st.dataframe(df.head())

        numeric_cols = df.select_dtypes(include=np.number).columns

        if len(numeric_cols) == 0:
            st.warning("No numerical columns found.")
        else:

            results = []

            st.subheader("Analysis")

            for col in numeric_cols:

                data = df[col].dropna()

                mean_val = data.mean()
                median_val = data.median()

                # Percentage difference
                if mean_val != 0:
                    diff_percent = abs(mean_val - median_val) / abs(mean_val) * 100
                else:
                    diff_percent = 0

                if diff_percent <= 10:
                    forecast_status = "✅ Suitable for Forecasting"
                else:
                    forecast_status = "⚠️ Distribution may be skewed"

                results.append({
                    "Column": col,
                    "Mean": round(mean_val, 2),
                    "Median": round(median_val, 2),
                    "Difference (%)": round(diff_percent, 2),
                    "Assessment": forecast_status
                })

                st.markdown("---")
                st.subheader(f"Column: {col}")

                col1, col2 = st.columns([2,1])

                with col1:
                    fig, ax = plt.subplots(figsize=(6,4))
                    ax.hist(data, bins=15)
                    ax.set_title(f"Histogram - {col}")
                    ax.set_xlabel(col)
                    ax.set_ylabel("Frequency")
                    st.pyplot(fig)

                with col2:
                    st.metric("Mean", round(mean_val,2))
                    st.metric("Median", round(median_val,2))
                    st.metric("Difference %", round(diff_percent,2))
                    st.write(forecast_status)

            st.subheader("Summary Table")

            summary_df = pd.DataFrame(results)
            st.dataframe(summary_df, use_container_width=True)

    except Exception as e:
        st.error(f"Error reading file: {e}")
