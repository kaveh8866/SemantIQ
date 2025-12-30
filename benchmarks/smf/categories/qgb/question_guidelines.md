# Question Guidelines: Query & Grounding (QGB)

## What makes a good QGB question?
*   **Citation:** "According to the text..."
*   **Negative Knowledge:** "Who is the king of Mars?" -> "There is none."
*   **Source Fidelity:** Stick strictly to provided sources, even if they contradict real world.

## What to avoid
*   **Open Book:** QGB often works best as "Closed Book" (RAG) or "Context only".
*   **Hallucination Traps:** Don't punish creativity, but punish stating fiction as fact.

## Bias & Neutrality
*   **Source Variety:** Use sources from different domains and viewpoints.

## Difficulty Scaling
*   **Level 1:** Retrieve one fact.
*   **Level 2:** Synthesize answer from 3 documents.
*   **Level 3:** Identify conflict between sources.
