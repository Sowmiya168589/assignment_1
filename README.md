# assignment_1
Personal UPI Usage and Financial Analyzer using LLMs

The Personal UPI Usage & Financial Analyzer is a FinTech-based web application designed to analyze and visualize personal UPI transaction data obtained from platforms such as Google Pay, PhonePe, and Paytm. The system allows users to upload their transaction history in CSV format and automatically processes the data to extract meaningful financial insights.

The application performs robust data cleaning and normalization, handling missing or inconsistent columns such as date, amount, category, and receiver without errors. Using Python and Pandas, it computes key financial metrics including total spend, average transaction value, maximum transaction, and total number of transactions.

With Streamlit as the frontend framework, the project delivers an interactive and user-friendly dashboard. Plotly is used to generate dynamic visualizations such as category-wise spending analysis and monthly spending trends, enabling users to clearly understand their spending patterns over time.

Additionally, the system identifies potentially wasteful or high-value transactions by comparing individual expenses with average spending behavior. The project is designed to be LLM-ready, enabling future integration of AI-based personalized financial advice and spending predictions.

Overall, this project demonstrates practical implementation of FinTech analytics, data preprocessing, and interactive dashboard development, making it suitable for personal finance management and financial behavior analysis.
