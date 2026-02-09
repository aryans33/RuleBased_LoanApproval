# 🏦 Loan Approval System

A professional, rule-based loan eligibility checker built with Streamlit. This application evaluates loan applications using deterministic decision logic based on debt-to-income ratios and other financial criteria.

---

## ✨ Features

- **Real-time Evaluation** – Instant loan eligibility decisions
- **DTI Calculator** – Automated debt-to-income ratio analysis
- **Multi-factor Assessment** – Considers employment, credit score, and loan-to-income ratio
- **Clean Interface** – Professional, easy-to-use design
- **Rule-based Logic** – Transparent, deterministic decision-making

---

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- pip package manager

### Installation & Run

1. **Navigate to project directory:**
   ```bash
   cd D:\TechBaton\RuleBased_LoanApproval
   ```

2. **Install dependencies:**
   ```bash
   pip install streamlit
   ```

3. **Launch application:**
   ```bash
   streamlit run app.py
   ```
   
   Or use the provided batch file:
   ```bash
   run_chatbot.bat
   ```

4. **Access the application:**
   - Open browser to: `http://localhost:8501`

---

## 📊 How It Works

### Decision Criteria

#### Primary Factor: Debt-to-Income Ratio (DTI)

**Formula:**
```
DTI = (Monthly Debt Payments / Gross Monthly Income) × 100
```

**Thresholds:**
- ✅ **0-36%** → Approved
- ⚠️ **37-43%** → Needs Review
- ❌ **Over 43%** → Declined

#### Additional Requirements

All of the following must be met:

1. **Employment Status**
   - ✅ Full-time OR Self-employed
   - ❌ Part-time, Unemployed, Retired

2. **Credit Score**
   - ✅ Fair or better (650+)
   - ❌ Poor or Very Poor (below 650)

3. **Loan-to-Income Ratio**
   - ✅ Requested amount ≤ 5× annual income
   - ❌ Requested amount > 5× annual income

---

## 💼 Using the Application

### Application Process

Complete the three-section form:

**1. Income & Debt**
- Enter monthly income (before taxes)
- Enter total monthly debt payments

**2. Loan Details**
- Specify requested loan amount

**3. Background**
- Select employment status
- Select credit score range

**4. Submit**
- Click "Submit Application"
- View instant decision with explanation

### Example Scenarios

#### ✅ Approved
```
Monthly Income:    ₹50,000
Monthly Debt:      ₹12,000
Loan Requested:    ₹2,00,000
Employment:        Full-time
Credit Score:      Good (700-749)

DTI: 24% → APPROVED
```

#### ⚠️ Needs Review
```
Monthly Income:    ₹40,000
Monthly Debt:      ₹16,000
Loan Requested:    ₹1,50,000
Employment:        Full-time
Credit Score:      Fair (650-699)

DTI: 40% → CONDITIONAL (Requires additional review)
```

#### ❌ Declined
```
Monthly Income:    ₹35,000
Monthly Debt:      ₹22,000
Loan Requested:    ₹2,00,000
Employment:        Full-time
Credit Score:      Good (700-749)

DTI: 63% → REJECTED (Exceeds 43% threshold)
```

---

## 📁 Project Structure

```
RuleBased_LoanApproval/
├── app.py              # Main application
├── requirements.txt    # Dependencies
├── run_chatbot.bat    # Windows launcher
└── README.md          # Documentation
```

---

## 🛠️ Technical Details

### Technology Stack

- **Framework:** Streamlit
- **Language:** Python 3.7+
- **Styling:** Custom CSS
- **Currency:** Indian Rupees (₹)

### Core Functions

**`calc_dti(monthly_income, monthly_debt)`**
- Calculates debt-to-income ratio
- Returns: DTI as percentage (float)

**`check_eligibility(income, debt, loan_amt, employment_status, credit_range)`**
- Main decision logic
- Returns: Dictionary with decision, DTI, and reason

### Design Features

- Light, professional color scheme
- Responsive two-column layout
- Clean white form containers
- Color-coded decision boxes
- Inline help text
- Real-time validation

---

## 🔒 Privacy & Security

- No data storage or logging
- All processing happens locally
- No external API calls
- Session-based state management
- No user data retention

---

## 📋 Decision Flow

```
User submits form
    ↓
Validate all inputs
    ↓
Calculate DTI
    ↓
Check employment status → If invalid: REJECT
    ↓
Check credit score → If below 650: REJECT
    ↓
Check loan-to-income → If exceeds 5×: REJECT
    ↓
Evaluate DTI:
    • 0-36%: APPROVE
    • 37-43%: CONDITIONAL
    • 44%+: REJECT
```

---

## 🐛 Troubleshooting

**Issue: Streamlit not found**
```bash
pip install --upgrade streamlit
```

**Issue: Port already in use**
```bash
streamlit run app.py --server.port 8502
```

**Issue: Browser doesn't open**
- Manually navigate to `http://localhost:8501`
