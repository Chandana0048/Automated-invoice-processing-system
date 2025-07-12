Automated Invoice Processing System
Welcome to the Automated Invoice Processing System — a lightweight, AI-powered PDF invoice extractor and dashboard built with Python and Streamlit.

It lets users upload invoice PDFs, extract essential details like Invoice Number, Date, Vendor, and Total Amount, store them in a local SQLite database, and visualize everything beautifully with interactive dashboards and charts.

Features
✅ Extract text from uploaded PDF invoices
✅ Detect and extract Invoice Number, Date, Vendor, and Total Amount
✅ Validate extracted amounts and dates
✅ Save invoice data into a SQLite database
✅ View an interactive Dashboard Overview
✅ Visualize:

📊 Vendor-wise Sales (Pie Chart)

📈 Date-wise Invoice Upload Trends (Line Chart)
✅ Filter invoices by Vendor and Minimum Amount
✅ 📥 Export filtered invoices to CSV
✅ Custom playful modern UI with blush backgrounds and coral buttons 💖

🖥️ Technologies Used
Python 3.10+
Streamlit
pdfplumber
SQLite (via sqlite3)
pandas
matplotlib
streamlit-option-menu

🖥️ Technologies Used
Python 3.10+
Streamlit
pdfplumber
SQLite (via sqlite3)
pandas
matplotlib
streamlit-option-menu

📦 Installation
1️⃣ Clone this repo:
git clone https://github.com/yourusername/invoice-processing-system.git
cd invoice-processing-system
2️⃣ (Optional) Create a virtual environment:
python -m venv venv
venv\Scripts\activate   # on Windows
3️⃣ Install dependencies:
pip install -r requirements.txt
4️⃣ If you haven’t already, create a Streamlit config file to set light theme:
Path: C:\Users\YourName\.streamlit\config.toml
[theme]
base = "light"
primaryColor = "#FF6B6B"
backgroundColor = "#fdfcfa"
secondaryBackgroundColor = "#FFF3E6"
textColor = "#333333"
5️⃣ Run the app:
streamlit run app.py


📚 What I Learned
✨ Working with pdfplumber for PDF text extraction
✨ Regex pattern crafting for reliably grabbing invoice details
✨ Managing a SQLite database with Python
✨ Customizing Streamlit apps with CSS and config themes
✨ Handling app state, caching issues, browser data conflicts
✨ Cleaning and formatting numeric data for dashboards
✨ Creating interactive visualizations with matplotlib and Streamlit

🛑 Limitations
Works only with machine-readable PDF invoices (no scanned image OCR yet)
Assumes a consistent invoice text structure for extraction

🚀 Future Enhancements
OCR support for scanned image invoices (with Tesseract)
Multi-page invoice handling
User login + multi-user dashboard stats
Export to Excel format

