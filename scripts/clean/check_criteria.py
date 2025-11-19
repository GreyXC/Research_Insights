import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


def load_criteria(path: str) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def match_any(text: str, patterns: List[str]) -> bool:
    if not text or not patterns:
        return False
    txt = text.lower()
    for pat in patterns:
        if pat and pat.lower() in txt:
            return True
    return False


def _normalize_list_field(field: Any) -> str:
    if isinstance(field, list):
        return " ".join(map(str, field)).lower()
    return str(field).lower() if field is not None else ""


def check_criteria(record: Dict[str, Any], criteria: Dict[str, Any]) -> Tuple[bool, str | None]:
    """Return (include_bool, reason_or_None)."""
    if not criteria:
        return True, None

    inc = criteria.get("inclusion", {})
    exc = criteria.get("exclusion", {})

    title = _normalize_list_field(record.get("title", ""))
    abstract = _normalize_list_field(record.get("abstract", ""))
    keywords = _normalize_list_field(record.get("keywords", ""))
    participants = _normalize_list_field(record.get("participants", ""))
    pub_type = _normalize_list_field(record.get("publication_type", ""))
    study_design = _normalize_list_field(record.get("study_design", ""))
    methods = _normalize_list_field(record.get("methods", ""))
    species = _normalize_list_field(record.get("species", ""))
    lang = _normalize_list_field(record.get("language", ""))

    # Year handling
    year_val = None
    y = record.get("year")
    try:
        if isinstance(y, (int, float)):
            year_val = int(y)
        else:
            year_str = str(y)
            if year_str and year_str[:4].isdigit():
                year_val = int(year_str[:4])
    except Exception:
        year_val = None

    # 1) Exclusion checks first
    if exc:
        if match_any(methods, exc.get("methodologies", [])):
            return False, "excl_methodology"
        if match_any(study_design, exc.get("study_designs", [])):
            return False, "excl_study_design"
        if match_any(pub_type, exc.get("publication_types", [])):
            return False, "excl_publication_type"
        if match_any(species, exc.get("species", [])):
            return False, "excl_species"
        # year exclusion
        if "year" in exc and exc["year"].get("before") and year_val is not None:
            try:
                if year_val < int(exc["year"]["before"]):
                    return False, "excl_year_before"
            except Exception:
                pass
        # language exclusion (if specified non-empty, treat as exclusion list)
        if exc.get("languages"):
            langs = [l.lower() for l in exc.get("languages", []) if l]
            if lang and lang in langs:
                return False, "excl_language"

    # 2) Inclusion checks
    if inc:
        # study designs
        allowed_designs = [d.lower() for d in inc.get("study_designs", []) if d]
        if allowed_designs and study_design and study_design not in allowed_designs:
            return False, "not_allowed_study_design"

        # publication type
        allowed_pub = [p.lower() for p in inc.get("publication_types", []) if p]
        if allowed_pub and pub_type and pub_type not in allowed_pub:
            return False, "not_allowed_pub_type"

        # comparisons
        comparisons = inc.get("comparisons", []) or []
        if comparisons and not (match_any(title, comparisons) or match_any(abstract, comparisons) or match_any(keywords, comparisons)):
            return False, "missing_required_comparison"

        # population
        pop_terms = inc.get("population_terms", []) or []
        if pop_terms and not (match_any(participants, pop_terms) or match_any(title, pop_terms) or match_any(abstract, pop_terms)):
            return False, "population_mismatch"

        # year inclusion bounds
        if "year" in inc and year_val is not None:
            y_min = inc["year"].get("min")
            y_max = inc["year"].get("max")
            try:
                if y_min and year_val < int(y_min):
                    return False, "year_too_early"
                if y_max and year_val > int(y_max):
                    return False, "year_too_recent"
            except Exception:
                return False, "invalid_year"
        elif "year" in inc and year_val is None:
            return False, "invalid_year"

        # language inclusion
        allowed_langs = [l.lower() for l in inc.get("languages", []) if l]
        if allowed_langs and lang and lang not in allowed_langs:
            return False, "language_mismatch"

    return True, None
