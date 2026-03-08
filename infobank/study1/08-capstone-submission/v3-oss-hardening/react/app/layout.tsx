import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MCP OSS Operations Console",
  description: "Study1 v3 OSS hardening demo"
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
