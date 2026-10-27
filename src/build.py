# Generates ../index.html (v2). Content sourced from ParBproject repo READMEs.
import pathlib, html
D = pathlib.Path(__file__).resolve().parent.parent

GH = '<svg class="h-4 w-4" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'
EXT = '<svg class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M11 3a1 1 0 100 2h2.59l-6.3 6.29a1 1 0 101.42 1.42L15 6.41V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"/><path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z"/></svg>'
ARROW = '<svg class="h-4 w-4 transition-transform group-hover:translate-x-0.5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M10.3 3.3a1 1 0 011.4 0l6 6a1 1 0 010 1.4l-6 6a1 1 0 01-1.4-1.4L14.58 11H3a1 1 0 110-2h11.59l-4.3-4.3a1 1 0 010-1.4z" clip-rule="evenodd"/></svg>'
CHECK = '<svg class="mt-0.5 h-4 w-4 shrink-0 text-accent" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M16.7 5.3a1 1 0 010 1.4l-8 8a1 1 0 01-1.4 0l-4-4a1 1 0 011.4-1.4L8 12.58l7.3-7.3a1 1 0 011.4 0z" clip-rule="evenodd"/></svg>'

TAGNAMES = {'forecasting': 'Forecasting', 'quant': 'Quant / Finance', 'ml': 'ML', 'analytics': 'Analytics', 'tools': 'Tools'}

