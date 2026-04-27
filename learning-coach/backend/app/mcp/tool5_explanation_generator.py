"""
MCP Tool 5: Explanation Generator
- LLM powered with topic-aware demo fallbacks
- Explains WHY wrong answer is wrong specifically
- Chat responses are context-aware
"""
from typing import Optional, List
from app.core.llm import call_llm, is_llm_available

# ── System prompts ────────────────────────────────────────────────────────────

_SYS_EXPLAIN = """You are a precise AI tutor. Explain the SPECIFIC concept asked.

Level guidelines:
- beginner: real-world analogy + simple language, 3 sentences max
- intermediate: technical explanation with an example, 3-4 sentences
- advanced: deep technical detail with complexity analysis, 4-5 sentences

CRITICAL RULES:
- Answer ONLY about the specific concept in the question
- Do NOT talk about unrelated topics
- Be concrete and specific, not generic
- Return plain text only, no markdown, no bullet points"""

_SYS_WRONG = """You are an AI tutor. A student answered a question incorrectly.
Explain specifically why they were wrong and what the correct answer means.

Be direct and educational in 3-4 sentences:
1. Their answer was wrong because... (specific reason)
2. The correct answer is right because... (clear explanation)
3. Key thing to remember: ... (one insight)

Return plain text only. Be specific to THIS question, not generic."""

_SYS_CHAT = """You are an expert AI tutor for a learning platform.
Current topic: {topic}
Student's weak areas: {weak}

Answer the student's question directly and specifically.
Rules:
- Give accurate, specific answers about the exact topic asked
- Use examples when helpful
- Keep it under 4 sentences
- Do NOT give generic motivational responses
- Do NOT say things like 'Great question!'
- If asked about a concept, explain it clearly
- If asked for a question, confirm you will generate one"""

# ── Topic-aware demo fallbacks (used when LLM unavailable) ───────────────────

