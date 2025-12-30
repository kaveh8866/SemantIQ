# Symbolic & Structural Benchmarks (SSB2)

## Conceptual Definition
Symbolic & Structural Benchmarks measure the model's ability to handle formal languages, code, structured data (JSON, XML), and symbolic logic. It evaluates precision in syntax and structure.

## Measured Capability
**Symbolic Manipulation:** The ability to process and generate strict formal structures.

## What It Measures
*   **Code Generation:** Writing syntactically correct code.
*   **Format Transformation:** JSON to XML.
*   **Math:** Solving equations (symbolically).
*   **Schema Adherence:** Outputting data that validates against a Pydantic model.

## What It Explicitly Does NOT Measure
*   **Natural Language Nuance (NCB):** Code is binary; it works or it doesn't.
*   **Creativity (CCB):** Code must follow spec.

## Typical Failure Modes
*   **Syntax Errors:** Missing brackets.
*   **Hallucinated Methods:** Calling functions that don't exist.
*   **Format Violation:** Returning markdown when JSON was requested.

## Relation to Other Categories
*   **Contrast with RFB:** RFB is logic in language; SSB2 is logic in symbols.

## Expected Benchmark Formats
*   **Coding Tasks:** LeetCode-style problems.
*   **Data Cleaning:** "Fix this broken JSON."
*   **Math Proofs:** Step-by-step symbolic derivation.