CARDS = [
    dict(img='rpa_dashboard.png', w=1440, h=900, alt='Streamlit dashboard comparing equal-weight and minimum-variance ETF portfolios with SPY: cumulative returns, drawdowns and a risk summary', pos='left top', tags=['quant', 'analytics'],
         title='Portfolio Risk & Performance Analyzer',
         desc='Equal-weight and minimum-variance portfolios of six ETFs against SPY, 2006 to 2026. Weights use only past data, and trading costs are included.',
         bullets=['Adjusted prices are a frozen Yahoo snapshot, checked with SHA-256, then loaded into SQLite', 'Equal weight cut volatility from 19.20% to 11.11% and max drawdown from −55.2% to −32.2%. Sharpe stayed about the same (0.52 vs 0.55)', 'Minimum variance had the lowest volatility (5.38%) and the worst Sharpe (0.35). It averaged 88% in AGG', 'A Streamlit dashboard for dates, weights, and the risk table. pytest covers the metrics and the SQL'],
         stack=['Python', 'pandas', 'NumPy', 'SQLite', 'Plotly', 'Streamlit', 'pytest'], code='https://github.com/ParBproject/portfolio-risk-performance-analyzer', live='https://parbproject.github.io/portfolio-risk-performance-analyzer/',
         extra=[('Streamlit dashboard', 'https://parb-portfolio-analyzer.streamlit.app/')]),
    dict(img='vfm_overview.png', w=1440, h=900, alt='Volatility forecasting app comparing realized SPY volatility with HAR and LSTM forecasts, loss tables and Diebold-Mariano tests', pos='left top', tags=['ml', 'forecasting'],
         title='Volatility Forecasting: HAR vs ML',
         desc='One-day-ahead realized volatility for SPY and nine sector ETFs. HAR-RV and GARCH(1,1) against gradient boosting and a small LSTM, walk-forward from 2013 to 2026, with no tuning.',
         bullets=['On QLIKE the LSTM is lowest on all 10 ETFs (mean 0.2968 vs 0.3262 for HAR, about 9% lower), significant at 5% on 8 of 10', 'On MSE, no model is significantly different from HAR. A few crash days dominate the squared error', 'Gradient boosting is about level with HAR on QLIKE (−0.3%). GARCH is worse on 7 of 10', 'A test scrambles all future data and checks that earlier forecasts do not change'],
         stack=['Python', 'PyTorch', 'scikit-learn', 'arch', 'React', 'Vite'], code='https://github.com/ParBproject/vol-forecast-ml', live='https://parbproject.github.io/vol-forecast-ml/'),
    dict(img='prl_overview.png', w=1440, h=900, alt='Portfolio Risk Lab allocator with strategy controls, equity curve, weights and risk metrics', pos='left top', tags=['quant'],
         title='Portfolio Risk Lab',
         desc='Mean-variance, risk parity, and Black-Litterman on 21 ETFs, walk-forward against SPY, 60/40, and equal weight, after costs (May 2012 to Sep 2026).',
         bullets=['No optimizer beat SPY (Sharpe 0.92) or 60/40 (0.84). Mean-variance reached 0.76', 'Risk parity cut max drawdown to −12.72% from −23.93% for SPY, at 5.45% volatility versus 14.03%', 'No strategy has a significant factor alpha. All |t| are under 2. Mean-variance alpha is −2.20% a year, t = −1.63', 'The browser allocator matches the Python numbers in tests'],
         stack=['Python', 'NumPy', 'SciPy', 'pandas', 'React', 'Vite'], code='https://github.com/ParBproject/portfolio-risk-lab', live='https://parbproject.github.io/portfolio-risk-lab/'),
    dict(img='ovs_overview.png', w=1440, h=900, alt='SPY implied-volatility surface app with a 3D SVI surface, term structure and skew', pos='left top', tags=['quant'],
         title='SPY Volatility Surface',
         desc='Black-Scholes pricing and Greeks, an implied-vol solver, and an SVI surface fit to one real SPY option chain (close of 22 Oct 2026), with arbitrage checks.',
         bullets=['1,077 out-of-the-money quotes across 11 expiries (7 to 603 days)', 'ATM implied vol is 15.75% at 7 days and 18.39% at 603 days, with a low of 14.52% at 39 days', 'SVI error is 0.22 to 0.67 vol points. All 11 expiries pass the butterfly check', '49 of 1,210 calendar-check points fail, all outside the quoted strikes, where the SVI curve is extrapolated'],
         stack=['Python', 'SciPy', 'yfinance', 'React', 'Vite', 'Canvas'], code='https://github.com/ParBproject/options-vol-surface', live='https://parbproject.github.io/options-vol-surface/'),
    dict(img='sp_panel.png', w=1280, h=800, alt='UNH long pitch scenario panel with beta toggle, FCF fan chart and value heatmap', pos='left top', tags=['quant'],
         title='UNH Equity Pitch',
         desc='A long note on UnitedHealth, from frozen filings and prices. The case that weakens it is in the write-up.',
         bullets=['DCF, reverse DCF, Fama-French factors, comps, and a walk-forward trend signal', 'Base case $526.64 against a $367.08 price on 30 Sep 2026', 'The full-sample beta (0.78) drops the value to $321.29, below the price', 'The trend signal (Sharpe 0.29) and buy-and-hold (0.49) both trail SPY (0.87)'],
         stack=['Python', 'pandas', 'statsmodels', 'Vite', 'ECharts', 'Playwright'], code='https://github.com/ParBproject/stock-pitch', live='https://parbproject.github.io/stock-pitch/',
         extra=[('PDF deck', 'https://parbproject.github.io/stock-pitch/deck/pitch.pdf')]),
    dict(img='dcf_overview.png', w=1440, h=1222, alt='DCF Valuation Model overview with valuations for six large caps', pos='left top', tags=['quant'],
         title='DCF Valuation Model',
         desc='A mechanical DCF for six large caps, built from SEC filings. Sliders, a sensitivity grid, and a 10,000-draw Monte Carlo.',
         bullets=['AAPL comes out at $122.18 against a $348.22 price. I did not tune that gap away', 'XOM is the only name above its price ($216.26 vs $178.23). In 71.9% of the Monte Carlo draws, value exceeds the price', 'The prices imply about 20.1% 10-year revenue growth for AAPL and 20.3% for CAT', 'The TypeScript engine matches the Python one within 0.01%'],
         stack=['Python', 'SEC XBRL', 'yfinance', 'FRED', 'React', 'TypeScript', 'Tailwind', 'd3'], code='https://github.com/ParBproject/dcf-valuation-model', live='https://parbproject.github.io/dcf-valuation-model/'),
    dict(img='esd_hero.png', w=1280, h=720, alt='Energy Sector Deep Dive explorer of oil and gas segments against oil', pos='left top', tags=['quant', 'analytics'],
         title='Energy Sector Deep Dive',
         desc='How 18 US oil and gas companies in five segments moved with oil from 2015 on. Fundamentals count from the SEC filing date, not the period end.',
         bullets=['Producers have the highest oil beta, 0.55 per 1% WTI move, against 0.27 for refiners', 'Producers fell 78.7% in the 2020 crash', 'Clustering on fundamentals mostly recovers the segments (adjusted Rand index 0.61)', 'Same-week factors fit. Last week’s factors do not: out-of-sample R² is −3.7% to −7.7%', 'Same WTI series as the <a href="#featured" class="text-accent hover:underline">commodity forecaster</a>'],
         stack=['Python', 'React', 'ECharts'], code='https://github.com/ParBproject/energy-sector-deep-dive', live='https://parbproject.github.io/energy-sector-deep-dive/',
         extra=[('Findings', 'https://github.com/ParBproject/energy-sector-deep-dive/blob/main/docs/findings.md')]),
    dict(img='bay_board.png', w=1440, h=900, alt='Bayline dock-to-stage control board', pos='left top', tags=['analytics'],
         title='Bayline — Fulfillment Control',
         desc='A dock-to-stage case study on seeded data (seed 42), not a real warehouse. I use it to show the SQL and the before/after test.',
         bullets=['DuckDB marts with joins, RANK() OVER, and LAG', 'A Mann–Whitney test and a bootstrap CI on the median', 'On this seeded sample, median cycle time goes from 110 to 85 minutes'],
         stack=['SQL', 'DuckDB', 'Python'], code='https://github.com/ParBproject/E-commerce-Order-Fulfillment-Process-Improvement', live='https://parbproject.github.io/E-commerce-Order-Fulfillment-Process-Improvement/'),
    dict(img='stroke_models.png', w=1440, h=900, alt='Stroke casebook model comparison and holdout ROC', pos='left top', tags=['ml', 'analytics'],
         title='Stroke Casebook',
         desc='A holdout study of the public Kaggle stroke file: 249 strokes in 5,110 rows. The source population is not documented, so this is not a clinical tool.',
         bullets=['The split comes first, before any imputation', 'Age alone is close to the fuller logistic on ROC-AUC (0.834 vs 0.842). The difference includes zero', 'The fuller model does help ranking of the rare class: PR-AUC 0.271 vs 0.197 for age'],
         stack=['scikit-learn', 'statsmodels', 'pandas'], code='https://github.com/ParBproject/Stroke', live='https://parbproject.github.io/Stroke/'),
]

