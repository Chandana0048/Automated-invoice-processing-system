import sys
print("Python Executable in use:", sys.executable)

import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# Force Streamlit light theme inside app
from streamlit import config
config.set_option("theme.base", "light")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

from pdf_extractor import extract_text_from_pdf
from data_parser import extract_invoice_number, extract_date, extract_vendor, extract_total_amount
from db_handler import create_table, insert_invoice, fetch_invoices, get_invoice_count, get_total_sales, get_recent_invoices
from validator import validate_date, validate_amount

# 🌸 Custom Playful Modern CSS styling
st.markdown("""
    <style>
    .main {
        background-color: #fdfcfa;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton button {
        background-color: #FF6B6B;
        color: white;
        border-radius: 10px;
        font-weight: 600;
    }
    .stDownloadButton button {
        background-color: #1DD3B0;
        color: white;
        border-radius: 10px;
        font-weight: 600;
    }
    .metric-card {
        background-color: #FFF3E6;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        text-align: center;
        box-shadow: 1px 1px 8px rgba(0,0,0,0.07);
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #333333;
    }
    .metric-label {
        font-size: 16px;
        color: #555555;
    }
    h1 {
        color: #FF6B6B;
        font-size: 38px;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown('<h1>🧾 Automated Invoice System</h1>', unsafe_allow_html=True)

# Create table when app runs
create_table()

# Sidebar Option Menu
selected = option_menu(
    menu_title="✨ Navigation",
    options=["Upload Invoice", "Dashboard"],
    icons=["file-earmark-arrow-up", "bar-chart-line"],
    menu_icon="cast",
    default_index=0,
    styles={
        "container": {"background-color": "#ffffff"},
        "icon": {"color": "#FF6B6B", "font-size": "20px"},
        "nav-link-selected": {"background-color": "#FFE8D6", "font-weight": "bold"},
    }
)

if selected == "Upload Invoice":
    st.subheader("📥 Upload an Invoice")

    uploaded_file = st.file_uploader("Choose a PDF Invoice", type="pdf", key="fileuploader")

    if uploaded_file is not None:
        extracted_text = extract_text_from_pdf(uploaded_file)

        invoice_number = extract_invoice_number(extracted_text)
        date = extract_date(extracted_text)
        vendor = extract_vendor(extracted_text)
        total_amount = extract_total_amount(extracted_text)

        st.markdown(f"**Invoice Number:** {invoice_number}")
        st.markdown(f"**Date:** {date}")
        st.markdown(f"**Vendor:** {vendor}")
        st.markdown(f"**Total Amount:** {total_amount}")

        if st.button("📥 Save to Database"):
            valid_date, date_msg = validate_date(date)
            valid_amount, amount_msg = validate_amount(total_amount)

            if not valid_date:
                st.error(f"Invalid Date: {date_msg}")
            elif not valid_amount:
                st.error(f"Invalid Amount: {amount_msg}")
            else:
                clean_amount = float(total_amount.replace(",", ""))
                result = insert_invoice(invoice_number, date, vendor, clean_amount)
                st.success(result)

if selected == "Dashboard":
    st.subheader("📊 Dashboard Overview")

    total_invoices = get_invoice_count()
    total_sales = get_total_sales()
    recent_invoices = get_recent_invoices()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{total_invoices}</div>
            <div class='metric-label'>Total Invoices</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>₹{total_sales:,.2f}</div>
            <div class='metric-label'>Total Sales</div>
        </div>
        """, unsafe_allow_html=True)

    if total_invoices > 0:
        df_numeric = pd.DataFrame(recent_invoices, columns=["ID", "Invoice Number", "Date", "Vendor", "Total Amount"])
        df_numeric["Total Amount"] = df_numeric["Total Amount"].astype(float)

        st.subheader("📝 Recent Invoices")
        df_display = df_numeric.copy()
        df_display["Total Amount"] = df_display["Total Amount"].map("₹{:,.2f}".format)
        st.dataframe(df_display)

        st.subheader("📊 Vendor-wise Sales")
        vendor_sales = df_numeric.groupby("Vendor")["Total Amount"].sum().reset_index()
        fig, ax = plt.subplots()
        ax.pie(vendor_sales["Total Amount"], labels=vendor_sales["Vendor"], autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

        st.subheader("📈 Daily Invoice Uploads")
        upload_counts = df_numeric.groupby("Date").size().reset_index(name='Invoice Count')
        st.line_chart(upload_counts.set_index("Date"))

        st.subheader("🔍 Filter Invoices")
        vendor_options = df_numeric["Vendor"].unique().tolist()
        selected_vendor = st.selectbox("Filter by Vendor", ["All"] + vendor_options)
        min_amount = st.number_input("Minimum Amount ₹", min_value=0.0, value=0.0, step=100.0)

        filtered_df = df_numeric.copy()
        if selected_vendor != "All":
            filtered_df = filtered_df[filtered_df["Vendor"] == selected_vendor]
        filtered_df = filtered_df[filtered_df["Total Amount"] >= min_amount]

        st.subheader("📄 Filtered Invoices")
        df_filtered_display = filtered_df.copy()
        df_filtered_display["Total Amount"] = df_filtered_display["Total Amount"].map("₹{:,.2f}".format)
        st.dataframe(df_filtered_display)

        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="filtered_invoices.csv",
            mime="text/csv"
        )
    else:
        st.info("No invoices found. Upload some to get started!")

