import type { AlertItem, Kpi, MarketPulse, ScreenerRow, WhaleChange } from "@/types";

export const kpis: Kpi[] = [
  { label: "Net worth", value: "₹48.24L", change: "+12.8%", tone: "positive", footnote: "vs. invested capital" },
  { label: "Invested capital", value: "₹32.61L", change: "+₹1.84L", tone: "positive", footnote: "30-day mark-to-market" },
  { label: "Portfolio alpha", value: "+6.4%", change: "+2.1%", tone: "positive", footnote: "vs. NIFTY 50 · 1Y" },
  { label: "Risk score", value: "67 / 100", change: "Moderate", tone: "warning", footnote: "concentration is elevated" },
];

export const marketPulse: MarketPulse[] = [
  { name: "NIFTY 50", value: "24,840.75", change: "+0.82%", tone: "positive" },
  { name: "SENSEX", value: "81,332.12", change: "+0.76%", tone: "positive" },
  { name: "BANK NIFTY", value: "56,112.40", change: "+1.28%", tone: "positive" },
  { name: "INDIA VIX", value: "13.42", change: "−3.06%", tone: "positive" },
  { name: "USD / INR", value: "85.67", change: "+0.14%", tone: "negative" },
];

export const whaleChanges: WhaleChange[] = [
  { name: "Mukul Agrawal", category: "Investor", action: "Added", holding: "Radico Khaitan", change: "+1.2%", signal: "positive", date: "Today" },
  { name: "Dolly Khanna", category: "Investor", action: "Trimmed", holding: "Mahanagar Gas", change: "−0.8%", signal: "warning", date: "Today" },
  { name: "Parag Parikh Flexi Cap", category: "Mutual fund", action: "New buy", holding: "HDFC AMC", change: "0.6%", signal: "positive", date: "Yesterday" },
  { name: "SBI Mutual Fund", category: "Mutual fund", action: "Exited", holding: "Zydus Lifesciences", change: "0.0%", signal: "negative", date: "Yesterday" },
  { name: "Ashish Kacholia", category: "Investor", action: "Added", holding: "SJS Enterprises", change: "+0.5%", signal: "positive", date: "18 Jun" },
];

export const alerts: AlertItem[] = [
  { id: "a1", type: "Smart money", title: "Mukul Agrawal added Radico Khaitan", description: "Position increased by an estimated 1.2% of portfolio.", time: "9 min ago", severity: "positive", unread: true },
  { id: "a2", type: "Portfolio risk", title: "IT sector crossed 34% allocation", description: "Your target band is 20–30%. Review concentration before adding.", time: "36 min ago", severity: "warning", unread: true },
  { id: "a3", type: "Corporate action", title: "TCS dividend record date approaching", description: "Record date is 26 Jun 2026. Expected dividend ₹11 / share.", time: "2 hr ago", severity: "neutral", unread: false },
  { id: "a4", type: "Fin-Debunk", title: "High-risk claim flagged: ABC Textiles", description: "Urgency language and volume anomaly detected; 4 of 7 checks failed.", time: "Yesterday", severity: "negative", unread: false },
];

export const screenerRows: ScreenerRow[] = [
  { ticker: "HDFCAMC", company: "HDFC Asset Management", sector: "Financials", price: "₹4,765", return30d: "+14.8%", composite: 92, quality: 90, momentum: 95, valuation: "Fair" },
  { ticker: "POLYCAB", company: "Polycab India", sector: "Industrials", price: "₹6,142", return30d: "+11.2%", composite: 88, quality: 92, momentum: 86, valuation: "Fair" },
  { ticker: "RADICO", company: "Radico Khaitan", sector: "Consumer", price: "₹2,412", return30d: "+9.4%", composite: 86, quality: 84, momentum: 89, valuation: "Rich" },
  { ticker: "CERA", company: "Cera Sanitaryware", sector: "Consumer", price: "₹7,891", return30d: "+7.6%", composite: 82, quality: 87, momentum: 77, valuation: "Fair" },
  { ticker: "KPITTECH", company: "KPIT Technologies", sector: "Technology", price: "₹1,421", return30d: "−2.1%", composite: 78, quality: 91, momentum: 64, valuation: "Rich" },
];

export const chartValues = [42, 39, 44, 43, 48, 52, 50, 57, 55, 61, 64, 60, 68, 66, 72, 75, 73, 79, 82, 78, 84, 87, 85, 92];
