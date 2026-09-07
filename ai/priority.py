def calculate_priority(size: int, severity_values: list, has_vulnerable_group: bool = False) -> dict:
    """
    Deterministic priority score — no LLM involved here, per the PDF's design principle.
    """
    avg_severity = sum(severity_values) / len(severity_values) if severity_values else 0

    # Weighted scoring — tune these weights as you see real data
    volume_score = min(size, 10) * 2          # caps volume influence at 10 reports
    severity_score = avg_severity * 3
    vulnerability_bonus = 5 if has_vulnerable_group else 0

    total_score = volume_score + severity_score + vulnerability_bonus

    if total_score >= 25:
        level = "high"
    elif total_score >= 12:
        level = "medium"
    else:
        level = "low"

    return {
        "score": round(total_score, 1),
        "level": level,
        "avg_severity": round(avg_severity, 1),
        "report_count": size,
    }