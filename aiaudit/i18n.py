"""Report text in more than one language.

Each language has a dictionary of text keys. The English text is the
reference. All languages must have the same keys.

Scope: this module translates the fixed text of the Markdown report
(headings, labels, table columns, types and cost levels). It does not
translate the opportunity text from the catalog or the action plan.
"""

LANGUAGES = ("en", "sv")
DEFAULT_LANGUAGE = "en"

TEXT: dict[str, dict[str, str]] = {
    "en": {
        "title": "AI Opportunity Audit: {name}",
        "date": "Date: {date}",
        "industry": "Industry: {industry}",
        "empty_1": "The audit found no clear AI opportunities from the answers.",
        "empty_2": "Do the audit again when the business changes.",
        "summary": "Summary",
        "found": "Opportunities found: {count}",
        "quick_wins": "Quick wins: {count}",
        "time_saved": "Estimated time saved: {hours} hours per week",
        "priority_list": "Priority list",
        "col_opportunity": "Opportunity",
        "col_area": "Area",
        "col_impact": "Impact",
        "col_effort": "Effort",
        "col_priority": "Priority",
        "col_type": "Type",
        "col_hours": "Hours/week",
        "col_cost": "Cost/month",
        "weights_used": "Area weights used for the priority:",
        "details": "Details",
        "example_tools": "Example tools: {tools}",
        "risks": "Risks and checks:",
        "gdpr_notes": "GDPR notes (this opportunity uses personal data):",
        "time_note": (
            "Time estimates are rough. They are for a small business and they\n"
            "change with the fit. Measure the real time before and after."
        ),
        "gdpr_footer": (
            "{count} of {total} opportunities use personal data. Read the\n"
            "GDPR notes for these opportunities before you start. The notes are a\n"
            "checklist. They are not legal advice."
        ),
        "cost_levels": "Cost levels are for the tool cost per month:",
        "next_step": "Next step",
        "next_step_text": "Start with the first quick win. Measure the time it saves for 4 weeks.",
        "quadrant.quick win": "quick win",
        "quadrant.strategic project": "strategic project",
        "quadrant.small improvement": "small improvement",
        "quadrant.not now": "not now",
        "cost.low": "low",
        "cost.medium": "medium",
        "cost.high": "high",
        "cost_text.low": "under 50 EUR",
        "cost_text.medium": "50-300 EUR",
        "cost_text.high": "more than 300 EUR",
    },
    "sv": {
        "title": "AI-möjlighetsanalys: {name}",
        "date": "Datum: {date}",
        "industry": "Bransch: {industry}",
        "empty_1": "Analysen hittade inga tydliga AI-möjligheter i svaren.",
        "empty_2": "Gör analysen igen när verksamheten ändras.",
        "summary": "Sammanfattning",
        "found": "Hittade möjligheter: {count}",
        "quick_wins": "Snabba vinster: {count}",
        "time_saved": "Uppskattad sparad tid: {hours} timmar per vecka",
        "priority_list": "Prioriteringslista",
        "col_opportunity": "Möjlighet",
        "col_area": "Område",
        "col_impact": "Effekt",
        "col_effort": "Insats",
        "col_priority": "Prioritet",
        "col_type": "Typ",
        "col_hours": "Timmar/vecka",
        "col_cost": "Kostnad/månad",
        "weights_used": "Vikter per område som används för prioriteten:",
        "details": "Detaljer",
        "example_tools": "Exempel på verktyg: {tools}",
        "risks": "Risker och kontroller:",
        "gdpr_notes": "GDPR-noteringar (möjligheten använder personuppgifter):",
        "time_note": (
            "Tidsuppskattningarna är grova. De gäller ett litet företag och de\n"
            "ändras med passformen. Mät den verkliga tiden före och efter."
        ),
        "gdpr_footer": (
            "{count} av {total} möjligheter använder personuppgifter. Läs\n"
            "GDPR-noteringarna för dessa möjligheter innan du börjar. Noteringarna\n"
            "är en checklista. De är inte juridisk rådgivning."
        ),
        "cost_levels": "Kostnadsnivåerna gäller verktygets kostnad per månad:",
        "next_step": "Nästa steg",
        "next_step_text": "Börja med den första snabba vinsten. Mät tiden den sparar i 4 veckor.",
        "quadrant.quick win": "snabb vinst",
        "quadrant.strategic project": "strategiskt projekt",
        "quadrant.small improvement": "liten förbättring",
        "quadrant.not now": "inte nu",
        "cost.low": "låg",
        "cost.medium": "medel",
        "cost.high": "hög",
        "cost_text.low": "under 50 EUR",
        "cost_text.medium": "50-300 EUR",
        "cost_text.high": "mer än 300 EUR",
    },
}


def validate_language(lang: str) -> str:
    """Return the language code if it is known.

    Raise ValueError if the language is not in LANGUAGES.
    """
    if lang not in TEXT:
        raise ValueError(f"unknown language '{lang}'. Use one of: {', '.join(LANGUAGES)}")
    return lang


def t(lang: str, key: str, **values: object) -> str:
    """Return the text for the key in the language.

    Put the values into the {name} fields of the text. If the language
    does not have the key, use the English text.
    """
    text = TEXT[validate_language(lang)].get(key, TEXT[DEFAULT_LANGUAGE][key])
    return text.format(**values) if values else text


def lines(lang: str, key: str, **values: object) -> list[str]:
    """Return the text for the key as a list of lines."""
    return t(lang, key, **values).split("\n")
