"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import Link from "next/link";
import * as d3 from "d3";
import { PILLARS, CONNECTIONS, getSubsectionById } from "@/lib/dag";
import type { Pillar, Connection } from "@/lib/types";

/**
 * ConnectionsGraph: D3 force-directed view of the whole DAG.
 *
 * Nodes are subsections (A1, A2, ..., J7), grouped by pillar. Two kinds of
 * links: sequential within-pillar (A1 → A2 → A3 ...) and the explicit
 * CONNECTIONS array between pillars.
 *
 * Pillars are anchored to a 5×2 grid via forceX/forceY so the clusters stay
 * readable, but nodes can settle organically inside their cluster. Drag to
 * reposition, scroll to zoom, click for details.
 */

type Node = d3.SimulationNodeDatum & {
  id: string;
  name: string;
  pillar: Pillar;
  topicCount: number;
  hotCount: number;
};

type Link = d3.SimulationLinkDatum<Node> & {
  kind: Connection["kind"] | "within";
  label?: string;
};

export function ConnectionsGraph() {
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const [hovered, setHovered] = useState<string | null>(null);

  // Build the highlight set: active node + its direct neighbors (cross + within)
  const highlightSet = useCallback((active: string | null) => {
    const set = new Set<string>();
    if (!active) return set;
    set.add(active);
    CONNECTIONS.forEach((c) => {
      if (c.from === active) set.add(c.to);
      if (c.to === active) set.add(c.from);
    });
    const sub = getSubsectionById(active);
    if (sub) {
      const i = sub.pillar.subs.findIndex((s) => s.id === active);
      if (i > 0) set.add(sub.pillar.subs[i - 1].id);
      if (i < sub.pillar.subs.length - 1) set.add(sub.pillar.subs[i + 1].id);
    }
    return set;
  }, []);

  // Render the graph once on mount
  useEffect(() => {
    if (!svgRef.current || !containerRef.current) return;

    const width = containerRef.current.clientWidth;
    const height = 720;

    // ----- nodes & links --------------------------------------------------
    const nodes: Node[] = PILLARS.flatMap((p) =>
      p.subs.map((s) => ({
        id: s.id,
        name: s.name,
        pillar: p,
        topicCount: s.topics.length,
        hotCount: s.topics.filter((t) => t.hot).length,
      })),
    );

    const withinLinks: Link[] = PILLARS.flatMap((p) =>
      p.subs.slice(0, -1).map((s, i) => ({
        source: s.id,
        target: p.subs[i + 1].id,
        kind: "within" as const,
      })),
    );
    const crossLinks: Link[] = CONNECTIONS.map((c) => ({
      source: c.from,
      target: c.to,
      kind: c.kind,
      label: c.label,
    }));
    const links: Link[] = [...withinLinks, ...crossLinks];

    // ----- pillar home positions (5 cols × 2 rows) ------------------------
    // Top row sits a bit lower than a centered grid so the pillar labels have
    // breathing room above; bottom row anchors near the lower edge.
    const cols = 5;
    const colW = width / cols;
    const topRowY = 240;
    const bottomRowY = height - 180;
    const pillarPos = new Map<string, { x: number; y: number }>();
    PILLARS.forEach((p, i) => {
      pillarPos.set(p.letter, {
        x: colW * ((i % cols) + 0.5),
        y: Math.floor(i / cols) === 0 ? topRowY : bottomRowY,
      });
    });
    nodes.forEach((n) => {
      const pos = pillarPos.get(n.pillar.letter)!;
      n.x = pos.x + (Math.random() - 0.5) * 60;
      n.y = pos.y + (Math.random() - 0.5) * 60;
    });

    // ----- SVG scaffolding -----------------------------------------------
    const svg = d3
      .select(svgRef.current)
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("width", width)
      .attr("height", height);
    svg.selectAll("*").remove();

    const root = svg.append("g").attr("class", "graph-root");

    // Pan + zoom
    const zoom = d3
      .zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.4, 3])
      .on("zoom", (event) =>
        root.attr("transform", event.transform.toString()),
      );
    svg.call(zoom);

    // Background pillar labels as auto-sized colored pills (rect sized to the
    // text bbox). Top row gets a larger offset to clear the topmost nodes.
    const labelGroups = root
      .append("g")
      .attr("class", "pillar-labels")
      .selectAll<SVGGElement, Pillar>("g")
      .data(PILLARS)
      .join("g")
      .attr("class", "pillar-label-group")
      .attr("transform", (d, i) => {
        const isTopRow = Math.floor(i / cols) === 0;
        const yOffset = isTopRow ? 195 : 150;
        const pos = pillarPos.get(d.letter)!;
        return `translate(${pos.x},${pos.y - yOffset})`;
      });

    labelGroups
      .append("text")
      .attr("class", "pillar-label")
      .attr("text-anchor", "middle")
      .attr("dy", "0.35em")
      .attr("fill", (d) => d.color)
      .text((d) => `${d.letter}. ${d.shortName || d.name}`);

    labelGroups.each(function (d) {
      const g = d3.select(this);
      const txt = g.select<SVGTextElement>("text").node();
      if (!txt) return;
      const bbox = txt.getBBox();
      const padX = 10;
      const padY = 4;
      g.insert("rect", "text")
        .attr("class", "pillar-label-bg")
        .attr("x", bbox.x - padX)
        .attr("y", bbox.y - padY)
        .attr("width", bbox.width + padX * 2)
        .attr("height", bbox.height + padY * 2)
        .attr("rx", (bbox.height + padY * 2) / 2)
        .attr("fill", d.color)
        .attr("fill-opacity", 0.16)
        .attr("stroke", d.color)
        .attr("stroke-opacity", 0.45)
        .attr("stroke-width", 1);
    });

    // Links
    const linkSel = root
      .append("g")
      .attr("class", "links")
      .attr("fill", "none")
      .selectAll<SVGPathElement, Link>("path")
      .data(links)
      .join("path")
      .attr(
        "class",
        (d) =>
          `link ${d.kind === "within" ? "within" : "cross"} kind-${d.kind}`,
      );

    // Nodes
    const nodeSel = root
      .append("g")
      .attr("class", "nodes")
      .selectAll<SVGGElement, Node>("g")
      .data(nodes)
      .join("g")
      .attr("class", "node");

    nodeSel
      .append("circle")
      .attr("r", (d) => 14 + Math.min(d.topicCount, 12))
      .attr("fill", (d) => d.pillar.color)
      .attr("fill-opacity", 0.88);

    nodeSel
      .append("text")
      .attr("text-anchor", "middle")
      .attr("dy", "0.35em")
      .attr("fill", "#0a0e1f")
      .style("font-weight", 800)
      .style("font-size", "12px")
      .text((d) => d.id);

    nodeSel.on("mouseenter", (_, d) => setHovered(d.id));
    nodeSel.on("mouseleave", () => setHovered(null));
    nodeSel.on("click", (_, d) => setSelected(d.id));

    // Tooltip on hover (name only: full info shows in panel after click)
    nodeSel.append("title").text((d) => `${d.id}: ${d.name}`);

    // ----- Force simulation -----------------------------------------------
    const sim = d3
      .forceSimulation<Node>(nodes)
      .force(
        "link",
        d3
          .forceLink<Node, Link>(links)
          .id((d) => d.id)
          .distance((l) => (l.kind === "within" ? 55 : 150))
          .strength((l) => (l.kind === "within" ? 0.85 : 0.12)),
      )
      .force("charge", d3.forceManyBody<Node>().strength(-360))
      .force(
        "collide",
        d3.forceCollide<Node>().radius((d) => 24 + Math.min(d.topicCount, 12)),
      )
      .force(
        "x",
        d3
          .forceX<Node>((n) => pillarPos.get(n.pillar.letter)!.x)
          .strength(0.22),
      )
      .force(
        "y",
        d3
          .forceY<Node>((n) => pillarPos.get(n.pillar.letter)!.y)
          .strength(0.32),
      );

    sim.on("tick", () => {
      linkSel.attr("d", (d) => {
        const s = d.source as Node;
        const t = d.target as Node;
        const dx = (t.x ?? 0) - (s.x ?? 0);
        const dy = (t.y ?? 0) - (s.y ?? 0);
        const dr = Math.sqrt(dx * dx + dy * dy) * 1.2;
        return `M${s.x},${s.y}A${dr},${dr} 0 0,1 ${t.x},${t.y}`;
      });
      nodeSel.attr("transform", (d) => `translate(${d.x ?? 0},${d.y ?? 0})`);
    });

    // Drag
    const drag = d3
      .drag<SVGGElement, Node>()
      .on("start", (event, d) => {
        if (!event.active) sim.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      })
      .on("drag", (event, d) => {
        d.fx = event.x;
        d.fy = event.y;
      })
      .on("end", (event, d) => {
        if (!event.active) sim.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      });
    nodeSel.call(drag);

    return () => {
      sim.stop();
    };
  }, []);

  // React to hover/select by toggling CSS classes on existing DOM nodes
  useEffect(() => {
    if (!svgRef.current) return;
    const active = hovered ?? selected;
    const set = highlightSet(active);
    const svg = d3.select(svgRef.current);
    svg
      .selectAll<SVGGElement, Node>(".node")
      .classed("dim", (d) => !!active && !set.has(d.id))
      .classed("active", (d) => d.id === active);
    svg
      .selectAll<SVGPathElement, Link>(".link")
      .classed("highlight", (d) => {
        if (!active) return false;
        const s = (d.source as Node).id ?? d.source;
        const t = (d.target as Node).id ?? d.target;
        return s === active || t === active;
      })
      .classed("dim", (d) => {
        if (!active) return false;
        const s = (d.source as Node).id ?? d.source;
        const t = (d.target as Node).id ?? d.target;
        return s !== active && t !== active;
      });
  }, [hovered, selected, highlightSet]);

  const selectedSub = selected ? getSubsectionById(selected) : null;

  return (
    <div className="flex flex-col gap-4">
      <div
        ref={containerRef}
        className="card relative overflow-hidden"
        style={{ height: 720 }}
      >
        <svg ref={svgRef} className="conn-graph w-full h-full" />
        <div className="absolute bottom-3 left-3 text-xs text-[var(--fg-mute)] bg-[var(--bg)]/80 px-2 py-1 rounded backdrop-blur">
          💡 arraste nós · scroll zoom · clique para detalhes
        </div>
      </div>

      <Legend />

      {selectedSub && (
        <SidePanel sub={selectedSub} onClose={() => setSelected(null)} />
      )}
    </div>
  );
}

