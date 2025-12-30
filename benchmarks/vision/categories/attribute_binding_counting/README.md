# Attribute Binding & Counting (ABC)

**Category ID:** `abc`

## Purpose
This category assesses the precision of "binding" attributes (color, material, shape) to specific objects and the ability to count items accurately. It challenges the "bag of words" processing nature of some T2I models.

## What This Category Measures
*   **Attribute Binding Precision:** Is the *red* cube actually red, and the *blue* sphere actually blue? (Avoiding "attribute leakage").
*   **Count Accuracy:** Are there exactly *five* apples, not four or six?
*   **Leakage Resistance:** Does the texture of one object affect the other?

## What It Does NOT Measure
*   **Spatial Relations:** Unless they are critical to the count (e.g., "row of 5").
*   **Complex Scenarios:** The focus is on the tight coupling of adjective-noun pairs.

## Typical Failure Modes
*   **Attribute Leakage:** "A red car and a blue truck" results in two purple vehicles or swapped colors.
*   **Counting Errors:** Generating "many" instead of a specific number, or off-by-one errors.
*   **Object Merging:** Counting 5 items but 2 are merged.

## Relation to Other Categories
*   **Refines MOC:** Adds strict constraint to multi-object generation.
*   **Inverse of NEX:** Focuses on what *must* be present and bound, rather than what must be absent.

## Relation to SMF / HACS
*   **SMF:** Related to "Precision" and "Attention to Detail".
*   **HACS:** Relates to "Clarity" and "Consistency".
