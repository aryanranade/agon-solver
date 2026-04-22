import asyncio
import httpx

API_URL = "http://127.0.0.1:8000/v1/answer"

def q(query, expected):
    return {"name": query[:70], "payload": {"query": query, "assets": []}, "expected": expected}

TEST_CASES = [
    # ── Public test case (unicode subscript/superscript) ────────────────────
    q("Compute the definite integral:∫₀³ (9 − x²) dx Output only the integer.", "18"),

    # ── Different bounds, same integrand ────────────────────────────────────
    # ∫₀³ (2x+1) dx = [x²+x]₀³ = 9+3 = 12
    q("Compute the definite integral:∫₀³ (2x + 1) dx Output only the integer.", "12"),
    # ∫₀³ x² dx = [x³/3]₀³ = 9
    q("Compute the definite integral:∫₀³ (x²) dx Output only the integer.", "9"),

    # ── Common polynomial integrals ─────────────────────────────────────────
    # ∫₀² x³ dx = [x⁴/4]₀² = 4
    q("Compute the definite integral:∫₀² (x³) dx Output only the integer.", "4"),
    # ∫₀⁴ (2x + 1) dx = [x²+x]₀⁴ = 16+4 = 20
    q("Compute the definite integral:∫₀⁴ (2x + 1) dx Output only the integer.", "20"),
    # ∫₁³ (x² − 1) dx = [x³/3 - x]₁³ = (9-3)-(1/3-1) = 6+2/3 → not int → skip
    # ∫₀² (3x² + 2x + 1) dx = [x³+x²+x]₀² = 8+4+2 = 14
    q("Compute the definite integral:∫₀² (3x² + 2x + 1) dx Output only the integer.", "14"),
    # ∫₀² (4 − x) dx = [4x - x²/2]₀² = 8-2 = 6
    q("Compute the definite integral:∫₀² (4 − x) dx Output only the integer.", "6"),
    # ∫₁² (x³ − x) dx = [x⁴/4 - x²/2]₁² = (4-2)-(1/4-1/2) = 2+1/4 → not int → skip
    # ∫₀³ (6x − x²) dx = [3x²-x³/3]₀³ = 27-9 = 18
    q("Compute the definite integral:∫₀³ (6x − x²) dx Output only the integer.", "18"),

    # ── Unicode minus in expression ─────────────────────────────────────────
    q("Compute the definite integral:∫₀³ (9 − x²) dx Output only the integer.", "18"),

    # ── Constant integrand ──────────────────────────────────────────────────
    # ∫₀⁵ 3 dx = 15
    q("Compute the definite integral:∫₀⁵ (3) dx Output only the integer.", "15"),

    # ── Higher powers ───────────────────────────────────────────────────────
    # ∫₀² x⁴ dx = [x⁵/5]₀² = 32/5 → not int → skip
    # ∫₀² (x³ + x) dx = [x⁴/4 + x²/2]₀² = 4+2 = 6
    q("Compute the definite integral:∫₀² (x³ + x) dx Output only the integer.", "6"),

    # ── Negative result ─────────────────────────────────────────────────────
    # ∫₀³ (x² − 9) dx = [x³/3 - 9x]₀³ = (9-27) = -18
    q("Compute the definite integral:∫₀³ (x² − 9) dx Output only the integer.", "-18"),

    # ── Large bounds ────────────────────────────────────────────────────────
    # ∫₀¹⁰ 2x dx = [x²]₀¹⁰ = 100
    q("Compute the definite integral:∫₀¹⁰ (2x) dx Output only the integer.", "100"),
]

async def run_tests():
    print(f"=== Level 12 Definite Integral Harness (Total: {len(TEST_CASES)}) ===\n")
    passed = 0
    async with httpx.AsyncClient() as client:
        for i, test in enumerate(TEST_CASES, 1):
            try:
                r = await client.post(API_URL, json=test["payload"], timeout=5.0)
                if r.status_code == 200:
                    output = r.json().get("output", "")
                    ok = output == test["expected"]
                    if ok:
                        passed += 1
                    print(f"{'✅' if ok else '❌'} [{i:02d}] Expected '{test['expected']}', got '{output}' | {test['name'][:60]}")
                else:
                    print(f"❌ [{i:02d}] HTTP {r.status_code}")
            except Exception as e:
                print(f"❌ [{i:02d}] Error: {e}")
    print(f"\n=== Report: {passed}/{len(TEST_CASES)} Passed ===")

if __name__ == "__main__":
    asyncio.run(run_tests())