function Legend() {
  const kinds = [
    {
      id: "shared-concept",
      label: "Conceito compartilhado",
      color: "var(--accent)",
    },
    { id: "uses", label: "Usa / depende de", color: "var(--partial)" },
    { id: "generalizes", label: "Generaliza", color: "var(--good)" },
    { id: "alternative", label: "Alternativa", color: "var(--hot)" },
    {
      id: "within",
      label: "Sequência dentro do pilar",
      color: "var(--fg-mute)",
    },
  ];
  return (
    <div className="flex gap-5 flex-wrap text-sm text-[var(--fg-dim)] px-2">
      {kinds.map((k) => (
        <span key={k.id} className="inline-flex items-center gap-2">
          <span
            className="inline-block w-7 h-[2px]"
            style={{ background: k.color }}
          />
          {k.label}
        </span>
      ))}
    </div>
  );
}

type SubResult = NonNullable<ReturnType<typeof getSubsectionById>>;

function SidePanel({ sub, onClose }: { sub: SubResult; onClose: () => void }) {
  const outgoing = CONNECTIONS.filter((c) => c.from === sub.id);
  const incoming = CONNECTIONS.filter((c) => c.to === sub.id);

  return (
    <div
      className="conn-panel card p-6"
      style={{ ["--panel-color" as never]: sub.pillar.color }}
    >
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="text-xs uppercase tracking-wider text-[var(--fg-dim)] mb-1">
            {sub.pillar.letter}. {sub.pillar.name}
          </div>
          <h3 className="m-0 text-xl font-bold">
            <span
              className="font-extrabold mr-2"
              style={{ color: sub.pillar.color }}
            >
              {sub.id}
            </span>
            {sub.name}
          </h3>
        </div>
        <div className="flex items-center gap-2">
          <Link
            href={`/pillar/${sub.pillar.letter}/${sub.id}`}
            className="btn no-underline"
            style={{
              background: sub.pillar.color,
              color: "var(--bg)",
              borderColor: sub.pillar.color,
              fontWeight: 600,
            }}
          >
            Ver subseção →
          </Link>
          <button onClick={onClose} className="btn" aria-label="fechar">
            ✕
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
        <div>
          <h4 className="text-xs uppercase tracking-wider text-[var(--fg-dim)] mb-2 font-semibold">
            Tópicos ({sub.topics.length})
          </h4>
          <ul className="list-none p-0 m-0 space-y-1 text-sm">
            {sub.topics.map((t) => (
              <li key={t.name} className="text-[var(--fg)]">
                <span className="text-[var(--fg-mute)] mr-2">
                  {t.status === "covered"
                    ? "✓"
                    : t.status === "partial"
                      ? "◐"
                      : "○"}
                </span>
                {t.name}
                {t.hot && <span className="ml-2 text-[var(--hot)]">★</span>}
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h4 className="text-xs uppercase tracking-wider text-[var(--fg-dim)] mb-2 font-semibold">
            Conexões ({outgoing.length + incoming.length})
          </h4>
          {outgoing.length > 0 && (
            <div className="mb-3">
              <div className="text-xs text-[var(--fg-mute)] mb-1">
                → saindo:
              </div>
              <ul className="list-none p-0 m-0 space-y-1 text-sm">
                {outgoing.map((c) => (
                  <li key={`${c.from}-${c.to}`}>
                    <span className="font-mono text-[var(--accent)]">
                      {c.to}
                    </span>{" "}
                    · {c.label}
                  </li>
                ))}
              </ul>
            </div>
          )}
          {incoming.length > 0 && (
            <div>
              <div className="text-xs text-[var(--fg-mute)] mb-1">
                ← entrando:
              </div>
              <ul className="list-none p-0 m-0 space-y-1 text-sm">
                {incoming.map((c) => (
                  <li key={`${c.from}-${c.to}`}>
                    <span className="font-mono text-[var(--accent)]">
                      {c.from}
                    </span>{" "}
                    · {c.label}
                  </li>
                ))}
              </ul>
            </div>
          )}
          {outgoing.length + incoming.length === 0 && (
            <p className="text-sm text-[var(--fg-mute)]">
              (Esta subseção ainda não tem conexões cruzadas definidas.)
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
