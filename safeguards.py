import re

HARMFUL_KEYWORDS = [
    "how to make a bomb", "synthesize drugs", "hack into",
    "self-harm", "suicide methods", "illegal weapon",
    "make explosives", "build a gun",
]

def content_filter(text: str) -> tuple[bool, str]:
    lowered = text.lower()
    for phrase in HARMFUL_KEYWORDS:
        if phrase in lowered:
            return False, f"Blocked: harmful keyword '{phrase}'"
    return True, ""

JAILBREAK_PATTERNS = [
    r"ignore (all |previous |prior )?instructions",
    r"pretend you('re| are) (not |no longer )?an? AI",
    r"act as (DAN|an? unfiltered|an? unrestricted)",
    r"bypass (your |all )?(safety|ethical|content) (filters?|guidelines?)",
    r"you (have no|don't have any) (restrictions|rules|limits)",
]

def jailbreak_detector(text: str) -> tuple[bool, str]:
    for pattern in JAILBREAK_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return False, "Blocked: jailbreak attempt detected."
    return True, ""

UNSAFE_OUTPUT_SIGNALS = [
    "step-by-step instructions to harm",
    "here's how to make a weapon",
    "to synthesize illegal",
    "how to build a bomb",
]

def output_safety_check(response: str) -> tuple[bool, str]:
    lowered = response.lower()
    for signal in UNSAFE_OUTPUT_SIGNALS:
        if signal in lowered:
            return False, "Blocked: unsafe content in model output."
    return True, ""

def run_input_guards(user_input: str) -> tuple[bool, str]:
    for check in [content_filter, jailbreak_detector]:
        safe, reason = check(user_input)
        if not safe:
            return False, reason
    return True, ""