import streamlit as st
import time

# Page setup
st.set_page_config(
    page_title="Loan Approval System",
    page_icon="🏦",
    layout="centered"
)

# Styling
st.markdown("""
    <style>
    .main {
        background: #f5f7fa;
    }
    .stApp {
        background: #f5f7fa;
    }
    
    /* Main title and text */
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a1a !important;
    }
    
    p, div, span {
        color: #1a1a1a !important;
    }
    
    /* Make all Streamlit markdown text visible */
    .stMarkdown {
        color: #1a1a1a !important;
    }
    
    /* Sidebar text */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] li {
        color: #1a1a1a !important;
    }
    
    div[data-testid="stForm"] {
        background: white;
        padding: 2.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e1e4e8;
    }
    
    label {
        color: #24292e !important;
        font-weight: 500 !important;
        font-size: 15px !important;
    }
    
    input[type="number"] {
        background: #fafbfc !important;
        color: #24292e !important;
        border: 1px solid #d1d5da !important;
        font-size: 15px !important;
    }
    
    /* Fix dropdown/select styling */
    select {
        background: #ffffff !important;
        color: #24292e !important;
        border: 1px solid #d1d5da !important;
        font-size: 15px !important;
        font-weight: 400 !important;
    }
    
    /* Dropdown options */
    select option {
        background: #ffffff !important;
        color: #24292e !important;
    }
    
    /* Streamlit selectbox widget */
    div[data-baseweb="select"] {
        background: #ffffff !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #24292e !important;
        border: 1px solid #d1d5da !important;
    }
    
    /* Selectbox text */
    div[data-baseweb="select"] span {
        color: #24292e !important;
    }
    
    /* Dropdown menu when opened */
    ul[role="listbox"] {
        background-color: #ffffff !important;
    }
    
    li[role="option"] {
        background-color: #ffffff !important;
        color: #24292e !important;
    }
    
    li[role="option"]:hover {
        background-color: #f6f8fa !important;
    }
    
    /* Submit button with BLACK text */
    .stButton > button,
    button[kind="formSubmit"],
    button[kind="primary"] {
        background-color: #0969da !important;
        color: #000000 !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        border-radius: 6px !important;
    }
    
    .stButton > button:hover,
    button[kind="formSubmit"]:hover {
        background-color: #0550ae !important;
    }
    
    /* Force all button text to be BLACK */
    .stButton > button *,
    button[kind="formSubmit"] *,
    button[kind="primary"] * {
        color: #000000 !important;
    }
    
    .section-divider {
        border-top: 1px solid #e1e4e8;
        margin: 1.5rem 0;
    }
    
    .approved {
        background: #f0f9ff;
        border-left: 4px solid #0969da;
        padding: 1.25rem;
        border-radius: 6px;
        margin: 1rem 0;
    }
    
    .conditional {
        background: #fff8e1;
        border-left: 4px solid #f59e0b;
        padding: 1.25rem;
        border-radius: 6px;
        margin: 1rem 0;
    }
    
    .rejected {
        background: #fff5f5;
        border-left: 4px solid #dc2626;
        padding: 1.25rem;
        border-radius: 6px;
        margin: 1rem 0;
    }
    
    /* Metric labels and values */
    div[data-testid="stMetricLabel"] {
        color: #24292e !important;
    }
    
    div[data-testid="stMetricValue"] {
        color: #1a1a1a !important;
    }
    </style>
""", unsafe_allow_html=True)


def calc_dti(monthly_income, monthly_debt):
    """Calculate debt-to-income ratio"""
    if monthly_income > 0:
        return round((monthly_debt / monthly_income) * 100, 2)
    return 0.0


def check_eligibility(income, debt, loan_amt, employment_status, credit_range):
    """Main eligibility logic"""
    
    dti = calc_dti(income, debt)
    annual_income = income * 12
    
    # Employment check
    if employment_status not in ['Full-time', 'Self-employed']:
        return {
            'decision': 'REJECTED',
            'dti': dti,
            'reason': f'We require applicants to have full-time or self-employed status. Your current status: {employment_status}.'
        }
    
    # Credit check
    if credit_range in ['Poor (600-649)', 'Very Poor (below 600)']:
        return {
            'decision': 'REJECTED',
            'dti': dti,
            'reason': 'Credit score does not meet minimum requirements. We need a score of at least 650.'
        }
    
    # Loan-to-income check
    if loan_amt > (annual_income * 5):
        return {
            'decision': 'REJECTED',
            'dti': dti,
            'reason': f'Requested amount (₹{loan_amt:,.0f}) exceeds maximum of 5x annual income (₹{annual_income:,.0f}).'
        }
    
    # DTI evaluation
    if dti <= 36:
        return {
            'decision': 'APPROVED',
            'dti': dti,
            'reason': f'Your DTI ratio is {dti}%, which meets our standard approval criteria. We\'ll need pay stubs, ID, and bank statements to proceed.'
        }
    elif dti <= 43:
        return {
            'decision': 'CONDITIONAL',
            'dti': dti,
            'reason': f'Your DTI of {dti}% requires additional review. You may need a co-signer or extra documentation. A loan officer will reach out within 2 business days.'
        }
    else:
        return {
            'decision': 'REJECTED',
            'dti': dti,
            'reason': f'DTI ratio of {dti}% exceeds our maximum threshold of 43%. Consider reducing debt or increasing income before reapplying.'
        }


