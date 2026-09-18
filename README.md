**Structured, rubric-based LLM evaluation for your agents.**

A Model Context Protocol (MCP) server that exposes TypeSafe AI's Jev System One evaluation API for scoring text or structured state against typed yes/no, single-choice, and rubric questions.


## Overview

The mewcp-jev MCP Server provides:

- One-call evaluation of a state (plain text or structured data) against any number of typed questions, each answered independently and in parallel
- Support for mixing yes/no (noul), single-select (choice), and rubric-scored (score) questions within the same request
- Discovery of the model aliases and versions this account can use for evaluation requests

Perfect for:

- Automated grading or QA of LLM outputs, chat transcripts, or agent state
- Evaluation pipelines that need yes/no, single-select, and rubric scoring in one pass
- Picking the right Jev model alias or pinned version before running an evaluation


## Tools


<details>
<summary><code>evaluate_state</code> — Evaluate a state against typed questions</summary>

Evaluates the given state against a map of typed questions and returns one structured answer per question, keyed by the same ids used in the request. Every question is evaluated independently and in parallel against the same state, and noul (yes/no), choice (single-select), and score (rubric) questions can be freely mixed within a single call.

**Inputs:**
```
- `state` (string | object | array, required) — The content to evaluate: a plain string for text, or structured data (object/array) for chat logs, records, or app state.
- `model` (string, required) — The model that handles the request, e.g. 'jev-latest' (alias) or a pinned version like 'jev-1.13.0'. See the models group.
- `questions` (object<string, Question>, required) — A map of typed Question objects, keyed by a caller-chosen id — answers come back under the same keys, and the key itself is never sent to the model. Each Question is a discriminated union on its required 'type' field, one of 'noul', 'choice', or 'score'; all three also accept 'instructions' (required, string | object | array | null — arbitrary JSON is accepted for clarity or to pass supporting data verbatim). Noul ('type': 'noul') is a yes/no question with an optional 'criteria' object holding optional 'true'/'false' descriptions (string, object, or array) of what a yes/no answer means. Choice ('type': 'choice') picks one option from a set and requires 'criteria': a map of option name to an optional rubric description (string, object, array, or null when the option needs no extra detail) — one entry per option. Score ('type': 'score') rates the state on a rubric and requires 'criteria': an ordered array of at least two level descriptions (each a string, or an object/array for structured rubric detail). Any mix of the three types is allowed in the same map.
```

**Output `data` schema:**

```typescript
{
  model: string;
  answers: {
    [question_id: string]: {
      type: string;
      noul?: number;
      choice?: string;
      probabilities?: { [option: string]: number };
      confidence?: number;
      score?: number;
      legend?: { [level: string]: string };
    };
  };
  usage: {
    input_tokens: number;
    output_tokens: number;
  };
}
```

</details>


<details>
<summary><code>list_models</code> — List available Jev models</summary>

Lists the model names and aliases this account can pass in the evaluate-state `model` field, with a description and release date for each. This list currently only surfaces aliases such as `jev-latest` and `jev-preview` — a versioned model ID (e.g. `jev-1.13.0`) is still accepted by the evaluate-state `model` field even when it does not appear here.

**Inputs:**

This tool takes no input parameters.

**Output `data` schema:**

```typescript
{
  models: {
    name: string;
    description: string;
    release_date: string;
  }[];
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Response Envelope</strong></summary>

Every tool returns the same top-level envelope. Only `data` varies per tool.

```json
// Success
{
  "success": true,
  "statusCode": 200,
  "retriable": false,
  "retry_after_seconds": null,
  "error": null,
  "data": { ... }
}

// Error
{
  "success": false,
  "statusCode": 400,
  "retriable": false,
  "retry_after_seconds": null,
  "error": { "code": "{ERROR_CODE}", "message": "{description}", "details": {} },
  "data": null
}
```

- `retriable` — `true` when it is safe to retry (rate limit, network error, 503). `false` for validation and auth errors.
- `retry_after_seconds` — seconds to wait before retrying; present only when `retriable` is `true` and the upstream specifies a delay.
- `error.code` — machine-readable string: `VALIDATION_ERROR`, `AUTH_ERROR`, `UPSTREAM_ERROR`, `SERVER_ERROR`.

</details>


## Getting Your TypeSafe AI API Key

<details>
<summary><strong>Steps</strong></summary>

1. Go to the [TypeSafe AI API Documentation](https://docs.typesafe.ai/api)
2. Follow the Authentication section to sign in to your TypeSafe AI account and open the API keys area
3. Click **Create API Key** (or equivalent)
4. Copy the generated key — you will only see it once

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** API key not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_API_KEY` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check API key is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No TypeSafe AI credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Connect your TypeSafe AI account (OAuth) or add your API key (static)
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>TypeSafe AI API Error</strong></summary>

- **Cause:** Upstream TypeSafe AI API returned an error
- **Solution:**
  1. Check the [TypeSafe AI API Documentation](https://docs.typesafe.ai/api) for current service notices
  2. Verify your credential has the required permissions
  3. Review the error message for specific details

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[TypeSafe AI API Documentation](https://docs.typesafe.ai)** — Official API reference
- **[TypeSafe AI API Reference](https://docs.typesafe.ai/api)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling


</details>
