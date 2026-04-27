import sys, asyncio
sys.path.insert(0, '.')

async def full_test():
    print("=" * 55)
    print("FULL SYSTEM TEST")
    print("=" * 55)

    # 1. Config check
    from app.core.config import settings
    from app.core.llm import call_llm, is_llm_available
    print(f"\n[CONFIG]")
    print(f"  LLM available : {is_llm_available()}")
    print(f"  Provider      : {settings.LLM_PROVIDER}")
    print(f"  Demo mode     : {settings.DEMO_MODE}")
    print(f"  Gemini key    : {'SET' if settings.GEMINI_API_KEY else 'MISSING'}")
    print(f"  OpenAI key    : {'SET' if settings.OPENAI_API_KEY else 'MISSING'}")

    # 2. LLM live call
    print(f"\n[LLM LIVE TEST]")
    r = await call_llm("You are a tutor. Answer in 1 sentence.", "What is a Python list?")
    if r:
        print(f"  PASS: {r[:120]}")
    else:
        print(f"  FAIL: LLM returned None")

    # 3. Explanation for wrong answer
    print(f"\n[WRONG ANSWER EXPLANATION]")
    from app.mcp.tool5_explanation_generator import explanation_generator
    exp = await explanation_generator.explain(
        "What is a Python list?", "intermediate", "Tuple", "Mutable ordered collection"
    )
    if "tuple" in exp.lower() or "mutable" in exp.lower() or "list" in exp.lower():
        print(f"  PASS (topic-specific): {exp[:120]}")
    else:
        print(f"  WARN (may be generic): {exp[:120]}")

    # 4. Concept explanation
    print(f"\n[CONCEPT EXPLANATION]")
    exp2 = await explanation_generator.explain("What is gradient descent?", "beginner")
    if "gradient" in exp2.lower() or "descent" in exp2.lower() or "loss" in exp2.lower():
        print(f"  PASS (topic-specific): {exp2[:120]}")
    else:
        print(f"  WARN (may be generic): {exp2[:120]}")

    # 5. Chat response
    print(f"\n[CHAT RESPONSE]")
    chat = await explanation_generator.chat_response(
        "what is a lambda function in python", "Python", [], ""
    )
    if "lambda" in chat.lower() or "python" in chat.lower() or "function" in chat.lower():
        print(f"  PASS (topic-specific): {chat[:120]}")
    else:
        print(f"  WARN (may be generic): {chat[:120]}")

    # 6. Dataset
    print(f"\n[DATASET]")
    from app.mcp.tool4_question_generator import QUESTION_BANK
    total = sum(len(v) for v in QUESTION_BANK.values())
    print(f"  Total questions : {total}")
    print(f"  Total topics    : {len(QUESTION_BANK)}")
    new_topics = [t for t in QUESTION_BANK if t in [
        "Generative AI", "LLMs", "Transformers", "Prompt Engineering",
        "Fine-tuning", "RAG", "AI Agents", "Agentic AI", "Multi-Agent Systems"
    ]]
    print(f"  New AI topics   : {new_topics}")

    # 7. Duplicate options check
    print(f"\n[OPTION QUALITY CHECK]")
    dup_issues = 0
    correct_missing = 0
    for topic, qs in QUESTION_BANK.items():
        for q in qs:
            opts = [o.lower().strip() for o in q['options']]
            correct = q['correct_answer'].lower().strip()
            if len(set(opts)) != len(opts):
                dup_issues += 1
            if correct not in opts:
                correct_missing += 1
    print(f"  Duplicate options  : {dup_issues}")
    print(f"  Correct not in opts: {correct_missing}")
    if dup_issues == 0 and correct_missing == 0:
        print(f"  ALL CLEAN")

    # 8. New features
    print(f"\n[NEW FEATURES]")
    try:
        from app.api.revision import router
        print(f"  Revision mode API  : OK")
    except Exception as e:
        print(f"  Revision mode API  : FAIL - {e}")
    try:
        from app.api.leaderboard import router
        print(f"  Leaderboard API    : OK")
    except Exception as e:
        print(f"  Leaderboard API    : FAIL - {e}")
    try:
        from app.mcp.leaderboard import get_leaderboard
        print(f"  Leaderboard module : OK")
    except Exception as e:
        print(f"  Leaderboard module : FAIL - {e}")

    # 9. All backend imports
    print(f"\n[ALL IMPORTS]")
    mods = [
        ("main",          "from main import app"),
        ("orchestrator",  "from app.mcp.orchestrator import orchestrator"),
        ("tool1",         "from app.mcp.tool1_knowledge_graph import knowledge_graph"),
        ("tool2",         "from app.mcp.tool2_learner_profiling import learner_profiler"),
        ("tool3",         "from app.mcp.tool3_adaptive_difficulty import adaptive_difficulty"),
        ("tool4",         "from app.mcp.tool4_question_generator import question_generator"),
        ("tool5",         "from app.mcp.tool5_explanation_generator import explanation_generator"),
        ("tool6",         "from app.mcp.tool6_vector_memory import vector_memory"),
        ("tool7",         "from app.mcp.tool7_progress_analytics import progress_analytics"),
    ]
    all_ok = True
    for name, stmt in mods:
        try:
            exec(stmt)
            print(f"  OK  {name}")
        except Exception as e:
            print(f"  ERR {name}: {e}")
            all_ok = False

    print(f"\n{'=' * 55}")
    print(f"RESULT: {'ALL SYSTEMS GO' if all_ok else 'SOME ISSUES FOUND'}")
    print(f"{'=' * 55}")

asyncio.run(full_test())