def _get_demo_explanation(concept: str, level: str) -> str:
    """Generate a topic-aware fallback explanation based on keywords in the concept."""
    c = concept.lower()

    if "python" in c or "list" in c or "lambda" in c or "generator" in c:
        demos = {
            "beginner": "A Python list is like a shopping list — it holds multiple items in order and you can add, remove, or change items anytime. You create one with square brackets: my_list = [1, 2, 3]. Lists are mutable, meaning you can modify them after creation.",
            "intermediate": "Python lists are dynamic arrays that store ordered, mutable sequences of objects. They support O(1) indexing, O(n) search, and amortized O(1) append. Common operations include slicing (list[1:3]), list comprehensions ([x*2 for x in list]), and methods like append(), pop(), and sort().",
            "advanced": "Python lists are implemented as dynamic arrays with over-allocation to achieve amortized O(1) appends. They store references to objects, not the objects themselves. For performance-critical code, consider numpy arrays (fixed-type, contiguous memory) or collections.deque (O(1) both ends).",
        }
    elif "neural" in c or "deep learning" in c or "backprop" in c:
        demos = {
            "beginner": "A neural network is like a chain of decisions. Each layer looks at the input and passes a transformed version to the next layer. The network learns by comparing its output to the correct answer and adjusting its internal settings to do better next time.",
            "intermediate": "Neural networks consist of layers of neurons where each neuron computes a weighted sum of inputs and applies an activation function. During training, backpropagation computes gradients of the loss with respect to each weight using the chain rule, and gradient descent updates the weights.",
            "advanced": "Neural networks are parameterized function approximators trained via empirical risk minimization. Backpropagation efficiently computes gradients using reverse-mode automatic differentiation. Modern architectures use residual connections, batch normalization, and attention mechanisms to train very deep networks.",
        }
    elif "machine learning" in c or "supervised" in c or "overfitting" in c:
        demos = {
            "beginner": "Machine learning is teaching a computer to learn from examples instead of programming every rule. You show it thousands of examples (like photos of cats and dogs), and it figures out the patterns on its own. Then it can recognize new photos it has never seen before.",
            "intermediate": "Machine learning algorithms learn a mapping from inputs to outputs by minimizing a loss function on training data. Supervised learning uses labeled examples, unsupervised learning finds patterns without labels. Key challenges include overfitting (memorizing training data) and underfitting (too simple to capture patterns).",
            "advanced": "ML models minimize empirical risk on training data as a proxy for true risk on the data distribution. The bias-variance tradeoff governs generalization: high-capacity models have low bias but high variance. Regularization, cross-validation, and ensemble methods are standard techniques to improve generalization.",
        }
    elif "transformer" in c or "attention" in c or "bert" in c or "gpt" in c:
        demos = {
            "beginner": "A Transformer is a type of AI model that reads all words in a sentence at once instead of one by one. It uses 'attention' to figure out which words are most important for understanding each other. This is why models like ChatGPT can understand context so well.",
            "intermediate": "Transformers use self-attention to compute relationships between all token pairs simultaneously, replacing recurrence with parallelism. Each attention head computes Q, K, V matrices and produces weighted sums of values. BERT uses bidirectional encoding while GPT uses causal (left-to-right) decoding.",
            "advanced": "Self-attention has O(n²) complexity in sequence length. Multi-head attention runs h parallel attention functions with projected Q, K, V matrices, concatenating results. Positional encodings (sinusoidal or learned) inject sequence order. Modern variants like Flash Attention reduce memory complexity to O(n).",
        }
    elif "gradient" in c or "optimization" in c or "loss" in c:
        demos = {
            "beginner": "Gradient descent is like finding the lowest point in a hilly landscape while blindfolded. You feel which direction is downhill and take a small step that way. Repeat this many times and you eventually reach the bottom — which means your model has learned well.",
            "intermediate": "Gradient descent minimizes the loss function by computing the gradient (direction of steepest ascent) and updating parameters in the opposite direction: θ = θ - α∇L(θ). Mini-batch SGD uses random subsets for efficiency. Adaptive optimizers like Adam adjust learning rates per parameter.",
            "advanced": "SGD with momentum approximates second-order optimization by accumulating gradient history. Adam combines momentum with RMSProp's adaptive learning rates: m_t = β₁m_{t-1} + (1-β₁)g_t, v_t = β₂v_{t-1} + (1-β₂)g_t². The bias-corrected update is θ -= α * m̂_t / (√v̂_t + ε).",
        }
    elif "algorithm" in c or "complexity" in c or "sort" in c or "search" in c:
        demos = {
            "beginner": "An algorithm is a step-by-step recipe for solving a problem. Binary search is like finding a word in a dictionary — you open the middle, decide which half your word is in, and repeat. This is much faster than checking every word one by one.",
            "intermediate": "Algorithm complexity measures how runtime or memory scales with input size n. Binary search runs in O(log n) by halving the search space each step. Merge sort achieves O(n log n) by recursively dividing and merging. Dynamic programming solves overlapping subproblems in polynomial time by memoization.",
            "advanced": "Time complexity analysis uses asymptotic notation to characterize worst/average/best case behavior. The Master Theorem solves recurrences T(n) = aT(n/b) + f(n). NP-complete problems have no known polynomial algorithm; reductions prove equivalence. Amortized analysis (like for dynamic arrays) averages cost over sequences of operations.",
        }
    elif "rag" in c or "retrieval" in c or "vector" in c or "embedding" in c:
        demos = {
            "beginner": "RAG (Retrieval-Augmented Generation) is like giving an AI a search engine. Instead of relying only on what it memorized during training, it can look up relevant documents first and then answer based on what it found. This makes answers more accurate and up-to-date.",
            "intermediate": "RAG combines a retriever (finds relevant documents using dense embeddings) with a generator (LLM that produces answers). The query is embedded, similar documents are retrieved from a vector database using approximate nearest neighbor search, and the retrieved context is prepended to the prompt.",
            "advanced": "RAG addresses the knowledge cutoff and hallucination problems of parametric LLMs. Dense retrieval uses bi-encoder models to embed queries and documents into a shared space, with FAISS or similar ANN indexes for sub-linear search. Advanced variants include HyDE, FLARE, and self-RAG with adaptive retrieval.",
        }
    else:
        # Generic but still better than neural network text
        demos = {
            "beginner": f"This concept is a fundamental building block in computer science and AI. The key idea is to break down a complex problem into simpler steps that a computer can follow. Understanding this will help you build more advanced skills in the field.",
            "intermediate": f"This is an important concept that appears frequently in practice. It works by applying a specific set of rules or transformations to input data to produce a desired output. Mastering this concept requires understanding both the theory and how to apply it to real problems.",
            "advanced": f"This concept has deep theoretical foundations and practical implications. Its formal definition involves precise mathematical properties that guarantee certain behaviors. Understanding the edge cases and computational complexity is essential for applying it correctly in production systems.",
        }

    return demos.get(level, demos["intermediate"])


