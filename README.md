# 🎙️ Clara AI: Zero-Cost Voice Agent Automation

Clara AI is a robust, version-controlled automation system designed to transform raw client conversation transcripts (Demo and Onboarding) into production-ready AI voice agent configurations. It specifically addresses the critical transition from initial discovery to finalized operational logic.

---

## 🏗️ Architecture

The system follows a modular, mini-SaaS backend architecture to ensure scalability, reproducibility, and strict data integrity.

### System Diagram (ASCII)
```text
  [ CORE ARCHITECTURE ]
  
  ┌──────────────────────────────────────────────────────────┐
  │                      INTERFACE LAYER                     │
  │           (main.py - Orchestration & Discovery)          │
  └──────────────┬──────────────────────────────┬────────────┘
                 ▼                              ▼
  ┌──────────────────────────────┐  ┌────────────────────────┐
  │        LOGIC LAYER           │  │      DATA LAYER        │
  │    (processor.py - State)    │  │  (schemas.py - Models) │
  └──────────────┬───────────────┘  └───────────┬────────────┘
                 ▼                              ▼
  ┌──────────────────────────────┐  ┌────────────────────────┐
  │       EXTRACTION LOGIC       │  │     PERSISTENCE        │
  │  (llm_service.py - Heuristic)│  │ (storage.py - Version) │
  └──────────────────────────────┘  └────────────────────────┘
```

### Component Breakdown
- **`main.py`**: The central entry point. It handles environment setup, file discovery logic across the `data/` directory, and triggers the multi-stage pipeline.
- **`src/processor.py`**: The core business logic layer. It manages the state transition from Discovery to Finalization, ensuring Stage 2 data correctly refines Stage 1 uncertainties.
- **`src/llm_service.py`**: A deterministic "Zero-Cost Extraction Engine". It processes raw transcripts into structured data using keyword-based heuristics, ensuring reliability without external API costs.
- **`src/schemas.py`**: The "Source of Truth" for data structures. Built with **Pydantic**, it enforces strict validation on all agent configurations to prevent "hallucinated" or malformed data.
- **`src/storage.py`**: Handles versioned file persistence and generates human-readable `changelog.txt` files using structural diffing (`DeepDiff`).

---

## 🔄 Data Flow

The automation flow is a systematic two-stage process designed to handle missing data responsibly:

1.  **Stage 1: Discovery (Demo Phase)**
    *   **Input**: `demoN.txt` transcripts.
    *   **Action**: Extracts high-level business goals (Services, Company Information) and explicitly flags "unknowns" (e.g., exact after-hours routing) for later resolution.
    *   **Outcome**: Generates a `v1` draft configuration in `output/account_N/v1/`.

2.  **Stage 2: Finalization (Onboarding Phase)**
    *   **Input**: `onboardingN.txt` transcripts + `v1` baseline.
    *   **Action**: Refines fields, resolves all Stage 1 uncertainties, and implements strict "After-Hours" routing logic as required by the system rubric.
    *   **Outcome**: Finalizes the `v2` configuration and generates a `changelog.txt`.

---

## 🛠️ Setup Steps

1.  **Environment**: Ensure Python 3.10+ is installed.
2.  **Dependencies**: Install required packages (Pydantic, DeepDiff):
    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 How to Run on Dataset

To process all account files (demo/onboarding pairs) currently in the `data/` folder:
```bash
python main.py
```
The script will automatically pick up matching pairs and populate the `output/` directory.

---

## 📊 Where Outputs are Stored

Each account is isolated in its own folder under `output/`, showcasing clear version control:
```text
output/
└── account_1/            # Unique Account Directory
    ├── v1/               # Stage 1 Discovery Results
    │   ├── account_memo.json
    │   └── agent_spec.json
    ├── v2/               # Stage 2 Finalized Results
    │   ├── account_memo.json
    │   └── agent_spec.json
    └── changelog.txt     # Human-readable transition log
```

---

## 🚧 Limitations

- **Mock Extraction Engine**: The current version uses keyword-based heuristics. While highly reliable for the benchmark dataset, it lacks the deep contextual understanding of a live LLM for multi-intent transcripts.
- **Local Storage**: Data is persisted to the local filesystem; a production version would require an RDS or NoSQL database for multi-user support.

---

## 💡 Improvements for Production

1.  **LLM Integration**: Switch to **OpenAI GPT-4o** or **Gemini 1.5 Pro** using Structured Output modes for perfect extraction from complex dialogue.
2.  **Voice Provider Sync**: Integrate with **Retell AI** or **VAPI** APIs to automatically push the generated `AgentSpec` to live voice agents.
3.  **Human-in-the-Loop**: Add a lightweight UI (e.g., Streamlit or React) to allow implementation specialists to review and "Approve" `v2` configs before deployment.
4.  **Audio Ingestion**: Add an STT (Speech-to-Text) layer to allow the system to process `.mp3` or `.wav` call recordings directly.
