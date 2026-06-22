// ========================================
// Loan Eligibility Agent - JavaScript
// ========================================

// Configuration
const CONFIG = {
  API_URL: 'http://localhost:8000',
  ANNUAL_RATE: 10.5, // Default annual interest rate
};

// Indian Cities List
const INDIAN_CITIES = [
  'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata',
  'Pune', 'Ahmedabad', 'Jaipur', 'Kochi', 'Coimbatore', 'Madurai',
  'Trivandrum', 'Vijayawada', 'Visakhapatnam', 'Lucknow', 'Chandigarh',
  'Indore', 'Bhopal', 'Nagpur', 'Surat', 'Vadodara', 'Goa', 'Dehradun',
  'Siliguri', 'Ranchi', 'Patna', 'Ludhiana', 'Amritsar', 'Varanasi',
  'Guwahati', 'Nashik', 'Jabalpur', 'Aurangabad', 'Srinagar', 'Kota',
  'Udaipur', 'Agra', 'Kanpur', 'Allahabad', 'Ghaziabad', 'Noida',
  'Gurgaon', 'Faridabad', 'Durgapur', 'Asansol', 'Thiruvananthapuram'
];

const LOAN_TYPES = [
  { value: 'Personal Loan', label: 'Personal Loan', icon: '💳' },
  { value: 'Home Loan', label: 'Home Loan', icon: '🏠' },
  { value: 'Car Loan', label: 'Car Loan', icon: '🚗' },
  { value: 'Education Loan', label: 'Education Loan', icon: '🎓' },
  { value: 'Business Loan', label: 'Business Loan', icon: '💼' }
];

const EMPLOYMENT_TYPES = ['SALARIED', 'SELF_EMPLOYED', 'FREELANCE', 'UNEMPLOYED'];

// ========================================
// Initialization
// ========================================

document.addEventListener('DOMContentLoaded', function() {
  initializeForm();
  setupEventListeners();
  loadFormData();
});

function initializeForm() {
  populateCities();
  populateLoanTypes();
  populateEmploymentTypes();
}

function populateCities() {
  const citySelect = document.getElementById('city');
  if (!citySelect) return;

  INDIAN_CITIES.sort().forEach(city => {
    const option = document.createElement('option');
    option.value = city;
    option.textContent = city;
    citySelect.appendChild(option);
  });
}

function populateLoanTypes() {
  const loanTypeSelect = document.getElementById('loanType');
  if (!loanTypeSelect) return;

  LOAN_TYPES.forEach(loan => {
    const option = document.createElement('option');
    option.value = loan.value;
    option.textContent = `${loan.icon} ${loan.label}`;
    loanTypeSelect.appendChild(option);
  });
}

function populateEmploymentTypes() {
  const employmentSelect = document.getElementById('employmentType');
  if (!employmentSelect) return;

  EMPLOYMENT_TYPES.forEach(type => {
    const option = document.createElement('option');
    option.value = type;
    option.textContent = type.replace(/_/g, ' ');
    employmentSelect.appendChild(option);
  });
}

// ========================================
// Event Listeners
// ========================================

function setupEventListeners() {
  const form = document.getElementById('loanForm');
  if (form) {
    form.addEventListener('submit', handleFormSubmit);
  }

  // Real-time calculations
  const monthlyIncomeInput = document.getElementById('monthlyIncome');
  const existingEmiInput = document.getElementById('existingEmi');
  const loanAmountInput = document.getElementById('loanAmount');
  const tenureInput = document.getElementById('tenure');

  if (monthlyIncomeInput) monthlyIncomeInput.addEventListener('input', updateStats);
  if (existingEmiInput) existingEmiInput.addEventListener('input', updateStats);
  if (loanAmountInput) loanAmountInput.addEventListener('input', updateStats);
  if (tenureInput) tenureInput.addEventListener('input', updateStats);

  // Reset button
  const resetBtn = document.getElementById('resetBtn');
  if (resetBtn) {
    resetBtn.addEventListener('click', resetForm);
  }

  // Apply Again button
  const applyAgainBtn = document.getElementById('applyAgainBtn');
  if (applyAgainBtn) {
    applyAgainBtn.addEventListener('click', applyAgain);
  }
}

// ========================================
// Form Validation
// ========================================

