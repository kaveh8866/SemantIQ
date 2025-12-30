# Negation & Exclusion Constraint (NEC) Guidelines

## 1. What Good Prompts Look Like
*   **Focus:** Absence of a specific element.
*   **Structure:** `[Scene] + [Negative Constraint]`.
*   **Example:** "An empty living room with no furniture."
*   **Example:** "A burger without cheese."

## 2. What Must Be Avoided
*   **Subtle Negation:** "Not very bright" (Subjective). Use "Pitch black".
*   **Paradoxes:** "A square circle."
*   **Implied Presence:** "A riderless horse" (Better than "Horse with no rider" sometimes, but testing "no X" syntax is key).

## 3. Variation Strategy
*   **Constraint Type:** Object removal (no people), Attribute removal (no color/black and white), Action removal (standing still).
*   **Syntax:** "no X", "without X", "excluding X".

## 4. Common Failure Patterns
*   **Ironic Presence:** The model draws exactly what was forbidden because the token is in the prompt.
*   **Ghosting:** Smudged artifacts where the object would be.
*   **Ignore:** Completely ignoring the constraint.

## 5. Fair Scoring Support
NEC tests control. Can the model *suppress* a concept as well as generate it?
