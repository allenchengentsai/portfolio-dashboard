# Portfolio Dashboard - Peter Lynch Style Analysis

Automated daily analysis of your stock portfolio using Claude AI and Peter Lynch's investment principles.

## 🎯 Features

- **Daily automated analysis** of all your holdings
- **Peter Lynch-style recommendations** (Buy/Hold/Trim/Sell)
- **Real catalyst detection** (product launches, contracts, partnerships)
- **Insider trading monitoring** 
- **Pre-market price tracking**
- **Email delivery** + **GitHub Pages hosting**
- **Fully configurable** settings

## 📊 What You Get Each Morning

- **Quick scan table** with alerts and recommendations
- **Detailed analysis** for each stock (click to expand)
- **Upcoming catalyst dates** with real events
- **Fundamental health checks** (revenue, debt, competition)
- **PEG ratio analysis** and valuation assessment
- **Competitor alternatives** in same sectors

## 🚀 Setup Instructions

### 1. Fork This Repository

1. Click the "Fork" button at the top of this page
2. This creates your own copy of the repository

### 2. Configure Your Portfolio

Edit `portfolio_tickers.txt` with your stocks:

```
# Format: TICKER,SHARES,COST_BASIS
RKLB,592,4.23
AAPL,100,150.00
TSLA,50,200.00
```

### 3. Add API Keys (Secrets)

In your forked repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"** and add:

**Required:**
- `CLAUDE_API_KEY`: Your Claude API key from console.anthropic.com

**Optional (for email delivery):**
- `EMAIL_PASSWORD`: Gmail app password (see setup below)

### 4. Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** / **root**
4. Click **Save**

Your dashboard will be available at: `https://yourusername.github.io/repository-name`

### 5. Test the Setup

1. Go to **Actions** tab
2. Click **"Daily Portfolio Analysis"**
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait 5-10 minutes for completion

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Email settings
EMAIL_RECIPIENT = "your-email@gmail.com"

# Schedule (8am EST on weekdays)
SCHEDULE_CRON = "0 13 * * 1-5"

# Analysis depth
ANALYSIS_DEPTH = "comprehensive"  # quick/standard/comprehensive
INCLUDE_PREMARKET = True
MAX_NEWS_DAYS = 3

# Display options
SORT_BY = "weight"  # weight/gain_percent/alerts/ticker
SHOW_SMALL_POSITIONS = True
```

## 📧 Email Setup (Optional)

To receive daily emails:

1. **Enable 2-factor authentication** on your Gmail account
2. **Generate app password:**
   - Google Account → Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Copy the 16-character password
3. **Add to GitHub Secrets:**
   - Secret name: `EMAIL_PASSWORD`
   - Value: The 16-character app password

## 💰 Cost Estimate

- **GitHub Actions**: FREE (2,000 minutes/month)
- **GitHub Pages**: FREE
- **Claude API**: ~$20-30/month for 35 stocks daily
- **Total**: ~$20-30/month

## 🔧 Customization

### Adding New Stocks

Edit `portfolio_tickers.txt`:
```
# Add new line
NVDA,25,400.00
```

### Changing Schedule

Edit `config.py`:
```python
SCHEDULE_CRON = "0 14 * * 1-5"  # 9am EST instead of 8am
```

### Adjusting Analysis Depth

```python
ANALYSIS_DEPTH = "quick"        # Faster, less detailed
ANALYSIS_DEPTH = "standard"     # Balanced
ANALYSIS_DEPTH = "comprehensive" # Full Peter Lynch analysis
```

## 📱 Daily Workflow

1. **8:00 AM EST**: GitHub Actions automatically runs analysis
2. **8:05 AM EST**: Updated dashboard available at your GitHub Pages URL
3. **8:06 AM EST**: Email delivered (if configured)
4. **Your morning**: Scan dashboard in 2-3 minutes, investigate any alerts

## 🚨 Troubleshooting

### Analysis Not Running
- Check **Actions** tab for error messages
- Verify `CLAUDE_API_KEY` is set correctly
- Check Claude API credit balance

### Email Not Working
- Verify Gmail app password is correct
- Check spam folder
- Ensure 2FA is enabled on Gmail

### Dashboard Not Updating
- Check if GitHub Pages is enabled
- Verify the workflow completed successfully
- Wait 5-10 minutes for Pages to deploy

## 🎯 Peter Lynch Principles Built-In

- **PEG Ratio Analysis**: Growth vs. valuation assessment
- **Insider Activity**: Flags heavy selling by executives
- **Earnings Quality**: Revenue growth vs. debt increases
- **Competitive Position**: Identifies better alternatives
- **Catalyst Dating**: Real events that move stocks
- **Position Sizing**: Trim recommendations after big gains

## 📊 Sample Analysis Output

```
RKLB: TRIM - Up 1,509%, Neutron launch Dec 2025 (key catalyst)
├── 🚨 Insider selling: $26.6M (3 months)
├── ✅ Revenue growth: +78% YoY  
├── ⚠️ Trading above analyst targets
└── 🎯 Recommendation: Trim from 15.7% to 8-10%

ENVX: HOLD* - Needs tier-1 customer wins by mid-2025
├── ⚠️ No major contracts yet ($2.1B valuation at risk)
├── ✅ $60M buyback shows confidence
└── 🎯 Set deadline: Customer wins by Q2 2025 or reassess
```

## 🔄 Updates and Maintenance

The system is designed to be **set-and-forget**, but you can:

- **Update tickers**: Edit `portfolio_tickers.txt` anytime
- **Adjust settings**: Modify `config.py` as needed  
- **Monitor costs**: Check Claude API usage monthly
- **Review recommendations**: Act on TRIM/SELL suggestions

## 📞 Support

If you run into issues:

1. Check the **Actions** tab for error logs
2. Review this README for troubleshooting steps
3. Verify all secrets are set correctly
4. Test with a smaller portfolio first (5-10 stocks)

---

**Disclaimer**: This tool provides analysis based on publicly available data and AI interpretation. Always do your own research before making investment decisions.
