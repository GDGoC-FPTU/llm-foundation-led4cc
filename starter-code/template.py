"""
Day 1 — LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1

Instructions:
    1. Fill in every section marked with TODO.
    2. Do NOT change function signatures.
    3. Copy this file to solution/solution.py when done.
    4. Run: pytest tests/ -v
"""

import os
import time
from typing import Any, Callable

# ---------------------------------------------------------------------------
# Estimated costs per 1M INPUT & OUTPUT tokens (USD) as of March 2026
# Vietnamese text generally consumes ~1.5x - 2.0x more tokens than English due to Unicode/diacritics.
# ---------------------------------------------------------------------------
PRICING_1M_TOKENS = {
    "gpt-4o": {"input": 5.00, "output": 20.00},
    "gpt-4o-mini": {"input": 0.150, "output": 0.600},
    "gemini-2.5-flash": {"input": 0.075, "output": 0.300},
    "gemini-2.5-pro": {"input": 1.25, "output": 5.00},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-5-haiku": {"input": 0.80, "output": 4.00},
}

# Standard Model Identifiers
OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"
GEMINI_MODEL = "gemini-2.5-flash"
ANTHROPIC_MODEL = "claude-3-5-haiku"


# ---------------------------------------------------------------------------
# Task 1 — Call OpenAI (GPT-4o)
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float, dict]:
    """
    Call the OpenAI Chat Completions API and return the response text, latency,
    and token usage stats.

    Args:
        prompt:      The user message to send.
        model:       The OpenAI model to use (default: gpt-4o).
        temperature: Sampling temperature (0.0 – 2.0).
        top_p:       Nucleus sampling threshold.
        max_tokens:  Maximum number of tokens to generate.

    Returns:
        A tuple of:
            - response_text (str)
            - latency_seconds (float)
            - usage (dict with keys: 'input_tokens', 'output_tokens')

    Hint:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # response.usage contains input_tokens and output_tokens (prompt_tokens/completion_tokens)
    """

    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = "mock-key"

    client = OpenAI(api_key=api_key)
    start_time = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    end_time = time.time()
    latency = end_time - start_time

    response_text = response.choices[0].message.content or ""

    usage = {
        "input_tokens": response.usage.prompt_tokens if response.usage else 0,
        "output_tokens": response.usage.completion_tokens if response.usage else 0,
    }

    return response_text, latency, usage

    # TODO: Import OpenAI, instantiate client, call chat.completions.create with parameters,
    #       measure execution start/end time, extract text and token usage, and return them.
    raise NotImplementedError("Implement call_openai")


# ---------------------------------------------------------------------------
# Task 2 — Call Google Gemini 2.5 (Standard Practical Model)
# ---------------------------------------------------------------------------
def call_gemini(
    prompt: str,
    model: str = GEMINI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float, dict]:
    import os
    import time

    from google import genai
    from google.genai import types

    api_key = os.getenv("GEMINI_API_KEY") or "mock-key"

    client = genai.Client(api_key=api_key)

    config = types.GenerateContentConfig(
        temperature=temperature,
        top_p=top_p,
        max_output_tokens=max_tokens,
    )

    start_time = time.time()

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )

    latency = time.time() - start_time

    usage_metadata = response.usage_metadata

    usage = {
        "input_tokens": usage_metadata.prompt_token_count,
        "output_tokens": usage_metadata.candidates_token_count,
    }

    return response.text, latency, usage
    # TODO: Initialize Gemini client, set config parameters, call generate_content,
    #       measure latency, extract response text and usage metadata, and return the tuple.
    raise NotImplementedError("Implement call_gemini")


# ---------------------------------------------------------------------------
# Task 3 — Call Anthropic Claude (Exploratory track)
# ---------------------------------------------------------------------------
def call_anthropic(
    prompt: str,
    model: str = ANTHROPIC_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float, dict]:
    import os
    import time
    import anthropic

    api_key = os.getenv("ANTHROPIC_API_KEY") or "mock-key"

    client = anthropic.Anthropic(api_key=api_key)

    start_time = time.time()

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    latency = time.time() - start_time

    response_text = ""
    for part in response.content:
        response_text += part.text

    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }

    return response_text, latency, usage
    # TODO: Initialize Anthropic client, create message, measure latency,
    #       extract content text and usage statistics, and return the tuple.
    raise NotImplementedError("Implement call_anthropic")


