/**
 * Passthrough. The pillar overview renders full width; the lesson sidebar lives
 * one level deeper, in pillar/[letter]/[subId]/layout.tsx.
 */
export default function PillarLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
