# Loan Eligibility Agent - Quick Start Guide

## 🚀 Start in 30 Seconds

```bash
cd /home/ubuntu/Desktop/Loan_Agent
python3 -m uvicorn Api.main:app --host 0.0.0.0 --port 8000 --reload
```

Then open your browser: **http://localhost:8000** ✨

## 📋 What You Get

### New UI Components
- ✅ Modern, professional HTML/CSS/JavaScript frontend
- ✅ Beautiful form with 4 sections (Applicant, Financial, Loan Details, etc.)
- ✅ Real-time calculation sidebar (EMI, DTI, Loan-to-Income)
- ✅ Professional results dashboard with color-coded status
- ✅ Progress bars for eligibility score and credit score
- ✅ Personalized recommendations

### New Features
- 📍 50+ Indian cities dropdown
- 🏦 5 loan types (Personal, Home, Car, Education, Business)
- 👔 4 employment types
- 📊 Real-time EMI calculator
- 🎯 Eligibility score (0-100%)
- 📈 Debt-to-Income ratio calculation
- 💳 Credit score categories (Poor/Average/Good/Excellent)
- ⚠️ Risk levels (Low/Medium/High)
- 💾 Form data saved to browser storage
- 📥 Download results as JSON
- ✅ Comprehensive input validation

### New API Endpoints
```
GET  /                           → Main form page
GET  /cities                     → List of Indian cities
GET  /loan-types                 → Available loan types
GET  /employment-types           → Employment options
POST /evaluate-loan              → Evaluate loan application
GET  /health                     → Health check
```

## 🎨 Design Highlights

- **Color Scheme**: Professional blue primary with green (approved), red (rejected), orange (review)
- **Responsive**: Works on desktop, tablet, and mobile
- **Animations**: Smooth transitions and loading spinners
- **Accessibility**: Clean, semantic HTML with ARIA labels

## 📁 New Files Created

```
templates/
├── index.html          # Main form page
└── results.html        # Results dashboard (optional)

static/
├── css/
│   └── style.css      # Complete styling (1000+ lines)
└── js/
    └── app.js         # Form logic & calculations (900+ lines)
```

## 🎯 File Locations

| File | Location |
|------|----------|
| Backend API | `Api/main.py` (UPDATED) |
| Data Models | `models.py` (UPDATED) |
| Form Page | `templates/index.html` (NEW) |
| Results Page | `templates/results.html` (NEW) |
| Stylesheet | `static/css/style.css` (NEW) |
| JavaScript | `static/js/app.js` (NEW) |
| Setup Guide | `SETUP_GUIDE.md` (NEW) |

## 📝 Form Fields

### Applicant Information
- Full Name (required)
- Age (18-100, required)

### Financial Information
- Monthly Income (₹5,000+, required)
- Existing EMI (₹0+, optional)
- Credit Score (300-850, required)
- Employment Type (dropdown, required)

### Loan Details
- Loan Amount Required (₹10,000+, required)
- Loan Tenure (6-360 months, required)
- Loan Type (dropdown, required)
- City (50+ Indian cities, required)

## 💡 Key Calculations

### EMI Calculator
```
EMI = (Principal × Monthly Rate × (1 + Monthly Rate)^Months) / 
      ((1 + Monthly Rate)^Months - 1)
Annual Rate = 10.5% (default)
```

### Eligibility Score
- Credit Score: 40%
- DTI Ratio: 35%
- Income Stability: 15%
- Employment Type: 10%

### Risk Level
- **Low**: DTI ≤ 0.30 + Credit Score ≥ 700
- **Medium**: Between Low and High
- **High**: DTI > 0.50 OR Credit Score < 600

## 🧪 Test with Sample Data

```
Name: John Doe
Age: 35
Monthly Income: ₹60,000
Existing EMI: ₹0
Credit Score: 720
Employment: SALARIED
Loan Amount: ₹500,000
Tenure: 60 months
Loan Type: Home Loan
City: Mumbai
```

Expected Results:
- Estimated EMI: ~₹9,956
- DTI Ratio: ~0.17
- Eligibility Score: ~85%
- Credit Score Category: Good
- Risk Level: Low

## 🔧 Customization

### Change Interest Rate
Edit `static/js/app.js` line 8:
```javascript
ANNUAL_RATE: 10.5,  // Change to your desired rate
```

### Add Cities
Edit `Api/main.py` in `get_cities()` function or `static/js/app.js` in `INDIAN_CITIES` array.

### Change Colors
Edit `static/css/style.css` root variables (lines 3-27).

## ⚠️ Troubleshooting

**"Port already in use"**
```bash
lsof -i :8000
kill -9 <PID>
```

**"Static files not found"**
- Check: `ls -la static/css/style.css`
- Verify: `curl http://localhost:8000/static/css/style.css`

**"Form won't submit"**
- Check browser console (F12)
- Verify API is running: `curl http://localhost:8000/health`
- Check validation errors in form

## 📱 Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS/Android)

## 🎓 Learn More

See `SETUP_GUIDE.md` for:
- Detailed API documentation
- Calculation formulas
- Customization guide
- Troubleshooting

## ✨ You're All Set!

1. Run the server
2. Open http://localhost:8000
3. Fill the form
4. See your beautiful results! 🎉

---

**Questions?** Check the console (F12) and server logs for error messages.