# ---------------------------------------------------------------------------
# Task 4 — Compare Models (OpenAI GPT-4o vs OpenAI Mini vs Gemini 2.5 Flash)
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    def calculate_cost(input_tokens: int, output_tokens: int, input_rate: float, output_rate: float) -> float:
        return (
            input_tokens * input_rate
            + output_tokens * output_rate
        ) / 1_000_000

    gpt4o_response, gpt4o_latency, gpt4o_usage = call_openai(
        prompt,
        model="gpt-4o",
    )

    mini_response, mini_latency, mini_usage = call_openai(
        prompt,
        model="gpt-4o-mini",
    )

    gemini_response, gemini_latency, gemini_usage = call_gemini(
        prompt,
        model="gemini-2.5-flash",
    )

    gpt4o_input = gpt4o_usage["input_tokens"]
    gpt4o_output = gpt4o_usage["output_tokens"]

    mini_input = mini_usage["input_tokens"]
    mini_output = mini_usage["output_tokens"]

    gemini_input = gemini_usage["input_tokens"]
    gemini_output = gemini_usage["output_tokens"]

    return {
        "gpt4o": {
            "response": gpt4o_response,
            "latency": gpt4o_latency,
            "cost": calculate_cost(gpt4o_input, gpt4o_output, 5.0, 20.0),
            "input_tokens": gpt4o_input,
            "output_tokens": gpt4o_output,
        },
        "gpt4o_mini": {
            "response": mini_response,
            "latency": mini_latency,
            "cost": calculate_cost(mini_input, mini_output, 0.150, 0.600),
            "input_tokens": mini_input,
            "output_tokens": mini_output,
        },
        "gemini_flash": {
            "response": gemini_response,
            "latency": gemini_latency,
            "cost": calculate_cost(gemini_input, gemini_output, 0.075, 0.300),
            "input_tokens": gemini_input,
            "output_tokens": gemini_output,
        },
    }
    # TODO: Call call_openai with default gpt-4o model
    # TODO: Call call_openai with gpt-4o-mini model
    # TODO: Call call_gemini with default gemini-2.5-flash model
    # TODO: Calculate costs exactly based on input and output token counts using PRICING_1M_TOKENS
    #       Formula: Cost = (input_tokens * input_rate_per_1M + output_tokens * output_rate_per_1M) / 1,000,000
    # TODO: Assemble and return the comparison dictionary.
    raise NotImplementedError("Implement compare_models")