MORE = [
    ('Portfolio Risk & Credit-Risk Modeling', 'https://github.com/ParBproject/Portfolio-Risk-Analysis-Credit-Risk-Modeling', 'A written memo on a synthetic 1,000-loan book, with stress tests', 'Finance', None),
    ('FinTools Pro — Screener & Backtester', 'https://github.com/ParBproject/-Stock-Screener-Strategy-Backtester-Insider-Institutional-Signal-Tracker-', 'A Streamlit screener and backtester. Local app, no public demo', 'Quant', None),
    ('Algorithmic Trading Research Framework', 'https://github.com/ParBproject/algo-trading-consultant', 'Backtests for mean reversion, momentum, and pairs. Research code, not a live trader', 'Quant', None),
    ('Generative AI Data', 'https://github.com/ParBproject/Generative-AI-Data', 'Small browser demos: sentiment, a churn what-if, and a storytelling page', 'Demo', 'https://parbproject.github.io/Generative-AI-Data/'),
]


CASES = [
    dict(title='DCF Valuation Model', code='https://github.com/ParBproject/dcf-valuation-model', live='https://parbproject.github.io/dcf-valuation-model/',
         q='How far are AAPL, MSFT, KO, JNJ, CAT, and XOM from a plain DCF, and what growth does the price imply?',
         m='Free cash flow to the firm from SEC XBRL 10-Ks. Revenue growth fades over 10 years. WACC uses a Blume-adjusted 5-year beta, a 5.13% Treasury yield (FRED DGS10), and a 4.23% Damodaran equity risk premium. I also run a sensitivity grid, a 10,000-draw Monte Carlo, and a reverse DCF. The TypeScript port matches Python within 0.01%.',
         f='The model is below the market for most names. AAPL is $122.18 against $348.22, and CAT is $279.82 against $704.05. XOM is the only one above its price ($216.26 vs $178.23), and 71.9% of the Monte Carlo draws put value above the price. The reverse DCF says the prices imply about 20.1% 10-year revenue growth for AAPL and 20.3% for CAT. I left that gap as it is.'),
    dict(title='UNH Equity Pitch', code='https://github.com/ParBproject/stock-pitch', live='https://parbproject.github.io/stock-pitch/',
         q='Is there a long case for UnitedHealth at $367.08 on 30 Sep 2026? The name came off a scored screen.',
         m='A two-stage FCF DCF. Bear, base, and bull growth come from the stock\'s own rolling FCF history. The discount rate is a CAPM cost of equity. I also fit Fama-French five factors plus momentum, look at peer comps, and test a walk-forward trend signal after 10 bp of costs. The files are frozen and hashed.',
         f='The base case is $526.64, about 43.5% above the price, in a range of $354.47 to $764.68. The price implies 6.0% stage-1 FCF growth, against 13.7% in the base case. With the full-sample beta of 0.78, the value falls to $321.29, 12.5% below the price. The trend signal (Sharpe 0.29) and buy-and-hold (0.49) both trail SPY (0.87).'),
    dict(title='Energy Sector Deep Dive', code='https://github.com/ParBproject/energy-sector-deep-dive', live='https://parbproject.github.io/energy-sector-deep-dive/',
         q='How do five US oil and gas segments trade against oil, and does anything else help once you know that?',
         m='Eighteen companies from 2015 on. Oil betas use HAC standard errors. Fundamentals are dated to the SEC filing, not the period end. I cluster on those fundamentals and run a weekly factor model walk-forward against an expanding mean. Companies that did not survive are listed in the config.',
         f='Producers are the most oil-sensitive segment (beta 0.55 per 1% WTI move, HAC t = 9.1) and refiners the least (0.27). Producers fell 78.7% in the 2020 crash. Clustering mostly recovers the segments (adjusted Rand index 0.61). Same-week factors explain 53.3% to 67.6% of segment returns out of sample. Last week\'s factors do not: out-of-sample R² is −3.7% to −7.7%.'),
    dict(title='Portfolio Risk Lab', code='https://github.com/ParBproject/portfolio-risk-lab', live='https://parbproject.github.io/portfolio-risk-lab/',
         q='Do mean-variance, risk parity, or Black-Litterman beat a simple benchmark on 21 ETFs, once the test is walk-forward and costs are paid?',
         m='Each month\'s weights use only the prior 60 months. Covariance is shrunk halfway to its diagonal. Long-only, 30% cap, 10 bp per unit of turnover. I report historical 95% VaR and CVaR, drawdowns, and a Fama-French five-factor plus momentum regression. The in-browser allocator is tested against the Python numbers.',
         f='From May 2012 to Sep 2026, no optimizer beat SPY (Sharpe 0.92) or 60/40 (0.84). Mean-variance reached 0.76. Risk parity cut max drawdown to −12.72% from −23.93% for SPY, with volatility of 5.45% versus 14.03%. No strategy has a significant alpha. Mean-variance is −2.20% a year, t = −1.63.'),
    dict(title='SPY Volatility Surface', code='https://github.com/ParBproject/options-vol-surface', live='https://parbproject.github.io/options-vol-surface/',
         q='What does one real SPY option chain imply for volatility, and can an SVI curve fit it without arbitrage?',
         m='Black-Scholes-Merton, with Brent root-finding for implied vol. Quotes are out-of-the-money prints from the 22 Oct 2026 close. The rate is 4.02% and the dividend yield is 1.22%. Each expiry gets its own raw SVI fit, then a butterfly check and a calendar check.',
         f='The snapshot has 1,077 quotes across 11 expiries, from 7 to 603 days. ATM implied vol goes from 15.75% at 7 days to 18.39% at 603 days, and is lowest at 14.52% (39 days). Put skew falls from 26.12 to 3.24 vol points. SVI error is 0.22 to 0.67 vol points, and all 11 slices pass the butterfly check. 49 of 1,210 calendar points fail, all outside the quoted strikes.'),
    dict(title='Volatility Forecasting (HAR vs ML)', code='https://github.com/ParBproject/vol-forecast-ml', live='https://parbproject.github.io/vol-forecast-ml/',
         q='Can gradient boosting or a small LSTM forecast next-day realized volatility for SPY and nine sector ETFs better than HAR-RV and GARCH(1,1)?',
         m='Walk-forward, 3,473 out-of-sample days per ETF, 2 Jan 2013 to 22 Oct 2026. I score QLIKE and MSE, and run Diebold-Mariano tests against HAR. The README figures are written from results/summary.json.',
         f='On QLIKE the LSTM is best on all 10 ETFs (mean 0.2968 vs 0.3262 for HAR, −9.0%) and significantly better on 8 of 10. Gradient boosting is level with HAR (−0.3%). GARCH is worse, significantly so on 7. On MSE, nothing is significantly different from HAR. The worst five days are 40% to 94% of HAR\'s squared error, so the LSTM edge is not a better call on the spikes.'),
    dict(title='Portfolio Risk &amp; Performance Analyzer', code='https://github.com/ParBproject/portfolio-risk-performance-analyzer', live='https://parbproject.github.io/portfolio-risk-performance-analyzer/',
         q='How does a six-ETF portfolio (SPY, EFA, AGG, TLT, GLD, VNQ) compare with holding SPY, from 2006 to 2026?',
         m='Total returns from a hashed Yahoo snapshot, loaded into SQLite. Eleven SQL queries are checked against pandas. Equal weight is rebalanced monthly. Minimum variance is re-estimated each month from the trailing 252 days only. Both pay 10 bp one-way costs.',
         f='From 4 Jan 2006 to 30 Sep 2026, equal weight cut volatility from 19.20% to 11.11% and max drawdown from −55.2% to −32.2%, and gave up about four points of return a year (7.08% vs 11.07%). Sharpe was 0.52 vs 0.55. Minimum variance, from Feb 2007, averaged 88% in AGG, with the lowest volatility (5.38%) and the lowest Sharpe (0.35). Lower risk, not a better Sharpe.'),
]

