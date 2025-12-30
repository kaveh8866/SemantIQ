# Question Guidelines: Robustness & Adversarial (RAS)

## What makes a good RAS question?
*   **Edge Cases:** Test inputs that break standard parsers (empty strings, huge numbers, noise).
*   **Adversarial Intent:** Simulate a user trying to break the system (without being harmful).
*   **Resilience:** The model should degrade gracefully, not crash or hallucinate.

## What to avoid
*   **Pure Safety:** RAS is about *robustness*, not just "refusing bomb recipes" (that's ELB).
*   **Unsolvable Noise:** If a human can't read it, the model shouldn't be expected to.

## Bias & Neutrality
*   **Attack Vectors:** Test robustness against non-English adversarial inputs too.

## Difficulty Scaling
*   **Level 1:** Typos and casing issues.
*   **Level 2:** Prompt injection attempts.
*   **Level 3:** Cognitive gaslighting (user insists 2+2=5).
