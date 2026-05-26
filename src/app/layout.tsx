import type { Metadata } from "next";
import "./globals.css";
import "katex/dist/katex.min.css";
import { Header } from "@/components/Header";

export const metadata: Metadata = {
  title: "AI Knowledge Tree",
  description:
    "Interactive DAG of Data Science, Machine Learning, Deep Learning and AI Engineering: with cross-pillar connections.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="pt-BR">
      <body>
        <Header />
        <main>{children}</main>
      </body>
    </html>
  );
}
