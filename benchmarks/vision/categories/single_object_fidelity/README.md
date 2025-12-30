# Single-Object Fidelity (SOF)

**Category ID:** `sof`

## Purpose
This category measures the baseline capability of a T2I model to generate a single, specific object correctly. It tests the model's internal vocabulary and its ability to render objects without severe deformation or hallucination.

## What This Category Measures
*   **Object Presence:** Is the requested object recognizable in the image?
*   **Attribute Fidelity:** Does the object have the correct intrinsic properties (e.g., shape, core features)?
*   **Semantic Coherence:** Is the object structurally sound (e.g., a chair has legs, a car has wheels)?

## What It Does NOT Measure
*   **Artistic Quality:** Lighting, texture realism (unless specified), or composition beauty.
*   **Complex Interactions:** Relationships with other objects.

## Typical Failure Modes
*   **Hallucination:** Generating a different object (e.g., a "dog" instead of a "cat").
*   **Deformation:** Missing limbs, distorted geometry.
*   **Concept Bleed:** Merging features of the object with the background.

## Relation to Other Categories
*   **Foundation for MOC:** If a model fails SOF, it will fail Multi-Object Composition.
*   **Prerequisite for ABC:** Attribute binding requires a stable object to bind to.

## Relation to SMF / HACS
*   **SMF:** Analogous to "factual correctness" in text generation.
*   **HACS:** Relates to "Clarity" (conceptual precision).
