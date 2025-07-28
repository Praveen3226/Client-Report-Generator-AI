import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from jinja2 import Template
import base64
import os
from xhtml2pdf import pisa
from jinja2 import Template
import base64
import requests
import json

GEMINI_MODEL = "models/gemini-2.0-flash:generateContent"
YOUR_GEMINI_API_KEY = "AIzaSyCiMT35cysNSXz9HqCmcmgG3fGSXfuk3Yw"  

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/{GEMINI_MODEL}?key={YOUR_GEMINI_API_KEY}"

TEMPLATE_PATH = "report_template.html"
CHART_PATH = "output/spend_chart.png"
PDF_PATH = "output/report.pdf"

def generate_gemini_insights(summary_df):
    summary_text = summary_df.round(2).reset_index().to_string(index=False)
    prompt_text = (
        "You are a marketing analyst. Given the campaign performance data below, "
        "write 5 clear, actionable insights for a client report.\n\n"
        f"{summary_text}\n\nInsights:"
    )

    model_name = "models/gemini-2.0-flash"
    api_url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateText"

    payload = {
        "prompt": {
            "text": prompt_text
        },
        "temperature": 0.7,
        "maxOutputTokens": 250
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {YOUR_GEMINI_API_KEY}"
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        # Extract output text - usually inside 'candidates' list
        insights_text = result.get("candidates", [{}])[0].get("output", "").strip()
        insights_list = [line.strip("-*• \n") for line in insights_text.split('\n') if line.strip()]
        return insights_list
    else:
        return [f"Error generating insights: {response.status_code} {response.text}"]


    
st.set_page_config(page_title="Client Report Generator", layout="centered")

st.title("📈 Client Report Generator")
st.markdown("Upload your campaign CSV file and get a clean PDF report.")

uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['Date'])

    # Metrics summary
    summary = df.groupby('Campaign').agg({
        'Impressions': 'sum',
        'Clicks': 'sum',
        'Cost': 'sum',
        'Conversions': 'sum'
    })
    summary['CTR (%)'] = (summary['Clicks'] / summary['Impressions']) * 100
    summary['CPC'] = summary['Cost'] / summary['Clicks']
    summary['ROAS'] = summary['Conversions'] / summary['Cost']

    summary_html = summary.round(2).reset_index().to_html(index=False, border=0, classes="table", justify='center')

    st.write("SUMMARY DF", summary.head())
    # Plot chart
    os.makedirs("output", exist_ok=True)
    plt.figure(figsize=(10, 4))
    df.groupby('Date')['Cost'].sum().plot(marker='o', title='Daily Spend (₹)')
    plt.xlabel("Date")
    plt.ylabel("Cost (₹)")
    plt.tight_layout()
    plt.savefig(CHART_PATH)
    plt.close()

    plt.figure(figsize=(10, 4))
    df.groupby('Date')['Clicks'].sum().plot(marker='o', color='green', title='Daily Clicks')
    plt.xlabel("Date")
    plt.ylabel("Clicks")
    plt.tight_layout()
    plt.savefig("output/clicks_chart.png")
    plt.close()

    plt.figure(figsize=(10, 4))
    df.groupby('Date')['Impressions'].sum().plot(marker='o', color='blue', title='Daily Impressions')
    plt.xlabel("Date")
    plt.ylabel("Impressions")
    plt.tight_layout()
    plt.savefig("output/impressions_chart.png")
    plt.close()

    plt.figure(figsize=(10, 4))
    df.groupby('Date')['Conversions'].sum().plot(marker='o', color='purple', title='Daily Conversions')
    plt.xlabel("Date")
    plt.ylabel("Conversions")
    plt.tight_layout()
    plt.savefig("output/conversions_chart.png")
    plt.close()

    plt.figure(figsize=(6, 6))
    plt.scatter(df['Cost'], df['Conversions'], alpha=0.6, c='red')
    plt.title('Cost vs. Conversions')
    plt.xlabel('Cost (₹)')
    plt.ylabel('Conversions')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("output/cost_vs_conversions.png")
    plt.close()

    daily = df.groupby('Date').agg({'Clicks': 'sum', 'Impressions': 'sum'})
    daily['CTR (%)'] = (daily['Clicks'] / daily['Impressions']) * 100

    plt.figure(figsize=(10, 4))
    daily['CTR (%)'].plot(marker='o', color='orange', title='Daily CTR (%)')
    plt.xlabel("Date")
    plt.ylabel("CTR (%)")
    plt.tight_layout()
    plt.savefig("output/ctr_chart.png")
    plt.close()


    # Custom insights
    st.subheader("🧠 AI-Generated Campaign Insights")

    insights = generate_gemini_insights(summary)
    for insight in insights:
        st.markdown(f"- {insight}")

    with open("report_template.html", "r", encoding="utf-8") as f:
        template = Template(f.read())


    # Render HTML
    with open(TEMPLATE_PATH) as f:
        template = Template(f.read())
    st.subheader("📊 Campaign Performance Summary")



    # Encode charts

    with open(CHART_PATH, "rb") as img_file:
        spend_chart_b64 = base64.b64encode(img_file.read()).decode()
    spend_chart_img = f'<img src="data:image/png;base64,{spend_chart_b64}" width="600">'

    with open("output/impressions_chart.png", "rb") as img_file:
        impressions_chart_b64 = base64.b64encode(img_file.read()).decode()
    impressions_chart_img = f'<img src="data:image/png;base64,{impressions_chart_b64}" width="600">'
    with open("output/conversions_chart.png", "rb") as img_file:
        conversions_chart_b64 = base64.b64encode(img_file.read()).decode()
    conversions_chart_img = f'<img src="data:image/png;base64,{conversions_chart_b64}" width="600">'
    with open("output/ctr_chart.png", "rb") as img_file:
        ctr_chart_b64 = base64.b64encode(img_file.read()).decode()
    ctr_chart_img = f'<img src="data:image/png;base64,{ctr_chart_b64}" width="600">'
    with open("output/clicks_chart.png", "rb") as img_file:
        clicks_chart_b64 = base64.b64encode(img_file.read()).decode()
    clicks_chart_img = f'<img src="data:image/png;base64,{clicks_chart_b64}" width="600">'
    with open("output/cost_vs_conversions.png", "rb") as img_file:
        cost_vs_conversions_b64 = base64.b64encode(img_file.read()).decode()
    cost_vs_conversions_img = f'<img src="data:image/png;base64,{cost_vs_conversions_b64}" width="600">'


    # Add summary table
    summary_html = summary.round(2).reset_index().to_html(index=False, border=0, classes="table", justify='center')

    # Render HTML
    html_out = template.render(
        summary_table=summary_html,
        insights=insights,
        spend_chart=spend_chart_img,
        clicks_chart=clicks_chart_img,
        impressions_chart=impressions_chart_img,
        conversions_chart=conversions_chart_img,
        cost_vs_conversions=cost_vs_conversions_img,
        ctr_chart=ctr_chart_img,
        month="July 2025"
    )

    st.subheader("🧾 Preview Report")
    st.components.v1.html(html_out, height=600, scrolling=True)

    # PDF generation
if st.button("📥 Generate PDF"):
    from xhtml2pdf import pisa

    with open("output/temp.html", "w") as f:
        f.write(html_out)

    with open("output/temp.html") as source, open(PDF_PATH, "wb") as output_file:
        pisa.CreatePDF(source.read(), dest=output_file)

    with open(PDF_PATH, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        
        # Styled HTML Download Button
        styled_button = f'''
        <div style="text-align: center; margin-top: 30px;">
            <a href="data:application/pdf;base64,{b64}" download="Client_Report.pdf"
                style="
                    background-color: #0077cc;
                    color: white;
                    padding: 12px 24px;
                    text-decoration: none;
                    font-size: 16px;
                    border-radius: 8px;
                    display: inline-block;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    transition: background-color 0.3s ease;
                "
                onmouseover="this.style.backgroundColor='#005fa3'"
                onmouseout="this.style.backgroundColor='#0077cc'"
            >📄 Download Report</a>
        </div>
        '''
        st.markdown(styled_button, unsafe_allow_html=True)

