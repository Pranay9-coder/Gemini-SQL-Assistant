# Gemini SQL Assistant 🤖

A **Streamlit-based SQL Query Generator** that uses **Google's Gemini API** to convert natural language questions into SQL queries, run them on a sample SQLite database, and display the results interactively.

## 🚀 Features
- Convert **plain English questions** into syntactically correct SQL queries.
- Uses **Google Gemini API** for natural language processing.
- Executes queries on a sample **SQLite database**.
- Interactive **Streamlit web UI**.
- Error handling for API, database, and input issues.
- Preloaded **sample student data** for testing.

## 📦 Tech Stack
- **Python 3.9+**
- **Streamlit** (Frontend UI)
- **SQLite3** (Database)
- **Google Generative AI (Gemini)** API
- **dotenv** for environment variable management

## 📂 Project Structure
.
├── app.py # Main Streamlit application
├── student.db # SQLite database (auto-created)
├── .env # Environment variables (Google API Key)
├── requirements.txt
└── 123.png # App logo (optional)

bash
Copy
Edit

## ⚙️ Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/Pranay9-coder/Gemini-SQL-Assistant.git
cd Gemini-SQL-Assistant
Create & activate a virtual environment (recommended)

bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # For Mac/Linux
venv\Scripts\activate      # For Windows
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Set up .env file
Create a .env file in the root folder:

ini
Copy
Edit
GOOGLE_API_KEY="your_actual_api_key"
Get your API key from the Google AI Studio.

Run the app

bash
Copy
Edit
streamlit run app.py
💡 How It Works
User enters a plain English question.

Gemini API converts it into a SQL query using the prompt template.

Query is executed on the STUDENT table in student.db.

Results are displayed in a data table.

🗄 Example Queries
"Show me all the students in section A"

"List the names of students who scored above 85 marks"

"How many students are in class 10th?"

🖼 Screenshot
(Add screenshot after running your app)