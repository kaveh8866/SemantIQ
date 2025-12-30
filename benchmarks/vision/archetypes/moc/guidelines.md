# Multi-Object Composition (MOC) Guidelines

## 1. What Good Prompts Look Like
*   **Focus:** Two or more distinct objects sharing a scene.
*   **Structure:** `[Object A] + [Object B] + [Shared Context]`.
*   **Example:** "A cat sitting next to a dog on a rug."
*   **Example:** "A blue apple and a yellow banana on a plate."

## 2. What Must Be Avoided
*   **Implied Interaction:** "A cat chasing a dog" (Action is secondary; presence is primary for MOC).
*   **Massive Crowds:** "A crowd of people" (This is counting/density, not composition).
*   **Impossible Geometry:** Overly complex constraints that confuse the parser.

## 3. Variation Strategy
*   **Category Mixing:** Natural (Cat + Dog) vs. Unnatural (Toaster + Tree).
*   **Attribute Independence:** Ensure attributes don't bleed (e.g., Red Car + Blue Truck).
*   **Scale:** Large object + Small object (Elephant + Mouse).

## 4. Common Failure Patterns
*   **Object Fusion:** A "cat-dog" hybrid.
*   **Missing Objects:** Asking for 3 items, getting 2.
*   **Attribute Leakage:** "Blue apple and yellow banana" -> Green apple.

## 5. Fair Scoring Support
MOC tests the "binding problem." It separates models that can "paste" objects together from those that understand distinct entities in a shared space.
