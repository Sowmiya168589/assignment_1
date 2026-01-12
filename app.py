import gradio as gr
import pandas as pd
import pdfplumber
import re
import matplotlib.pyplot as plt
from transformers import pipeline

# ---------------- LOAD REAL LLM ----------------
llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_length=256
)

# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text(pdf):
    lines = []
    with pdfplumber.open(pdf) as pdf_file:
        for page in pdf_file.pages:
            text = page.extract_text()
            if text:
                lines.extend(text.split("\n"))
    return lines

# ---------------- CATEGORY NLP ----------------
def categorize(text):
    t = text.lower()
    if any(x in t for x in ["grocery", "milk", "vegetable", "supermarket"]):
        return "Grocery"
    if any(x in t for x in ["electricity", "water", "gas", "recharge", "bill"]):
        return "Bills"
    if any(x in t for x in ["swiggy", "zomato", "restaurant", "food"]):
        return "Food"
    if any(x in t for x in ["movie", "netflix", "spotify", "entertainment"]):
        return "Entertainment"
    if any(x in t for x in ["amazon", "flipkart", "shopping"]):
        return "Shopping"
    if any(x in t for x in ["uber", "ola", "cab"]):
        return "Travel"
    return "Others"

# ---------------- REAL LLM ADVICE ----------------
def ai_advice(summary_df, waste_count):
    if summary_df.empty:
        return "No sufficient transaction data available."

    prompt = f"""
    You are a personal finance advisor.

    Below is a category-wise UPI spending summary:
    {summary_df.to_string(index=False)}

    Number of wasteful or unnecessary transactions: {waste_count}

    Provide:
    1. Key financial insight
    2. Spending improvement suggestions
    3. Savings recommendation
    """

    response = llm(prompt)[0]["generated_text"]
    return response

# ---------------- MAIN ANALYSIS ----------------
def analyze(pdf):
    if pdf is None:
        return None, None, None, "No file uploaded"

    raw = extract_text(pdf.name)
    rows = [l for l in raw if re.search(r"\d+\.\d{2}", l)]

    if not rows:
        return None, None, None, "No valid transactions detected"

    df = pd.DataFrame(rows, columns=["Transaction"])
    df["Amount"] = df["Transaction"].str.extract(r"([\d,]+\.?\d*)")[0]
    df["Amount"] = df["Amount"].str.replace(",", "", regex=False).astype(float)
    df["Category"] = df["Transaction"].apply(categorize)

    summary = df.groupby("Category")["Amount"].sum().reset_index()
    summary = summary.sort_values("Amount", ascending=False)

    # Visualization
    fig, ax = plt.subplots()
    ax.bar(summary["Category"], summary["Amount"])
    ax.set_title("Category-wise Spending")
    ax.set_ylabel("Amount")
    ax.set_xlabel("Category")
    plt.xticks(rotation=30)

    # Wasteful spending
    wasteful = df[
        (df["Category"] == "Entertainment") |
        ((df["Category"] == "Shopping") & (df["Amount"] < 500))
    ]

    advice = ai_advice(summary, len(wasteful))
    return df, fig, wasteful, advice

# ---------------- GRADIO UI ----------------
demo = gr.Interface(
    fn=analyze,
    inputs=gr.File(label="📄 Upload UPI PDF", file_types=[".pdf"]),
    outputs=[
        gr.Dataframe(label="📄 Transactions"),
        gr.Plot(label="📊 Category Summary"),
        gr.Dataframe(label="⚠ Wasteful Spending"),
        gr.Markdown(label="🤖 LLM-Generated Financial Advice"),
    ],
    title="💰 Personal UPI Usage & Financial Analyzer (Real LLM-Based)",
    description="Uses a real Transformer LLM (FLAN-T5) to generate personalized financial insights.",
)

demo.launch(server_name="0.0.0.0", server_port=7860)
