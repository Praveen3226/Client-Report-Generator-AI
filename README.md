# 📈 Client Report Generator – AI + Visual Reporting Engine

Turn raw CSV campaign data into stunning, insight-packed PDF reports in **minutes**.  
This tool uses **Google Gemini 2.0 Flash** to generate intelligent campaign summaries, plots performance charts using **Matplotlib**, and compiles everything into a beautifully formatted **PDF report**.

> ✨ Perfect for marketing analysts, agencies, or freelancers who want to automate client deliverables with AI-powered insights.

---

## 🔍 What This App Does

- 🧠 **Analyzes marketing data** (Impressions, Clicks, Cost, Conversions) from a CSV file
- 📊 Generates insightful **charts** (CTR, Spend, Impressions, Conversions, etc.)
- 🤖 Uses **Gemini 2.0 Flash** (Google Generative Language Model) to write **smart insights**
- 📄 Renders HTML reports using **Jinja2** templating
- 🧾 Exports to PDF using **xhtml2pdf**
- 💻 Built with **Streamlit** for a clean, interactive UI

---

## 🤖 What Kind of AI Model Is Used?

This project integrates with **Google Gemini 2.0 Flash**, a **generative large language model (LLM)** optimized for fast, structured completions and intelligent summarization.

### Gemini 2.0 Flash Overview:

| Feature | Description |
|--------|-------------|
| Type   | Transformer-based LLM |
| Usage  | Text summarization, data explanation, marketing insights |
| API    | Google Generative Language API (via `v1beta` endpoint) |
| Ideal For | Use cases requiring short, fast, and insightful text completions |

---

## 🧠 AI-Generated Insights
## Here’s what Gemini outputs:

- Campaign A has the highest ROAS of 4.2, indicating strong performance.
- Campaign B's CTR is below 1%, suggesting poor ad engagement.
- Daily spend peaked on July 10th, aligning with a spike in conversions.

---

## 🛠️ Tech Stack

| Layer        | Technology                |
|--------------|---------------------------|
| UI           | Streamlit                 |
| Data         | Pandas                    |
| Charts       | Matplotlib                |
| AI Summary   | Google Gemini 2.0 Flash   |
| PDF Engine   | xhtml2pdf + Jinja2        |
| Images       | Base64 Encoding for inline HTML |
| Report Logic | HTML Templates            |

---

## 📦 Folder Structure

client-report-generator/
│
├── app.py                   # Main Streamlit app
├── report_template.html     # HTML Jinja2 report template
├── output/
│   ├── spend_chart.png
│   ├── clicks_chart.png
│   ├── ctr_chart.png
│   ├── report.pdf
│   └── ...                  # Other generated files
├── requirements.txt         # Python dependencies
└── README.md                # You're here 💡

