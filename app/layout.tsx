import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Astra Wealth — Indian market intelligence",
  description: "A compliance-first AI wealth terminal for Indian investors.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