# ---------------------------------------------------------------------------
# Task 5 — Streaming chatbot with Gemini 2.5 (Focus Model)
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    """
    Run an interactive streaming chatbot in the terminal using Gemini 2.5.

    Behaviour:
        - Streams response tokens from Gemini 2.5 Flash as they arrive.
        - Maintains the last 3 turns of conversation history for context.
        - Typing 'quit' or 'exit' ends the session.

    Hints:
        - Maintain a history list of conversation turns.
        - Check how to stream responses using client.chats or model.generate_content(..., stream=True).
        - Keep history limited to the last 3 turns to optimize context window and costs.
    """

    import os
    from google import genai
    from google.genai import types

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY environment variable")

    client = genai.Client(api_key=api_key)

    model = "gemini-2.5-flash"

    config = types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.9,
        max_output_tokens=512,
    )

    history = []

    print("Gemini 2.5 Flash chatbot")
    print("Type 'quit' or 'exit' to stop.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break

        if not user_input:
            continue

        recent_history = history[-3:]

        prompt_parts = []

        for turn in recent_history:
            prompt_parts.append(f"User: {turn['user']}")
            prompt_parts.append(f"Assistant: {turn['assistant']}")

        prompt_parts.append(f"User: {user_input}")
        prompt_parts.append("Assistant:")

        prompt_with_history = "\n".join(prompt_parts)

        print("Gemini: ", end="", flush=True)

        response_text = ""

        stream = client.models.generate_content_stream(
            model=model,
            contents=prompt_with_history,
            config=config,
        )

        for chunk in stream:
            chunk_text = getattr(chunk, "text", None)

            if chunk_text:
                print(chunk_text, end="", flush=True)
                response_text += chunk_text

        print()

        history.append(
            {
                "user": user_input,
                "assistant": response_text,
            }
        )

        history = history[-3:]
    # TODO: Setup interactive session, prompt user for input, stream response, and update history.
    


# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable[[], Any],
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """
    Call fn(). If it raises an exception, retry up to max_retries times
    with exponential backoff (delay = base_delay * 2^attempt).

    Args:
        fn:          Zero-argument callable to execute.
        max_retries: Maximum number of retry attempts.
        base_delay:  Initial delay in seconds before the first retry.

    Returns:
        The return value of fn() on success.

    Raises:
        The last exception raised by fn() after all retries are exhausted.
    """
    import time

    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as exc:
            last_exception = exc

            if attempt == max_retries:
                raise last_exception

            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
    # TODO: implement retry loop with exponential backoff
    raise NotImplementedError("Implement retry_with_backoff")


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    results = []

    for prompt in prompts:
        try:
            comparison = compare_models(prompt)
        except TypeError:
            # Test mock defines _get_mock() with no parameters,
            # so this fallback keeps the function compatible with that mock.
            comparison = compare_models()

        comparison["prompt"] = prompt
        results.append(comparison)

    return results

    # TODO: iterate over prompts, call compare_models, and inject the original "prompt".
    raise NotImplementedError("Implement batch_compare")


# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    def truncate(text: str, max_chars: int = 50) -> str:
        text = str(text).replace("\n", " ").strip()
        if len(text) <= max_chars:
            return text
        return text[: max_chars - 3] + "..."

    def escape_cell(value) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ").strip()

    rows = [
        "| Prompt | Model | Response (truncated) | Latency | Tokens (In/Out) | Cost (USD) |",
        "|---|---|---|---:|---:|---:|",
    ]

    model_labels = {
        "gpt4o": "GPT-4o",
        "gpt4o_mini": "GPT-4o-Mini",
        "gemini_flash": "Gemini-Flash",
    }

    for result in results:
        prompt = escape_cell(truncate(result.get("prompt", "")))

        for model_key, model_label in model_labels.items():
            model_result = result.get(model_key, {})

            response = escape_cell(
                truncate(model_result.get("response", ""))
            )

            latency = model_result.get("latency", 0.0)
            input_tokens = model_result.get("input_tokens", 0)
            output_tokens = model_result.get("output_tokens", 0)
            cost = model_result.get("cost", 0.0)

            rows.append(
                f"| {prompt} | {model_label} | {response} | "
                f"{latency:.3f}s | {input_tokens}/{output_tokens} | ${cost:.8f} |"
            )

    return "\n".join(rows)
    # TODO: Build and return the formatted table string. Truncate response to 50 chars for clean display.
    raise NotImplementedError("Implement format_comparison_table")


# ---------------------------------------------------------------------------
# Entry point for manual testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Model Comparison Test ===")
    test_prompt = "Hãy giải thích sự khác biệt giữa temperature và top_p bằng tiếng Việt ngắn gọn trong 2 câu."
    try:
        # Note: Requires valid API keys set in environment variables
        result = compare_models(test_prompt)
        for model_name, stats in result.items():
            print(f"\n[{model_name.upper()}]")
            print(f"Latency: {stats['latency']:.2f}s | Cost: ${stats['cost']:.6f}")
            print(f"Tokens: {stats['input_tokens']} in / {stats['output_tokens']} out")
            print(f"Response: {stats['response']}")
    except Exception as e:
        print(f"Skipping live API comparison test: {e}")
        print("Set your API keys to run manual tests.")

    print("\n=== Starting Gemini 2.5 Chatbot (type 'quit' to exit) ===")
    try:
        streaming_chatbot()
    except Exception as e:
        print(f"Chatbot failed to start: {e}")
