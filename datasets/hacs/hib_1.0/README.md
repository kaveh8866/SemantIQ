# HACS / HIB 1.0 Dataset

## Overview
This directory contains the **Human-AI Comparative Score (HACS)** benchmark dataset, version **HIB 1.0**.
It consists of **70 questions** distributed across 5 modules, designed to be solvable by both humans and AI systems with comparable scoring criteria.

## Structure
The dataset is split into 5 YAML files, one for each module:

- **H1: Meaning & Context** (15 questions) - `h1_meaning_context.yaml`
  - Focus: Synonyms, idioms, ambiguity, register.
- **H2: Bias Resilience** (20 questions) - `h2_bias_resilience.yaml`
  - Focus: Loaded questions, stereotypes, controversial topics, cultural perspective, emotional regulation.
- **H3: Knowledge Illusion & Fiction** (15 questions) - `h3_knowledge_illusion.yaml`
  - Focus: Fake entities, misconceptions, source attribution, impossible tasks.
- **H4: Reflection & Meta-Cognition** (10 questions) - `h4_reflection_metacognition.yaml`
  - Focus: Confidence calibration, self-correction, boundary recognition.
- **H5: Long-Form & Consistency** (10 questions) - `h5_longform_consistency.yaml`
  - Focus: Structured narratives, logical progression, constraint compliance.

## Purpose & Methodology
HACS aims to measure "response maturity" rather than raw intelligence or fact retrieval.
- **Symmetry:** Every question is designed to be fair for humans (no obscure trivia) and AI (no adversarial attacks).
- **Scoring:** Responses are evaluated on 6 criteria: Clarity, Consistency, Depth, Neutrality, Reflection, Stability.
- **Anti-Coaching:** Questions rely on cognitive patterns (archetypes) rather than memorizable answers.

## Usage
This dataset is intended to be used with the SemantIQ benchmarking CLI.

```bash
# List all questions
bench hacs list-questions

# Show a specific question
bench hacs show-question h1_q_01
```

## Ethical & Methodological Notes
1.  **Not an IQ Test:** These questions assess semantic processing and behavioral stability, not g-factor intelligence.
2.  **Social Desirability:** While "neutrality" is a criterion, the benchmark explicitly differentiates between "robotic refusal" (low quality) and "balanced engagement" (high quality).
3.  **Comparability:** Human baselines are established via crowdsourcing to ensure the "human-solvable" claim holds true.
4.  **Language:** All prompts are in English (en), though the framework supports localization.

## License
Proprietary / SemantIQ Project Internal.
