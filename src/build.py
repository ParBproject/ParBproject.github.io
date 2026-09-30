# Generates ../index.html (v2). Content sourced from ParBproject repo READMEs.
import pathlib, html
D = pathlib.Path(__file__).resolve().parent.parent

GH = '<svg class="h-4 w-4" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'
EXT = '<svg class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M11 3a1 1 0 100 2h2.59l-6.3 6.29a1 1 0 101.42 1.42L15 6.41V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"/><path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z"/></svg>'
ARROW = '<svg class="h-4 w-4 transition-transform group-hover:translate-x-0.5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M10.3 3.3a1 1 0 011.4 0l6 6a1 1 0 010 1.4l-6 6a1 1 0 01-1.4-1.4L14.58 11H3a1 1 0 110-2h11.59l-4.3-4.3a1 1 0 010-1.4z" clip-rule="evenodd"/></svg>'
CHECK = '<svg class="mt-0.5 h-4 w-4 shrink-0 text-accent" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M16.7 5.3a1 1 0 010 1.4l-8 8a1 1 0 01-1.4 0l-4-4a1 1 0 011.4-1.4L8 12.58l7.3-7.3a1 1 0 011.4 0z" clip-rule="evenodd"/></svg>'

TAGNAMES = {'forecasting': 'Forecasting', 'quant': 'Quant / Finance', 'ml': 'ML', 'analytics': 'Analytics', 'tools': 'Tools'}

CARDS = [
    dict(img='afm_dashboard.png', w=1600, h=1004, alt='Dark-theme Streamlit dashboard for Advanced Financial Models', pos='left top', tags=['quant', 'forecasting'],
         title='Advanced Financial Modeling Suite',
         desc='Excel workbook, a tested Python modeling core and a Streamlit dashboard for liquidity, credit and portfolio risk.',
         bullets=['Expected loss = EAD × PD × LGD, with capped stress scenarios', 'HHI concentration and covariance-aware wᵀΣw risk', 'Seeded Monte Carlo; numerical regression tests in CI', 'Zero-correlation baseline: volatility 6.82%, Sharpe ratio 0.83. Dashboard headline is covariance-aware volatility 9.68%. NPV of monthly net cash flows of $410,751.'],
         stack=['Python', 'Excel', 'Streamlit'], code='https://github.com/ParBproject/Advanced-Financial-Models', live='https://parbproject.github.io/Advanced-Financial-Models/'),
    dict(img='spp_lstm.png', w=2082, h=1183, alt='LSTM predicted vs actual close price', pos='left top', tags=['ml', 'forecasting'],
         title='Stock Price Predictor',
         desc='Next-day forecasting with LSTM vs Random Forest, then checked in a Backtrader workflow.',
         bullets=['Explicit t+1 targets and train-only scaling', 'No future-news leakage in sentiment features', 'Commission-aware sizing; regression tests in CI'],
         stack=['TensorFlow', 'scikit-learn', 'Backtrader'], code='https://github.com/ParBproject/stock-price-predictor', live='https://parbproject.github.io/stock-price-predictor/'),
    dict(img='po_frontier.png', w=1809, h=1182, alt='Markowitz efficient frontier', pos='center', tags=['quant'],
         title='Markowitz Portfolio Optimizer',
         desc='Interactive mean-variance optimization with an efficient frontier, diagnostics and backtesting.',
         bullets=['Constrained optimization with CVXPY', 'Global minimum-variance & max-Sharpe portfolios', 'Backtest against an equal-weight benchmark'],
         stack=['CVXPY', 'Plotly', 'Streamlit'], code='https://github.com/ParBproject/Portfolio-Optimizer', live='https://parbproject.github.io/Portfolio-Optimizer/'),
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
    dict(img='skycast.svg', w=1440, h=900, alt='SkyCast weather intelligence dashboard', pos='left top', tags=['tools'],
         title='SkyCast',
         desc='Installable weather and air-quality dashboard on Open-Meteo — no framework, backend or API key.',
         bullets=['Validated, normalized multi-API payloads', 'PWA with offline shell and labeled fallbacks', 'Node + Python tests, CI, GitHub Pages'],
         stack=['JavaScript', 'SVG', 'PWA'], code='https://github.com/ParBproject/skycast', live='https://parbproject.github.io/skycast/'),
]

MORE = [
    ('AI-Investment-Dashboard', 'https://github.com/ParBproject/AI-Investment-Dashboard', 'Efficient frontier, Monte Carlo, Black–Scholes and what-if scenarios', 'Quant', None),
    ('Portfolio Risk & Credit-Risk Modeling', 'https://github.com/ParBproject/Portfolio-Risk-Analysis-Credit-Risk-Modeling', 'Credit memo on a synthetic 1,000-loan book with stress testing', 'Finance', None),
    ('FinTools Pro — Screener & Backtester', 'https://github.com/ParBproject/-Stock-Screener-Strategy-Backtester-Insider-Institutional-Signal-Tracker-', 'Factor screening, strategy backtests, insider/institutional signals', 'Quant', None),
    ('Algorithmic Trading Research Framework', 'https://github.com/ParBproject/algo-trading-consultant', 'Indicators, backtesting, grid/Bayesian search, walk-forward review', 'Quant', None),
    ('Crypto Trading Bot', 'https://github.com/ParBproject/Crypto-Trading-Bot', 'LSTM signals, risk controls and a paper-trading research system', 'ML', None),
    ('Generative AI Data', 'https://github.com/ParBproject/Generative-AI-Data', 'Browser demos: in-browser transformer sentiment, churn, storytelling', 'AI', 'https://parbproject.github.io/Generative-AI-Data/'),
    ('denly-uptime', 'https://github.com/ParBproject/denly-uptime', 'Off-host GitHub Actions uptime probe for denlyai.com, every 5 min', 'Tools', None),
    ('Cosmic Clock', 'https://github.com/ParBproject/-A-Real-Time-Astronomical-Cosmological-Timepiece-', 'Real-time sky map and cosmic timeline with Skyfield & Astropy', 'Tools', None),
]

def card(c):
    tags = ''.join(f'<span class="chip">{TAGNAMES[t]}</span>' for t in c['tags'])
    bullets = ''.join(f'<li class="flex gap-2.5">{CHECK}<span>{b}</span></li>' for b in c['bullets'])
    stack = ' · '.join(c['stack'])
    live = f'<a href="{c["live"]}" class="link-main">Live demo {EXT}</a>' if c.get('live') else ''
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
                <div class="mt-4 flex items-center gap-5 border-t border-white/[0.06] pt-4">
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
out = tpl.replace('{{CARDS}}', ''.join(card(c) for c in CARDS)).replace('{{MORE}}', ''.join(more(m) for m in MORE))
out = out.replace('{{GH}}', GH).replace('{{EXT}}', EXT).replace('{{ARROW}}', ARROW).replace('{{CHECK}}', CHECK)
(D/'index.html').write_text(out)
print('wrote', D/'index.html', len(out))
