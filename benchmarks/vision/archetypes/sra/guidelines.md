# Spatial Relation Assertion (SRA) Guidelines

## 1. What Good Prompts Look Like
*   **Focus:** The geometric relationship between objects.
*   **Structure:** `[Object A] + [Relation] + [Object B]`.
*   **Example:** "A cup on top of a book."
*   **Example:** "A person standing to the left of a tree."

## 2. What Must Be Avoided
*   **Ambiguous Prepositions:** "Near" (Subjective). Use "Touching" or "Left of".
*   **Camera Angles:** "Seen from below" (Confounds the spatial relation).
*   **Abstract Relations:** "A represents B".

## 3. Variation Strategy
*   **Relations:** On, Under, Left, Right, Inside, Behind.
*   **Object Types:** Rigid (Box) vs. Organic (Cat).
*   **Depth:** Foreground/Background distinctness.

## 4. Common Failure Patterns
*   **Reversal:** Left/Right confusion is very common.
*   **2D Flattening:** "Behind" rendered as "Above".
*   **Merging:** Objects intersecting physically rather than relating spatially.

## 5. Fair Scoring Support
SRA isolates "world modeling." Does the model understand 3D space, or just pixel co-occurrence?
