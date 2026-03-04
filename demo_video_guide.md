# 🎬 Demo Video Guide: Clara AI Automation

This guide will help you record a professional 3-5 minute demo video that will impress viewers and clearly explain the technical depth of your project.

---

## 🛠️ Preparation
Before you start recording, have these open in your IDE (VS Code):
1.  **`data/demo1.txt`** and **`data/onboarding1.txt`** (to show raw input).
2.  **`main.py`** (to show the entry point).
3.  **`output/account_1/`** folder (to show the results).
4.  **Terminal** (cleared and ready to run `python main.py`).

---

## 🎙️ Suggested Video Script

### 1. Introduction (30s)
*   **What to say**: "Hi, I'm [Your Name]. Today I'm demonstrating **Clara AI**, a zero-cost automation system I built to transform raw client conversations into structured AI voice agent configurations."
*   **What to show**: Your GitHub repository (`README.md`) showing the ASCII architecture diagram.

### 2. The Problem & Input (45s)
*   **What to say**: "Voice agents need strict configurations. Usually, this data is buried in transcripts. Here is a raw **Demo Call** where we identify high-level needs, and an **Onboarding Call** where we finalize complex logic like after-hours routing."
*   **What to show**: Briefly scroll through `demo1.txt` and `onboarding1.txt`. Highlight the "Emergency" or "Business Hours" mentions in the text.

### 3. Execution (30s)
*   **What to say**: "The system is designed as a modular pipeline. I'll run the orchestrator now. It automatically pairs matching transcripts and uses a heuristic extraction engine to build the specs."
*   **What to show**: Run `python main.py` in the terminal and let the progress messages scroll by.

### 4. Showing the Output (1m 30s)
*   **What to say**: "Let's look at the results for Account 1. The system generated two versions."
    *   **Show `v1/agent_spec.json`**: "V1 is the discovery draft. Notice it has basic details but flags 'unknowns' for things we hadn't confirmed yet."
    *   **Show `v2/agent_spec.json`**: "V2 is the finalized production spec. It now includes the **After Hours Flow** and specific **Emergency Routing Rules** extracted from the second call."
*   **Highlight the Changelog**: "The system also generates a human-readable `changelog.txt` using structural diffing, showing exactly what evolved between the two stages."

### 5. Conclusion (30s)
*   **What to say**: "This modular architecture ensures strict data integrity, version control, and is completely free to run. Thank you for watching!"

---

## 💡 Pro-Tips for "Wow" Factor
- **Zoom In**: Make sure your code font size is large enough (Ctrl + '+' in VS Code).
- **Highlight the Logic**: Mention that you used **Pydantic** for validation to ensure no "hallucinations" occur in the data.
- **Tools**: Use **OBS Studio** or **Loom** for recording. They allow you to record your screen and your voice (and face) easily.
- **No Silence**: If the code takes a second to run, keep talking! Explain *why* the architecture is modular.
