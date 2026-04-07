# 🔐 SecureLog Analyzer

> *Analyze logs. Detect threats. Visualize insights.*

---

## 📌 Overview

**SecureLog Analyzer** is a desktop-based cybersecurity application developed using Python.
It is designed to simplify the process of analyzing system log files by automatically detecting suspicious activities and presenting insights through clear visualizations and reports.

This tool helps users understand system behavior and identify potential security threats without requiring advanced cybersecurity knowledge.

---

## 🎯 Features

* 📂 Upload and analyze log files (`.txt`, `.log`, `.csv`)
* 🔍 Detect suspicious activities using rule-based analysis:

  * Multiple failed login attempts
  * Unusual login times
  * Suspicious IP activity
* 📊 Visualize data using:

  * Bar charts
  * Pie charts
  * Line graphs
* 📋 Display structured log data in tables
* 🚨 Generate alerts for potential threats
* 📑 Export reports (PDF / CSV) *(optional feature)*

---

## 🛠️ Technologies Used

* **Python**
* **Pandas** – Data processing
* **Matplotlib** – Data visualization
* **PyQt / Tkinter** – GUI development
* **ReportLab** *(optional)* – PDF generation

---

## 🧠 How It Works

1. Upload a log file into the system
2. The application processes and parses the data
3. Rule-based detection identifies suspicious patterns
4. Results are displayed through:

   * Tables
   * Alerts
   * Visual charts

---

## 📂 Project Structure

```
SecureLog-Analyzer/
│── main.py
│── ui/
│   ├── dashboard.py
│   ├── components/
│── logic/
│   ├── parser.py
│   ├── detector.py
│── data/
│── reports/
│── assets/
│   ├── logo.png
│── README.md
│── requirements.txt
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/securelog-analyzer.git
cd securelog-analyzer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python main.py
```

---

## 📈 Future Improvements

* Real-time log monitoring
* Machine learning-based threat detection
* Advanced filtering and search
* Cloud integration

---

## 👤 Author

* Wathsiluni Liyanage

---

## 📜 License

This project is licensed under the MIT License.
