# answers-jury

<img width="696" height="710" alt="Captura de pantalla 2026-03-30 a les 12 38 26" src="https://github.com/user-attachments/assets/cc71a87b-2985-4a90-89dd-20530c5439f7" />


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

