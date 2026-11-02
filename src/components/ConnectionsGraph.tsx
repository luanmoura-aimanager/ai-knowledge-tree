"use client";

import { useEffect, useRef, useState, useCallback, useMemo } from "react";
import Link from "next/link";
import * as d3 from "d3";
import { PILLARS, CONNECTIONS, getSubsectionById } from "@/lib/dag";
import {
  MAX_ZOOM,
  studyFraction,
  studyOpacity,
  zoomLimitAt,
  type StudyMap,
  type ZoomLimit,
} from "@/lib/study-graph";
import type { Pillar, Connection } from "@/lib/types";
import { usePathHighlight } from "@/components/PathHighlightProvider";

/**
 * ConnectionsGraph: D3 force-directed view of the whole DAG.
 *
 * Nodes are subsections (A1, A2, ..., J7), grouped by pillar. Two kinds of
 * links: sequential within-pillar (A1 → A2 → A3 ...) and the explicit
 * CONNECTIONS array between pillars.
 *
 * Pillars are anchored to a 7×2 grid via forceX/forceY so the clusters stay
 * readable, but nodes can settle organically inside their cluster. The layout
 * is settled once the card nears the viewport and the SVG viewBox is fitted to
 * it, so the whole graph always shows. The wheel is left to the page: zoom is
 * button-only. Drag to reposition, click for details.
 *
 * Signed-in callers pass `study` (per-subsection progress), which adds a
 * "Studied graph" view shading each node from dim (0%) to full color (100%).
 */

// Logical layout size; the viewBox scales it to whatever the card measures.
const WIDTH = 1232;
const HEIGHT = 720;
const FIT_PADDING = 24;
const ZOOM_STEP = 1.6;

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

