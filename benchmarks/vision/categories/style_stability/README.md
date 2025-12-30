# Style Stability (STB)

**Category ID:** `stb`

## Purpose
This category evaluates the consistency of style application and the model's resistance to "default style bias." It tests whether a requested style (e.g., "line art", "pixel art") is applied uniformly and whether neutral prompts trigger specific, unrequested aesthetics.

## What This Category Measures
*   **Style Adherence:** Does the image match the requested style description?
*   **Subject Consistency:** Can the model apply the *same* style to *different* subjects without reverting to training defaults?
*   **Medium Fidelity:** Does "oil painting" look like oil paint (texture, strokes)?

## What It Does NOT Measure
*   **Subject Accuracy:** Secondary to style correctness (though subject should be recognizable).
*   **Aesthetic Preference:** "Good" pixel art vs "Bad" pixel art is less relevant than "Is it pixel art?"

## Typical Failure Modes
*   **Default Bias:** A prompt for "a futuristic city" reverting to "cyberpunk neon" even if "pencil sketch" was requested.
*   **Inconsistent Application:** Background is photorealistic while foreground is cartoonish.
*   **Style Bleed:** Mixing two requested styles poorly.

## Relation to Other Categories
*   **Orthogonal to SOF/MOC:** Style applies to *how* things are rendered, not *what*.
*   **Prerequisite for Consistency:** A model must be stylistically stable to be useful for serial generation (e.g., storyboards).

## Relation to SMF / HACS
*   **SMF:** Related to "Consistency".
*   **HACS:** Relates to "Stability" and "Neutrality" (avoiding default biases).
