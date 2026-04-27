import sys
sys.path.insert(0, '.')
from app.mcp.tool4_question_generator import QUESTION_BANK

print("Checking for duplicate options...")
issues = 0
for topic, questions in QUESTION_BANK.items():
    for q in questions:
        opts = [o.lower().strip() for o in q['options']]
        correct = q['correct_answer'].lower().strip()
        if len(set(opts)) != len(opts):
            qtext = q['question'][:50]
            print(f"DUPLICATE OPTIONS: {qtext}")
            print(f"  Options: {q['options']}")
            issues += 1
        if correct not in opts:
            qtext = q['question'][:50]
            print(f"CORRECT NOT IN OPTIONS: {qtext}")
            issues += 1
        if opts.count(correct) > 1:
            qtext = q['question'][:50]
            print(f"CORRECT REPEATED: {qtext}")
            issues += 1

total = sum(len(v) for v in QUESTION_BANK.values())
print(f"\nTotal questions: {total}")
print(f"Issues found: {issues}")
if issues == 0:
    print("ALL CLEAN - no duplicate options!")

# Show 3 sample questions
print("\nSample questions:")
for topic in list(QUESTION_BANK.keys())[:2]:
    q = QUESTION_BANK[topic][0]
    print(f"\n  Topic: {topic}")
    print(f"  Q: {q['question']}")
    for i, o in enumerate(q['options']):
        marker = "<-- CORRECT" if o == q['correct_answer'] else ""
        print(f"  {chr(65+i)}: {o} {marker}")
