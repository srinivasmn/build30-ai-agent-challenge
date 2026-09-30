import sys

from llm import ask_gemini


def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py "your prompt"')
        return

    prompt = " ".join(sys.argv[1:])
    answer, usage = ask_gemini(prompt)

    print("\n--- Gemini Response ---")
    print(answer)
    print("\n--- Token Usage ---")
    print(f"Input tokens: {usage.prompt_token_count}")
    print(f"Output tokens: {usage.candidates_token_count}")
    print(f"Thinking tokens: {usage.thoughts_token_count}")
    print(f"Total tokens: {usage.total_token_count}")


if __name__ == "__main__":
    main()