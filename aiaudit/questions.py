"""Audit questions.

Each question has a key. The catalog uses the same keys as signals.
An answer is yes/no, so a business owner can answer quickly.
An answer can also be a number from 0 to 3 (see aiaudit.scoring).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Question:
    key: str
    text: str


QUESTIONS: tuple[Question, ...] = (
    Question("sells_products", "Do you sell physical or digital products?"),
    Question("many_products", "Do you have more than 50 products or services?"),
    Question("multi_language", "Do you work in more than one language?"),
    Question("support_volume", "Do you get more than 20 customer questions each week?"),
    Question("repeat_questions", "Do customers often ask the same questions?"),
    Question("email_heavy", "Do you spend more than 1 hour each day on email?"),
    Question("posts_social", "Do you post on social media for your business?"),
    Question("small_team", "Do you have fewer than 10 people in the team?"),
    Question("has_leads", "Do you get new sales leads each month?"),
    Question("uses_crm", "Do you use a CRM or a customer list?"),
    Question("writes_quotes", "Do you write quotes or offers for customers?"),
    Question("paper_invoices", "Do you get invoices or receipts as PDF or paper?"),
    Question("manual_bookkeeping", "Do you type financial data by hand?"),
    Question("monthly_reports", "Do you make monthly reports?"),
    Question("holds_stock", "Do you keep stock in a warehouse or at home?"),
    Question("foreign_suppliers", "Do you buy from suppliers in other countries?"),
    Question("many_meetings", "Do you have more than 5 meetings each week?"),
    Question("many_documents", "Do you have many internal documents or procedures?"),
    Question("staff_ask_same", "Do staff often ask the same internal questions?"),
)


def keys() -> set[str]:
    """Return all question keys."""
    return {q.key for q in QUESTIONS}
