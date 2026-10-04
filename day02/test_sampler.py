from sampler import (
    greedy_index,
    softmax,
    top_k_filter,
    top_p_filter,
)

logits = [6.0, 3.5, 3.0, 2.0, 1.0]

print("Logits:")
print(logits)

print("\n1. Greedy:")
print(greedy_index(logits))

print("\n2. Softmax:")
probs = softmax(logits, temperature=2.0)
print(probs)
print("Sum:", sum(probs))

print("\n3. Top-K (k=3):")
top_k = top_k_filter(probs, 3)
print(top_k)
print("Sum:", sum(top_k))

print("\n4. Top-P (p=0.8):")
top_p = top_p_filter(probs, 0.8)
print(top_p)
print("Sum:", sum(top_p))