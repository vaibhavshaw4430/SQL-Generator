import json
import google.generativeai as genai
import re
import streamlit as st

genai.configure(api_key="AIzaSyBg9W6ucT0VNoBVEIQdlQxf11rp1TeQxJg")

with open('dbo_product_schema.json', "r") as f:
  metadata = json.load(f)


model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")

st.set_page_config(page_title="Oracle SQL Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 Oracle SQL Generator (Gemini Model)")
st.write("Ask a business question in plain English, and I'll generate the Oracle SQL query for you.")

# User input
question = st.text_area("Enter your business question:", placeholder="e.g. Show top 10 active products by price")

relevant = {}
for table, info in metadata.items():
    print(table)
    print(info['business_terms'])
    for term in info["business_terms"]:
        if term.lower() in question.lower():
            relevant[table] = info

if st.button("Generate SQL"):
    if not question.strip():
        st.warning("Please enter a question first.")
    else:
      prompt1 = f'''
      You are a business data assistant for Oracle Product Data Hub. Try to understand the given business use case through the description field in the below json file.
      Use the following relevant tables and their columns to generate safe Oracle SQL queries.
      Only use SELECT statements.
      {json.dumps(relevant, indent=2)}
      Project Number is like a primary key, Business is always concerned with ISBN.
      Follow Oracle SQL Syntax and give onlt the sql statement as the output.
      Question: {question}
      '''
      with st.spinner("Generating SQL using Gemini..."):
            try:
                response = model.generate_content(prompt1)
                sql_query = response.text.strip()

                st.subheader("Generated SQL")
                st.code(sql_query, language="sql")

                st.success("✅ SQL generated successfully!")

            except Exception as e:
                st.error(f"Error: {str(e)}")