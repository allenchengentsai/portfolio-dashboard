#!/usr/bin/env python3
"""
Portfolio Dashboard - Peter Lynch Style Analysis
Automated daily analysis of your stock portfolio using Claude API
"""

import os
import json
import time
import smtplib
import yfinance as yf
import requests
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Tuple, Optional
import logging
from config import *

# Setup logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PortfolioAnalyzer:
    def __init__(self):
        self.claude_api_key = os.getenv('CLAUDE_API_KEY')
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.email_password = os.getenv('EMAIL_PASSWORD')  # App password for Gmail
        
        if not self.claude_api_key:
            raise ValueError("CLAUDE_API_KEY environment variable not set")
        
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'x-api-key': self.claude_api_key,
            'anthropic-version': '2023-06-01'
        })
    
    def load_portfolio(self) -> List[Dict]:
        """Load portfolio tickers from file"""
        portfolio = []
        
        try:
            with open(PORTFOLIO_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split(',')
                        ticker = parts[0].strip()
                        shares = float(parts[1]) if len(parts) > 1 and parts[1].strip() else None
                        cost_basis = float(parts[2]) if len(parts) > 2 and parts[2].strip() else None
                        
                        portfolio.append({
                            'ticker': ticker,
                            'shares': shares,
                            'cost_basis': cost_basis
                        })
        except FileNotFoundError:
            logger.error(f"Portfolio file {PORTFOLIO_FILE} not found")
            raise
        
        logger.info(f"Loaded {len(portfolio)} stocks from portfolio")
        return portfolio
    
    def get_stock_data(self, ticker: str) -> Dict:
        """Fetch current stock data including pre-market if available"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="5d")
            
            if hist.empty:
                logger.warning(f"No historical data for {ticker}")
                return None
            
            current_price = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            
            # Try to get pre-market data
            premarket_change = 0
            premarket_percent = 0
            
            if INCLUDE_PREMARKET:
                try:
                    # Get pre-market data from Yahoo Finance
                    premarket_data = stock.get_premarket_price()
                    if premarket_data:
                        premarket_change = premarket_data - current_price
                        premarket_percent = (premarket_change / current_price) * 100
                except:
                    pass  # Pre-market data not always available
            
            regular_change = current_price - prev_close
            regular_percent = (regular_change / prev_close) * 100 if prev_close != 0 else 0
            
            return {
                'ticker': ticker,
                'company_name': info.get('longName', ticker),
                'current_price': current_price,
                'regular_change': regular_change,
                'regular_percent': regular_percent,
                'premarket_change': premarket_change,
                'premarket_percent': premarket_percent,
                'volume': hist['Volume'].iloc[-1],
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE'),
                'peg_ratio': info.get('pegRatio'),
                'debt_to_equity': info.get('debtToEquity'),
                'revenue_growth': info.get('revenueGrowth'),
                'earnings_growth': info.get('earningsGrowth'),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown')
            }
            
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {e}")
            return None
    
    def analyze_stock_with_claude(self, stock_data: Dict, position_data: Dict) -> Dict:
        """Analyze a single stock using Claude API"""
        
        # Calculate position metrics
        position_value = 0
        gain_percent = 0
        weight_percent = 0
        
        if position_data['shares'] and position_data['cost_basis']:
            position_value = position_data['shares'] * stock_data['current_price']
            total_cost = position_data['shares'] * position_data['cost_basis']
            gain_percent = ((position_value - total_cost) / total_cost) * 100
        
        prompt = f"""
        Analyze this stock using Peter Lynch's investment principles. Provide a comprehensive analysis including:

        STOCK DATA:
        - Ticker: {stock_data['ticker']}
        - Company: {stock_data['company_name']}
        - Current Price: ${stock_data['current_price']:.2f}
        - Daily Change: {stock_data['regular_percent']:.2f}%
        - Pre-market Change: {stock_data['premarket_percent']:.2f}%
        - Sector: {stock_data['sector']}
        - Market Cap: ${stock_data['market_cap']:,}
        - P/E Ratio: {stock_data['pe_ratio']}
        - PEG Ratio: {stock_data['peg_ratio']}
        - Debt/Equity: {stock_data['debt_to_equity']}

        POSITION DATA:
        - Shares Owned: {position_data['shares']}
        - Cost Basis: ${position_data['cost_basis']:.2f}
        - Current Value: ${position_value:,.2f}
        - Gain/Loss: {gain_percent:.1f}%

        Please provide analysis in this JSON format:
        {{
            "recent_news": ["List of 3-5 recent news items affecting the stock"],
            "fundamental_health": {{
                "revenue_trend": "improving/declining/stable",
                "earnings_trend": "improving/declining/stable", 
                "debt_situation": "healthy/concerning/critical",
                "competitive_position": "strong/average/weak"
            }},
            "red_flags": ["List any Peter Lynch red flags"],
            "green_flags": ["List any Peter Lynch positive signals"],
            "upcoming_catalysts": [
                {{"date": "YYYY-MM-DD", "event": "Description of catalyst"}},
                {{"date": "YYYY-MM-DD", "event": "Description of catalyst"}}
            ],
            "insider_activity": {{
                "recent_buying": "amount or none",
                "recent_selling": "amount or none",
                "net_sentiment": "bullish/bearish/neutral"
            }},
            "competitors": ["List 2-3 main competitors in same space"],
            "peg_analysis": {{
                "current_peg": {stock_data['peg_ratio']},
                "assessment": "undervalued/fairly_valued/overvalued",
                "reasoning": "Brief explanation"
            }},
            "lynch_score": {{
                "recommendation": "BUY/HOLD/TRIM/SELL",
                "reasoning": "Peter Lynch style explanation",
                "price_target": "estimated fair value",
                "risk_level": "low/medium/high"
            }}
        }}

        Focus on finding REAL catalysts (product launches, contracts, partnerships, regulatory approvals) not just earnings dates.
        Search for recent news from the past {MAX_NEWS_DAYS} days.
        Consider the current gain of {gain_percent:.1f}% in your recommendation.
        """

        try:
            response = self.session.post(
                'https://api.anthropic.com/v1/messages',
                json={
                    'model': CLAUDE_MODEL,
                    'max_tokens': MAX_TOKENS_PER_STOCK,
                    'messages': [{'role': 'user', 'content': prompt}]
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis_text = result['content'][0]['text']
                
                # Try to parse JSON from the response
                try:
                    # Extract JSON from the response (it might be wrapped in markdown)
                    json_start = analysis_text.find('{')
                    json_end = analysis_text.rfind('}') + 1
                    json_str = analysis_text[json_start:json_end]
                    analysis = json.loads(json_str)
                    
                    # Add calculated metrics
                    analysis['position_value'] = position_value
                    analysis['gain_percent'] = gain_percent
                    analysis['weight_percent'] = weight_percent
                    
                    return analysis
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON for {stock_data['ticker']}: {e}")
                    return self._create_fallback_analysis(stock_data, position_data)
            else:
                logger.error(f"Claude API error for {stock_data['ticker']}: {response.status_code}")
                return self._create_fallback_analysis(stock_data, position_data)
                
        except Exception as e:
            logger.error(f"Error analyzing {stock_data['ticker']}: {e}")
            return self._create_fallback_analysis(stock_data, position_data)
    
    def _create_fallback_analysis(self, stock_data: Dict, position_data: Dict) -> Dict:
        """Create basic analysis when Claude API fails"""
        return {
            "recent_news": ["API error - unable to fetch recent news"],
            "fundamental_health": {
                "revenue_trend": "unknown",
                "earnings_trend": "unknown",
                "debt_situation": "unknown",
                "competitive_position": "unknown"
            },
            "red_flags": [],
            "green_flags": [],
            "upcoming_catalysts": [],
            "insider_activity": {
                "recent_buying": "unknown",
                "recent_selling": "unknown", 
                "net_sentiment": "unknown"
            },
            "competitors": [],
            "peg_analysis": {
                "current_peg": stock_data.get('peg_ratio'),
                "assessment": "unknown",
                "reasoning": "API error"
            },
            "lynch_score": {
                "recommendation": "HOLD",
                "reasoning": "Unable to analyze due to API error",
                "price_target": "unknown",
                "risk_level": "unknown"
            },
            "position_value": position_data['shares'] * stock_data['current_price'] if position_data['shares'] else 0,
            "gain_percent": 0,
            "weight_percent": 0
        }
    
    def generate_dashboard_html(self, analyses: List[Dict]) -> str:
        """Generate the HTML dashboard"""
        
        # Calculate portfolio totals
        total_value = sum(a.get('position_value', 0) for a in analyses)
        total_alerts = sum(len(a.get('red_flags', [])) for a in analyses)
        
        # Sort analyses based on configuration
        if SORT_BY == "weight":
            analyses.sort(key=lambda x: x.get('position_value', 0), reverse=True)
        elif SORT_BY == "gain_percent":
            analyses.sort(key=lambda x: x.get('gain_percent', 0), reverse=True)
        elif SORT_BY == "alerts":
            analyses.sort(key=lambda x: len(x.get('red_flags', [])), reverse=True)
        
        # Filter small positions if configured
        if not SHOW_SMALL_POSITIONS:
            analyses = [a for a in analyses if a.get('position_value', 0) >= 1000]
        
        # Generate HTML (using the template from earlier but with dynamic data)
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Portfolio Analysis Dashboard - Peter Lynch Style</title>
            <style>
                /* Include the CSS from the earlier template */
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 20px; background-color: #f8f9fa; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
                /* ... rest of CSS ... */
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Portfolio Analysis Dashboard</h1>
                <p>Peter Lynch Style Analysis - Updated: {timestamp}</p>
            </div>
            
            <div class="portfolio-summary">
                <div class="summary-card">
                    <h3>Total Portfolio Value</h3>
                    <div class="value">${total_value:,.0f}</div>
                </div>
                <div class="summary-card">
                    <h3>Stocks with Alerts</h3>
                    <div class="value" style="color: #dc3545;">{total_alerts} 🚨</div>
                </div>
            </div>
            
            <div class="stocks-table">
                <table>
                    <thead>
                        <tr>
                            <th>Stock</th>
                            <th>Price/Change</th>
                            <th>Position</th>
                            <th>Gain %</th>
                            <th>Alerts</th>
                            <th>Lynch Score</th>
                            <th>Next Events</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </div>
            
            <script>
                function toggleDetails(stockId) {{{{
                    const details = document.getElementById(stockId + '-details');
                    if (details.classList.contains('show')) {{{{
                        details.classList.remove('show');
                    }}}} else {{{{
                        document.querySelectorAll('.expanded-details.show').forEach(el => {{{{
                            el.classList.remove('show');
                        }}}});
                        details.classList.add('show');
                    }}}}
                }}}}
            </script>
        </body>
        </html>
        """
        
        # Generate table rows (simplified for now)
        table_rows = ""
        for analysis in analyses:
            # This would generate the actual table rows with all the data
            # For brevity, I'm showing the structure
            table_rows += f"""
            <tr class="stock-row" onclick="toggleDetails('{analysis.get('ticker', 'unknown')}')">
                <td>{analysis.get('ticker', 'N/A')}</td>
                <td>${analysis.get('current_price', 0):.2f}</td>
                <td>${analysis.get('position_value', 0):,.0f}</td>
                <td>{analysis.get('gain_percent', 0):.1f}%</td>
                <td>{len(analysis.get('red_flags', []))}</td>
                <td>{analysis.get('lynch_score', {}).get('recommendation', 'HOLD')}</td>
                <td>Next events...</td>
            </tr>
            """
        
        return html_template.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S EST"),
            total_value=total_value,
            total_alerts=total_alerts,
            table_rows=table_rows
        )
    
    def send_email(self, html_content: str):
        """Send dashboard via email"""
        if not self.email_password:
            logger.warning("Email password not set, skipping email delivery")
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = "portfolio.dashboard@gmail.com"  # You'll need to set this up
            msg['To'] = EMAIL_RECIPIENT
            msg['Subject'] = EMAIL_SUBJECT
            
            msg.attach(MIMEText(html_content, 'html'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("portfolio.dashboard@gmail.com", self.email_password)
            server.send_message(msg)
            server.quit()
            
            logger.info("Email sent successfully")
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
    
    def save_to_github_pages(self, html_content: str):
        """Save dashboard to GitHub Pages"""
        try:
            with open(DASHBOARD_FILENAME, 'w') as f:
                f.write(html_content)
            logger.info(f"Dashboard saved to {DASHBOARD_FILENAME}")
        except Exception as e:
            logger.error(f"Failed to save dashboard: {e}")
    
    def run_analysis(self):
        """Main analysis function"""
        logger.info("Starting portfolio analysis...")
        
        # Load portfolio
        portfolio = self.load_portfolio()
        
        # Analyze each stock
        analyses = []
        for i, position in enumerate(portfolio):
            logger.info(f"Analyzing {position['ticker']} ({i+1}/{len(portfolio)})")
            
            # Get stock data
            stock_data = self.get_stock_data(position['ticker'])
            if not stock_data:
                continue
            
            # Analyze with Claude
            analysis = self.analyze_stock_with_claude(stock_data, position)
            analysis['ticker'] = position['ticker']
            analysis['current_price'] = stock_data['current_price']
            analyses.append(analysis)
            
            # Rate limiting
            if RATE_LIMIT_DELAY > 0:
                time.sleep(RATE_LIMIT_DELAY)
        
        # Generate dashboard
        html_content = self.generate_dashboard_html(analyses)
        
        # Save/send dashboard
        if GITHUB_PAGES_ENABLED:
            self.save_to_github_pages(html_content)
        
        if EMAIL_RECIPIENT:
            self.send_email(html_content)
        
        logger.info("Analysis complete!")
        return analyses

def main():
    """Main entry point"""
    try:
        analyzer = PortfolioAnalyzer()
        analyzer.run_analysis()
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise

if __name__ == "__main__":
    main()
