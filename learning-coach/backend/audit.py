import sys, os
sys.path.insert(0, '.')

print("=" * 50)
print("BACKEND AUDIT")
print("=" * 50)

mods = [
    ('main',          'from main import app'),
    ('config',        'from app.core.config import settings'),
    ('llm',           'from app.core.llm import call_llm, is_llm_available'),
    ('orchestrator',  'from app.mcp.orchestrator import orchestrator'),
    ('tool1_kg',      'from app.mcp.tool1_knowledge_graph import knowledge_graph'),
    ('tool2_profile', 'from app.mcp.tool2_learner_profiling import learner_profiler'),
    ('tool3_diff',    'from app.mcp.tool3_adaptive_difficulty import adaptive_difficulty'),
    ('tool4_qgen',    'from app.mcp.tool4_question_generator import question_generator, QUESTION_BANK'),
    ('tool5_explain', 'from app.mcp.tool5_explanation_generator import explanation_generator'),
    ('tool6_vector',  'from app.mcp.tool6_vector_memory import vector_memory'),
    ('tool7_analytics','from app.mcp.tool7_progress_analytics import progress_analytics'),
    ('api_questions', 'from app.api.questions import router'),
    ('api_answers',   'from app.api.answers import router'),
    ('api_chat',      'from app.api.chat import router'),
    ('api_progress',  'from app.api.progress import router'),
    ('api_analytics', 'from app.api.analytics import router'),
    ('api_lp',        'from app.api.learning_path import router'),
    ('api_upload',    'from app.api.upload import router'),
]

ok = 0
fail = 0
for name, stmt in mods:
    try:
        exec(stmt)
        print(f"  OK   {name}")
        ok += 1
    except Exception as e:
        print(f"  FAIL {name}: {e}")
        fail += 1

print()
print("DATASET CHECK")
from app.mcp.tool4_question_generator import QUESTION_BANK
total = sum(len(v) for v in QUESTION_BANK.values())
print(f"  Questions: {total}")
print(f"  Topics:    {len(QUESTION_BANK)}")
for t, qs in QUESTION_BANK.items():
    print(f"    {t}: {len(qs)}")

print()
print("ENV CHECK")
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    with open(env_path) as f:
        content = f.read()
    has_openai = 'OPENAI_API_KEY' in content
    has_gemini = 'GEMINI_API_KEY' in content
    print(f"  .env exists: YES")
    print(f"  OPENAI_API_KEY present: {has_openai}")
    print(f"  GEMINI_API_KEY present: {has_gemini}")
else:
    print("  .env MISSING!")

print()
print(f"RESULT: {ok} OK, {fail} FAILED")
print("=" * 50)
