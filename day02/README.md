# Day 02 — Temperature, Sampling & Response Control

Day 2 of the 30 Days AI Agent Build Challenge.

This day focuses on understanding how an LLM selects and generates tokens, how sampling parameters influence generation, and how application code can control the shape and length of model responses.

---

## What I Learned

The main concepts covered in Day 2:

- Logits
- Greedy token selection
- Softmax
- Temperature
- Top-K sampling
- Top-P (nucleus) sampling
- Combining sampling controls
- Model-specific parameter support
- Response formatting
- Stop sequences
- Maximum output tokens
- Finish reasons
- Comparing model behavior

---

## 1. Logits

A language model produces a score for each possible next token.

These scores are called **logits**.

Example:

```text
Paris       6.0
Lyon        3.5
beautiful   3.0
a           2.0
Berlin      1.0
```

A higher logit means the token is more strongly preferred before converting the scores into probabilities.

---

## 2. Greedy Selection

Greedy decoding simply chooses the token with the highest logit.

```python
def greedy_index(logits):
    return max(range(len(logits)), key=lambda i: logits[i])
```

For:

```text
[6.0, 3.5, 3.0, 2.0, 1.0]
```

the highest value is `6.0`, so the first token is selected.

This is deterministic.

---

## 3. Softmax

Softmax converts logits into probabilities.

The probabilities add up to approximately 1.

For example:

```text
Paris       0.579
Lyon        0.166
beautiful   0.129
a           0.078
Berlin      0.048
```

The model can then use these probabilities when selecting the next token.

---

## 4. Temperature

Temperature changes the shape of the probability distribution.

### Low temperature

Example:

```text
temperature = 0.2
```

The highest-probability token becomes strongly dominant.

In the toy experiment:

```text
Paris ≈ 1.000
```

This makes generation more predictable.

### Normal temperature

```text
temperature = 1.0
```

The probability distribution is less concentrated.

### Higher temperature

```text
temperature = 2.0
```

The probability distribution becomes flatter, allowing lower-ranked tokens to have a greater chance of being selected.

The important point is:

> Temperature changes the probability distribution used during token selection. It is not simply a "creativity switch."

---

## 5. Top-K Sampling

Top-K limits the candidate tokens to the K highest-probability tokens.

For example:

```text
Top-K = 3
```

means only the three highest-probability tokens remain candidates.

The remaining probabilities are set to zero and the probabilities are normalized again.

---

## 6. Top-P Sampling

Top-P, also called nucleus sampling, keeps the smallest group of highest-probability tokens whose cumulative probability reaches the specified threshold.

For example:

```text
Top-P = 0.90
```

keeps enough of the highest-probability tokens to reach approximately 90% cumulative probability.

This means the number of candidate tokens can change depending on the probability distribution.

---

## 7. Combining Sampling Controls

The `pick_token()` function combines the sampling steps:

```text
Logits
   |
   v
Temperature
   |
   v
Softmax probabilities
   |
   v
Top-K filtering
   |
   v
Top-P filtering
   |
   v
Random selection
   |
   v
Selected token
```

When:

```text
temperature = 0
```

the implementation uses greedy selection instead of sampling.

---

## 8. Real LLM Experiment

The toy sampling implementation was then connected to a real Gemini model.

The project uses:

```text
sampler.py
    |
    v
settings.py
    |
    v
llm.py
    |
    v
Gemini API
    |
    v
compare.py
```

The experiment compares different presets:

```text
precise
balanced
wild
```

The purpose is to observe whether changing generation settings produces visibly different model behavior.

---

## 9. Model-Specific Parameter Support

An important observation from the real-model experiment was that not every model necessarily supports every generation parameter.

For example, for one of the tested models:

```text
temperature -> dropped
top_p       -> dropped
```

The application therefore checks the model's declared capabilities before sending settings.

This leads to an important practical lesson:

> A parameter configured in the application does not necessarily mean that the selected model supports or applies that parameter.

The `--force` option was also used to experiment with sending settings even when they were not declared as supported.

---

## 10. Response Formatting

`formats.py` demonstrates three different response shapes:

### One line

```text
Answer in one short sentence.
```

### Bullets

```text
- item 1
- item 2
- item 3
```

### JSON

```json
{
  "name": "...",
  "reason": "..."
}
```

The `shape()` function combines the question with the requested output format.

The JSON response is then validated using Python's `json.loads()`.

This demonstrates an important application pattern:

> Prompting asks the LLM for a particular structure; application code should validate the response before relying on it.

---

## 11. Stop Sequences

A stop sequence tells the model when to stop generating.

The experiment used:

```text
stop_sequences = ("3.",)
```

with:

```text
List 5 fruits as a numbered list.
```

The response stopped before item 3.

The result reported:

```text
finish STOP
```

---

## 12. Maximum Output Tokens

The experiment deliberately used a small output limit:

```text
max_output_tokens = 12
```

The prompt asked:

```text
Explain what an API is in three sentences.
```

The response was intentionally cut short and reported:

```text
finish MAX_TOKENS
```

This demonstrates the difference between:

```text
STOP
```

and:

```text
MAX_TOKENS
```

A `MAX_TOKENS` finish indicates that generation was constrained by the configured output-token limit.

---

## Project Structure

```text
day02/
|
├── compare.py
├── formats.py
├── lab.py
├── llm.py
├── requirements.txt
├── sampler.py
├── settings.py
├── shape.py
├── test_sampler.py
└── readme.md
```

The `.env` file contains the API key and is intentionally excluded from Git.

---

## Running the Experiments

Run the local sampling test:

```powershell
python test_sampler.py
```

Run the local sampling experiment:

```powershell
python lab.py
```

Compare model behavior:

```powershell
python compare.py --model gemma
```

Test the `new` model:

```powershell
python compare.py --model new
```

Experiment with forced settings:

```powershell
python compare.py --model new --force
```

Test response formatting, stop sequences and maximum output tokens:

```powershell
python shape.py
```

---

## Key Takeaways

1. LLMs generate tokens based on probability distributions derived from model scores.
2. Softmax converts logits into probabilities.
3. Temperature changes the probability distribution.
4. Top-K limits the candidate set to the highest-probability tokens.
5. Top-P keeps the smallest probability set reaching the chosen cumulative threshold.
6. Different models can support different generation parameters.
7. Output formatting can be controlled through prompt instructions.
8. LLM output should be validated when an application expects a specific structure.
9. Stop sequences and maximum output tokens provide different ways to control generation.
10. Finish reasons provide useful information about why generation stopped.

---

## Day 2 Outcome

The main learning from Day 2 was moving from a simple idea of:

```text
Prompt -> Response
```

to understanding the generation process more clearly:

```text
Prompt
  |
  v
Model scores / logits
  |
  v
Sampling configuration
  |
  v
Token selection
  |
  v
Generated response
  |
  v
Output constraints / validation
```

This provides a foundation for understanding how LLM APIs behave before moving into more advanced AI-agent concepts.
