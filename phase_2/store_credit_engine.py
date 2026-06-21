"""
Nexus Shopkeeper - Phase 2: Reactive Store Credit Engine
Manages customer credit balances, ledger entries, loyalty bonuses, and micro-loans
with segment-specific interest rates and credit limits.
"""

import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

# Add project root to python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from backend.core.support import atomic_write_json

# ---------------------------------------------------------------------------
# Pydantic Models for Ledger and Loans
# ---------------------------------------------------------------------------

class LedgerEntry(BaseModel):
    entry_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    customer_id: str
    type: str  # "credit", "debit", "loan_disbursement", "loan_payment", "loyalty_bonus", "interest_accrual"
    amount: float
    balance_after: float
    reason: str

class LoanRecord(BaseModel):
    loan_id: str = Field(default_factory=lambda: "LOAN-" + str(uuid.uuid4())[:6].upper())
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    customer_id: str
    principal: float
    interest_rate: float  # Annual interest rate (e.g. 0.05 for 5%)
    interest_accrued: float = 0.0
    total_due: float
    is_active: bool = True
    reason: str


# ---------------------------------------------------------------------------
# Store Credit Engine
# ---------------------------------------------------------------------------

class StoreCreditEngine:
    # Segment-specific configurations
    INTEREST_RATES = {
        "Ultra-Luxury Spender": 0.00,
        "Mid-Tier Consistent": 0.02,
        "High-Value Impulse": 0.05,
        "Essential Bulk Buyer": 0.03,
        "Strict Budget Spender": 0.08,
        "Strategic Deal-Hunter": 0.04,
        "Unknown": 0.05
    }

    CREDIT_LIMITS = {
        "Ultra-Luxury Spender": 5000.00,
        "Mid-Tier Consistent": 1000.00,
        "High-Value Impulse": 500.00,
        "Essential Bulk Buyer": 2000.00,
        "Strict Budget Spender": 200.00,
        "Strategic Deal-Hunter": 750.00,
        "Unknown": 100.00
    }

    LOYALTY_BONUS = {
        "Ultra-Luxury Spender": 50.00,
        "Mid-Tier Consistent": 20.00,
        "High-Value Impulse": 15.00,
        "Essential Bulk Buyer": 10.00,
        "Strict Budget Spender": 5.00,
        "Strategic Deal-Hunter": 10.00,
        "Unknown": 5.00
    }

    def __init__(self, customers_path: Optional[Path] = None, state_dir: Optional[Path] = None):
        self.state_dir = state_dir or (PROJECT_ROOT / "data" / "processed")
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        self.customers_path = customers_path or (PROJECT_ROOT / "data" / "raw" / "customers_segmented.json")
        if not self.customers_path.exists():
            # Fallback to the raw customers file if segmented file isn't created yet
            self.customers_path = PROJECT_ROOT / "data" / "raw" / "customers.json"
            
        self.customers: Dict[str, Dict[str, Any]] = {}
        self.ledger: List[LedgerEntry] = []
        self.loans: Dict[str, List[LoanRecord]] = {}  # customer_id -> list of loans

        self.ledger_file = self.state_dir / "credit_ledger.json"
        self.loans_file = self.state_dir / "active_loans.json"

        # Load initial states
        self.load_customers()
        self.load_ledger()
        self.load_loans()

    def load_customers(self):
        """Loads customers from file."""
        if not self.customers_path.exists():
            print(f"  ⚠ Customers path {self.customers_path} does not exist. Initializing empty customer database.")
            return

        with open(self.customers_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.customers = {c["customer_id"]: c for c in data}

    def save_customers(self):
        """Saves current customer states back to file."""
        if not self.customers_path.exists():
            return
        atomic_write_json(self.customers_path, list(self.customers.values()))

    def load_ledger(self):
        """Loads credit transaction history."""
        if self.ledger_file.exists():
            with open(self.ledger_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.ledger = [LedgerEntry(**entry) for entry in data]
                except Exception as e:
                    print(f"  ⚠ Error reading ledger: {e}. Starting fresh.")
                    self.ledger = []

    def save_ledger(self):
        """Saves credit transaction history."""
        atomic_write_json(self.ledger_file, [entry.dict() for entry in self.ledger])

    def load_loans(self):
        """Loads loans records."""
        if self.loans_file.exists():
            with open(self.loans_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.loans = {}
                    for cid, loan_list in data.items():
                        self.loans[cid] = [LoanRecord(**l) for l in loan_list]
                except Exception as e:
                    print(f"  ⚠ Error reading loans: {e}. Starting fresh.")
                    self.loans = {}

    def save_loans(self):
        """Saves loan records."""
        serialized = {cid: [l.dict() for l in l_list] for cid, l_list in self.loans.items()}
        atomic_write_json(self.loans_file, serialized)

    def get_segment(self, customer_id: str) -> str:
        """Determines customer segment, returning 'Unknown' if not found."""
        cust = self.customers.get(customer_id)
        if not cust:
            return "Unknown"
        # Check both segment_label (from schema) and segment (from kmeans engine output)
        return cust.get("segment_label") or cust.get("segment") or "Unknown"

    def get_balance(self, customer_id: str) -> float:
        """Returns the store credit balance of the customer."""
        cust = self.customers.get(customer_id)
        if not cust:
            raise ValueError(f"Customer {customer_id} not found.")
        return float(cust.get("store_credit_balance", 0.0))

    def add_credit(self, customer_id: str, amount: float, reason: str) -> LedgerEntry:
        """Adds credit to a customer's balance and appends to ledger."""
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if customer_id not in self.customers:
            raise ValueError(f"Customer {customer_id} not found.")

        current = self.get_balance(customer_id)
        new_balance = round(current + amount, 2)
        
        self.customers[customer_id]["store_credit_balance"] = new_balance
        
        entry = LedgerEntry(
            customer_id=customer_id,
            type="credit",
            amount=amount,
            balance_after=new_balance,
            reason=reason
        )
        self.ledger.append(entry)
        
        self.save_customers()
        self.save_ledger()
        return entry

    def deduct_credit(self, customer_id: str, amount: float, reason: str) -> LedgerEntry:
        """Deducts credit from a customer's balance. Balance cannot go below zero."""
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if customer_id not in self.customers:
            raise ValueError(f"Customer {customer_id} not found.")

        current = self.get_balance(customer_id)
        if current < amount:
            raise ValueError(f"Insufficient store credit. Balance: ${current:.2f}, Requested: ${amount:.2f}")

        new_balance = round(current - amount, 2)
        self.customers[customer_id]["store_credit_balance"] = new_balance

        entry = LedgerEntry(
            customer_id=customer_id,
            type="debit",
            amount=amount,
            balance_after=new_balance,
            reason=reason
        )
        self.ledger.append(entry)

        self.save_customers()
        self.save_ledger()
        return entry

    def apply_loyalty_bonus(self, customer_id: str) -> float:
        """Calculates and applies loyalty store credit bonus based on segment."""
        segment = self.get_segment(customer_id)
        bonus = self.LOYALTY_BONUS.get(segment, 5.00)
        self.add_credit(customer_id, bonus, f"Loyalty bonus reward ({segment} tier)")
        return bonus

    def request_credit_loan(self, customer_id: str, amount: float) -> LoanRecord:
        """
        Processes a micro-loan request. If approved (amount falls within 
        segment-specific limit and outstanding debt permits), adds amount to balance.
        """
        if amount <= 0:
            raise ValueError("Loan amount must be positive.")
        if customer_id not in self.customers:
            raise ValueError(f"Customer {customer_id} not found.")

        segment = self.get_segment(customer_id)
        limit = self.CREDIT_LIMITS.get(segment, 100.0)
        rate = self.INTEREST_RATES.get(segment, 0.05)

        # Check total active debt
        active_loans = self.get_active_loans(customer_id)
        current_debt = sum(l.total_due for l in active_loans)
        
        if current_debt + amount > limit:
            raise ValueError(
                f"Loan denied. Credit limit exceeded for {segment}. "
                f"Limit: ${limit:.2f}, Current debt: ${current_debt:.2f}, Requested: ${amount:.2f}"
            )

        # Create loan record
        loan = LoanRecord(
            customer_id=customer_id,
            principal=amount,
            interest_rate=rate,
            total_due=round(amount * (1.0 + rate), 2),
            reason=f"Instant micro-loan approved for {segment}"
        )

        if customer_id not in self.loans:
            self.loans[customer_id] = []
        self.loans[customer_id].append(loan)

        # Disburse funds by adding to store credit
        self.add_credit(
            customer_id, 
            amount, 
            f"Loan disbursement: {loan.loan_id} (${amount:.2f} principal, {rate:.0%} interest)"
        )

        self.save_loans()
        return loan

    def pay_loan(self, customer_id: str, loan_id: str, amount: float) -> float:
        """Pays off an active loan using store credit or external simulation."""
        if customer_id not in self.loans:
            raise ValueError(f"No loans found for customer {customer_id}")

        loan = None
        for l in self.loans[customer_id]:
            if l.loan_id == loan_id and l.is_active:
                loan = l
                break

        if not loan:
            raise ValueError(f"Active loan {loan_id} not found for customer {customer_id}")

        balance = self.get_balance(customer_id)
        payment = min(amount, loan.total_due)
        
        if balance < payment:
            raise ValueError(f"Insufficient store credit to make payment. Balance: ${balance:.2f}, Payment needed: ${payment:.2f}")

        # Deduct payment from store credit
        self.deduct_credit(customer_id, payment, f"Loan payment for {loan_id}")
        
        loan.total_due = round(loan.total_due - payment, 2)
        if loan.total_due <= 0.01:
            loan.total_due = 0.0
            loan.is_active = False
            reason = f"Loan {loan_id} fully repaid."
        else:
            reason = f"Loan payment of ${payment:.2f} received. Remaining: ${loan.total_due:.2f}"

        # Record event in ledger
        entry = LedgerEntry(
            customer_id=customer_id,
            type="loan_payment",
            amount=payment,
            balance_after=self.get_balance(customer_id),
            reason=reason
        )
        self.ledger.append(entry)

        self.save_loans()
        self.save_ledger()
        return payment

    def calculate_interest(self, customer_id: str) -> float:
        """Accumulates monthly interest on all active loans for a customer."""
        active_loans = self.get_active_loans(customer_id)
        total_interest = 0.0

        for loan in active_loans:
            # Simple interest step (accrued once upon trigger)
            interest = round(loan.principal * (loan.interest_rate / 12.0), 2)
            if interest > 0:
                loan.interest_accrued = round(loan.interest_accrued + interest, 2)
                loan.total_due = round(loan.total_due + interest, 2)
                total_interest += interest

                # Log to ledger
                entry = LedgerEntry(
                    customer_id=customer_id,
                    type="interest_accrual",
                    amount=interest,
                    balance_after=self.get_balance(customer_id),
                    reason=f"Interest accrual on loan {loan.loan_id}"
                )
                self.ledger.append(entry)

        if total_interest > 0:
            self.save_loans()
            self.save_ledger()

        return total_interest

    def get_active_loans(self, customer_id: str) -> List[LoanRecord]:
        """Returns list of active loans for a customer."""
        return [l for l in self.loans.get(customer_id, []) if l.is_active]

    def get_ledger(self, customer_id: str) -> List[LedgerEntry]:
        """Returns transaction history for a customer."""
        return [entry for entry in self.ledger if entry.customer_id == customer_id]

    def get_credit_summary(self) -> Dict[str, Any]:
        """Calculates general stats for the dashboard."""
        total_issued = 0.0
        total_outstanding_debt = 0.0
        active_loans_count = 0
        default_risk_value = 0.0
        
        # Calculate totals
        for cid, loan_list in self.loans.items():
            for l in loan_list:
                if l.is_active:
                    total_outstanding_debt += l.total_due
                    active_loans_count += 1
                    segment = self.get_segment(cid)
                    # Budget and deal hunters represent higher default risk mathematically
                    if segment == "Strict Budget Spender":
                        default_risk_value += l.total_due * 0.15
                    elif segment == "Strategic Deal-Hunter":
                        default_risk_value += l.total_due * 0.08
                    else:
                        default_risk_value += l.total_due * 0.02

        # Sum total credit distributed through ledger
        for entry in self.ledger:
            if entry.type in ["credit", "loan_disbursement", "loyalty_bonus"]:
                total_issued += entry.amount

        default_rate = 0.0
        if total_outstanding_debt > 0:
            default_rate = (default_risk_value / total_outstanding_debt) * 100

        total_store_balance = sum(self.get_balance(c) for c in self.customers.keys())

        return {
            "total_credit_issued": round(total_issued, 2),
            "total_outstanding_debt": round(total_outstanding_debt, 2),
            "active_loans_count": active_loans_count,
            "estimated_default_rate_pct": round(default_rate, 2),
            "total_store_balance": round(total_store_balance, 2)
        }


def main():
    print("========================================================================")
    print("  NEXUS SHOPKEEPER - Phase 2 Store Credit Engine Demonstration")
    print("========================================================================")

    engine = StoreCreditEngine()
    print(f"Loaded {len(engine.customers)} customers.")

    if engine.customers:
        sample_cust_id = list(engine.customers.keys())[0]
        sample_cust = engine.customers[sample_cust_id]
        print(f"\nTesting customer: {sample_cust['name']} ({sample_cust_id})")
        print(f"  Segment: {engine.get_segment(sample_cust_id)}")
        print(f"  Initial Balance: ${engine.get_balance(sample_cust_id):.2f}")

        # Test credit addition
        print("\nAdding $50.00 store credit...")
        engine.add_credit(sample_cust_id, 50.00, "Promotional customer reward")
        print(f"  New Balance: ${engine.get_balance(sample_cust_id):.2f}")

        # Test loyalty bonus
        print("\nApplying loyalty bonus...")
        bonus = engine.apply_loyalty_bonus(sample_cust_id)
        print(f"  Applied bonus: ${bonus:.2f}")
        print(f"  New Balance: ${engine.get_balance(sample_cust_id):.2f}")

        # Test loan request
        print("\nRequesting loan of $150.00...")
        try:
            loan = engine.request_credit_loan(sample_cust_id, 150.00)
            print(f"  Loan Approved: {loan.loan_id} (principal=${loan.principal:.2f}, total_due=${loan.total_due:.2f})")
            print(f"  New Balance: ${engine.get_balance(sample_cust_id):.2f}")

            # Test loan payment
            print(f"\nPaying off $50.00 on loan {loan.loan_id}...")
            engine.pay_loan(sample_cust_id, loan.loan_id, 50.00)
            print(f"  New Balance: ${engine.get_balance(sample_cust_id):.2f}")
            print(f"  Remaining Loan Debt: ${engine.get_active_loans(sample_cust_id)[0].total_due:.2f}")

        except Exception as e:
            print(f"  Loan Request Failed: {e}")

        # Test ledger print
        print(f"\nTransaction Ledger for {sample_cust_id}:")
        for idx, entry in enumerate(engine.get_ledger(sample_cust_id)):
            print(f"  {idx+1}. [{entry.timestamp}] {entry.type.upper()}: ${entry.amount:.2f} (Reason: {entry.reason})")

        # Dashboard stats
        print("\nSystem-Wide Store Credit Summary:")
        summary = engine.get_credit_summary()
        for k, v in summary.items():
            print(f"  {k:30} : {v}")


if __name__ == "__main__":
    main()
