# Single-Object Isolation (SOI) Guidelines

## 1. What Good Prompts Look Like
*   **Focus:** A single, clearly defined subject.
*   **Structure:** `[Subject] + [Core Attributes] + [Neutral Background]`.
*   **Example:** "A red ceramic mug on a white table."
*   **Example:** "A standing golden retriever facing left."

## 2. What Must Be Avoided
*   **Multiple Objects:** "A dog and a cat" (This is MOC).
*   **Complex Backgrounds:** "in a busy city street" (Distracts from object fidelity).
*   **Ambiguous Terms:** "A nice car" (Subjective). Use "A red 1965 Ford Mustang" (Objective).

## 3. Variation Strategy
*   **Object Class:** Rotate through WordNet categories (mammals, vehicles, household items).
*   **Attributes:** Vary color, material, texture, and state (broken, wet, new).
*   **Viewpoint:** Front, side, top-down, isometric.

## 4. Common Failure Patterns
*   **Hallucination:** Adding unrequested objects (e.g., a person holding the mug).
*   **Attribute Failure:** The mug is blue instead of red.
*   **Incomplete Rendering:** Missing legs on a dog.

## 5. Fair Scoring Support
SOI is the baseline. If a model fails here, it will fail everywhere. It isolates the model's internal "dictionary" of visual concepts.
