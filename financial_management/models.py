from django.db import models
from django.conf import settings
from core.utils import phone_number_model_validator
from django.utils.translation import gettext_lazy as _
from authentication.models import User, Institution, Country
from core.models import Status


from core.mixins import (
    BasePermissionMixin,
    DeletionMarkerMixin,
    HistoricalDataMixin,
    TimestampMixin,
)

ACCOUNT_TYPE_CHOICES = settings.ACCOUNT_TYPE_CHOICES
TRANSACTION_TYPE_CHOICES = settings.TRANSACTION_TYPE_CHOICES
JOURNAL_TYPES = settings.JOURNAL_TYPES
TYPE_CHOICES = settings.TYPE_CHOICES
FINANCIAL_STATEMENT_TYPE_CHOICES = settings.FINANCIAL_STATEMENT_TYPE_CHOICES
REPORT_TYPE_CHOICES = settings.REPORT_TYPE_CHOICES
RATIO_CATEGORY_CHOICES = settings.RATIO_CATEGORY_CHOICES
RATIO_SOURCE_CHOICES = settings.RATIO_SOURCE_CHOICES
RATIO_FREQUENCY_CHOICES = settings.RATIO_FREQUENCY_CHOICES
ANALYSIS_TYPE_CHOICES = settings.ANALYSIS_TYPE_CHOICES