function validateForm() {
  const errors = {};

  const fields = {
    applicantName: { value: document.getElementById('applicantName')?.value || '', min: 2, type: 'text' },
    age: { value: parseInt(document.getElementById('age')?.value || 0), min: 18, max: 100, type: 'number' },
    monthlyIncome: { value: parseFloat(document.getElementById('monthlyIncome')?.value || 0), min: 5000, type: 'number' },
    creditScore: { value: parseInt(document.getElementById('creditScore')?.value || 0), min: 300, max: 850, type: 'number' },
    loanAmount: { value: parseFloat(document.getElementById('loanAmount')?.value || 0), min: 10000, type: 'number' },
    tenure: { value: parseInt(document.getElementById('tenure')?.value || 0), min: 6, max: 360, type: 'number' },
    city: { value: document.getElementById('city')?.value || '', type: 'required' },
    loanType: { value: document.getElementById('loanType')?.value || '', type: 'required' },
    employmentType: { value: document.getElementById('employmentType')?.value || '', type: 'required' }
  };

  // Validate name
  if (fields.applicantName.value.length < fields.applicantName.min) {
    errors.applicantName = `Name must be at least ${fields.applicantName.min} characters`;
  }

  // Validate age
  if (fields.age.value < fields.age.min || fields.age.value > fields.age.max) {
    errors.age = `Age must be between ${fields.age.min} and ${fields.age.max}`;
  }

  // Validate monthly income
  if (fields.monthlyIncome.value < fields.monthlyIncome.min) {
    errors.monthlyIncome = `Monthly income must be at least ₹${formatCurrency(fields.monthlyIncome.min)}`;
  }

  // Validate credit score
  if (fields.creditScore.value < fields.creditScore.min || fields.creditScore.value > fields.creditScore.max) {
    errors.creditScore = `Credit score must be between ${fields.creditScore.min} and ${fields.creditScore.max}`;
  }

  // Validate loan amount
  if (fields.loanAmount.value < fields.loanAmount.min) {
    errors.loanAmount = `Loan amount must be at least ₹${formatCurrency(fields.loanAmount.min)}`;
  }

  // Validate loan amount vs monthly income
  if (fields.loanAmount.value > fields.monthlyIncome.value * 60) {
    errors.loanAmount = 'Loan amount is too high compared to monthly income';
  }

  // Validate tenure
  if (fields.tenure.value < fields.tenure.min || fields.tenure.value > fields.tenure.max) {
    errors.tenure = `Tenure must be between ${fields.tenure.min} and ${fields.tenure.max} months`;
  }

  // Validate required fields
  if (!fields.city.value) errors.city = 'City is required';
  if (!fields.loanType.value) errors.loanType = 'Loan type is required';
  if (!fields.employmentType.value) errors.employmentType = 'Employment type is required';

  return errors;
}

function displayValidationErrors(errors) {
  // Clear previous errors
  document.querySelectorAll('.form-group').forEach(group => {
    group.classList.remove('error');
    const errorMsg = group.querySelector('.error-message');
    if (errorMsg) errorMsg.remove();
  });

  // Display new errors
  Object.entries(errors).forEach(([field, message]) => {
    const input = document.getElementById(field) ||
                 document.getElementById(field.replace(/([A-Z])/g, letter => `_${letter.toLowerCase()}`));

    if (input) {
      const group = input.closest('.form-group');
      if (group) {
        group.classList.add('error');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        group.appendChild(errorDiv);
      }
    }
  });
}

// ========================================
// Calculations
// ========================================

function calculateEMI(principal, annualRate, months) {
  const monthlyRate = annualRate / 100 / 12;
  if (monthlyRate === 0) return principal / months;

  const emi = (principal * monthlyRate * Math.pow(1 + monthlyRate, months)) /
              (Math.pow(1 + monthlyRate, months) - 1);
  return emi;
}

function getCreditScoreCategory(score) {
  if (score < 600) return 'Poor';
  if (score < 700) return 'Average';
  if (score < 750) return 'Good';
  return 'Excellent';
}