# Header
st.title("🏦 Loan Application")
st.write("Complete the form below to check your eligibility")
st.write("")

# Application form
with st.form("application"):
    
    st.subheader("Income & Debt")
    
    col1, col2 = st.columns(2)
    
    with col1:
        income = st.number_input(
            "Monthly Income (₹)",
            min_value=0.0,
            value=0.0,
            step=1000.0,
            help="Gross monthly income before taxes"
        )
    
    with col2:
        debt = st.number_input(
            "Monthly Debt Payments (₹)",
            min_value=0.0,
            value=0.0,
            step=1000.0,
            help="Total of all monthly debt obligations"
        )
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.subheader("Loan Details")
    
    loan_amount = st.number_input(
        "Amount Requested (₹)",
        min_value=0.0,
        value=0.0,
        step=10000.0
    )
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.subheader("Background")
    
    col3, col4 = st.columns(2)
    
    with col3:
        employment = st.selectbox(
            "Employment Status",
            ['', 'Full-time', 'Part-time', 'Self-employed', 'Unemployed', 'Retired']
        )
    
    with col4:
        credit_score = st.selectbox(
            "Credit Score",
            ['', 'Excellent (750+)', 'Good (700-749)', 'Fair (650-699)', 
             'Poor (600-649)', 'Very Poor (below 600)']
        )
    
    st.write("")
    submit = st.form_submit_button("Submit Application", use_container_width=True)


# Handle submission
if submit:
    
    validation_errors = []
    
    if income <= 0:
        validation_errors.append("Please enter your monthly income")
    if debt < 0:
        validation_errors.append("Debt amount cannot be negative")
    if loan_amount <= 0:
        validation_errors.append("Please enter the loan amount you're requesting")
    if not employment:
        validation_errors.append("Please select your employment status")
    if not credit_score:
        validation_errors.append("Please select your credit score range")
    
    if validation_errors:
        for err in validation_errors:
            st.error(err)
    else:
        # Show summary
        st.write("")
        st.subheader("Application Summary")
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Monthly Income", f"₹{income:,.0f}")
        col_b.metric("Monthly Debt", f"₹{debt:,.0f}")
        col_c.metric("Requested Amount", f"₹{loan_amount:,.0f}")
        
        col_d, col_e = st.columns(2)
        col_d.metric("Employment", employment)
        col_e.metric("DTI Ratio", f"{calc_dti(income, debt)}%")
        
        st.write("")
        
        # Process application
        with st.spinner("Reviewing application..."):
            time.sleep(1.2)
            result = check_eligibility(income, debt, loan_amount, employment, credit_score)
        
        # Show decision
        st.subheader("Decision")
        
        if result['decision'] == 'APPROVED':
            st.markdown(f"""
                <div class="approved">
                    <h4 style="margin:0; color:#0969da;">✓ Approved</h4>
                    <p style="margin:0.5rem 0 0 0; color:#24292e;">{result['reason']}</p>
                </div>
            """, unsafe_allow_html=True)
            st.balloons()
            
        elif result['decision'] == 'CONDITIONAL':
            st.markdown(f"""
                <div class="conditional">
                    <h4 style="margin:0; color:#f59e0b;">⚠ Needs Review</h4>
                    <p style="margin:0.5rem 0 0 0; color:#24292e;">{result['reason']}</p>
                </div>
            """, unsafe_allow_html=True)
            
        else:
            st.markdown(f"""
                <div class="rejected">
                    <h4 style="margin:0; color:#dc2626;">✕ Not Approved</h4>
                    <p style="margin:0.5rem 0 0 0; color:#24292e;">{result['reason']}</p>
                </div>
            """, unsafe_allow_html=True)
        
        if st.button("New Application"):
            st.rerun()


# Sidebar
with st.sidebar:
    st.subheader("How It Works")
    st.write("""
    We evaluate applications based on several factors:
    
    **Debt-to-Income Ratio (DTI)**
    - 36% or less: Approved
    - 37-43%: Needs review
    - Over 43%: Declined
    
    **Other Requirements**
    - Stable employment (full-time or self-employed)
    - Credit score 650+
    - Loan amount within 5x annual income
    """)
    
    st.write("")
    st.subheader("Quick Examples")
    
    with st.expander("Approved"):
        st.write("Income: ₹50,000 | Debt: ₹12,000")
        st.write("DTI: 24% → Approved")
    
    with st.expander("Needs Review"):
        st.write("Income: ₹40,000 | Debt: ₹16,000")
        st.write("DTI: 40% → Review needed")
    
    with st.expander("Declined"):
        st.write("Income: ₹35,000 | Debt: ₹22,000")
        st.write("DTI: 63% → Declined")