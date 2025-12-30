# SemantIQ-Vision: T2I Reproducibility & Rendering

This document outlines the reproducibility strategy for the SemantIQ-Vision Text-to-Image benchmark.

## Core Philosophy

Reproducibility in Text-to-Image (T2I) generation is inherently challenging due to:
1.  **Stochasticity**: Diffusion models are probabilistic. Even with fixed seeds, differences in hardware (GPU architecture), driver versions, or floating-point precision can lead to pixel-level divergence.
2.  **Provider Opacity**: API providers often update model weights, change backend schedulers, or inject hidden prompts/safety filters without notice.
3.  **Non-Determinism**: Some samplers or optimizations (e.g., Flash Attention) may introduce non-deterministic behavior.

Therefore, **Pixel-Perfect Identity is NOT required** for SemantIQ-Vision. Instead, we focus on **Semantic Reproducibility** and **Traceability**.

## Input-Level Hashing

To ensure traceability, we generate a stable **Prompt Hash** for every generation request. This hash uniquely identifies the *input state*, not the output pixels.

### Hash Calculation
The hash is a SHA-256 digest of the following concatenated components:
1.  **Prompt Text** (Exact string)
2.  **Prompt ID** (e.g., `vision_sof_01`)
3.  **Normalized Parameters** (JSON string, sorted keys)

Formula:
```python
prompt_hash = sha256(prompt_text + prompt_id + params_json)
```

This guarantees that if two runs use the exact same prompt and settings, they will share the same identifier structure, allowing easy comparison of outputs across runs.

## Normalized Rendering Parameters

To minimize variance, we enforce a strict set of normalized parameters across all providers:

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | int | 1024 | Image width |
| `height` | int | 1024 | Image height |
| `num_images` | int | 1 | Images per prompt |
| `seed` | int | None | Random seed (optional) |
| `steps` | int | None | Inference steps (optional) |
| `guidance_scale` | float | None | Classifier-free guidance scale (optional) |

**Handling Missing Parameters:**
- If a provider does not support a parameter (e.g., `seed`), it is omitted from the request, and a warning is logged in `IMAGE_METADATA.json`.
- Missing optional parameters default to provider-specific optimal values.

## Reproducibility Rules

1.  **No Implicit Rewriting**: The benchmark pipeline MUST NOT alter the prompt text (e.g., "enhancing" prompts) unless explicitly part of the provider's documented API behavior that cannot be disabled.
2.  **No Auto-Style Fallback**: If a style is requested, the model must attempt it or fail; the pipeline should not inject "photorealistic" or other style keywords automatically.
3.  **Seed Reporting**: If a provider supports seeds, the used seed must be recorded. If the provider returns a seed even if not requested, it must be captured.

## Risks & Mitigations

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| **Provider Updates** | Model behavior changes over time | Record `provider` and `model` version in metadata. |
| **Hidden Defaults** | API injects "safe" or "diverse" prompts | Use input-level hashing; document observed behavior. |
| **Hardware Variance** | Slight pixel shifts | Focus evaluation on semantic content, not pixel matching. |
| **Rate Limits** | Partial run completion | Robust error handling and retry logic (future work). |

## Directory Structure

All rendering artifacts are stored in `runs/vision/<run_id>/`:
- `images/`: Contains generated images named `<prompt_id>_<hash>.<ext>`.
- `metadata/`: Contains `RUN_METADATA.json` and `IMAGE_METADATA.json`.
