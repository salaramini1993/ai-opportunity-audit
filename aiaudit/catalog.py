"""Catalog of AI opportunities.

Each opportunity is one task in a business that AI can make faster,
cheaper or better. The audit asks questions to find which
opportunities apply to a business, then scores them.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Opportunity:
    """One AI opportunity that the audit can recommend."""

    key: str
    area: str
    title: str
    description: str
    # Question keys that show this task exists in the business.
    signals: tuple[str, ...]
    # 1 (low) to 5 (high): how difficult it is to put in place.
    base_effort: int
    # Example tools. These are examples only, not endorsements.
    example_tools: tuple[str, ...] = field(default_factory=tuple)


AREAS = (
    "sales",
    "marketing",
    "customer_support",
    "operations",
    "finance",
    "admin",
)

CATALOG: tuple[Opportunity, ...] = (
    Opportunity(
        key="support_faq_assistant",
        area="customer_support",
        title="FAQ assistant for customer questions",
        description=(
            "Use an AI assistant to answer common customer questions. "
            "Send difficult questions to a person."
        ),
        signals=("support_volume", "repeat_questions"),
        base_effort=2,
        example_tools=("Helpdesk AI add-on", "Chat widget with LLM"),
    ),
    Opportunity(
        key="support_reply_drafts",
        area="customer_support",
        title="Draft replies for support emails",
        description=(
            "Let AI write a first draft of each reply. "
            "A person checks and sends the reply."
        ),
        signals=("support_volume", "email_heavy"),
        base_effort=1,
        example_tools=("Email client AI", "Helpdesk AI add-on"),
    ),
    Opportunity(
        key="product_descriptions",
        area="marketing",
        title="Product descriptions and listings",
        description=(
            "Generate product titles and descriptions from a short "
            "specification. Translate them to more languages."
        ),
        signals=("sells_products", "many_products", "multi_language"),
        base_effort=1,
        example_tools=("LLM with a prompt template",),
    ),
    Opportunity(
        key="social_content",
        area="marketing",
        title="Social media content plan",
        description=(
            "Make a weekly plan of posts and first drafts of the text. "
            "A person approves each post."
        ),
        signals=("posts_social", "small_team"),
        base_effort=1,
        example_tools=("LLM", "Scheduling tool with AI"),
    ),
    Opportunity(
        key="lead_qualification",
        area="sales",
        title="Lead sorting and follow-up",
        description=(
            "Sort new leads by fit and draft follow-up messages. "
            "Record the result in the CRM."
        ),
        signals=("has_leads", "uses_crm"),
        base_effort=3,
        example_tools=("CRM AI features", "Automation platform + LLM"),
    ),
    Opportunity(
        key="quote_generation",
        area="sales",
        title="Faster quotes and offers",
        description=(
            "Make quote documents from a template and the customer "
            "request. A person checks prices."
        ),
        signals=("writes_quotes",),
        base_effort=2,
        example_tools=("Document template + LLM",),
    ),
    Opportunity(
        key="invoice_extraction",
        area="finance",
        title="Read invoices and receipts automatically",
        description=(
            "Extract data from invoices and receipts and put it into "
            "the accounting system."
        ),
        signals=("paper_invoices", "manual_bookkeeping"),
        base_effort=2,
        example_tools=("Accounting OCR", "Document AI"),
    ),
    Opportunity(
        key="cashflow_summary",
        area="finance",
        title="Monthly finance summary",
        description=(
            "Make a short summary of income, costs and trends "
            "from the monthly export."
        ),
        signals=("manual_bookkeeping", "monthly_reports"),
        base_effort=2,
        example_tools=("Spreadsheet AI", "LLM with data export"),
    ),
    Opportunity(
        key="inventory_forecast",
        area="operations",
        title="Stock and reorder forecast",
        description=(
            "Use sales history to estimate when to reorder stock "
            "and how much to order."
        ),
        signals=("holds_stock", "sells_products"),
        base_effort=4,
        example_tools=("Inventory system forecasts", "Spreadsheet model"),
    ),
    Opportunity(
        key="supplier_communication",
        area="operations",
        title="Supplier messages and translation",
        description=(
            "Draft and translate messages to suppliers. "
            "Summarise long supplier threads."
        ),
        signals=("foreign_suppliers", "multi_language"),
        base_effort=1,
        example_tools=("LLM", "Email client AI"),
    ),
    Opportunity(
        key="meeting_notes",
        area="admin",
        title="Meeting notes and action items",
        description=(
            "Record meetings, make a summary and a list of tasks "
            "for each person."
        ),
        signals=("many_meetings",),
        base_effort=1,
        example_tools=("Meeting recorder with AI",),
    ),
    Opportunity(
        key="document_search",
        area="admin",
        title="Search internal documents",
        description=(
            "Let staff ask questions about internal documents, "
            "for example procedures and price lists."
        ),
        signals=("many_documents", "staff_ask_same"),
        base_effort=3,
        example_tools=("Workspace AI search", "RAG assistant"),
    ),
)


def by_key(key: str) -> Opportunity:
    """Return the opportunity with this key."""
    for item in CATALOG:
        if item.key == key:
            return item
    raise KeyError(f"Unknown opportunity: {key}")