def _get_demo_wrong_explanation(question: str, wrong: str, correct: str) -> str:
    """Generate a specific wrong-answer explanation without LLM."""
    return (
        f"'{wrong}' is incorrect because it does not accurately describe what the question is asking about. "
        f"The correct answer is '{correct}' — this is the standard definition used in computer science and AI. "
        f"Remember: when you see this type of question, focus on the precise technical meaning rather than a general guess."
    )


def _get_demo_chat(message: str, topic: str) -> str:
    """Generate a topic-aware chat response without LLM."""
    m = message.lower()
    t = topic.lower()

    if "what is" in m or "explain" in m or "how" in m:
        return (
            f"In {topic}, the key concept you're asking about works by applying specific rules to transform input into output. "
            f"The best way to understand it is through practice — try answering a few questions on this topic and I'll explain any mistakes. "
            f"Would you like me to generate a practice question on {topic}?"
        )
    elif "why" in m and "wrong" in m:
        return (
            f"Your answer was likely wrong because of a subtle distinction in the definition. "
            f"In {topic}, precise terminology matters — similar-sounding concepts often have very different meanings. "
            f"Review the correct answer carefully and try the next question to reinforce the concept."
        )
    elif "question" in m or "practice" in m or "quiz" in m:
        return f"I'll generate a practice question on {topic} for you right now!"
    else:
        return (
            f"That's a good question about {topic}. "
            f"The core idea here is understanding the precise definition and how it applies in practice. "
            f"Try answering a few more questions on this topic — I'll give you detailed explanations for any mistakes."
        )


# ── Main class ────────────────────────────────────────────────────────────────

class ExplanationGenerator:

    async def explain(self, concept: str, level: str = "intermediate",
                      wrong_answer: Optional[str] = None,
                      correct_answer: Optional[str] = None) -> str:
        """Explain a concept or why an answer was wrong."""
        if is_llm_available():
            if wrong_answer and correct_answer:
                prompt = (
                    f"Question: {concept}\n"
                    f"Student's wrong answer: '{wrong_answer}'\n"
                    f"Correct answer: '{correct_answer}'\n\n"
                    f"Explain specifically why '{wrong_answer}' is wrong and why '{correct_answer}' is correct."
                )
                result = await call_llm(_SYS_WRONG, prompt)
            else:
                prompt = f"Explain this at {level} level: {concept}"
                result = await call_llm(_SYS_EXPLAIN, prompt)

            if result:
                return result.strip()

        # LLM unavailable — use topic-aware demo
        if wrong_answer and correct_answer:
            return _get_demo_wrong_explanation(concept, wrong_answer, correct_answer)
        return _get_demo_explanation(concept, level)

    async def chat_response(self, message: str, topic: str,
                            weak_topics: List[str], context_summary: str) -> str:
        """Generate a chat response from the AI tutor."""
        if is_llm_available():
            system = _SYS_CHAT.format(
                topic=topic,
                weak=", ".join(weak_topics) if weak_topics else "none yet"
            )
            result = await call_llm(system, message)
            if result:
                return result.strip()

        return _get_demo_chat(message, topic)


explanation_generator = ExplanationGenerator()
