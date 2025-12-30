# Spatial Relations (SPR)

**Category ID:** `spr`

## Purpose
This category tests the model's understanding of spatial prepositions and geometric logic. It evaluates whether objects are placed correctly relative to one another (e.g., "left of", "under", "inside").

## What This Category Measures
*   **Positional Accuracy:** Is object A correctly placed relative to object B?
*   **Relative Orientation:** Are objects facing the correct direction if specified?
*   **Depth Layering:** Is the "foreground/background" distinction respected?

## What It Does NOT Measure
*   **Object Detail:** High fidelity is less important than correct placement (though objects must be recognizable).
*   **Photorealism:** A diagrammatic representation is acceptable if spatial logic is correct.

## Typical Failure Modes
*   **Reversal:** "Left" becomes "Right".
*   **2D Flattening:** Failure to represent depth (e.g., "behind" rendered as "next to").
*   **Preposition Ignorance:** The model generates the objects but ignores the spatial constraint entirely.

## Relation to Other Categories
*   **Requires MOC:** Needs multiple objects to test relations.
*   **distinct from ABC:** Focuses on *where* things are, not *what* they look like.

## Relation to SMF / HACS
*   **SMF:** Strongly related to "Reasoning" and "Logic".
*   **HACS:** Relates to "Stability" (consistent application of spatial rules).
