# SMF Question Archetypes & Design Patterns

## 1. What is a Question Archetype?

A **Question Archetype** is a formalized, abstract pattern for a benchmark task. It serves as a blueprint from which multiple concrete benchmark "instances" (questions or prompts) can be generated.

In the Semantic Maturity Framework (SMF), we do not just write a list of 100 questions. Instead, we define **archetypes** that capture the *structural essence* of a test.

### Distinction

| Concept | Definition | Example |
| :--- | :--- | :--- |
| **Category** | The high-level capability being measured. | `mcb` (Meaning Coherence) |
| **Archetype** | The abstract structure of the task. | `mcb-01-definition-consistency` |
| **Instance** | A concrete realization of the archetype. | "Define 'Entropy' in physics vs. information theory." |
| **Prompt** | The exact string sent to the LLM. | "System: You are a physicist... User: Define..." |

## 2. Why Archetypes are Critical

### A. Comparability & Standardization
By adhering to archetypes, we ensure that every model is tested on the *same kinds* of structural challenges, even if the specific topics vary.

### B. Anti-Overfitting & Anti-Gaming
If we release a static dataset of questions, models will eventually "memorize" the answers. With archetypes:
*   We can generate infinite variations (e.g., changing the topic from "Entropy" to "Osmosis").
*   We can rotate the specific instances in public vs. private leaderboards while keeping the *structure* identical.

### C. Scaling
Archetypes allow us to programmatically generate test cases. For example, an archetype requiring "Translation of idiomatic expressions" can be instantiated with hundreds of idioms across dozens of languages.

## 3. Anatomy of an Archetype

Every SMF Question Archetype is defined in `benchmarks/smf/question_archetypes.yaml` and includes:

*   **ID:** A stable, unique identifier (e.g., `mcb-01`).
*   **Intent:** What specific cognitive or semantic muscle is being stressed?
*   **Input Structure:** What does the model see? (e.g., "Two conflicting statements").
*   **Expected Output:** What characterizes a good response? (e.g., "Synthesis of both views").
*   **Variation Axes:** How can we change this question without breaking the test? (e.g., "Change the topic," "Change the tone").
*   **Disallowed Patterns:** What makes this test invalid? (e.g., "Do not use common riddles").
*   **Failure Modes:** How do models typically fail? (e.g., "Hallucinating non-existent details").

## 4. Versioning

Archetypes are version-controlled. If the methodology for testing "Reasoning" changes, the archetype is updated or deprecated. This ensures that scores remain meaningful over time.
