# Style Anchoring & Stability (SAS) Guidelines

## 1. What Good Prompts Look Like
*   **Focus:** Adherence to a visual style over semantic content.
*   **Structure:** `[Simple Subject] + [Explicit Style Medium]`.
*   **Example:** "A cat drawn in charcoal."
*   **Example:** "A low-poly 3D render of a tree."

## 2. What Must Be Avoided
*   **Artist Names:** "Picasso", "Van Gogh" (Tests memorization).
*   **Vague Adjectives:** "Beautiful", "Artistic".
*   **Conflicting Styles:** "A photorealistic charcoal sketch".

## 3. Variation Strategy
*   **Media:** Pencil, Oil, Watercolor, 3D Render, Pixel Art.
*   **Eras:** 1980s VHS, Victorian Engraving.
*   **Subjects:** Keep subjects simple (Apple, Car, House) to isolate style performance.

## 4. Common Failure Patterns
*   **Reversion:** Drifting back to photorealism (default mode for many models).
*   **Subject Corruption:** The style is so heavy the object is unrecognizable.
*   **Text Artifacts:** Signatures appearing in corners.

## 5. Fair Scoring Support
SAS ensures the model can modulate its output distribution away from the mean (photorealism) without breaking semantic consistency.
