import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_seo_with_gpt35(page_data):
    prompt = f"""
You are an SEO expert. Analyze the following webpage elements and give precise, actionable SEO feedback.

Page Title: {page_data['title']}
Meta Description: {page_data['meta_description']}
Headings:
H1: {page_data['headings']['h1']}
H2: {page_data['headings']['h2']}
H3: {page_data['headings']['h3']}
Main Text Snippet: {page_data['main_text_snippet']}

Your output should:
- Identify SEO problems
- Suggest improvements (like better titles, missing headers, keyword usage, etc.)
- Be formatted in bullet points
- Be clear, helpful, and brief
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[ERROR] GPT API call failed: {e}"