function getEligibilityScore() {
  const creditScore = parseInt(document.getElementById('creditScore')?.value || 0);
  const monthlyIncome = parseFloat(document.getElementById('monthlyIncome')?.value || 0);
  const existingEmi = parseFloat(document.getElementById('existingEmi')?.value || 0);
  const loanAmount = parseFloat(document.getElementById('loanAmount')?.value || 0);
  const tenure = parseInt(document.getElementById('tenure')?.value || 0);
  const employmentType = document.getElementById('employmentType')?.value || '';

  let score = 0;

  // Credit score component (40%)
  if (creditScore >= 750) score += 40;
  else if (creditScore >= 700) score += 30;
  else if (creditScore >= 600) score += 20;
  else score += 10;

  // DTI ratio component (35%)
  const monthlyEmi = tenure > 0 ? calculateEMI(loanAmount, CONFIG.ANNUAL_RATE, tenure) : 0;
  const totalEmi = monthlyEmi + existingEmi;
  const dtiRatio = monthlyIncome > 0 ? totalEmi / monthlyIncome : 1;

  if (dtiRatio <= 0.30) score += 35;
  else if (dtiRatio <= 0.40) score += 25;
  else if (dtiRatio <= 0.50) score += 15;
  else score += 5;

  // Employment type component (15%)
  if (employmentType === 'SALARIED') score += 15;
  else if (employmentType === 'SELF_EMPLOYED') score += 10;
  else if (employmentType === 'FREELANCE') score += 8;
  else score += 3;

  // Income stability component (15%)
  if (monthlyIncome >= 100000) score += 15;
  else if (monthlyIncome >= 75000) score += 12;
  else if (monthlyIncome >= 50000) score += 10;
  else if (monthlyIncome >= 25000) score += 7;
  else score += 3;

  return Math.min(100, Math.max(0, score));
}

function getRiskLevel(dtiRatio, creditScore) {
  if (dtiRatio <= 0.30 && creditScore >= 700) return 'Low';
  if (dtiRatio > 0.50 || creditScore < 600) return 'High';
  return 'Medium';
}

function updateStats() {
  const monthlyIncome = parseFloat(document.getElementById('monthlyIncome')?.value || 0);
  const existingEmi = parseFloat(document.getElementById('existingEmi')?.value || 0);
  const loanAmount = parseFloat(document.getElementById('loanAmount')?.value || 0);
  const tenure = parseInt(document.getElementById('tenure')?.value || 0);

  // Calculate EMI
  const monthlyEmi = tenure > 0 ? calculateEMI(loanAmount, CONFIG.ANNUAL_RATE, tenure) : 0;
  updateStatCard('emiStat', formatCurrency(Math.round(monthlyEmi)), 'Estimated Monthly EMI');

  // Calculate DTI
  const totalEmi = monthlyEmi + existingEmi;
  const dtiRatio = monthlyIncome > 0 ? totalEmi / monthlyIncome : 0;
  updateStatCard('dtiStat', dtiRatio.toFixed(2), 'Debt-to-Income Ratio');

  // Calculate Loan to Income
  const loanToIncome = monthlyIncome > 0 ? (loanAmount / (monthlyIncome * 12)).toFixed(2) : 0;
  updateStatCard('ltiStat', `${loanToIncome}x`, 'Loan-to-Income Ratio');
}

function updateStatCard(elementId, value, label) {
  const element = document.getElementById(elementId);
  if (element) {
    element.textContent = value;
    const labelElement = element.parentElement?.querySelector('.stat-label');
    if (labelElement) labelElement.textContent = label;
  }
}

// ========================================
// Form Submission
// ========================================

async function handleFormSubmit(e) {
  e.preventDefault();

  // Validate form
  const errors = validateForm();
  if (Object.keys(errors).length > 0) {
    displayValidationErrors(errors);
    alert('Please fix the errors in the form');
    return;
  }

  // Clear validation errors
  document.querySelectorAll('.form-group.error').forEach(group => {
    group.classList.remove('error');
    const errorMsg = group.querySelector('.error-message');
    if (errorMsg) errorMsg.remove();
  });

  // Show loading
  showLoading();

  try {
    const formData = {
      applicant_id: generateApplicantId(),
      applicant_name: document.getElementById('applicantName').value,
      age: parseInt(document.getElementById('age').value),
      income: parseFloat(document.getElementById('monthlyIncome').value) * 12, // Convert to annual
      monthly_income: parseFloat(document.getElementById('monthlyIncome').value),
      employment_type: document.getElementById('employmentType').value,
      credit_score: parseInt(document.getElementById('creditScore').value),
      loan_amount: parseFloat(document.getElementById('loanAmount').value),
      tenure_months: parseInt(document.getElementById('tenure').value),
      existing_liabilities: parseFloat(document.getElementById('existingEmi').value) * parseInt(document.getElementById('tenure').value),
      location: document.getElementById('city').value,
      city: document.getElementById('city').value,
      loan_type: document.getElementById('loanType').value
    };

    // Save form data to local storage
    saveFormData(formData);

    // Make API request
    const response = await fetch(`${CONFIG.API_URL}/evaluate-loan`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Evaluation failed');
    }

    const result = await response.json();

    // Enhance result with calculated values
    const enhancedResult = enhanceResultWithCalculations(formData, result);

    // Display results
    displayResults(enhancedResult);

    // Save results to local storage
    localStorage.setItem('lastResult', JSON.stringify(enhancedResult));

  } catch (error) {
    console.error('Error:', error);
    hideLoading();
    alert(`Error: ${error.message}`);
  }
}

