# Attribute Binding & Counting (ABC) Guidelines

## 1. What Good Prompts Look Like
*   **Focus:** Exact numbers and specific attribute assignment.
*   **Structure:** `[Count] + [Attribute 1] + [Object A] + [Count] + [Attribute 2] + [Object B]`.
*   **Example:** "Three red spheres and two blue cubes."
*   **Example:** "A green shirt and red pants."

## 2. What Must Be Avoided
*   **Vague Quantifiers:** "Many", "Some", "A few". Use integers.
*   **Implied Attributes:** "A fire truck" (Implies red). Use "A blue fire truck" to test binding.
*   **Clutter:** Distracting background objects that might be counted.

## 3. Variation Strategy
*   **Numbers:** Small (1-5) vs. Medium (6-10).
*   **Attributes:** Color is standard, but use Texture (wooden/metal) and Shape.
*   **Symmetry:** Equal counts vs. unequal counts.

## 4. Common Failure Patterns
*   **Bleeding:** The red from the spheres turns the cubes purple.
*   **Count Error:** Generating 4 instead of 3.
*   **Object Identity Loss:** Cubes becoming spheres.

## 5. Fair Scoring Support
ABC is the rigorous math test of T2I. It exposes the lack of symbolic reasoning in diffusion models.
