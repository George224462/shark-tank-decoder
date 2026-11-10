# ============================================================
# PROJECT: Shark Tank Decoder
# FILE: python/clean_data.py
# PURPOSE: Standardize dataset & populate pitch_analytics table
# ============================================================

import pandas as pd
import sqlite3
import os

raw_path = r"C:\Users\pc\shark-tank-decoder\data\raw\shark_tank_raw.csv"
db_path = r"C:\Users\pc\shark-tank-decoder\data\shark_tank.db"
processed_dir = r"C:\Users\pc\shark-tank-decoder\data\processed"
processed_csv = os.path.join(processed_dir, "pitch_analytics_clean.csv")

os.makedirs(processed_dir, exist_ok=True)

print("📂 Loading Shark Tank dataset...")
df = pd.read_csv(raw_path)

# Helper function to clean numeric strings
def clean_val(val):
    if pd.isna(val):
        return 0.0
    s = str(val).replace('$', '').replace('%', '').replace(',', '').strip()
    try:
        return float(s)
    except:
        return 0.0

# 1. Standardize Metadata
clean_df = pd.DataFrame()
clean_df['pitch_id'] = range(1, len(df) + 1)

# Find Company/Startup column
comp_col = [c for c in df.columns if 'name' in c.lower() or 'company' in c.lower() or 'startup' in c.lower()][0]
clean_df['company_name'] = df[comp_col].fillna('Unknown')

# Find Industry column
ind_col = [c for c in df.columns if 'industry' in c.lower()][0]
clean_df['industry'] = df[ind_col].fillna('General')

# Season
season_col = [c for c in df.columns if 'season' in c.lower()][0]
clean_df['season'] = df[season_col].apply(clean_val).astype(int)

# 2. Financial Ask Columns
ask_amt_col = [c for c in df.columns if 'ask' in c.lower() and 'amount' in c.lower()][0]
ask_eq_col = [c for c in df.columns if 'ask' in c.lower() or 'offered' in c.lower()][0]

clean_df['ask_amount_usd'] = df[ask_amt_col].apply(clean_val)
clean_df['ask_equity_pct'] = df[ask_eq_col].apply(clean_val)

# Implied Ask Valuation = Ask Amount / (Equity / 100)
clean_df['implied_ask_valuation_usd'] = clean_df.apply(
    lambda r: round(r['ask_amount_usd'] / (r['ask_equity_pct'] / 100.0), 2) if r['ask_equity_pct'] > 0 else 0.0, axis=1
)

# 3. Deal Outcome (Got Offer or Accepted Offer)
deal_cols = [c for c in df.columns if 'got_offer' in c.lower() or 'accepted_offer' in c.lower() or 'deal' in c.lower()]
if deal_cols:
    clean_df['deal_made'] = df[deal_cols[0]].apply(lambda x: 1 if clean_val(x) > 0 or str(x).strip().lower() in ['yes', 'true', '1'] else 0)
else:
    clean_df['deal_made'] = 0

# 4. Actual Deal Amounts
deal_amt_cols = [c for c in df.columns if 'deal' in c.lower() and 'amount' in c.lower()]
deal_eq_cols = [c for c in df.columns if 'deal' in c.lower() and 'equity' in c.lower()]

clean_df['deal_amount_usd'] = df[deal_amt_cols[0]].apply(clean_val) if deal_amt_cols else 0.0
clean_df['deal_equity_pct'] = df[deal_eq_cols[0]].apply(clean_val) if deal_eq_cols else 0.0

# 5. Shark Investment Flags
sharks = {
    'Mark_Cuban': ['mark'],
    'Lori_Greiner': ['lori'],
    'Kevin_OLeary': ['kevin', 'o_leary', 'oleary'],
    'Daymond_John': ['daymond'],
    'Barbara_Corcoran': ['barbara'],
    'Robert_Herjavec': ['robert']
}

for shark_name, keys in sharks.items():
    # Find columns indicating investment by this shark
    matching_cols = [c for c in df.columns if any(k in c.lower() for k in keys) and ('investment' in c.lower() or 'amount' in c.lower())]
    if matching_cols:
        clean_df[shark_name] = df[matching_cols[0]].apply(lambda x: 1 if clean_val(x) > 0 else 0)
    else:
        clean_df[shark_name] = 0

# Save to SQLite database
conn = sqlite3.connect(db_path)
clean_df.to_sql("pitch_analytics", conn, if_exists="replace", index=False)
conn.close()

# Save CSV for Tableau
clean_df.to_csv(processed_csv, index=False)

print("\n" + "="*55)
print("✅ DATA PIPELINE SUCCESSFUL!")
print(f"Total Clean Records Processed: {len(clean_df):,}")
print(f"Total Deals Funded: {clean_df['deal_made'].sum():,} ({clean_df['deal_made'].mean()*100:.2f}% deal rate)")
print(f"Average Ask Amount: ${clean_df['ask_amount_usd'].mean():,.2f}")
print("="*55)