# Create your models here.
# Accounting Models
class Account(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    """
    Explanation: Represents individual accounts such as assets, liabilities, equity, revenue, and expenses.
    """
    name = models.CharField(_("Name"), max_length=255)
    account_type = models.CharField(_("Type"), choices=ACCOUNT_TYPE_CHOICES, max_length=20)
    account_number = models.CharField(_("Number"), max_length=20)
    description = models.TextField(_("Description"), blank=True, null=True)
    currency = models.CharField(_("Currency"), max_length=3, default='USD')
    country_currency = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='accounts_country_currenct')
    balance = models.DecimalField(_("Balance"), max_digits=15, decimal_places=2, default=0)
    opening_balance = models.DecimalField(_("Opening Balance"), max_digits=15, decimal_places=2, default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    
    


class Journal(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    """
    Explanation: Groups related transactions together, such as sales journal, purchase journal, cash receipts journal, and cash disbursements journal.
    """
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    journal_type = models.CharField(_("Journal Type"), max_length=20, choices=JOURNAL_TYPES)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Journal"
        verbose_name_plural = "Journals"

    def __str__(self):
        return self.name
    

class Attachment(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    name = models.CharField(max_length=255, verbose_name="Name")
    file = models.FileField(upload_to="attachments/", verbose_name="File")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Uploaded At")
    # Add more fields as needed

    def __str__(self):
        return self.name


class Transaction(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    """
    Explanation: Records financial transactions, including debits and credits, with details such as date, amount, description, and reference.
    """
    date = models.DateField(_("Date"))
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)
    description = models.TextField(_("Description"))
    reference_number = models.CharField(_("Reference Number"), max_length=50, blank=True, null=True)
    transaction_type = models.CharField(_("Transaction Type"), max_length=50, choices=TRANSACTION_TYPE_CHOICES)
    debit_account = models.ForeignKey(Account, related_name='debit_transactions', on_delete=models.CASCADE)
    credit_account = models.ForeignKey(Account, related_name='credit_transactions', on_delete=models.CASCADE)
    country_currency = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='transaction_country_currenct')
    attachments = models.ManyToManyField('Attachment', verbose_name=_("Attachments"), blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)  # Foreign key to the Status model
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='transactions')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    


class Ledger(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    """
    Explanation: Summarizes transactions by account, providing balances for each account.
    """
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    debit_amount = models.DecimalField(_("Debit Amount"), max_digits=10, decimal_places=2)
    credit_amount = models.DecimalField(_("Credit Amount"), max_digits=10, decimal_places=2)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    


class TrialBalance(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    """
    Explanation: Lists all accounts and their balances to ensure that debits equal credits.
    """
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    balance = models.DecimalField(_("Balance"), max_digits=10, decimal_places=2)
    debit_balance = models.DecimalField(_("Debit Balance"), max_digits=10, decimal_places=2)
    credit_balance = models.DecimalField(_("Credit Balance"), max_digits=10, decimal_places=2)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    


class FinancialStatement(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    """
    Explanation: Represents financial statements such as the balance sheet, income statement, and cash flow statement.
    """
    # 
    type = models.CharField(_("Type"), max_length=20, choices=FINANCIAL_STATEMENT_TYPE_CHOICES)
    period_covered_start = models.DateField(_("Period Covered Start"), blank=True, null=True)
    period_covered_end = models.DateField(_("Period Covered End"), blank=True, null=True)
    reference_number = models.CharField(_("Reference Number"), max_length=100, blank=True, null=True)
    country_currency = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='financial_statement_country_currenct')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Financial Statement")
        verbose_name_plural = _("Financial Statements")

    def __str__(self):
        return self.get_type_display()
    


# Financial Reporting Models
class Report(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    """
    Explanation: Represents various financial reports generated by the system, such as balance sheet, income statement, cash flow statement, and financial ratios.
    """
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    report_type = models.CharField(_("Type"), max_length=50, choices=REPORT_TYPE_CHOICES)
    date_generated = models.DateField(_("Date Generated"), auto_now_add=True)
    reference_number = models.CharField(_("Reference Number"), max_length=100, blank=True, null=True)
    period_covered_start = models.DateField(_("Period Covered (Start)"), blank=True, null=True)
    period_covered_end = models.DateField(_("Period Covered (End)"), blank=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    
    # Add more fields as needed


class ReportTemplate(
    DeletionMarkerMixin,
    HistoricalDataMixin,
    TimestampMixin
):
    """
    Explanation: Defines the structure and format of financial reports, including headers, footers, sections, and data fields.
    """
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    created_by = models.ForeignKey(
        User,
        verbose_name=_("Created By"),
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    last_updated_at = models.DateTimeField(_("Last Updated At"), auto_now=True)
    is_active = models.BooleanField(_("Is Active?"), default=True)

    # Define fields for headers, footers, sections, and data fields
    header_text = models.TextField(_("Header Text"), blank=True, null=True)
    footer_text = models.TextField(_("Footer Text"), blank=True, null=True)

    # Define fields for sections (e.g., income statement, balance sheet)
    income_statement_section = models.TextField(_("Income Statement Section"), blank=True, null=True)
    balance_sheet_section = models.TextField(_("Balance Sheet Section"), blank=True, null=True)

    # Define fields for data fields (e.g., revenue, expenses)
    revenue_field = models.CharField(_("Revenue Field"), max_length=100, blank=True, null=True)
    expenses_field = models.CharField(_("Expenses Field"), max_length=100, blank=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Report Template")
        verbose_name_plural = _("Report Templates")

    def __str__(self):
        return self.name


class RevenueItem(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class ExpenseItem(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class CashFlow(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    

# Budgeting Models
class Budget(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    """
    Explanation: Represents a financial plan for a specific period, detailing expected revenues, expenses, and cash flows.
    """
    name = models.CharField(_("Name"), max_length=255)
    start_date = models.DateField(_("Start Date"), null=True, blank=True)
    end_date = models.DateField(_("End Date"), null=True, blank=True)
    revenue_items = models.ManyToManyField('RevenueItem', verbose_name=_("Revenue Items"), blank=True)
    expense_items = models.ManyToManyField('ExpenseItem', verbose_name=_("Expense Items"), blank=True)
    cash_flows = models.ManyToManyField('CashFlow', verbose_name=_("Cash Flows"), blank=True)
    notes = models.TextField(_("Notes"), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"


class BudgetVariance(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    """
    Explanation: Tracks the differences between budgeted and actual amounts for revenue and expense categories.
    """
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, verbose_name=_("Budget"))
    revenue_item = models.ForeignKey(RevenueItem, on_delete=models.CASCADE, verbose_name=_("Revenue Item"), null=True, blank=True)
    expense_item = models.ForeignKey(ExpenseItem, on_delete=models.CASCADE, verbose_name=_("Expense Item"), null=True, blank=True)
    actual_amount = models.DecimalField(_("Actual Amount"), max_digits=15, decimal_places=2)
    budgeted_amount = models.DecimalField(_("Budgeted Amount"), max_digits=15, decimal_places=2)
    variance = models.DecimalField(_("Variance"), max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = _("Budget Variance")
        verbose_name_plural = _("Budget Variances")


class BudgetLine(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    """
    Explanation: Represents a line item in the budget, specifying the amount allocated for a particular category or activity.
    """
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = _("Budget Line")
        verbose_name_plural = _("Budget Lines")


class BudgetRevision(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    """
    Explanation: Tracks changes made to the original budget, including additions, modifications, and deletions.
    """
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, verbose_name=_("Budget"))
    revision_date = models.DateField(_("Revision Date"), auto_now_add=True)
    revised_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Revised By"))
    notes = models.TextField(_("Notes"), blank=True)

    class Meta:
        verbose_name = _("Budget Revision")
        verbose_name_plural = _("Budget Revisions")


# Financial Analysis Models
class Ratio(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    """
    Explanation: Represents financial ratios calculated based on financial statement data, such as liquidity ratios, profitability ratios, leverage ratios, and efficiency ratios.
    """
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    formula = models.TextField(_("Formula"))
    category = models.CharField(_("Category"), max_length=100, choices=RATIO_CATEGORY_CHOICES)
    source = models.CharField(_("Source"), max_length=100, choices=RATIO_SOURCE_CHOICES)
    frequency = models.CharField(_("Frequency"), max_length=50, choices=RATIO_FREQUENCY_CHOICES)
    benchmark = models.CharField(_("Benchmark"), max_length=100, blank=True, null=True)
    ideal_range = models.CharField(_("Ideal Range"), max_length=100, blank=True, null=True)

    # name: A CharField representing the name of the financial ratio.
    # description: A TextField providing a description of the financial ratio. It's optional and allows for additional information.
    # formula: A TextField representing the mathematical formula used to calculate the financial ratio.
    # category: A CharField representing the category of the financial ratio, such as liquidity, profitability, leverage, or efficiency. It's defined using choices (RATIO_CATEGORY_CHOICES).
    # source: A CharField representing the source of the financial ratio data, such as financial statements, industry benchmarks, or external sources. It's defined using choices (RATIO_SOURCE_CHOICES).
    # frequency: A CharField representing the frequency at which the financial ratio is calculated or reported, such as quarterly, annually, or monthly. It's defined using choices (RATIO_FREQUENCY_CHOICES).
    # benchmark: A CharField representing the benchmark or target value for the financial ratio, if applicable. It's optional and allows for comparison against a target value.
    # ideal_range: A CharField representing the ideal range or acceptable range of values for the financial ratio, if applicable. It's optional and allows for comparison against a range of values.


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Ratio")
        verbose_name_plural = _("Ratios")


class TrendAnalysis(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    """
    Explanation: Tracks changes in financial data over time, allowing users to analyze trends, patterns, and fluctuations.
    """
    name = models.CharField(_("Name"), max_length=255)
    analysis_type = models.CharField(_("Analysis Type"), max_length=50, choices=ANALYSIS_TYPE_CHOICES)
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"))
    data = models.JSONField(_("Data"))
    notes = models.TextField(_("Notes"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Trend Analysis")
        verbose_name_plural = _("Trend Analyses")


class VarianceAnalysis(DeletionMarkerMixin, HistoricalDataMixin, TimestampMixin):
    """
    Explanation: Compares actual financial performance against budgeted or expected performance to identify differences and analyze causes.
    """
    name = models.CharField(_("Name"), max_length=255)
    analysis_date = models.DateField(_("Analysis Date"))  # Date when the variance analysis was conducted
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)  # Reference to the related budget
    actual_amount = models.DecimalField(_("Actual Amount"), max_digits=10, decimal_places=2)  # Actual financial performance
    expected_amount = models.DecimalField(_("Expected Amount"), max_digits=10, decimal_places=2)  # Budgeted or expected financial performance
    variance_amount = models.DecimalField(_("Variance Amount"), max_digits=10, decimal_places=2)  # Difference between actual and expected amounts
    variance_percentage = models.DecimalField(_("Variance Percentage"), max_digits=5, decimal_places=2)  # Percentage difference between actual and expected amounts
    analysis_notes = models.TextField(_("Analysis Notes"), blank=True)  # Additional notes or explanations for the variance analysis

    # analysis_date: Date when the variance analysis was conducted.
    # budget: ForeignKey to the related budget against which the actual performance is being compared.
    # actual_amount: Actual financial performance for the period being analyzed.
    # expected_amount: Budgeted or expected financial performance for the same period.
    # variance_amount: The absolute difference between the actual and expected amounts.
    # variance_percentage: Percentage difference between the actual and expected amounts, calculated as (actual_amount - expected_amount) / expected_amount * 100.
    # analysis_notes: Additional notes or explanations for the variance analysis, such as the reasons behind significant variances or corrective actions to be taken.

    class Meta:
        verbose_name = _("Variance Analysis")
        verbose_name_plural = _("Variance Analyses")

    






