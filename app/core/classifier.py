import re
from typing import List
from app.models.enums import TaskType
from app.core.logger import logger

class TaskClassifier:
    """
    Analyzes the query and assets to heuristically assign a TaskType.
    As levels progress, add more complex heuristics here before defaulting to UNKNOWN.
    """
    
    @staticmethod
    def classify(query: str, assets: List[str]) -> TaskType:
        query_lower = query.lower()

        # Heuristic -2: Definite integral — "∫" symbol or "definite integral"
        if '∫' in query or 'definite integral' in query_lower:
            logger.info("Classifier: Detected TaskType.DEFINITE_INTEGRAL")
            return TaskType.DEFINITE_INTEGRAL

        # Heuristic -1: Rule engine — "Apply rules in order to input number X:"
        if re.match(r'apply rules in order to input number', query_lower):
            logger.info("Classifier: Detected TaskType.RULE_ENGINE")
            return TaskType.RULE_ENGINE

        # Heuristic 0: List operations — MUST be checked first because "sum" also triggers arithmetic
        # Key signal: query starts with "Numbers:" or contains a comma-separated number list
        if re.search(r'numbers?\s*:', query_lower) or re.search(r'\d+\s*,\s*\d+', query_lower):
            list_op_keywords = ["sum even", "sum odd", "sum all", "sum the", "count even", "count odd", "count",
                                 "maximum", "minimum", "average", "mean", "sort", "product", "multiply",
                                 "largest", "smallest", "greatest", "lowest", "range"]
            if any(kw in query_lower for kw in list_op_keywords) or re.search(r'\bsum\b', query_lower):
                logger.info("Classifier: Detected TaskType.LIST_OPS")
                return TaskType.LIST_OPS

        # Heuristic A: Named entity comparison BEFORE arithmetic — catches "Alice has 5, Bob has 12" style 
        comparison_keywords = ["highest", "lowest", "most", "least", "tallest", "shortest",
                               "oldest", "youngest", "fastest", "slowest", "largest", "smallest",
                               "first", "last", "best", "worst", "more", "fewer", "greater", "scored"]
        has_who = "who" in query_lower
        has_names = len(re.findall(r'\b[A-Z][a-z]+\b', query)) >= 2
        has_numbers = bool(re.search(r'\d+', query_lower))
        if has_who and has_names and has_numbers and any(kw in query_lower for kw in comparison_keywords):
            logger.info("Classifier: Detected TaskType.COMPARISON")
            return TaskType.COMPARISON

        # Heuristic 1: Math operations, numbers, and arithmetic keywords
        math_keywords = ["what is", "sum", "difference", "product", "minus", "times", "divided", "apples", "sells", "half", "third", "remain", "left"]
        if any(kw in query_lower for kw in math_keywords) and re.search(r'\d+', query_lower):
            logger.info("Classifier: Detected TaskType.ARITHMETIC")
            return TaskType.ARITHMETIC
            
        # Heuristic 2: Keywords indicating extraction or parsing
        extract_keywords = ["extract", "find", "email", "date", "phone", "amount", "cost"]
        if any(kw in query_lower for kw in extract_keywords) and not 'what is' in query_lower:
            logger.info("Classifier: Detected TaskType.EXTRACTION")
            return TaskType.EXTRACTION

        # Heuristic 3: Boolean / Classification questions
        classification_keywords = ["is ", "are ", "does ", "can ", "will ", "was ", "were "]
        if any(query_lower.startswith(kw) for kw in classification_keywords) and re.search(r'\d+|prime|even|odd|positive|negative|perfect|factor|multiple|divisible', query_lower):
            logger.info("Classifier: Detected TaskType.CLASSIFICATION")
            return TaskType.CLASSIFICATION
            
        # Heuristic 4: Named entity comparison — "who scored highest", "who is tallest", etc.
        # Key signals: "who" question + multiple capitalized names + a number + comparison word
        comparison_keywords = ["highest", "lowest", "most", "least", "tallest", "shortest",
                               "oldest", "youngest", "fastest", "slowest", "largest", "smallest",
                               "first", "last", "best", "worst", "more", "fewer", "greater", "scored"]
        has_who = "who" in query_lower
        has_names = len(re.findall(r'\b[A-Z][a-z]+\b', query)) >= 2
        has_numbers = bool(re.search(r'\d+', query_lower))
        if has_who and has_names and has_numbers and any(kw in query_lower for kw in comparison_keywords):
            logger.info("Classifier: Detected TaskType.COMPARISON")
            return TaskType.COMPARISON

        # Heuristic 5: Polynomial GCD degree problems
        if 'gcd' in query_lower and 'degree' in query_lower and re.search(r'[a-zA-Z]\s*\(x\)\s*=', query_lower):
            logger.info("Classifier: Detected TaskType.POLY_GCD")
            return TaskType.POLY_GCD

        # Default fallback
        logger.info("Classifier: Detected TaskType.UNKNOWN")
        return TaskType.UNKNOWN