function enhanceResultWithCalculations(formData, apiResult) {
  const monthlyEmi = calculateEMI(formData.loan_amount, CONFIG.ANNUAL_RATE, formData.tenure_months);
  const totalEmi = monthlyEmi + (formData.existing_liabilities / formData.tenure_months);
  const dtiRatio = formData.monthly_income > 0 ? totalEmi / formData.monthly_income : 0;
  const creditScoreCategory = getCreditScoreCategory(formData.credit_score);
  const eligibilityScore = getEligibilityScore();
  const riskLevel = getRiskLevel(dtiRatio, formData.credit_score);

  return {
    ...apiResult,
    applicant_name: formData.applicant_name,
    city: formData.city,
    loan_type: formData.loan_type,
    estimated_emi: monthlyEmi,
    eligibility_score: eligibilityScore,
    credit_score_category: creditScoreCategory,
    risk_level: riskLevel,
    debt_to_income_ratio: dtiRatio,
    recommendation: generateRecommendation(apiResult.decision, dtiRatio, formData.credit_score)
  };
}

function generateRecommendation(decision, dtiRatio, creditScore) {
  if (decision === 'APPROVED') {
    if (creditScore >= 750 && dtiRatio <= 0.30) {
      return 'Excellent profile! You qualify for premium terms with competitive rates.';
    } else if (creditScore >= 700 && dtiRatio <= 0.40) {
      return 'Good profile! You are eligible for favorable loan terms.';
    } else {
      return 'You are approved. Standard terms will apply based on your profile.';
    }
  } else if (decision === 'REJECTED') {
    if (creditScore < 600) {
      return 'Your credit score needs improvement. Consider building credit history and apply again.';
    } else if (dtiRatio > 0.50) {
      return 'Your debt-to-income ratio is high. Reduce existing liabilities or increase income.';
    } else {
      return 'Unfortunately, your profile does not meet our current lending criteria.';
    }
  } else {
    return 'Your application requires manual review. Our team will contact you soon.';
  }
}

// ========================================
// Results Display
// ========================================