export function ConnectionsGraph({ study }: { study?: StudyMap }) {
  const svgRef = useRef<SVGSVGElement>(null);
  const zoomRef = useRef<{ by: (factor: number) => void; reset: () => void }>(
    null,
  );
  const [selected, setSelected] = useState<string | null>(null);
  const [hovered, setHovered] = useState<string | null>(null);
  const [zoomLimit, setZoomLimit] = useState<ZoomLimit>("min");
  const [nearViewport, setNearViewport] = useState(false);
  const [studiedView, setStudiedView] = useState(false);
  // `study` can go away while mounted (signing out redirects to the same route).
  const showStudied = studiedView && Boolean(study);

  // The suggested path the user picked (null when none). Its ids light up the
  // matching nodes and its consecutive pairs are drawn as a route overlay.
  const activePath = usePathHighlight()?.active ?? null;
  const pathIds = activePath?.ids;
  const pathColor = activePath?.color;

  // Consecutive (a, b) pairs along the path order — the route to draw. A path is
  // an ordered sequence, so these edges may not exist in the base graph links.
  const pathPairs = useMemo<[string, string][]>(() => {
    if (!pathIds || pathIds.length < 2) return [];
    return pathIds.slice(0, -1).map((id, i) => [id, pathIds[i + 1]]);
  }, [pathIds]);

  // Refs let the once-on-mount tick handler redraw the route as nodes move,
  // without rebuilding the simulation when the active path changes.
  const pathPairsRef = useRef<[string, string][]>([]);
  const pathColorRef = useRef<string | undefined>(undefined);
  const drawPathRef = useRef<() => void>(() => {});

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

  // Settling the layout blocks the main thread, so wait until the card is about
  // to scroll into view instead of doing it during page hydration.
  useEffect(() => {
    if (!svgRef.current) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        setNearViewport(true);
        observer.disconnect();
      },
      { rootMargin: "400px" },
    );
    observer.observe(svgRef.current);
    return () => observer.disconnect();
  }, []);

  // Render the graph once
  useEffect(() => {
    if (!nearViewport || !svgRef.current) return;
    const svgNode = svgRef.current;

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

    // ----- pillar home positions (7 cols × 2 rows) ------------------------
    // Top row sits a bit lower than a centered grid so the pillar labels have
    // breathing room above; bottom row anchors near the lower edge.
    const cols = 7;
    const colW = WIDTH / cols;
    const topRowY = 240;
    const bottomRowY = HEIGHT - 180;
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
    const svg = d3.select(svgNode).attr("viewBox", `0 0 ${WIDTH} ${HEIGHT}`);
    svg.selectAll("*").remove();

    const root = svg.append("g").attr("class", "graph-root");

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

    // Route overlay for a selected suggested path: drawn above the base links
    // but below the nodes, so node circles sit on top of the route.
    const pathLayer = root
      .append("g")
      .attr("class", "path-links")
      .attr("fill", "none");

    const nodeById = new Map(nodes.map((n) => [n.id, n]));

    // Redraw the route between the active path's consecutive nodes from their
    // current positions. Called on every tick (so it follows drag/settle) and
    // imperatively when the active path changes while the sim is at rest.
    const drawPathLinks = () => {
      const sel = pathLayer
        .selectAll<SVGPathElement, [string, string]>("path")
        .data(pathPairsRef.current, (d) => `${d[0]}-${d[1]}`);
      sel.exit().remove();
      sel
        .enter()
        .append("path")
        .attr("class", "path-link")
        .merge(sel)
        .attr("stroke", pathColorRef.current ?? "var(--accent)")
        .attr("d", ([a, b]) => {
          const s = nodeById.get(a);
          const t = nodeById.get(b);
          if (!s || s.x == null || t == null || t.x == null) return null;
          const dx = (t.x ?? 0) - (s.x ?? 0);
          const dy = (t.y ?? 0) - (s.y ?? 0);
          const dr = Math.sqrt(dx * dx + dy * dy) * 1.2;
          return `M${s.x},${s.y}A${dr},${dr} 0 0,1 ${t.x},${t.y}`;
        });
    };
    drawPathRef.current = drawPathLinks;

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

    const render = () => {
      linkSel.attr("d", (d) => {
        const s = d.source as Node;
        const t = d.target as Node;
        const dx = (t.x ?? 0) - (s.x ?? 0);
        const dy = (t.y ?? 0) - (s.y ?? 0);
        const dr = Math.sqrt(dx * dx + dy * dy) * 1.2;
        return `M${s.x},${s.y}A${dr},${dr} 0 0,1 ${t.x},${t.y}`;
      });
      nodeSel.attr("transform", (d) => `translate(${d.x ?? 0},${d.y ?? 0})`);
      drawPathLinks();
    };

    // Settle the layout up front: the fit below needs the final positions.
    // Ticks after this only come from drags re-heating the sim.
    sim.stop();
    sim.tick(
      Math.ceil(Math.log(sim.alphaMin()) / Math.log(1 - sim.alphaDecay())),
    );
    render();
    sim.on("tick", render);

    // ----- Fit + zoom ------------------------------------------------------
    // Fit the viewBox to the nodes and pillar labels. d3.zoom reads the viewBox
    // as its extent, so scale 1 is exactly the full graph.
    const boxes = [".nodes", ".pillar-labels"].map((s) =>
      root.select<SVGGElement>(s).node()!.getBBox(),
    );
    const x0 = Math.min(...boxes.map((b) => b.x)) - FIT_PADDING;
    const y0 = Math.min(...boxes.map((b) => b.y)) - FIT_PADDING;
    const x1 = Math.max(...boxes.map((b) => b.x + b.width)) + FIT_PADDING;
    const y1 = Math.max(...boxes.map((b) => b.y + b.height)) + FIT_PADDING;
    svg.attr("viewBox", `${x0} ${y0} ${x1 - x0} ${y1 - y0}`);

    const zoom = d3
      .zoom<SVGSVGElement, unknown>()
      .scaleExtent([1, MAX_ZOOM])
      .translateExtent([
        [x0, y0],
        [x1, y1],
      ])
      // Panning only means something once zoomed in; at full view let touch
      // swipes through to the page.
      .filter(
        (event) =>
          !event.ctrlKey &&
          !event.button &&
          zoomLimitAt(d3.zoomTransform(svgNode).k) !== "min",
      )
      .on("zoom", (event) => {
        const limit = zoomLimitAt(event.transform.k);
        root.attr("transform", event.transform.toString());
        svg.classed("zoomed", limit !== "min");
        setZoomLimit(limit);
      });
    // Wheel and double-click stay with the page; zoom goes through the buttons.
    svg.call(zoom).on("wheel.zoom", null).on("dblclick.zoom", null);

    zoomRef.current = {
      by: (factor) => svg.transition().duration(250).call(zoom.scaleBy, factor),
      reset: () =>
        svg.transition().duration(250).call(zoom.transform, d3.zoomIdentity),
    };

    // Drag. Not on touch, where a swipe starting on a node should scroll.
    const drag = d3
      .drag<SVGGElement, Node>()
      .touchable(false)
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
  }, [nearViewport]);

  // React to hover/select (or a picked suggested path) by toggling CSS classes
  // on existing DOM nodes. A hovered/clicked node always wins; otherwise, if a
  // suggested path is active, light up exactly its subsections.
  useEffect(() => {
    if (!nearViewport || !svgRef.current) return;
    const svg = d3.select(svgRef.current);
    const linkEnd = (e: string | number | Node) => (e as Node).id ?? e;

    const active = hovered ?? selected;
    // A hovered/clicked node wins over a selected path. Node mode lights the node
    // + neighbors and highlights their edges; path mode lights the path's
    // subsections and draws an explicit route overlay between them instead.
    const pathMode = !active && pathPairs.length > 0;
    const set = active ? highlightSet(active) : new Set(pathIds ?? []);
    const anyHighlight = set.size > 0;

    // Feed the route overlay (drawn imperatively by the d3 layer, not React).
    pathPairsRef.current = pathMode ? pathPairs : [];
    pathColorRef.current = pathColor;
    drawPathRef.current();

    svg
      .selectAll<SVGGElement, Node>(".node")
      .classed("dim", (d) => anyHighlight && !set.has(d.id))
      .classed("linked", (d) => set.has(d.id))
      .classed("active", (d) => (active ? d.id === active : set.has(d.id)));

    svg
      .selectAll<SVGPathElement, Link>(".link")
      .classed("highlight", (d) => {
        // Only single-node mode highlights base edges; path mode uses the route.
        if (!active) return false;
        const s = linkEnd(d.source);
        const t = linkEnd(d.target);
        return s === active || t === active;
      })
      .classed("dim", (d) => {
        if (!anyHighlight) return false;
        // In path mode every base link is dimmed in favor of the route overlay.
        if (pathMode) return true;
        const s = linkEnd(d.source);
        const t = linkEnd(d.target);
        return s !== active && t !== active;
      });
  }, [
    nearViewport,
    hovered,
    selected,
    highlightSet,
    pathIds,
    pathPairs,
    pathColor,
  ]);

  // Shade nodes by study progress on the existing DOM (the CSS only applies
  // --study-opacity under .studied-view), without rebuilding the simulation.
  useEffect(() => {
    if (!nearViewport || !svgRef.current) return;
    const svg = d3.select(svgRef.current).classed("studied-view", showStudied);

    svg
      .selectAll<SVGGElement, Node>(".node")
      .classed(
        "complete",
        (d) => showStudied && study?.[d.id]?.state === "done",
      )
      .style("--study-opacity", (d) =>
        studyOpacity(studyFraction(study?.[d.id])),
      );

    svg.selectAll<SVGTitleElement, Node>(".node title").text((d) => {
      const base = `${d.id}: ${d.name}`;
      const p = study?.[d.id];
      if (!showStudied || !p) return base;
      const started = p.inProgress > 0 ? `, ${p.inProgress} in progress` : "";
      return `${base}: ${p.studied}/${p.total} studied${started}`;
    });
  }, [nearViewport, showStudied, study]);

  const selectedSub = selected ? getSubsectionById(selected) : null;

  return (
    <div className="flex flex-col gap-4">
      {study && (
        <div className="flex justify-end gap-2">
          <button
            className={`btn ${showStudied ? "" : "active"}`}
            aria-pressed={!showStudied}
            onClick={() => setStudiedView(false)}
          >
            Connections
          </button>
          <button
            className={`btn ${showStudied ? "active" : ""}`}
            aria-pressed={showStudied}
            onClick={() => setStudiedView(true)}
          >
            Studied graph
          </button>
        </div>
      )}

      <div
        className="card relative overflow-hidden"
        style={{ aspectRatio: "12 / 7", maxHeight: "85vh", minHeight: 320 }}
      >
        <svg ref={svgRef} className="conn-graph w-full h-full" />
        <div className="hidden sm:pointer-fine:block absolute bottom-3 left-3 text-xs text-[var(--fg-mute)] bg-[var(--bg)]/80 px-2 py-1 rounded backdrop-blur">
          💡 drag nodes · + / − to zoom · click for details
        </div>
        <div className="absolute bottom-3 right-3 flex gap-1.5">
          <button
            className="btn disabled:opacity-40"
            aria-label="Zoom out"
            disabled={zoomLimit === "min"}
            onClick={() => zoomRef.current?.by(1 / ZOOM_STEP)}
          >
            −
          </button>
          <button
            className="btn disabled:opacity-40"
            aria-label="Zoom in"
            disabled={zoomLimit === "max"}
            onClick={() => zoomRef.current?.by(ZOOM_STEP)}
          >
            +
          </button>
          <button
            className="btn disabled:opacity-40"
            aria-label="Fit the full graph"
            disabled={zoomLimit === "min"}
            onClick={() => zoomRef.current?.reset()}
          >
            Fit
          </button>
        </div>
      </div>

      {showStudied && study ? <StudiedLegend study={study} /> : <Legend />}

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
      label: "Shared concept",
      color: "var(--accent)",
    },
    { id: "uses", label: "Uses / depends on", color: "var(--partial)" },
    { id: "generalizes", label: "Generalizes", color: "var(--good)" },
    { id: "alternative", label: "Alternative", color: "var(--hot)" },
    {
      id: "within",
      label: "Sequence within pillar",
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

function StudiedLegend({ study }: { study: StudyMap }) {
  const subs = Object.values(study);
  const total = subs.reduce((n, s) => n + s.total, 0);
  const studied = subs.reduce((n, s) => n + s.studied, 0);
  const complete = subs.filter((s) => s.state === "done").length;
  return (
    <div className="flex gap-5 flex-wrap items-center text-sm text-[var(--fg-dim)] px-2">
      <span className="inline-flex items-center gap-2">
        0%
        <span
          className="inline-block w-24 h-2 rounded"
          style={{
            background:
              "linear-gradient(90deg, color-mix(in srgb, var(--accent) 18%, transparent), var(--accent))",
          }}
        />
        100%
      </span>
      <span>
        {studied} of {total} lessons studied · {complete}{" "}
        {complete === 1 ? "subsection" : "subsections"} complete
      </span>
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
            View subsection →
          </Link>
          <button onClick={onClose} className="btn" aria-label="close">
            ✕
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
        <div>
          <h4 className="text-xs uppercase tracking-wider text-[var(--fg-dim)] mb-2 font-semibold">
            Topics ({sub.topics.length})
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
            Connections ({outgoing.length + incoming.length})
          </h4>
          {outgoing.length > 0 && (
            <div className="mb-3">
              <div className="text-xs text-[var(--fg-mute)] mb-1">
                → outgoing:
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
                ← incoming:
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
              (This subsection has no cross-pillar connections defined yet.)
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
