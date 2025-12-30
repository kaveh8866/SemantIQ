# Provider Integration

This guide details how to configure and use the various model providers supported by SemantIQ.

## Supported Providers

- **OpenAI** (ChatGPT, GPT-4)
- **OpenRouter** (Access to various open and closed models)
- **Marber** (Gateway/Proxy)
- **Dummy** (For testing and debugging)

## Configuration

SemantIQ uses environment variables for configuration. Create a `.env` file in the project root:

```bash
# OpenAI
OPENAI_API_KEY=sk-...

# OpenRouter
OPENROUTER_API_KEY=sk-or-...

# Marber
MARBER_API_KEY=mb-...
MARBER_API_URL=https://api.marber.ai/v1
```

**Security Note**: Never commit your `.env` file to version control. It is already added to `.gitignore`.

## Usage via CLI

You can select the provider and model using the `--provider` (`-p`) and `--model` (`-m`) flags.

### OpenAI
```bash
semantiq run code_writer_v1 --provider openai --model gpt-4-turbo --temperature 0.7
```

### OpenRouter
```bash
semantiq run code_writer_v1 --provider openrouter --model anthropic/claude-3-opus --max-tokens 4000
```

### Marber
```bash
semantiq run code_writer_v1 --provider marber --model meta-llama/llama-3-70b
```

### Dummy (Default)
```bash
semantiq run code_writer_v1 --provider dummy --model test-v1
```

## Supported Flags

The adapters support the following generic flags which are mapped to the provider's API:

- `--temperature`: Controls randomness (0.0 - 2.0).
- `--max-tokens`: The maximum number of tokens to generate.
- `--seed`: For reproducible outputs (supported by OpenAI and some OpenRouter models).

## Limitations

- **Rate Limits**: The system handles rate limits (429) with exponential backoff, but excessive usage may still lead to failures.
- **Cost Tracking**: Usage tokens are captured in the results, but exact cost calculation is not yet implemented.
- **Marber**: The adapter assumes a standard chat completion compatible payload. Specific model parameters might vary.