function displayResults(result) {
  hideLoading();

  const resultsContainer = document.getElementById('resultsContainer');
  if (!resultsContainer) return;

  const statusClass = result.decision === 'APPROVED' ? 'approved' :
                     result.decision === 'REJECTED' ? 'rejected' : 'review';
  const statusText = result.decision === 'APPROVED' ? '✅ Approved' :
                    result.decision === 'REJECTED' ? '❌ Rejected' : '⏳ Review Required';

  const html = `
    <div class="results-header">
      <h2>Loan Eligibility Assessment Results</h2>
      <div class="status-badge ${statusClass}">${statusText}</div>
    </div>

    <div class="results-grid">
      <div class="result-card">
        <div class="result-label">📋 Eligibility Status</div>
        <div class="result-value">${result.decision}</div>
      </div>
      <div class="result-card">
        <div class="result-label">💰 Loan Amount Requested</div>
        <div class="result-value">₹${formatCurrency(result.loan_amount || 0)}</div>
      </div>
      <div class="result-card">
        <div class="result-label">📊 Estimated Monthly EMI</div>
        <div class="result-value">₹${formatCurrency(Math.round(result.estimated_emi || 0))}</div>
      </div>
      <div class="result-card">
        <div class="result-label">📈 Debt-to-Income Ratio</div>
        <div class="result-value">${(result.debt_to_income_ratio || 0).toFixed(2)}</div>
      </div>
      <div class="result-card">
        <div class="result-label">🎯 Credit Score Category</div>
        <div class="result-value">${result.credit_score_category || 'N/A'}</div>
      </div>
      <div class="result-card">
        <div class="result-label">⚠️ Risk Level</div>
        <div class="result-value">${result.risk_level || 'N/A'}</div>
      </div>
      <div class="result-card">
        <div class="result-label">🏙️ Selected City</div>
        <div class="result-value">${result.city || 'N/A'}</div>
      </div>
      <div class="result-card">
        <div class="result-label">🏷️ Loan Type</div>
        <div class="result-value">${result.loan_type || 'N/A'}</div>
      </div>
    </div>

    <div class="progress-section">
      <div class="progress-item">
        <div class="progress-label">
          <span>Eligibility Score</span>
          <span class="progress-percentage">${Math.round(result.eligibility_score || 0)}%</span>
        </div>
        <div class="progress-bar-container">
          <div class="progress-bar" style="width: ${result.eligibility_score || 0}%"></div>
        </div>
      </div>
      <div class="progress-item">
        <div class="progress-label">
          <span>Credit Score Range</span>
          <span class="progress-percentage">${((result.credit_score || 300) / 850 * 100).toFixed(0)}%</span>
        </div>
        <div class="progress-bar-container">
          <div class="progress-bar" style="width: ${((result.credit_score || 300) / 850 * 100).toFixed(0)}%"></div>
        </div>
      </div>
    </div>

    <div class="recommendation-section">
      <div class="recommendation-title">💡 Recommendation</div>
      <div class="recommendation-text">${result.recommendation || 'Thank you for your application.'}</div>
    </div>

    <div class="button-group">
      <button type="button" id="downloadBtn" class="btn btn-primary" onclick="downloadResults()">
        📥 Download Results (JSON)
      </button>
      <button type="button" id="applyAgainBtn" class="btn btn-secondary" onclick="applyAgain()">
        🔄 Apply Again
      </button>
    </div>
  `;

  resultsContainer.innerHTML = html;
  resultsContainer.classList.add('show');

  // Scroll to results
  resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ========================================
// Utility Functions
// ========================================

function formatCurrency(value) {
  return value.toLocaleString('en-IN', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  });
}

function generateApplicantId() {
  return `APP${Date.now().toString().slice(-6)}`;
}

function showLoading() {
  const spinner = document.getElementById('loadingSpinner');
  if (spinner) {
    spinner.classList.add('active');
  }
}

function hideLoading() {
  const spinner = document.getElementById('loadingSpinner');
  if (spinner) {
    spinner.classList.remove('active');
  }
}

function resetForm() {
  document.getElementById('loanForm').reset();
  document.querySelectorAll('.form-group.error').forEach(group => {
    group.classList.remove('error');
    const errorMsg = group.querySelector('.error-message');
    if (errorMsg) errorMsg.remove();
  });
  document.getElementById('resultsContainer').classList.remove('show');
  updateStats();
}

function applyAgain() {
  resetForm();
  document.getElementById('applicantName').focus();
}

function downloadResults() {
  const result = localStorage.getItem('lastResult');
  if (result) {
    const data = JSON.parse(result);
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `loan_evaluation_${data.applicant_id}_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }
}

// ========================================
// Local Storage
// ========================================

function saveFormData(data) {
  localStorage.setItem('formData', JSON.stringify(data));
}

function loadFormData() {
  const data = localStorage.getItem('formData');
  if (data) {
    try {
      const formData = JSON.parse(data);
      // Populate form fields from saved data
      document.getElementById('applicantName').value = formData.applicant_name || '';
      document.getElementById('age').value = formData.age || '';
      document.getElementById('monthlyIncome').value = formData.monthly_income || '';
      document.getElementById('existingEmi').value = formData.existing_liabilities / (formData.tenure_months || 1) || '';
      document.getElementById('creditScore').value = formData.credit_score || '';
      document.getElementById('loanAmount').value = formData.loan_amount || '';
      document.getElementById('tenure').value = formData.tenure_months || '';
      document.getElementById('city').value = formData.city || '';
      document.getElementById('loanType').value = formData.loan_type || '';
      document.getElementById('employmentType').value = formData.employment_type || '';

      // Update stats
      updateStats();
    } catch (e) {
      console.log('Could not load saved form data');
    }
  }
}
