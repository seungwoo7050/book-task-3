import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MCP Recommendation Ops Demo",
  description: "Study1 v0 initial demo"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
