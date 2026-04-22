import asyncio
import httpx

API_URL = "http://127.0.0.1:8000/v1/answer"

def l11(p_roots, q_roots):
    def factors(roots):
        return ''.join(f'(x-{r})' for r in roots)
    query = (
        f"Let: p(x) = {factors(p_roots)} "
        f"q(x) = {factors(q_roots)} "
        "Compute the degree of the GCD polynomial gcd(p(x), q(x)) over ℚ. Output only the integer."
    )
    expected = str(len(set(p_roots) & set(q_roots)))
    return query, expected

# Also test with unicode minus (as Agon sends it)
def l11_unicode(p_roots, q_roots):
    def factors(roots):
        return ''.join(f'(x−{r})' for r in roots)
    query = (
        f"Let: p(x) = {factors(p_roots)} "
        f"q(x) = {factors(q_roots)} "
        "Compute the degree of the GCD polynomial gcd(p(x), q(x)) over ℚ. Output only the integer."
    )
    expected = str(len(set(p_roots) & set(q_roots)))
    return query, expected

def make(name, p_roots, q_roots, unicode=False):
    fn = l11_unicode if unicode else l11
    q, e = fn(p_roots, q_roots)
    return {"name": name, "payload": {"query": q, "assets": []}, "expected": e}

TEST_CASES = [
    # Public test case (unicode minus, as Agon sends)
    make("L11-Public: unicode minus degree 4",     [1,2,3,4,5,6], [3,4,5,6,7,8], unicode=True),

    # Same case with ASCII minus
    make("L11: ASCII minus degree 4",              [1,2,3,4,5,6], [3,4,5,6,7,8]),

    # Different overlap sizes
    make("L11: degree 3",                          [1,2,3,4,5],   [3,4,5,6,7]),
    make("L11: degree 2",                          [1,2,3,4],     [3,4,5,6]),
    make("L11: degree 1",                          [1,2,3],       [3,4,5]),
    make("L11: degree 0 (no common roots)",        [1,2,3],       [4,5,6]),
    make("L11: degree 5 (large overlap)",          [1,2,3,4,5,6], [2,3,4,5,6,7]),
    make("L11: degree 6 (identical polys)",        [1,2,3,4,5,6], [1,2,3,4,5,6]),

    # Different root ranges
    make("L11: shifted roots degree 4",            [3,4,5,6,7,8], [5,6,7,8,9,10]),
    make("L11: high numbers degree 3",             [10,11,12,13], [11,12,13,14,15]),
    make("L11: single common root",                [1,2,4,5],     [3,4,6,7]),

    # Unicode minus variants
    make("L11: unicode degree 3",                  [1,2,3,4,5],   [3,4,5,6,7],  unicode=True),
    make("L11: unicode degree 0",                  [1,2,3],       [4,5,6],      unicode=True),
    make("L11: unicode degree 6",                  [1,2,3,4,5,6], [1,2,3,4,5,6], unicode=True),
]

async def run_tests():
    print(f"=== Level 11 Poly GCD Harness (Total: {len(TEST_CASES)}) ===\n")
    passed = 0
    async with httpx.AsyncClient() as client:
        for i, test in enumerate(TEST_CASES, 1):
            try:
                response = await client.post(API_URL, json=test["payload"], timeout=5.0)
                if response.status_code == 200:
                    output = response.json().get("output", "")
                    if output == test["expected"]:
                        print(f"✅ [{i:02d}] {test['name']} -> '{output}'")
                        passed += 1
                    else:
                        print(f"❌ [{i:02d}] {test['name']} -> Expected '{test['expected']}', got '{output}'")
                else:
                    print(f"❌ [{i:02d}] HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ [{i:02d}] Error: {e}")

    print(f"\n=== Report: {passed}/{len(TEST_CASES)} Passed ===")

if __name__ == "__main__":
    asyncio.run(run_tests())