def case(c):
    def para(label, text):
        return f'<div><p class="font-mono text-[11px] uppercase tracking-wider text-accent">{label}</p><p class="mt-2 text-[14.5px] leading-relaxed text-slate-300">{text}</p></div>'
    return f'''
          <article class="pcard p-6 sm:p-8">
            <div class="flex flex-wrap items-baseline justify-between gap-3">
              <h3 class="text-xl font-semibold tracking-tight text-white">{c['title']}</h3>
              <div class="flex flex-wrap items-center gap-x-5 gap-y-2"><a href="{c['code']}" class="link-main">{GH} Code</a><a href="{c['live']}" class="link-main">Live demo {EXT}</a></div>
            </div>
            <div class="mt-6 grid gap-6 md:grid-cols-3">{para('Question', c['q'])}{para('Method', c['m'])}{para('Findings', c['f'])}</div>
          </article>'''

def card(c):
    tags = ''.join(f'<span class="chip">{TAGNAMES[t]}</span>' for t in c['tags'])
    bullets = ''.join(f'<li class="flex gap-2.5">{CHECK}<span>{b}</span></li>' for b in c['bullets'])
    stack = ' · '.join(c['stack'])
    live = f'<a href="{c["live"]}" class="link-main">Live demo {EXT}</a>' if c.get('live') else ''
    live += ''.join(f'<a href="{u}" class="link-main">{n} {EXT}</a>' for n, u in c.get('extra', []))
    return f'''
          <article class="pcard group" data-tags="{' '.join(c['tags'])}">
            <a href="{c['code']}" class="thumb-wrap" aria-label="{html.escape(c['title'])} repository">
              <img src="assets/{c['img']}" alt="{c['alt']}" width="{c['w']}" height="{c['h']}" loading="lazy" decoding="async" style="object-position:{c['pos']}" />
            </a>
            <div class="flex flex-1 flex-col p-6">
              <div class="flex flex-wrap gap-1.5">{tags}</div>
              <h3 class="mt-4 text-lg font-semibold tracking-tight text-white">{c['title']}</h3>
              <p class="mt-2 text-[14.5px] leading-relaxed text-slate-400">{c['desc']}</p>
              <ul class="mt-4 space-y-2 text-sm leading-snug text-slate-300">{bullets}</ul>
              <div class="mt-auto pt-6">
                <p class="font-mono text-[11px] tracking-wide text-slate-400">{stack}</p>
                <div class="mt-4 flex flex-wrap items-center gap-x-5 gap-y-2 border-t border-white/[0.06] pt-4">
                  <a href="{c['code']}" class="link-main">{GH} Code</a>{live}
                </div>
              </div>
            </div>
          </article>'''

def more(m):
    name, url, desc, tag, live = m
    livehtml = f'<a href="{live}" class="link-sub text-xs">Live {EXT}</a>' if live else ''
    return f'''
            <li class="more-row">
              <div class="min-w-0">
                <a href="{url}" class="font-medium text-slate-200 hover:text-white">{name}</a>
                <p class="mt-0.5 text-sm text-slate-400">{desc}</p>
              </div>
              <div class="flex shrink-0 items-center gap-3"><span class="font-mono text-[10.5px] uppercase tracking-wider text-slate-400">{tag}</span>{livehtml}</div>
            </li>'''

tpl = (D/'src'/'template.html').read_text()
out = tpl.replace('{{CARDS}}', ''.join(card(c) for c in CARDS)).replace('{{CASES}}', ''.join(case(c) for c in CASES)).replace('{{MORE}}', ''.join(more(m) for m in MORE))
out = out.replace('{{GH}}', GH).replace('{{EXT}}', EXT).replace('{{ARROW}}', ARROW).replace('{{CHECK}}', CHECK)
(D/'index.html').write_text(out)
print('wrote', D/'index.html', len(out))
