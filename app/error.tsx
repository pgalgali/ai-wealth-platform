"use client";

export default function GlobalError({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return <main style={{ minHeight: "100vh", display: "grid", placeItems: "center", background: "#0b0e0f", color: "#f0f5f2", fontFamily: "sans-serif", padding: 24 }}><section style={{ maxWidth: 420, textAlign: "center" }}><p style={{ color: "#b7ff57", fontFamily: "monospace", letterSpacing: ".1em" }}>ASTRA WEALTH</p><h1>Workspace temporarily unavailable.</h1><p style={{ color: "#829095", lineHeight: 1.6 }}>The UI could not load this workspace. Your data remains unchanged. Try again or check the API health endpoint.</p><button onClick={reset} style={{ border: 0, borderRadius: 6, padding: "10px 14px", background: "#b7ff57", color: "#101511", fontWeight: 700 }}>Retry</button></section></main>;
}
