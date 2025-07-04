# Log Diagnostic CLI Tool

A lightweight, Python-based command-line utility to parse and summarize backend system logs, with optional offline error insights powered by Gemma 2B via Ollama.

## Features

- Parses plain `.log` files
- Summarizes errors, warnings, and recent failures
- Highlights the most frequent error and explains it using a local LLM (Gemma 2B)
- Color-coded terminal preview for quick diagnosis
- Designed for privacy — logs never leave your machine
- Easy to automate via cron jobs or scheduled tasks

## Usage

```bash
python log_tool.py --log sample_logs/sample.log --summary report/summary.txt --preview
```

## About LLM Integration
- This tool uses Gemma 2B running locally via Ollama to explain the most frequent error in your logs.
- This ensures maximum data privacy, making it ideal for sensitive or enterprise environments.

## Extensibility
- Easily adaptable to support .json logs, custom formats, or domain-specific patterns

- Could be automated to run daily with cron or Task Scheduler

- Modular design makes it easy to plug in other models (e.g., Mistral, Phi)

- To reduce hallucinations, adjust generation parameters like temperature, top-k, or change the prompt in the code.

## Proof of Concept
- This tool is a functional prototype intended to showcase:

- Real-world error analysis automation

- Private, explainable AI integration

- Cross-domain backend compatibility

