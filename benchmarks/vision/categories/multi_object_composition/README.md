# Multi-Object Composition (MOC)

**Category ID:** `moc`

## Purpose
This category evaluates the model's ability to generate multiple distinct objects within a single scene. It tests the "compositional generalization" capability—can the model combine known concepts (verified in SOF) into a novel scene?

## What This Category Measures
*   **Object Count Accuracy:** Are all requested objects present?
*   **Object Distinctness:** Are the objects separate and not blended into a chimera?
*   **Scene Coherence:** Do the objects exist in a shared, logical space?

## What It Does NOT Measure
*   **Spatial Precision:** Exact relative positioning (handled by SPR), though rough placement is expected.
*   **Interaction:** Whether objects are interacting (e.g., "playing catch") is secondary to their coexistence.

## Typical Failure Modes
*   **Object Omission:** One or more requested objects are missing.
*   **Blending:** Two objects merge into one (e.g., a "cat-dog" hybrid).
*   **Attribute Leakage:** Attributes of one object bleed into another (e.g., a "blue car" and "red ball" becomes "blue car" and "blue ball").

## Relation to Other Categories
*   **Extends SOF:** Requires successful single-object generation.
*   **Precedes SPR:** Spatial relations require multiple objects to be successfully generated first.

## Relation to SMF / HACS
*   **SMF:** Related to "Reasoning Depth" (handling complexity).
*   **HACS:** Relates to "Consistency" (internal coherence of the scene).
