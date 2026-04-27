"""
MCP Tool 4: Question Generator
LLM is PRIMARY. Dataset is fallback only.
Fixes: no duplicate options, no repeated questions per session.
"""
import json, random, os, csv
from typing import Optional, Dict, List
from app.core.llm import call_llm, is_llm_available
from app.core.config import settings

QUESTION_BANK: Dict[str, List[Dict]] = {}

# Track asked questions per user per topic to avoid repeats
_asked: Dict[str, set] = {}  # user_id -> set of question strings

def _load_dataset():
    base = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.normpath(os.path.join(base, "../../data/questions.csv")),
        os.path.normpath(os.path.join(base, "../../../data/questions.csv")),
        os.path.normpath(os.path.join(os.getcwd(), "data/questions.csv")),
        os.path.normpath(os.path.join(os.getcwd(), "../data/questions.csv")),
    ]
    path = next((c for c in candidates if os.path.exists(c)), None)
    if not path:
        print(f"Dataset not found")
        return
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            topic = row.get("topic", "General").strip()
            try:
                correct = row["correct_answer"].strip()
                # Build 4 unique options: option_a, option_b, option_c + correct
                # Avoid duplicating correct answer if it already appears in a/b/c
                raw_opts = [
                    row["option_a"].strip(),
                    row["option_b"].strip(),
                    row["option_c"].strip(),
                ]
                # Remove any option that equals correct_answer to avoid duplicates
                unique_opts = [o for o in raw_opts if o.lower() != correct.lower()]
                # Take up to 3 unique wrong options
                unique_opts = list(dict.fromkeys(unique_opts))[:3]
                # Add correct answer
                all_opts = unique_opts + [correct]
                # Pad to 4 if needed
                while len(all_opts) < 4:
                    all_opts.append(f"None of the above ({len(all_opts)})")
                random.shuffle(all_opts)
                entry = {
                    "question": row["question"].strip(),
                    "options": all_opts,
                    "correct_answer": correct,
                    "explanation": row.get("explanation", "").strip(),
                    "difficulty": int(row.get("difficulty", 2)),
                    "topic": topic,
                }
                QUESTION_BANK.setdefault(topic, []).append(entry)
            except Exception:
                continue
    total = sum(len(v) for v in QUESTION_BANK.values())
    print(f"Dataset loaded: {total} questions across {len(QUESTION_BANK)} topics")

_load_dataset()

_SYS = """You are an expert question generator for an AI/ML learning platform.
Generate a multiple-choice question in STRICT JSON format with NO markdown:
{
  "question": "clear question text",
  "options": ["option1", "option2", "option3", "option4"],
  "correct_answer": "must exactly match one of the 4 options",
  "explanation": "2-3 sentence clear explanation of why the answer is correct",
  "difficulty": <integer 1-5>,
  "topic": "topic name"
}
RULES:
- All 4 options must be DIFFERENT from each other
- correct_answer must EXACTLY match one option string
- No duplicate options
- Return ONLY valid JSON, no markdown fences"""

_DIFF_LABELS = {1: "Easy", 2: "Beginner", 3: "Intermediate", 4: "Hard", 5: "Advanced"}


class QuestionGenerator:
    async def generate(self, topic: str, difficulty: int, user_id: str = "default") -> Dict:
        # Try LLM first when available
        if is_llm_available() and not settings.DEMO_MODE:
            q = await self._from_llm(topic, difficulty)
            if q and self._is_valid(q):
                self._mark_asked(user_id, q["question"])
                return q
        # Dataset fallback — pick unasked question
        return self._from_dataset(topic, difficulty, user_id)

    async def _from_llm(self, topic: str, difficulty: int) -> Optional[Dict]:
        label = _DIFF_LABELS.get(difficulty, "Intermediate")
        prompt = f"Generate a {label} level multiple-choice question about: {topic}. Make it specific and educational."
        try:
            raw = await call_llm(_SYS, prompt)
            if not raw:
                return None
            # Strip markdown fences
            raw = raw.strip()
            for fence in ["```json", "```"]:
                raw = raw.replace(fence, "")
            raw = raw.strip()
            data = json.loads(raw)
            data["topic"] = topic
            data["difficulty"] = difficulty
            return data
        except Exception as e:
            print(f"LLM question error: {e}")
            return None

    def _is_valid(self, q: Dict) -> bool:
        opts = q.get("options", [])
        correct = q.get("correct_answer", "")
        if len(opts) != 4:
            return False
        if len(set(o.lower() for o in opts)) != 4:
            return False  # duplicate options
        if not any(o.lower() == correct.lower() for o in opts):
            return False  # correct answer not in options
        return True

    def _from_dataset(self, topic: str, difficulty: int, user_id: str) -> Dict:
        bank = QUESTION_BANK.get(topic, [])
        if not bank:
            for k in QUESTION_BANK:
                if k.lower() in topic.lower() or topic.lower() in k.lower():
                    bank = QUESTION_BANK[k]
                    break
        if not bank:
            bank = [q for qs in QUESTION_BANK.values() for q in qs]
        if not bank:
            return self._fallback(topic, difficulty)

        asked = _asked.get(user_id, set())
        # Filter out already-asked questions
        unasked = [q for q in bank if q["question"] not in asked]
        # If all asked, reset for this user+topic
        if not unasked:
            _asked[user_id] = set()
            unasked = bank

        # Pick by closest difficulty from unasked
        by_diff = sorted(unasked, key=lambda q: abs(q["difficulty"] - difficulty))
        # Pick randomly from top 3 closest difficulty matches
        candidates = by_diff[:min(3, len(by_diff))]
        chosen = random.choice(candidates)

        self._mark_asked(user_id, chosen["question"])
        # Re-shuffle options each time
        result = dict(chosen)
        opts = list(result["options"])
        random.shuffle(opts)
        result["options"] = opts
        result["topic"] = topic
        return result

    def _mark_asked(self, user_id: str, question: str):
        if user_id not in _asked:
            _asked[user_id] = set()
        _asked[user_id].add(question)

    def _fallback(self, topic: str, difficulty: int) -> Dict:
        return {
            "question": f"What is the primary purpose of {topic}?",
            "options": [
                f"To solve problems in {topic} domain",
                f"To replace traditional computing",
                f"To store large amounts of data",
                f"To create visual interfaces"
            ],
            "correct_answer": f"To solve problems in {topic} domain",
            "explanation": f"{topic} is designed to solve specific problems in its domain using specialized techniques.",
            "difficulty": difficulty,
            "topic": topic,
        }


question_generator = QuestionGenerator()
