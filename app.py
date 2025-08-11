from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from google.api_core import exceptions

# Load all the environment variables from the .env file
load_dotenv() 

# Configure the Generative AI API key
# Make sure your .env file has GOOGLE_API_KEY="your_actual_key"
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API Key not found. Please set it in your .env file.")
else:
    genai.configure(api_key=api_key)

# --- Function Definitions ---

def setup_database():
    """
    Creates the database and the STUDENT table if they don't exist,
    and populates the table with some sample data.
    """
    conn = sqlite3.connect("student.db")
    cur = conn.cursor()
    
    # Create the table only if it doesn't already exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS STUDENT(
        NAME VARCHAR(25), 
        CLASS VARCHAR(25), 
        SECTION VARCHAR(25), 
        MARKS INT
    );
    """)
    
    # Check if the table is empty before inserting data to avoid duplicates
    cur.execute("SELECT COUNT(*) FROM STUDENT")
    if cur.fetchone()[0] == 0:
        # Populate the table with some sample data
        students_data = [
            ('Pranay', '10th', 'A', 90),
            ('John', '10th', 'B', 85),
            ('Jane', '11th', 'A', 95),
            ('Peter', '10th', 'A', 78),
            ('Mary', '11th', 'B', 88)
        ]
        cur.executemany("INSERT INTO STUDENT(NAME, CLASS, SECTION, MARKS) VALUES (?, ?, ?, ?)", students_data)
        print("Database populated with sample data.")

    conn.commit()
    conn.close()

def get_gemini_response(question, prompt):
    """
    Loads the Gemini model and generates an SQL query response.
    Includes error handling for API calls and empty responses.
    """
    try:
        # Using a generally available model to avoid quota/access issues
        model = genai.GenerativeModel('gemini-2.5-pro') 
        response = model.generate_content([prompt, question])

        # Add a check to ensure the response has content before accessing .text
        if not response.parts:
            st.error("The API returned an empty response. This might be due to safety filters blocking the content.")
            st.warning(f"Prompt Feedback: {response.prompt_feedback}")
            return None
            
        return response.text
        
    # Catching the specific rate limit error
    except exceptions.ResourceExhausted as e:
        st.error("API Rate Limit Exceeded. You have made too many requests to the Gemini API.")
        st.error("Please wait a while before trying again or check your Google Cloud billing plan.")
        return None
    except exceptions.GoogleAPICallError as e:
        st.error(f"API Call Error: {e}")
        st.error("This often means there's an issue with your API key or the model name. Please check that the key is valid and has the Generative Language API enabled.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None


def read_sql_query(sql, db):
    """
    Executes a given SQL query on the specified database and returns the results.
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        return rows
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return None
    finally:
        conn.close()

# --- Database Setup ---
# Call the setup function to make sure the DB and table exist
setup_database()

# --- Prompt Template ---

prompt = '''
You are an expert in converting English questions to SQL queries.
Your task is to convert a natural language question into a syntactically correct SQL query 
based on the provided table schema. You must only output the SQL query and nothing else.

**Database Schema:**
```sql
Create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT);
```

**Examples:**

**Question:** "Show me all the students in section A."
**SQL Query:** SELECT * FROM STUDENT WHERE SECTION = 'A';

**Question:** "What are the names of students who scored more than 80 marks?"
**SQL Query:** SELECT NAME FROM STUDENT WHERE MARKS > 80;

**Question:** "How many students are there in total?"
**SQL Query:** SELECT COUNT(*) FROM STUDENT;

---

Now, generate an SQL query for the given question.
'''

# --- Streamlit App UI ---

st.set_page_config(page_title="SQL Query Generator", page_icon="🤖")

col1, col2 = st.columns([1, 4])

with col1:
    try:
        st.image("123.png", width=100)
    except FileNotFoundError:
        st.warning("Image not found.")

with col2:
    st.header("Gemini SQL Assistant")
    st.caption("Ask any question, and I'll generate the SQL query for you!")


question = st.text_input("Enter your query in plain English:", key="input")
submit = st.button("✨ Generate SQL Query")

# --- App Logic ---

if submit and question and api_key:
    with st.spinner("Generating query..."):
        sql_query = get_gemini_response(question, prompt)
        
        if sql_query:
            if "```sql" in sql_query:
                sql_query = sql_query.split("```sql")[1].split("```")[0].strip()
            
            st.code(sql_query, language="sql")
            
            db_rows = read_sql_query(sql_query, "student.db")

            st.subheader("Query Results:")
            if db_rows is not None:
                st.dataframe(db_rows)
            else:
                st.info("No records found or an error occurred during execution.")

elif submit and not question:
    st.warning("Please enter a question first!")