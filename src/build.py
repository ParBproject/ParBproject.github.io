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
         desc='Does a diversified ETF portfolio beat an equity benchmark on return, risk and drawdowns? Equal-weight and minimum-variance portfolios of six ETFs against SPY, 2006 to 2026, with weights estimated from past data only and costs included.',
         bullets=['Reproducible pipeline: adjusted prices frozen with checksums, cleaned and stored in SQLite with SQL analysis queries', 'Equal weight halves SPY volatility and cuts max drawdown from -55.2% to -32.2%, but Sharpe is about even (0.52 vs 0.55)', 'Minimum variance has the lowest risk but the worst Sharpe (0.35), drifting into bonds', 'Streamlit dashboard with date filters, weights and risk summary; 114 pytest tests'],
         stack=['Python', 'pandas', 'NumPy', 'SQLite', 'Plotly', 'Streamlit', 'pytest'], code='https://github.com/ParBproject/portfolio-risk-performance-analyzer', live='https://parbproject.github.io/portfolio-risk-performance-analyzer/'),
    dict(img='vfm_overview.png', w=1440, h=900, alt='Volatility forecasting app comparing realized SPY volatility with HAR and LSTM forecasts, loss tables and Diebold-Mariano tests', pos='left top', tags=['ml', 'forecasting'],
         title='Volatility Forecasting: HAR vs ML',
         desc='One-day-ahead realized-volatility forecasts for SPY and 9 sector ETFs: HAR-RV and GARCH(1,1) against gradient boosting and an LSTM, strictly walk-forward (2013-01 to 2026-10), with no tuning.',
         bullets=['LSTM mean QLIKE 9.0% below HAR, lowest on 10 of 10 ETFs; significant (Diebold-Mariano, 5%) on 8', 'Honest result on MSE: no model significantly beats HAR on any ETF, because a few crash days dominate the loss', 'Gradient boosting roughly ties HAR (-0.3% QLIKE); GARCH significantly worse than HAR on 7 of 10', 'No-lookahead tests: scrambling all future data leaves every past forecast bit-identical'],
         stack=['Python', 'PyTorch', 'scikit-learn', 'arch', 'React', 'Vite'], code='https://github.com/ParBproject/vol-forecast-ml', live='https://parbproject.github.io/vol-forecast-ml/'),
    dict(img='prl_overview.png', w=1440, h=900, alt='Portfolio Risk Lab allocator with strategy controls, equity curve, weights and risk metrics', pos='left top', tags=['quant'],
         title='Portfolio Risk Lab',
         desc='Mean-variance, risk parity and Black-Litterman on a 21-ETF multi-asset universe, tested walk-forward against SPY, 60/40 and 1/N after trading costs (2012-05 to 2026-09).',
         bullets=['Honest result: no optimizer beat SPY (Sharpe 0.92) or 60/40 (0.84); mean-variance reached 0.76', 'Risk parity cut max drawdown to -12.72% vs -23.93% for SPY', 'VaR/CVaR, drawdowns and Fama-French 5 + momentum attribution; no significant alpha (all |t| &lt; 2)', 'Interactive allocator recomputes every metric in the browser, tested to match Python'],
         stack=['Python', 'NumPy', 'SciPy', 'pandas', 'React', 'Vite'], code='https://github.com/ParBproject/portfolio-risk-lab', live='https://parbproject.github.io/portfolio-risk-lab/'),
    dict(img='ovs_overview.png', w=1440, h=900, alt='SPY implied-volatility surface app with a 3D SVI surface, term structure and skew', pos='left top', tags=['quant'],
         title='SPY Volatility Surface',
         desc='Black-Scholes pricing and Greeks, implied-vol solving and an SVI-fitted surface from a real SPY option-chain snapshot (close of 2026-10-22), with arbitrage checks.',
         bullets=['1,077 out-of-the-money quotes across 11 expiries (7 to 603 days)', 'ATM implied vol 15.75% at 7 days rising to 18.39% at 603 days', 'SVI fit error 0.22 to 0.67 vol points; butterfly-arbitrage-free on 11 of 11 expiries', '49 of 1,210 calendar-check points fail, all from SVI extrapolation beyond the quoted strikes'],
         stack=['Python', 'SciPy', 'yfinance', 'React', 'Vite', 'Canvas'], code='https://github.com/ParBproject/options-vol-surface', live='https://parbproject.github.io/options-vol-surface/'),
    dict(img='sp_panel.png', w=1280, h=800, alt='UNH long pitch scenario panel with beta toggle, FCF fan chart and value heatmap', pos='left top', tags=['quant'],
         title='UNH Equity Pitch',
         desc='A long call built like a quant research project: a long thesis on UnitedHealth, built from frozen, hash-checked data.',
         bullets=['DCF and reverse DCF, Fama-French factors, comps and risk metrics', 'Walk-forward backtest against SPY', 'Interactive deck with a live scenario panel', 'Every number generated by code and pinned by tests, including the risk that weakens the call: the full-sample beta moves the base case below the price'],
         stack=['Python', 'pandas', 'statsmodels', 'Vite', 'ECharts', 'Playwright'], code='https://github.com/ParBproject/stock-pitch', live='https://parbproject.github.io/stock-pitch/',
         extra=[('PDF deck', 'https://parbproject.github.io/stock-pitch/deck/pitch.pdf')]),
    dict(img='dcf_overview.png', w=1440, h=1222, alt='DCF Valuation Model overview with valuations for six large caps', pos='left top', tags=['quant'],
         title='DCF Valuation Model',
         desc='Interactive DCF valuation of six large caps, built from SEC filings, with live sliders, scenarios, sensitivity heatmaps and a 10,000-draw Monte Carlo.',
         bullets=['AAPL valued at $122.18 vs a $348.22 price', 'XOM is the only stock valued above its price ($216.26 vs $178.23; 71.9% chance its value exceeds it)', 'Reverse DCF: prices imply about 20% 10-year revenue growth for AAPL and CAT', 'TypeScript engine matches the Python one within 0.01%'],
         stack=['Python', 'SEC XBRL', 'yfinance', 'FRED', 'React', 'TypeScript', 'Tailwind', 'd3'], code='https://github.com/ParBproject/dcf-valuation-model', live='https://parbproject.github.io/dcf-valuation-model/'),
    dict(img='esd_hero.png', w=1280, h=720, alt='Energy Sector Deep Dive explorer of oil and gas segments against oil', pos='left top', tags=['quant', 'analytics'],
         title='Energy Sector Deep Dive',
         desc='Point-in-time research on how 18 US oil and gas companies in 5 segments trade against oil from 2015 on, in a linked, shareable explorer with an oil-scenario tool.',
         bullets=['Producers have the highest oil beta: 0.55 vs 0.27 for refiners', 'Producers fell 78.7% in the 2020 crash', 'Clustering mostly rediscovers the segments (adjusted Rand index 0.61)', 'Walk-forward factor model honestly shows no next-week predictability', 'Companion to the <a href="#featured" class="text-accent hover:underline">commodity forecasting case study</a>'],
         stack=['Python', 'React', 'ECharts'], code='https://github.com/ParBproject/energy-sector-deep-dive', live='https://parbproject.github.io/energy-sector-deep-dive/',
         extra=[('Findings', 'https://github.com/ParBproject/energy-sector-deep-dive/blob/main/docs/findings.md')]),
    dict(img='bay_board.png', w=1440, h=900, alt='Bayline dock-to-stage control board', pos='left top', tags=['analytics'],
         title='Bayline — Fulfillment Control',
         desc='Three-building dock-to-stage case study: find the bottleneck, test a process change, price the labor.',
         bullets=['DuckDB SQL marts with JOINs, RANK() OVER, LAG', 'Mann–Whitney test and bootstrap CI on the median', 'Median cycle 110 → 85 min <span class="text-slate-400">(seeded, illustrative data)</span>'],
         stack=['SQL', 'DuckDB', 'Python'], code='https://github.com/ParBproject/E-commerce-Order-Fulfillment-Process-Improvement', live='https://parbproject.github.io/E-commerce-Order-Fulfillment-Process-Improvement/'),
    dict(img='stroke_models.png', w=1440, h=900, alt='Stroke casebook model comparison and holdout ROC', pos='left top', tags=['ml', 'analytics'],
         title='Stroke Casebook',
         desc='Holdout study of the public Kaggle stroke file (249 strokes in 5,110 rows), treated as a rare-event problem.',
         bullets=['Stratified split before any imputation', 'Baselines vs logistic, tree and random forest', 'PR-AUC, calibration (Brier) and an operating threshold'],
         stack=['scikit-learn', 'statsmodels', 'pandas'], code='https://github.com/ParBproject/Stroke', live='https://parbproject.github.io/Stroke/'),
]

