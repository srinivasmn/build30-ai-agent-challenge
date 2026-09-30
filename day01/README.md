# Build30 Day 1 — Gemini LLM Call & Token Usage Tracker

## Overview

This project is Day 1 of my **Build30 30-Day AI Agent Engineering Challenge**.

The objective of Day 1 is to move beyond simply making an LLM API call and understand how an LLM application can capture and track **token usage** for each request.

The implementation uses Python and the Gemini API to:

- Make an LLM request
- Receive the generated response
- Capture LLM usage metadata
- Track input, output, thinking, and total tokens
- Store usage records in an append-only JSONL log
- Keep API credentials outside the source code

---

## Objective

The main objective is to build a small foundation for **LLM usage observability**.

The application follows this flow:

```text
User Prompt
     |
     v
  main.py
     |
     v
   llm.py
     |
     v
 Gemini API
     |
     +----------------------+
     |                      |
     v                      v
Response              Usage Metadata
                          |
                          v
                     tracker.py
                          |
                          v
                  token_log.jsonl
```

---

## What I Built

### `main.py`

The application entry point.

It accepts a prompt from the command line, sends it to the LLM layer, and displays the generated response and token usage.

Example:

```powershell
python main.py "Explain what RAG is in one sentence."
```

### `llm.py`

The LLM integration layer.

It is responsible for:

- Loading Gemini configuration
- Creating the Gemini client
- Sending the prompt to the configured model
- Receiving the response
- Extracting usage metadata

### `tracker.py`

The token tracking component.

It records:

- Input tokens
- Output tokens
- Thinking tokens
- Total tokens

The usage information is appended to `token_log.jsonl`.

---

## Application Flow

A single request flows through the application as follows:

```text
User
  |
  | Prompt
  v
main.py
  |
  v
llm.py
  |
  | API request
  v
Gemini API
  |
  | Response + Usage Metadata
  v
llm.py
  |
  +--------------------+
  |                    |
  v                    v
Response           tracker.py
  |                    |
  |                    v
  |              token_log.jsonl
  |
  v
Terminal
```

The separation keeps the application entry point, LLM integration, and usage tracking responsibilities independent.

---

## Token Usage Tracking

An important observation from the Gemini response is that an LLM request provides usage metadata in addition to the generated response.

For example:

```json
{
  "input_tokens": 10,
  "output_tokens": 30,
  "thinking_tokens": null,
  "total_tokens": 40
}
```

Each request is stored as a separate JSONL record.

This creates a simple history of LLM token consumption.

---

## Why Track Tokens?

Token usage is an important operational metric for LLM applications.

Tracking tokens can help answer questions such as:

- How much input context is being sent?
- How much output is being generated?
- Which requests consume the most tokens?
- Are users approaching configured usage limits?
- What usage patterns are causing increased consumption?
- How can token usage eventually be related to cost?

Simply counting the number of LLM requests is not sufficient to understand LLM consumption.

---

## Real-World Relevance

This exercise connects with a real-world project scenario I have encountered where users were found to have exceeded configured token-usage limits.

That experience highlighted the importance of being able to measure and understand token consumption.

Questions that become important in such a scenario include:

- How many tokens is each request consuming?
- Which users or applications are consuming the most tokens?
- Are users approaching their configured limits?
- What usage patterns are causing the increase?
- Can the application alert or respond when a limit is exceeded?

The Day 1 implementation provides the basic **measurement and recording** layer:

```text
LLM Request
     |
     v
Token Usage
     |
     v
Track
     |
     v
Store
```

A production implementation could extend this into:

```text
User / Application
        |
        v
    LLM Gateway
        |
        v
   LLM Provider
        |
        v
   Usage Metadata
        |
        v
 Usage / Metrics Store
        |
        +----------------+
        |                |
        v                v
   Quota Check       Monitoring
        |                |
        v                v
 Alerts / Limits    Dashboards
```

This provides a path from basic token tracking to broader **LLM observability, quota management, and cost management**.

---

## Project Structure

```text
day01/
|
├── .env
├── .env.example
├── .venv/
├── hello.py
├── main.py
├── llm.py
├── tracker.py
├── requirements.txt
├── README.md
└── token_log.jsonl
```

> Note: `.env`, `.venv/`, and `token_log.jsonl` are local files and are excluded from Git through `.gitignore`.

---

## Setup

Create the virtual environment:

```powershell
python -m venv .venv
```

Activate the environment and install the dependencies:

```powershell
pip install -r requirements.txt
```

Create a local `.env` file containing:

```text
GEMINI_API_KEY=your_actual_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

The actual API key is never committed to GitHub.

---

## Running the Application

From the `day01` directory:

```powershell
python main.py "Explain what RAG is in one sentence."
```

The generated response is displayed in the terminal.

Token usage is recorded in:

```text
token_log.jsonl
```

To inspect the log:

```powershell
Get-Content .\token_log.jsonl
```

---

## Security

The project keeps sensitive and generated files out of source control.

The repository `.gitignore` excludes:

```text
.env
.venv/
__pycache__/
*.jsonl
```

The `.env.example` file provides a safe configuration template without exposing the actual API key.

Before pushing to GitHub, the staged files are checked to ensure that the API key and local token log are not included.

---

## Key Learning

The main learning from Day 1 is that an LLM application should not be treated as a black box.

An LLM request produces more than just text:

```text
Request
   |
   v
LLM
   |
   +----> Generated Response
   |
   +----> Usage Metadata
              |
              +--> Input Tokens
              +--> Output Tokens
              +--> Thinking Tokens
              +--> Total Tokens
```

Capturing this metadata provides the foundation for:

- Usage analysis
- Prompt optimization
- Cost estimation
- Quota management
- Monitoring
- Alerting
- LLM observability

---

## Future Enhancements

Possible enhancements include:

- Add timestamps to usage records
- Record the model name
- Add request IDs
- Track request latency
- Track user/application identifiers
- Calculate estimated token cost
- Add configurable token limits
- Add quota validation
- Generate alerts when limits are approached
- Store usage in a database
- Build a usage dashboard
- Extend tracking to multi-agent workflows
- Add automated tests

---

## Build30 Learning Context

This project is part of my **Build30 30-Day AI Agent Engineering Challenge**.

The challenge is being approached as a hands-on engineering track focused on building practical AI/LLM capabilities through implementation, documentation, GitHub contributions, and real-world architectural thinking.

Day 1 establishes the foundation:

```text
LLM API
   |
   v
Response + Usage Metadata
   |
   v
Token Tracking
   |
   v
Basic LLM Observability
```

---

## Author

**Srinivas N**

AI / Cloud / Software Architecture | Generative AI | Agentic AI

LinkedIn: [Add your LinkedIn profile URL]

GitHub: [Add your GitHub profile URL]
