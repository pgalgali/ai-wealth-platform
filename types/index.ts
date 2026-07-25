export type Workspace = "Overview" | "Copilot" | "Whale Watch" | "Screener" | "Portfolio" | "Alerts";

export type Tone = "positive" | "negative" | "neutral" | "warning";

export interface Kpi { label: string; value: string; change: string; tone: Tone; footnote: string; }
export interface MarketPulse { name: string; value: string; change: string; tone: Tone; }
export interface WhaleChange { name: string; category: string; action: string; holding: string; change: string; signal: Tone; date: string; }
export interface AlertItem { id: string; type: string; title: string; description: string; time: string; severity: Tone; unread: boolean; }
export interface ScreenerRow { ticker: string; company: string; sector: string; price: string; return30d: string; composite: number; quality: number; momentum: number; valuation: string; }
