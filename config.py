# Portfolio Dashboard Configuration
# Edit these settings to customize your dashboard

# Email Configuration
EMAIL_RECIPIENT = "allenchengentsai@gmail.com"
EMAIL_SUBJECT = "Daily Portfolio Analysis - Peter Lynch Style"

# Schedule Configuration (GitHub Actions cron format)
# Current: 8:00 AM EST (13:00 UTC) on weekdays
# Format: "minute hour * * day_of_week" (0=Sunday, 1=Monday, etc.)
SCHEDULE_CRON = "0 13 * * 1-5"  # 8am EST, Monday-Friday

# Analysis Configuration
ANALYSIS_DEPTH = "comprehensive"  # Options: "quick", "standard", "comprehensive"
INCLUDE_PREMARKET = True  # Include pre-market price movements
INCLUDE_COMPETITORS = True  # Find competitor alternatives
INCLUDE_INSIDER_ACTIVITY = True  # Check insider buying/selling
MAX_NEWS_DAYS = 3  # How many days back to search for news

# Portfolio Configuration
PORTFOLIO_FILE = "portfolio_tickers.txt"
POSITION_TRACKING = True  # Track your actual positions vs just tickers

# Display Configuration
SORT_BY = "weight"  # Options: "weight", "gain_percent", "alerts", "ticker"
SHOW_SMALL_POSITIONS = True  # Show positions under $1000
ALERT_THRESHOLD_GAIN = 1000  # Alert if gain % exceeds this (for trim recommendations)
ALERT_THRESHOLD_LOSS = -20  # Alert if loss % exceeds this

# API Configuration
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"  # Latest Claude model
MAX_TOKENS_PER_STOCK = 4000  # Limit output length per stock
RATE_LIMIT_DELAY = 1  # Seconds between API calls to avoid rate limits

# GitHub Pages Configuration
GITHUB_PAGES_ENABLED = True  # Host dashboard on GitHub Pages
DASHBOARD_FILENAME = "index.html"  # Will be accessible at your-username.github.io/repo-name

# Advanced Options
DEBUG_MODE = False  # Enable detailed logging
CACHE_FINANCIAL_DATA = True  # Cache basic financial data to reduce API costs
RETRY_FAILED_STOCKS = True  # Retry analysis if a stock fails
MAX_RETRIES = 2

# Peter Lynch Scoring Weights (adjust to your preference)
LYNCH_WEIGHTS = {
    "growth_vs_pe": 0.25,      # PEG ratio importance
    "insider_activity": 0.20,   # Insider buying/selling weight
    "earnings_growth": 0.20,    # Earnings growth trend weight
    "debt_levels": 0.15,        # Debt-to-equity importance
    "market_position": 0.10,    # Competitive position weight
    "valuation": 0.10          # Overall valuation weight
}

# Notification Thresholds
URGENT_ALERTS = {
    "insider_selling_threshold": 10000000,  # Alert if insider selling > $10M
    "earnings_miss_percent": -10,           # Alert if earnings miss > 10%
    "debt_increase_percent": 50,            # Alert if debt increases > 50%
    "revenue_decline_percent": -15          # Alert if revenue declines > 15%
}
