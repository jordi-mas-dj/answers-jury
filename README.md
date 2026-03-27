# answers-jury

## Setup

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- For Claude: [Claude CLI](https://code.claude.com/docs/en/quickstart) installed

### Configuration

Create a `.env` file in the project root with:

```
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

### Install dependencies

```bash
uv sync
```

## Run

```bash
uv run streamlit run app.py
```

