import { ConnectionsGraph } from "@/components/ConnectionsGraph";
import { CONNECTIONS, PILLARS } from "@/lib/dag";

export default function ConnectionsPage() {
  const nNodes = PILLARS.reduce((n, p) => n + p.subs.length, 0);
  const nCross = CONNECTIONS.length;

  return (
    <div className="max-w-[1280px] mx-auto px-6 py-12">
      <h1 className="text-4xl font-bold tracking-tight mb-2 bg-gradient-to-r from-[#7aa2f7] via-[#bb9af7] to-[#f7768e] bg-clip-text text-transparent">
        Connections
      </h1>
      <p className="text-[var(--fg-dim)] max-w-2xl mb-8">
        Grafo D3 force-directed das {nNodes} subseções em {PILLARS.length} pilares,
        com {nCross} conexões cruzadas. As subseções se ligam dentro do pilar
        (sequência) e entre pilares quando compartilham conceitos ou um depende
        do outro.
      </p>

      <ConnectionsGraph />
    </div>
  );
}
