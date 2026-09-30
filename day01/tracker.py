import json
from pathlib import Path


LOG_FILE = Path(__file__).parent / "token_log.jsonl"


def log_usage(usage):
    record = {
        "input_tokens": usage.prompt_token_count,
        "output_tokens": usage.candidates_token_count,
        "thinking_tokens": usage.thoughts_token_count,
        "total_tokens": usage.total_token_count,
    }

    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")