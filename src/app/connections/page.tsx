import { unstable_rethrow } from "next/navigation";
import { ConnectionsGraph } from "@/components/ConnectionsGraph";
import { studyMap } from "@/lib/curriculum";
import { CONNECTIONS, PILLARS } from "@/lib/dag";
import { getProgressMap, isSignedIn } from "@/lib/progress";

/** The overlay is optional: if progress can't load, show the plain graph. */
async function loadStudy() {
  try {
    return (await isSignedIn()) ? studyMap(await getProgressMap()) : undefined;
  } catch (err) {
    unstable_rethrow(err);
    console.error("Loading study progress failed", err);
    return undefined;
  }
}

export default async function ConnectionsPage() {
  const nNodes = PILLARS.reduce((n, p) => n + p.subs.length, 0);
  const nCross = CONNECTIONS.length;
  const study = await loadStudy();

  return (
    <div className="max-w-[1280px] mx-auto px-6 py-12">
      <h1 className="text-4xl font-bold tracking-tight mb-2 bg-gradient-to-r from-[#7aa2f7] via-[#bb9af7] to-[#f7768e] bg-clip-text text-transparent">
        Connections
      </h1>
      <p className="text-[var(--fg-dim)] max-w-2xl mb-8">
        D3 force-directed graph of {nNodes} subsections across {PILLARS.length}{" "}
        pillars, with {nCross} cross-pillar connections. Subsections link within
        a pillar (sequence) and across pillars when they share concepts or one
        depends on another.
      </p>

      <ConnectionsGraph study={study} />
    </div>
  );
}
