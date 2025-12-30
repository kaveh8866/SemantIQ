# Semantic Maturity Framework (SMF)

The Semantic Maturity Framework (SMF) is a comprehensive benchmarking domain designed to evaluate Large Language Models (LLMs) across a multi-dimensional spectrum of semantic, cognitive, ethical, and integrative capabilities.

Unlike traditional task-based benchmarks that focus on specific "jobs" (e.g., "write Python code"), SMF focuses on **underlying capability maturity**. It asks not just "can the model do X?", but "how robustly, coherently, and ethically does the model handle the semantic structures underlying X?".

## Architecture & Integration

SMF benchmarks are integrated into the Semantiq platform as a specialized domain (`benchmarks/smf/`).

### Integration Points
*   **Pipeline:** SMF benchmarks utilize the standard Semantiq pipeline for execution, ensuring consistent matrix runs, caching, and result management.
*   **Scoring:** SMF employs specialized scorers (mostly qualitative and semi-quantitative) that map to the specific `measured_capability` of each category.
*   **Web UI:** The UI will feature a dedicated "SMF Radar" visualization, aggregating scores across the 12+ dimensions defined in the registry.
*   **Versioning:** SMF benchmarks follow strict semantic versioning. Changes to the `registry.yaml` or underlying criteria increment the framework version.

## Architecture & Risk Notes

### Provider-Agnostic Design
SMF benchmarks are strictly provider-agnostic. They measure output behavior, not internal model architecture. This ensures that closed-source models (OpenAI, Anthropic) and open-weights models (Llama, Mistral) are evaluated on an identical footing.

### Risk Mitigation Strategies

#### 1. Semantic Overfitting
*   **Risk:** Models optimizing for specific phrasings in public benchmarks.
*   **Mitigation:** SMF uses abstract category definitions (`registry.yaml`) decoupled from specific prompt implementations. Future prompt sets will be versioned and rotated to prevent overfitting to a static test set.

#### 2. Prompt Memorization
*   **Risk:** Models memorizing the exact text of benchmark questions.
*   **Mitigation:**
    *   **Dynamic Prompts:** Key variables in prompts are templated.
    *   **Private Test Sets:** The framework supports "held-out" datasets that follow the public specs but contain unseen samples.

#### 3. Category Leakage
*   **Risk:** Capabilities from one category (e.g., Logic) influencing scores in another (e.g., Creativity) inappropriately.
*   **Mitigation:** Strict isolation of subdimensions. For example, `ccb` (Creativity) explicitly rewards novelty, while `mcb` (Meaning Coherence) rewards stability. The scoring rubrics are orthogonal.

### Focus on Output Behavior
SMF treats the model as a black box. It does not inspect attention weights or activations. It evaluates the **semantic maturity of the generated artifact**—its coherence, grounding, and alignment with the prompt's intent.

## Registry

The single source of truth for all SMF categories is `benchmarks/smf/registry.yaml`. This file defines the hierarchy, capabilities, and subdimensions for the entire framework.
