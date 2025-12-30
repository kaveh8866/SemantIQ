# Human-AI Symmetry in Delivery

## 1. The Symmetry Principle
HACS is founded on the principle that **humans and AI systems must face the exact same semantic stimulus**.

### What this means:
1.  **Identical Wording:** The `question_text` and `constraints` are identical.
2.  **Identical Context:** The "instructions" (system prompt) are semantically equivalent.
    -   **AI:** Receives `system.md` content in the "system" role.
    -   **Human:** Sees the `system.md` content as "Instructions" at the top of the screen.

## 2. Delivery Mechanisms

### AI Delivery (API)
-   **Role:** `system`
-   **Content:** `prompts/hacs/core/v1/system.md`
-   **Role:** `user`
-   **Content:** `prompts/hacs/core/v1/user.md` (rendered with question)

### Human Delivery (Web UI)
-   **Header:** "Instructions"
-   **Content:** Text from `prompts/hacs/core/v1/system.md`
-   **Body:** "Task"
-   **Content:** Text from `prompts/hacs/core/v1/user.md` (rendered)

## 3. UI Elements vs. Prompt
To maintain symmetry, UI elements are **not** considered part of the prompt:
-   **Timers:** Visible to humans, implicit for AI (timeout).
-   **Text Fields:** Where humans type.
-   **Submit Buttons:** Mechanics of the medium.

These elements facilitate the *response* but do not change the *task*.

## 4. Risks of Asymmetry
If the AI receives "You are an AI..." and the human receives "You are a participant...", the comparison is invalid because the **role expectation** differs.
Therefore, HACS uses a neutral framing: "You are asked to respond..." which applies equally to both.
