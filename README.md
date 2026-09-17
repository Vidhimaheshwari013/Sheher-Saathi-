# 🏙️ Sheher Saathi

### AI-Powered Civic Issue Intelligence for Smarter, More Responsive Cities

**Sheher Saathi** is an AI-powered civic intelligence platform that transforms scattered citizen complaints into **structured, connected, and actionable civic issues**.

Instead of simply storing complaints as individual tickets, Sheher Saathi uses AI to understand what citizens are reporting, identify related complaints, discover underlying problems, and help authorities prioritize issues based on real evidence.

---

## 💡 The Problem

Traditional civic complaint systems mainly focus on **collecting and closing tickets**.

This creates a problem:

* Multiple citizens may report the same underlying issue separately.
* Complaints can be written in informal language, Hindi, Hinglish, or English.
* Important information such as severity, duration, or affected groups may be missing.
* Authorities often see individual complaints rather than the **larger pattern behind them**.
* Recurring and rapidly emerging problems can be difficult to identify.

A city may have **hundreds of complaints but only a few underlying civic problems**.

---

## 🚀 Our Solution

Sheher Saathi acts as an intelligence layer between **citizens and authorities**.

### Citizen Complaint

Citizens describe their problem naturally in English, Hindi, or Hinglish.

⬇️

### AI Understanding

**Llama through Groq** analyzes the complaint and extracts structured information such as:

* Category
* Subcategory
* Location
* Severity
* Duration
* Affected population
* Relevant context
* Missing information

⬇️

### Intelligent Follow-Up

If important information is missing, the system asks targeted follow-up questions instead of forcing citizens through lengthy forms.

⬇️

### Semantic Similarity

Multilingual embeddings identify complaints that are describing similar problems, even when the wording is different.

⬇️

### Issue Clustering

Related complaints are grouped into a single **underlying civic issue**.

⬇️

### Priority & Intelligence

A transparent priority engine considers factors such as severity, report volume, duration, and affected population.

⬇️

### Civic Intelligence

Authorities can view:

* Current hotspots
* Recurring issues
* Emerging problems
* Historical patterns
* Related citizen reports
* Priority levels
* Evidence behind each insight

---

## ✨ Key Features

### 🗣️ Multilingual Complaint Understanding

Understands complaints written in **English, Hindi, and Hinglish**, including informal citizen language.

### 🤖 AI-Powered Structuring

Llama converts unstructured complaints into structured civic data that can be analyzed by the system.

### 💬 Intelligent Follow-Ups

The system identifies missing information and asks relevant questions to improve the quality of a report.

### 🔗 Semantic Similarity

Uses multilingual embeddings to recognize complaints that are related even when they use completely different wording.

### 🧩 Civic Issue Clustering

Multiple individual complaints can be grouped into one underlying issue.

For example:

> "Park ke paas street light nahi chal rahi."

> "Park gate ke bahar raat ko darkness hai."

> "Broken light pole near the park."

These can be recognized as one potential **Street Lighting Failure** issue.

### 🚨 Transparent Priority Engine

Priority is determined using measurable signals rather than relying entirely on an AI-generated score.

Factors can include:

* Severity
* Number of related reports
* Duration
* Affected population
* Safety/context signals

### 🧠 Civic Memory

The platform remembers historical patterns and recurring civic problems.

For example:

**Waterlogging — Sector 14**

* 2024 → 12 reports
* 2025 → 19 reports
* 2026 → 37 reports

This helps authorities understand whether an issue is **recurring, worsening, or improving**.

### 📈 Civic Pulse

Provides a snapshot of what is happening across the city right now and highlights rapidly increasing issue categories.

### 🔥 Emerging Issue Detection

Detects unusual increases in complaints over a recent time window, helping authorities identify problems before they become larger crises.

### 🗺️ Civic Hotspots

Visualizes areas where multiple related or high-priority complaints are concentrated.

### 👤 Human-in-the-Loop Verification

AI identifies, groups, and summarizes issues, while authorities remain responsible for verification and action.

---

## 🧠 Role of AI

Sheher Saathi follows a simple principle:

> **AI understands → Data verifies → Humans decide**

The LLM is not used as a generic chatbot or as the sole decision-maker.

It is primarily used for:

* Natural language understanding
* Multilingual interpretation
* Information extraction
* Follow-up question generation
* Context understanding
* Evidence-based summaries

Deterministic backend logic handles measurable calculations such as priority, while human authorities verify important civic insights.

---

## 🏗️ Architecture

```text
Citizen
   │
   ▼
Complaint Interface
   │
   ▼
Llama + Groq
   │
   ├── Complaint Understanding
   ├── Information Extraction
   └── Missing Information Detection
   │
   ▼
Structured Complaint
   │
   ▼
Multilingual Embeddings
   │
   ▼
Semantic Similarity
   │
   ▼
Issue Clustering
   │
   ▼
Priority Engine
   │
   ├── Civic Memory
   ├── Civic Pulse
   └── Emerging Issue Detection
   │
   ▼
Authority Dashboard
   │
   ▼
Human Verification & Action
```

---

## 🛠️ Technology Stack

| Component     | Technology                           |
| ------------- | ------------------------------------ |
| LLM           | Llama                                |
| LLM Inference | Groq                                 |
| Backend       | FastAPI                              |
| Frontend      | HTML, CSS, JavaScript                           |
| Embeddings    | Multilingual Embedding Model         |
| Vector Search | FAISS                                |
| Clustering    | DBSCAN / Similarity-based Clustering |
| Database      | SQLite / PostgreSQL                  |
| Maps          | Leaflet / OpenStreetMap              |

---

## 🔌 Core API Endpoints

```text
POST /complaints
POST /complaints/analyze

GET  /complaints

GET  /clusters
GET  /clusters/{id}

GET  /dashboard
GET  /pulse

POST /verify
```

---

## 🎯 What Makes Sheher Saathi Different?

Traditional systems ask:

> **“How many complaints were received?”**

Sheher Saathi asks:

> **“How many underlying civic problems are actually happening, where are they, how serious are they, and have we seen them before?”**

This shifts civic technology from **ticket management to civic intelligence**.

---

## 🌱 Responsible AI

Sheher Saathi is designed with responsible AI principles:

* AI-generated insights are distinguishable from verified information.
* Important issues can remain in a **Needs Verification** state.
* Priority is based on transparent, measurable signals.
* Complaint volume alone does not determine importance.
* The system avoids unnecessary personal information.
* AI summaries are grounded in available complaint data.
* Unsupported claims should not be presented as facts.

---

## 🔮 Vision

Sheher Saathi aims to create a civic system where citizen voices are not treated as isolated complaints, but as **collective signals about how a city is functioning**.

By connecting citizen reports across language, location, time, and meaning, cities can move from simply **responding to complaints** toward **understanding problems earlier and acting more intelligently**.

---

### 🏙️ Sheher Saathi

**Listen to the city. Find the pattern. Remember the problem. Help the city act.**
