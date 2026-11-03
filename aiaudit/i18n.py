"""Report text in more than one language.

Each language has a dictionary of text keys. The English text is the
reference. All languages must have the same keys.

Scope: this module translates the fixed text of the Markdown and HTML
reports (headings, labels, table columns, types, cost levels and the
30/60/90-day action plan). Keys that start with "chart_" are for the
chart section of the HTML report, including the labels inside the chart. The title, the description, the risks and
the GDPR notes of each opportunity are translated in the catalog file,
in the "translations" field of each opportunity.

Persian ("fa") has the fixed text of the reports. The catalog has the
Persian title, description, risks and GDPR notes of each opportunity.
Persian is written from right to left. The numbers in the Persian text are Western
digits, because the scores and the hours use Western digits.

Keys that start with "plan." are for the action plan. Text with more
than one line uses "\n" between the lines.
"""

LANGUAGES = ("en", "sv", "fa")
DEFAULT_LANGUAGE = "en"
# Languages that are written from right to left.
RTL_LANGUAGES = ("fa",)

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
        "chart_heading": "Impact and effort",
        "chart_intro": (
            "Each circle is one opportunity. The number is the position in the "
            "priority list. Start with the circles in the top-left area."
        ),
        "chart_svg_title": "Impact and effort of each opportunity",
        "chart_quick_wins": "Quick wins",
        "chart_strategic": "Strategic projects",
        "chart_small": "Small improvements",
        "chart_not_now": "Not now",
        "chart_x_axis": "Effort (1 = low)",
        "chart_y_axis": "Impact (5 = high)",
        "chart_point": "{number}. {title} (impact {impact}, effort {effort})",
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
        "plan.heading": "30/60/90-day action plan",
        "plan.goal": "Goal: {goal}",
        "plan.steps": "Steps:",
        "plan.none": "No new opportunity. Continue the work from before.",
        "plan.1.title": "Days 1-30",
        "plan.1.goal": "Start one opportunity and measure the result.",
        "plan.1.steps": (
            "Measure the time the task takes now, for 1 week.\n"
            "Select a tool and test it on real work.\n"
            "Write down the checks a person must do on the AI output."
        ),
        "plan.2.title": "Days 31-60",
        "plan.2.goal": "Keep what works and add small changes.",
        "plan.2.steps": (
            "Compare the time before and after the first change.\n"
            "Stop the change if it does not save time or quality drops.\n"
            "Start the next opportunities in the list."
        ),
        "plan.3.title": "Days 61-90",
        "plan.3.goal": "Plan a larger project.",
        "plan.3.steps": (
            "Write a short plan with the goal, the cost and the owner.\n"
            "Do a small pilot before you change the full process.\n"
            "Do the audit again to find new opportunities."
        ),
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
        "chart_heading": "Effekt och insats",
        "chart_intro": (
            "Varje cirkel är en möjlighet. Numret är platsen i "
            "prioriteringslistan. Börja med cirklarna uppe till vänster."
        ),
        "chart_svg_title": "Effekt och insats för varje möjlighet",
        "chart_quick_wins": "Snabba vinster",
        "chart_strategic": "Strategiska projekt",
        "chart_small": "Små förbättringar",
        "chart_not_now": "Inte nu",
        "chart_x_axis": "Insats (1 = låg)",
        "chart_y_axis": "Effekt (5 = hög)",
        "chart_point": "{number}. {title} (effekt {impact}, insats {effort})",
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
        "plan.heading": "Handlingsplan för 30/60/90 dagar",
        "plan.goal": "Mål: {goal}",
        "plan.steps": "Steg:",
        "plan.none": "Ingen ny möjlighet. Fortsätt med arbetet från tidigare.",
        "plan.1.title": "Dag 1-30",
        "plan.1.goal": "Starta en möjlighet och mät resultatet.",
        "plan.1.steps": (
            "Mät hur lång tid uppgiften tar nu, under 1 vecka.\n"
            "Välj ett verktyg och testa det på riktigt arbete.\n"
            "Skriv ner de kontroller en person måste göra av AI-resultatet."
        ),
        "plan.2.title": "Dag 31-60",
        "plan.2.goal": "Behåll det som fungerar och lägg till små ändringar.",
        "plan.2.steps": (
            "Jämför tiden före och efter den första ändringen.\n"
            "Stoppa ändringen om den inte sparar tid eller om kvaliteten sjunker.\n"
            "Starta nästa möjligheter i listan."
        ),
        "plan.3.title": "Dag 61-90",
        "plan.3.goal": "Planera ett större projekt.",
        "plan.3.steps": (
            "Skriv en kort plan med mål, kostnad och ansvarig.\n"
            "Gör ett litet pilotprojekt innan du ändrar hela processen.\n"
            "Gör analysen igen för att hitta nya möjligheter."
        ),
    },
    "fa": {
        "title": "ممیزی فرصت‌های هوش مصنوعی: {name}",
        "date": "تاریخ: {date}",
        "industry": "صنعت: {industry}",
        "empty_1": "ممیزی در پاسخ‌ها هیچ فرصت روشنی برای هوش مصنوعی پیدا نکرد.",
        "empty_2": "وقتی کسب‌وکار تغییر کرد، ممیزی را دوباره انجام دهید.",
        "summary": "خلاصه",
        "found": "فرصت‌های پیداشده: {count}",
        "quick_wins": "بردهای سریع: {count}",
        "time_saved": "زمان صرفه‌جویی‌شده (تخمینی): {hours} ساعت در هفته",
        "priority_list": "فهرست اولویت‌ها",
        "col_opportunity": "فرصت",
        "col_area": "حوزه",
        "col_impact": "اثر",
        "col_effort": "تلاش",
        "col_priority": "اولویت",
        "col_type": "نوع",
        "col_hours": "ساعت/هفته",
        "col_cost": "هزینه/ماه",
        "weights_used": "وزن حوزه‌ها که برای اولویت به کار رفت:",
        "chart_heading": "اثر و تلاش",
        "chart_intro": (
            "هر دایره یک فرصت است. عدد، جایگاه آن در فهرست اولویت‌ها است. "
            "از دایره‌های بالا و چپ شروع کنید."
        ),
        "chart_svg_title": "اثر و تلاش هر فرصت",
        "chart_quick_wins": "بردهای سریع",
        "chart_strategic": "پروژه‌های راهبردی",
        "chart_small": "بهبودهای کوچک",
        "chart_not_now": "فعلاً نه",
        "chart_x_axis": "تلاش (1 = کم)",
        "chart_y_axis": "اثر (5 = زیاد)",
        "chart_point": "{number}. {title} (اثر {impact}، تلاش {effort})",
        "details": "جزئیات",
        "example_tools": "نمونه ابزارها: {tools}",
        "risks": "ریسک‌ها و بررسی‌ها:",
        "gdpr_notes": "یادداشت‌های GDPR (این فرصت از داده‌های شخصی استفاده می‌کند):",
        "time_note": (
            "تخمین‌های زمان تقریبی هستند. آن‌ها برای یک کسب‌وکار کوچک هستند و\n"
            "با میزان تناسب تغییر می‌کنند. زمان واقعی را قبل و بعد اندازه بگیرید."
        ),
        "gdpr_footer": (
            "{count} فرصت از {total} فرصت از داده‌های شخصی استفاده می‌کنند.\n"
            "پیش از شروع، یادداشت‌های GDPR این فرصت‌ها را بخوانید. این یادداشت‌ها\n"
            "یک چک‌لیست هستند. آن‌ها مشاوره حقوقی نیستند."
        ),
        "cost_levels": "سطح‌های هزینه برای هزینه ماهانه ابزار هستند:",
        "next_step": "گام بعدی",
        "next_step_text": "با اولین برد سریع شروع کنید. زمانی را که صرفه‌جویی می‌کند 4 هفته اندازه بگیرید.",
        "quadrant.quick win": "برد سریع",
        "quadrant.strategic project": "پروژه راهبردی",
        "quadrant.small improvement": "بهبود کوچک",
        "quadrant.not now": "فعلاً نه",
        "cost.low": "کم",
        "cost.medium": "متوسط",
        "cost.high": "زیاد",
        "cost_text.low": "کمتر از 50 یورو",
        "cost_text.medium": "50 تا 300 یورو",
        "cost_text.high": "بیشتر از 300 یورو",
        "plan.heading": "برنامه اقدام 30/60/90 روزه",
        "plan.goal": "هدف: {goal}",
        "plan.steps": "گام‌ها:",
        "plan.none": "فرصت جدیدی نیست. کار قبلی را ادامه دهید.",
        "plan.1.title": "روزهای 1 تا 30",
        "plan.1.goal": "یک فرصت را شروع کنید و نتیجه را اندازه بگیرید.",
        "plan.1.steps": (
            "زمانی را که کار الان می‌گیرد، به مدت 1 هفته اندازه بگیرید.\n"
            "یک ابزار انتخاب کنید و آن را روی کار واقعی آزمایش کنید.\n"
            "بررسی‌هایی را که یک نفر باید روی خروجی هوش مصنوعی انجام دهد، بنویسید."
        ),
        "plan.2.title": "روزهای 31 تا 60",
        "plan.2.goal": "آنچه کار می‌کند را نگه دارید و تغییرهای کوچک اضافه کنید.",
        "plan.2.steps": (
            "زمان قبل و بعد از اولین تغییر را مقایسه کنید.\n"
            "اگر تغییر زمان صرفه‌جویی نمی‌کند یا کیفیت پایین می‌آید، آن را متوقف کنید.\n"
            "فرصت‌های بعدی فهرست را شروع کنید."
        ),
        "plan.3.title": "روزهای 61 تا 90",
        "plan.3.goal": "یک پروژه بزرگ‌تر را برنامه‌ریزی کنید.",
        "plan.3.steps": (
            "یک برنامه کوتاه با هدف، هزینه و مسئول بنویسید.\n"
            "پیش از تغییر کل فرایند، یک آزمایش کوچک انجام دهید.\n"
            "ممیزی را دوباره انجام دهید تا فرصت‌های جدید پیدا کنید."
        ),
    },
}


def validate_language(lang: str) -> str:
    """Return the language code if it is known.

    Raise ValueError if the language is not in LANGUAGES.
    """
    if lang not in TEXT:
        raise ValueError(f"unknown language '{lang}'. Use one of: {', '.join(LANGUAGES)}")
    return lang


def text_direction(lang: str) -> str:
    """Return the text direction of the language: "rtl" or "ltr".

    Use the value for the HTML dir attribute.
    """
    return "rtl" if validate_language(lang) in RTL_LANGUAGES else "ltr"


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
