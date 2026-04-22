import asyncio
import httpx

API_URL = "http://127.0.0.1:8000/v1/answer"

def q(query, expected):
    return {"name": query[:60], "payload": {"query": query, "assets": []}, "expected": expected}

TEST_CASES = [
    # ── Public test case (unicode minus, as Agon sends it) ──────────────────
    q("Let: p(x) = (x−1)(x−2)(x−3)(x−4)(x−5)(x−6) q(x) = (x−3)(x−4)(x−5)(x−6)(x−7)(x−8) Compute the degree of the GCD polynomial gcd(p(x), q(x)) over ℚ. Output only the integer.", "4"),

    # ── ASCII minus variants ────────────────────────────────────────────────
    q("Let: p(x) = (x-1)(x-2)(x-3)(x-4)(x-5)(x-6) q(x) = (x-3)(x-4)(x-5)(x-6)(x-7)(x-8) Compute the degree of the GCD polynomial gcd(p(x), q(x)) over ℚ. Output only the integer.", "4"),

    # ── Different overlap sizes ─────────────────────────────────────────────
    q("Let: p(x) = (x-1)(x-2)(x-3)(x-4)(x-5) q(x) = (x-3)(x-4)(x-5)(x-6)(x-7) Compute the degree of the GCD polynomial gcd(p(x), q(x)) over ℚ. Output only the integer.", "3"),
    q("Let: p(x) = (x-1)(x-2)(x-3)(x-4) q(x) = (x-3)(x-4)(x-5)(x-6) Compute the degree of the GCD polynomial gcd(p(x), q(x)) over ℚ. Output only the integer.", "2"),
    q("Let: p(x) = (x-1)(x-2)(x-3) q(x) = (x-3)(x-4)(x-5) Compute the degree of the GCD polynomial gcd(p(x), q(x)) over ℚ. Output only the integer.", "1"),
    q("Let: p(x) = (x-1)(x-2)(x-3) q(x) = (x-4)(x-5)(x-6) Compute the degree of the GCD polynomial gcd(p(x), q(x)) over ℚ. Output only the integer.", "0"),
    q("Let: p(x) = (x-1)(x-2)(x-3)(x-4)(x-5)(x-6) q(x) = (x-1)(x-2)(x-3)(x-4)(x-5)(x-6) Compute the degree of the GCD polynomial gcd(p(x), q(x)) over ℚ. Output only the integer.", "6"),

    # ── Repeated roots (x-3)^2 ─────────────────────────────────────────────
    q("Let: p(x) = (x-1)(x-2)(x-3)^2 q(x) = (x-3)(x-4)(x-5) Compute the degree of the GCD polynomial gcd(p(x), q(x)) over ℚ. Output only the integer.", "1"),
    q("Let: p(x) = (x-2)^2(x-3)(x-4) q(x) = (x-2)^2(x-3)(x-5) Compute the degree of the GCD polynomial gcd(p(x), q(x)) over ℚ. Output only the integer.", "3"),

    # ── Polynomial with coefficients (2x-6) = 2(x-3) ──────────────────────
    q("Let: p(x) = (x-1)(2x-6)(x-4) q(x) = (x-3)(x-4)(x-5) Compute the degree of the GCD polynomial gcd(p(x), q(x)) over ℚ. Output only the integer.", "2"),

    # ── Unicode minus, different root sets ─────────────────────────────────
    q("Let: p(x) = (x−1)(x−2)(x−3)(x−4)(x−5) q(x) = (x−3)(x−4)(x−5)(x−6)(x−7) Compute the degree of the GCD polynomial gcd(p(x), q(x)) over ℚ. Output only the integer.", "3"),
    q("Let: p(x) = (x−1)(x−2)(x−3) q(x) = (x−4)(x−5)(x−6) Compute the degree of the GCD polynomial gcd(p(x), q(x)) over ℚ. Output only the integer.", "0"),

    # ── Different polynomial names (f, g) ───────────────────────────────────
    q("Let: f(x) = (x-1)(x-2)(x-3)(x-4) g(x) = (x-3)(x-4)(x-5)(x-6) Compute the degree of the GCD polynomial gcd(f(x), g(x)) over ℚ. Output only the integer.", "2"),

    # ── Shifted root ranges ─────────────────────────────────────────────────
    q("Let: p(x) = (x-3)(x-4)(x-5)(x-6)(x-7)(x-8) q(x) = (x-5)(x-6)(x-7)(x-8)(x-9)(x-10) Compute the degree of the GCD polynomial gcd(p(x), q(x)) over ℚ. Output only the integer.", "4"),
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
                    status = "✅" if output == test["expected"] else "❌"
                    if output == test["expected"]:
                        passed += 1
                    print(f"{status} [{i:02d}] Expected '{test['expected']}', got '{output}' | {test['name'][:55]}")
                else:
                    print(f"❌ [{i:02d}] HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ [{i:02d}] Error: {e}")

    print(f"\n=== Report: {passed}/{len(TEST_CASES)} Passed ===")

if __name__ == "__main__":
    asyncio.run(run_tests())
