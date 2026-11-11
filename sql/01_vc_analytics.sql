-- ============================================================
-- SHARK TANK VC ANALYTICS: EXPLORATORY SQL QUERIES
-- Database: C:\Users\pc\shark-tank-decoder\data\shark_tank.db
-- Table: pitch_analytics
-- ============================================================

-- Query 1: Overall Deal Success Rate & Total Capital Deployed
SELECT 
    COUNT(*) AS total_pitches,
    SUM(deal_made) AS total_deals,
    ROUND(AVG(deal_made) * 100.0, 2) AS deal_success_rate_pct,
    ROUND(AVG(ask_amount_usd), 2) AS avg_ask_amount,
    ROUND(AVG(deal_amount_usd), 2) AS avg_deal_amount
FROM pitch_analytics;

-- Query 2: Male vs Female vs Mixed Founder Deal Rates
SELECT 
    CASE 
        WHEN pitch_males > 0 AND pitch_females = 0 THEN 'Male Only'
        WHEN pitch_females > 0 AND pitch_males = 0 THEN 'Female Only'
        WHEN pitch_males > 0 AND pitch_females > 0 THEN 'Mixed Team'
        ELSE 'Unknown'
    END AS founder_team_type,
    COUNT(*) AS pitch_count,
    SUM(deal_made) AS deals_won,
    ROUND(AVG(deal_made) * 100.0, 2) AS success_rate_pct
FROM pitch_analytics
GROUP BY founder_team_type
ORDER BY success_rate_pct DESC;

-- Query 3: Equity Dilution Analysis (Difference between Asked Equity and Given Equity)
SELECT 
    industry,
    COUNT(*) AS total_deals,
    ROUND(AVG(ask_equity_pct), 2) AS avg_asked_equity,
    ROUND(AVG(deal_equity_pct), 2) AS avg_given_equity,
    ROUND(AVG(deal_equity_pct - ask_equity_pct), 2) AS avg_equity_surrendered
FROM pitch_analytics
WHERE deal_made = 1
GROUP BY industry
HAVING COUNT(*) >= 10
ORDER BY avg_equity_surrendered DESC;

-- Query 4: Shark Investment Volume Leaderboard
SELECT 
    'Mark Cuban' AS shark_name, SUM(mark_cuban) AS deals_made FROM pitch_analytics
UNION ALL
SELECT 'Lori Greiner', SUM(lori_greiner) FROM pitch_analytics
UNION ALL
SELECT 'Robert Herjavec', SUM(robert_herjavec) FROM pitch_analytics
UNION ALL
SELECT 'Barbara Corcoran', SUM(barbara_corcoran) FROM pitch_analytics
UNION ALL
SELECT 'Kevin OLeary', SUM(kevin_oleary) FROM pitch_analytics
UNION ALL
SELECT 'Daymond John', SUM(daymond_john) FROM pitch_analytics
ORDER BY deals_made DESC;