MORE = [
    ('Portfolio Risk & Credit-Risk Modeling', 'https://github.com/ParBproject/Portfolio-Risk-Analysis-Credit-Risk-Modeling', 'Credit memo on a synthetic 1,000-loan book with stress testing', 'Finance', None),
    ('FinTools Pro — Screener & Backtester', 'https://github.com/ParBproject/-Stock-Screener-Strategy-Backtester-Insider-Institutional-Signal-Tracker-', 'Factor screening, strategy backtests, insider/institutional signals', 'Quant', None),
    ('Algorithmic Trading Research Framework', 'https://github.com/ParBproject/algo-trading-consultant', 'Indicators, backtesting, grid/Bayesian search, walk-forward review', 'Quant', None),
    ('Generative AI Data', 'https://github.com/ParBproject/Generative-AI-Data', 'Browser demos: in-browser transformer sentiment, churn, storytelling', 'AI', 'https://parbproject.github.io/Generative-AI-Data/'),
]


CASES = [
    dict(title='DCF Valuation Model', code='https://github.com/ParBproject/dcf-valuation-model', live='https://parbproject.github.io/dcf-valuation-model/',
         q='How far are six large US caps (AAPL, MSFT, KO, JNJ, CAT, XOM) from a mechanical, fully sourced DCF value, and what growth do their prices imply?',
         m='Free cash flow to the firm built from SEC EDGAR XBRL 10-K data, with revenue growth fading over 10 years to terminal growth and a terminal value that reinvests g/ROIC at 15% ROIC. WACC uses a Blume-adjusted 5-year regression beta, rf 5.13% (FRED DGS10) and a 4.23% Damodaran ERP. Risk comes from sensitivity grids, a 10,000-draw Monte Carlo and a reverse DCF. A TypeScript port matches the Python engine to 0.01% and runs live in the browser.',
         f='The model sits well below the market for most names: AAPL is valued at $122.18 against $348.22, and CAT at $279.82 against $704.05. XOM is the only stock valued above its price ($216.26 vs $178.23, with a 71.9% Monte Carlo probability that value exceeds price). The reverse DCF shows prices imply about 20.1% 10-year revenue growth for AAPL and 20.3% for CAT. The gap is analysed in a calibration review rather than tuned away.'),
    dict(title='UNH Equity Pitch', code='https://github.com/ParBproject/stock-pitch', live='https://parbproject.github.io/stock-pitch/',
         q='Is there a defensible long case for UnitedHealth at $367.08 (2026-09-30), chosen by a scored screen rather than picked to fit a story?',
         m='A two-stage FCF DCF with bear/base/bull scenarios from the stock\'s own rolling FCF growth, a reverse DCF, CAPM discounting, Fama-French five factors plus momentum with Newey-West t-stats, peer comps, and a walk-forward trend signal tested out-of-sample net of 10 bp costs. All data is frozen with SHA-256 manifests, and tests fail if a number does not come from the results file.',
         f='The base case is $526.64 (43.5% upside), with a range of $354.47 to $764.68, while the reverse DCF says the price implies 6.0% stage-1 FCF growth against 13.7% in the base case. The risks are stated plainly: with the full-sample beta of 0.78 the value drops to $321.29 (-12.5%), and the trend signal (Sharpe 0.29) and buy-and-hold (0.49) both trail SPY (0.87).'),
    dict(title='Energy Sector Deep Dive', code='https://github.com/ParBproject/energy-sector-deep-dive', live='https://parbproject.github.io/energy-sector-deep-dive/',
         q='How do the five segments of US oil and gas (majors, producers, midstream, refiners, services) trade against oil, and do fundamentals or factors tell you anything beyond that?',
         m='A point-in-time pipeline over 18 companies from 2015 on: HAC-robust oil-beta regressions, drawdowns in three shocks, fundamentals keyed to SEC filing dates, k-means and Ward clustering, and a weekly factor model evaluated walk-forward against an expanding-mean baseline. Survivorship bias is listed company by company.',
         f='Producers are the most oil-sensitive segment (beta 0.55 per 1% WTI move, HAC t = 9.1) and refiners the least (0.27); producers fell 78.7% in the 2020 crash. Clustering on fundamentals largely rediscovers the segments (adjusted Rand index 0.61). Same-week factors explain 53.3% to 67.6% of segment returns out-of-sample, but last week\'s factors give negative out-of-sample R² (-3.7% to -7.7%): no next-week predictability.'),
    dict(title='Portfolio Risk Lab', code='https://github.com/ParBproject/portfolio-risk-lab', live='https://parbproject.github.io/portfolio-risk-lab/',
         q='Do mean-variance, risk parity or Black-Litterman beat simple benchmarks on a 21-ETF multi-asset universe once you test walk-forward and pay trading costs?',
         m='Each month\'s weights use only the prior 60 months, with covariance shrunk 50% toward its diagonal, long-only with a 30% cap, and 10 bps per unit of turnover. Risk uses historical 95% VaR/CVaR and drawdowns, and returns are attributed to Fama-French 5 factors plus momentum. An in-browser allocator recomputes every metric and is tested to match Python.',
         f='Out-of-sample from 2012-05 to 2026-09, no optimizer beat SPY (Sharpe 0.92) or 60/40 (0.84); mean-variance reached 0.76. Risk parity cut max drawdown to -12.72% vs -23.93% for SPY, at 5.45% volatility vs 14.03%. No strategy shows significant alpha (all |t| &lt; 2; mean-variance -2.20% a year, t = -1.63).'),
    dict(title='SPY Volatility Surface', code='https://github.com/ParBproject/options-vol-surface', live='https://parbproject.github.io/options-vol-surface/',
         q='What does SPY\'s implied-volatility surface look like from a real option chain, and can a smooth SVI fit represent it without arbitrage?',
         m='Black-Scholes-Merton pricing with Brent root-finding for implied vol, filtered to out-of-the-money quotes from the 2026-10-22 close, using a 4.02% rate and a 1.22% dividend yield. Each expiry gets a raw SVI fit on total variance, then Gatheral butterfly and calendar arbitrage checks.',
         f='The snapshot has 1,077 OTM quotes across 11 expiries (7 to 603 days). ATM implied vol rises from 15.75% at 7 days to 18.39% at 603 days, with a low of 14.52% at 39 days, and put skew falls from 26.12 to 3.24 vol points. SVI errors are 0.22 to 0.67 vol points and all 11 slices are butterfly-arbitrage-free. 49 of 1,210 calendar-check points fail, all from SVI extrapolation outside the quoted strikes, and this is reported rather than hidden.'),
    dict(title='Volatility Forecasting (HAR vs ML)', code='https://github.com/ParBproject/vol-forecast-ml', live='https://parbproject.github.io/vol-forecast-ml/',
         q='Can gradient boosting or a small LSTM forecast next-day realized volatility for SPY and the nine SPDR sector ETFs better than the HAR-RV and GARCH(1,1) baselines?',
         m='A strictly walk-forward test over 3,473 out-of-sample trading days per ETF (2013-01-02 to 2026-10-22, 10 ETFs). Every model is scored with QLIKE and MSE, and Diebold-Mariano tests compare each one with HAR. Every README number is generated from the committed results/summary.json and pinned by tests.',
         f='On QLIKE the LSTM is best on 10 of 10 ETFs (mean 0.2968 vs 0.3262 for HAR, -9.0%) and significantly better than HAR on 8 of 10. Gradient boosting is level with HAR (-0.3%), and GARCH is worst (significantly worse on 7). On MSE no model is significantly different from HAR on any ETF: the worst 5 days make up 40% to 94% of HAR\'s MSE, so the LSTM edge is proportional, not a better read on volatility spikes.'),
    dict(title='Portfolio Risk &amp; Performance Analyzer', code='https://github.com/ParBproject/portfolio-risk-performance-analyzer', live='https://parbproject.github.io/portfolio-risk-performance-analyzer/',
         q='How does a diversified six-ETF portfolio (SPY, EFA, AGG, TLT, GLD, VNQ) compare with holding SPY alone in return, risk and drawdowns over 2006 to 2026?',
         m='Total-return Adj Close data from a SHA-256-verified Yahoo snapshot, loaded into SQLite with 11 SQL analysis queries tested against pandas. An equal-weight portfolio is rebalanced monthly, and a long-only minimum-variance portfolio is re-estimated each month from only the trailing 252 days, both paying 10 bp one-way costs. Sharpe, Sortino, drawdown, Calmar, beta and rolling metrics are computed in Python.',
         f='From 2006-01-04 to 2026-09-30, equal weight cut annualised volatility from 19.20% to 11.11% and max drawdown from -55.2% to -32.2%, giving up about 4 points of return a year (7.08% vs 11.07%). Its Sharpe was close to SPY\'s (0.52 vs 0.55). Minimum variance (2007-02 to 2026-09) held 88% AGG on average, reached the lowest volatility (5.38%) and the lowest Sharpe (0.35): diversification bought lower risk, not better risk-adjusted return.'),
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
