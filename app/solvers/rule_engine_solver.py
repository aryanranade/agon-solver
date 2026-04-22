import re
from typing import List, Optional
from app.solvers.base import BaseSolver
from app.core.logger import logger

class RuleEngineSolver(BaseSolver):
    @property
    def name(self) -> str:
        return "Deterministic_Level7_RuleEngineSolver"

    @staticmethod
    def _apply_op(value: int, op_text: str) -> int:
        op = op_text.lower().strip().rstrip('.')
        if 'double' in op: return value * 2
        if 'triple' in op: return value * 3
        if 'halve' in op or 'half' in op: return value // 2
        m = re.search(r'add\s+(\d+)', op)
        if m: return value + int(m.group(1))
        m = re.search(r'subtract\s+(\d+)', op)
        if m: return value - int(m.group(1))
        m = re.search(r'multiply\s+by\s+(\d+)', op)
        if m: return value * int(m.group(1))
        m = re.search(r'divide\s+by\s+(\d+)', op)
        if m: return value // int(m.group(1))
        return value

    async def solve(self, query: str, assets: List[str]) -> Optional[str]:
        if not re.search(r'apply rules', query, re.IGNORECASE):
            return None

        # Clean unicode arrows → to ->
        query_clean = query.replace('\u2192', '->').replace('\u201c', '"').replace('\u201d', '"')

        # Step 1: Extract the input number
        n_match = re.search(r'input number\s+(\d+)', query_clean, re.IGNORECASE)
        if not n_match:
            return None
        value = int(n_match.group(1))
        logger.info(f"RuleEngine: Starting with input={value}")

        # Step 2: Split into rule blocks
        rule_blocks = re.split(r'Rule\s+\d+\s*:', query_clean, flags=re.IGNORECASE)
        rule_blocks = [b.strip() for b in rule_blocks if b.strip()]
        rule_blocks = [b for b in rule_blocks if 'input number' not in b.lower()]

        for i, rule_text in enumerate(rule_blocks):
            rule_num = i + 1
            logger.info(f"RuleEngine: Rule {rule_num} value={value} text='{rule_text[:80]}'")

            # Rule type A: IF EVEN → ... IF ODD → ...
            even_match = re.search(r'if even\s*->\s*([^.]+?)\.?\s*if odd', rule_text, re.IGNORECASE)
            odd_match  = re.search(r'if odd\s*->\s*([^.]+?)\.', rule_text, re.IGNORECASE)
            if even_match and odd_match:
                value = self._apply_op(value, even_match.group(1) if value % 2 == 0 else odd_match.group(1))
                logger.info(f"RuleEngine: After Rule {rule_num} (even/odd): value={value}")
                continue

            # Rule type B: IF result > X → op. Otherwise → op.
            r2_match = re.search(
                r'if (?:result|value)?\s*([<>]=?|==)\s*(\d+)\s*->\s*([^.]+?)\.?\s*otherwise\s*->\s*([^.]+?)\.?',
                rule_text, re.IGNORECASE
            )
            if r2_match:
                op_sym, threshold, then_op, else_op = r2_match.groups()
                threshold = int(threshold)
                cond_map = {'>': value > threshold, '<': value < threshold,
                            '>=': value >= threshold, '<=': value <= threshold, '==': value == threshold}
                cond = cond_map.get(op_sym, False)
                value = self._apply_op(value, then_op if cond else else_op)
                logger.info(f"RuleEngine: After Rule {rule_num} (comparison): value={value}")
                continue

            # Rule type C: IF divisible by X → output "WORD". Otherwise → output the number.
            r3_match = re.search(
                r'divisible by\s*(\d+)\s*->\s*output\s*"?(\w+)"?\.?\s*otherwise\s*->\s*output the number',
                rule_text, re.IGNORECASE
            )
            if r3_match:
                divisor, output_word = int(r3_match.group(1)), r3_match.group(2).strip()
                result = output_word if value % divisor == 0 else str(value)
                logger.info(f"RuleEngine: Final output='{result}'")
                return result

        return str(value)
