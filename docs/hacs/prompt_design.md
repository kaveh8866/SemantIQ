# HACS Prompt Design Principles

## 1. Neutral Task Delivery
Unlike SMF (Semantic Mapping Framework), which uses specialized prompt strategies (QBE, CE, CRT, etc.) to stress-test specific cognitive functions, HACS (Human-AI Comparative Score) aims for **neutral task delivery**.

### Why "Neutral"?
-   **Goal:** To measure "response maturity" in a way that is comparable between humans and AI.
-   **Method:** The prompt must not "coach" the model or the human. It should simply present the task.
-   **Constraint:** No meta-instructions like "be creative", "think step-by-step", or "act as an expert". These bias the output and reduce comparability.

## 2. No Category or Module Leakage
HACS prompts **never** mention:
-   The module name (e.g., "Bias Resilience").
-   The archetype ID.
-   The scoring criteria (e.g., "You will be scored on clarity").

**Reasoning:**
-   Knowing the category (e.g., "Knowledge Illusion") would tip off the subject to be skeptical.
-   Knowing the scoring criteria allows for "gaming" the system (e.g., artificially inflating length for "Depth").

## 3. Strict Determinism
-   **Single Template:** All 70 questions use the exact same `system.md` and `user.md` wrapper.
-   **No Variation:** We do not adapt the system prompt based on the module.
-   **Hashing:** The final prompt is hashed (SHA-256) to ensure that the exact same text was presented to every subject.

## 4. Difference from SMF
| Feature | SMF | HACS |
| :--- | :--- | :--- |
| **Goal** | Stress-test specific failures | Measure comparable maturity |
| **Templates** | Many (QBE, CE, CRT...) | One (Core V1) |
| **System Prompt** | "You are a specialized engine..." | "You are asked to respond..." |
| **Complexity** | High (few-shot, complex instructions) | Minimal (Task + Constraints) |
