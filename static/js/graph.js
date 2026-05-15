const canvas = document.querySelector("[data-graph-canvas]");
const ctx = canvas.getContext("2d");
const root = document.querySelector("[data-graph-root]");
const panel = document.querySelector("[data-graph-panel]");
const titleEl = document.querySelector("[data-node-title]");
const typeEl = document.querySelector("[data-node-type]");
const summaryEl = document.querySelector("[data-node-summary]");
const linkEl = document.querySelector("[data-node-link]");
const filters = Array.from(document.querySelectorAll("[data-filter]"));

let graph = { nodes: [], links: [] };
let nodes = [];
let links = [];
let selected = null;
let hovered = null;
let filter = "all";
let pointer = { x: 0, y: 0, down: false, dragging: null };
let running = true;
const siteRoot = root.dataset.siteRoot || "/";

const typeLabel = {
  article: "Article",
  topic: "Topic",
  concept: "Concept",
  claim: "Claim",
  keyword: "Keyword",
};

function resize() {
  const rect = canvas.getBoundingClientRect();
  const dpr = Math.max(1, window.devicePixelRatio || 1);
  canvas.width = Math.floor(rect.width * dpr);
  canvas.height = Math.floor(rect.height * dpr);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

function visibleNode(node) {
  return filter === "all" || node.type === filter || node.type === "article";
}

function resetPositions() {
  const rect = canvas.getBoundingClientRect();
  const centerX = rect.width * 0.47;
  const centerY = rect.height * 0.52;
  nodes.forEach((node, index) => {
    const ring = node.type === "article" ? 70 : 170 + node.level * 34;
    const angle = (index / Math.max(1, nodes.length)) * Math.PI * 2;
    node.x = centerX + Math.cos(angle) * ring + (Math.random() - 0.5) * 80;
    node.y = centerY + Math.sin(angle) * ring + (Math.random() - 0.5) * 80;
    node.vx = 0;
    node.vy = 0;
    node.radius = 7 + Math.sqrt(node.weight || 1) * 3.2;
  });
}

function simulate() {
  const rect = canvas.getBoundingClientRect();
  const cx = rect.width * 0.47;
  const cy = rect.height * 0.52;
  const visible = nodes.filter(visibleNode);
  const visibleIds = new Set(visible.map((node) => node.id));

  for (const node of visible) {
    node.vx += (cx - node.x) * 0.0009 * (node.type === "article" ? 1.8 : 1);
    node.vy += (cy - node.y) * 0.0009 * (node.type === "article" ? 1.8 : 1);
  }

  for (let i = 0; i < visible.length; i += 1) {
    for (let j = i + 1; j < visible.length; j += 1) {
      const a = visible[i];
      const b = visible[j];
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const distance = Math.max(1, Math.hypot(dx, dy));
      const force = ((a.radius + b.radius + 48) / distance) ** 2 * 0.08;
      const fx = (dx / distance) * force;
      const fy = (dy / distance) * force;
      a.vx -= fx;
      a.vy -= fy;
      b.vx += fx;
      b.vy += fy;
    }
  }

  for (const link of links) {
    if (!visibleIds.has(link.source.id) || !visibleIds.has(link.target.id)) continue;
    const dx = link.target.x - link.source.x;
    const dy = link.target.y - link.source.y;
    const distance = Math.max(1, Math.hypot(dx, dy));
    const ideal = 95 + (10 - Math.min(10, link.weight || 1)) * 9;
    const force = (distance - ideal) * 0.006;
    const fx = (dx / distance) * force;
    const fy = (dy / distance) * force;
    link.source.vx += fx;
    link.source.vy += fy;
    link.target.vx -= fx;
    link.target.vy -= fy;
  }

  for (const node of visible) {
    if (pointer.dragging === node) continue;
    node.vx *= 0.86;
    node.vy *= 0.86;
    node.x += node.vx;
    node.y += node.vy;
    node.x = Math.max(node.radius + 12, Math.min(rect.width - node.radius - 12, node.x));
    node.y = Math.max(node.radius + 12, Math.min(rect.height - node.radius - 12, node.y));
  }
}

function draw() {
  const rect = canvas.getBoundingClientRect();
  ctx.clearRect(0, 0, rect.width, rect.height);

  const glow = ctx.createRadialGradient(rect.width * 0.48, rect.height * 0.48, 20, rect.width * 0.48, rect.height * 0.48, rect.width * 0.7);
  glow.addColorStop(0, "rgba(127, 90, 240, 0.22)");
  glow.addColorStop(0.42, "rgba(0, 166, 251, 0.10)");
  glow.addColorStop(1, "rgba(255, 255, 255, 0)");
  ctx.fillStyle = glow;
  ctx.fillRect(0, 0, rect.width, rect.height);

  const visibleIds = new Set(nodes.filter(visibleNode).map((node) => node.id));
  const activeIds = new Set();
  if (selected || hovered) {
    const focus = selected || hovered;
    activeIds.add(focus.id);
    links.forEach((link) => {
      if (link.source.id === focus.id || link.target.id === focus.id) {
        activeIds.add(link.source.id);
        activeIds.add(link.target.id);
      }
    });
  }

  for (const link of links) {
    if (!visibleIds.has(link.source.id) || !visibleIds.has(link.target.id)) continue;
    const active = activeIds.size === 0 || (activeIds.has(link.source.id) && activeIds.has(link.target.id));
    ctx.beginPath();
    ctx.moveTo(link.source.x, link.source.y);
    ctx.lineTo(link.target.x, link.target.y);
    ctx.strokeStyle = active ? "rgba(34, 34, 34, 0.34)" : "rgba(34, 34, 34, 0.08)";
    ctx.lineWidth = active ? 1.4 : 0.8;
    ctx.stroke();
  }

  const now = performance.now() / 1000;
  for (const node of nodes) {
    if (!visibleNode(node)) continue;
    const active = activeIds.size === 0 || activeIds.has(node.id);
    const pulse = Math.sin(now * 2.2 + node.weight) * 0.9;
    const radius = node.radius + (active ? pulse : 0);

    ctx.beginPath();
    ctx.arc(node.x, node.y, radius + 8, 0, Math.PI * 2);
    ctx.fillStyle = active ? `${hexToRgba(node.color, 0.16)}` : "rgba(0,0,0,0.03)";
    ctx.fill();

    ctx.beginPath();
    ctx.arc(node.x, node.y, radius, 0, Math.PI * 2);
    ctx.fillStyle = active ? node.color : hexToRgba(node.color, 0.28);
    ctx.fill();

    ctx.beginPath();
    ctx.arc(node.x - radius * 0.32, node.y - radius * 0.34, Math.max(2, radius * 0.22), 0, Math.PI * 2);
    ctx.fillStyle = "rgba(255,255,255,0.46)";
    ctx.fill();

    if (active && (node.type !== "keyword" || selected === node || hovered === node)) {
      ctx.font = node.type === "claim" ? "600 12px system-ui" : "700 13px system-ui";
      ctx.fillStyle = "#222";
      ctx.textAlign = "center";
      ctx.textBaseline = "top";
      wrapText(node.label, node.x, node.y + radius + 10, node.type === "claim" ? 170 : 120, 16);
    }
  }
}

function wrapText(text, x, y, maxWidth, lineHeight) {
  const words = String(text).split("");
  let line = "";
  let lines = 0;
  for (const word of words) {
    const test = line + word;
    if (ctx.measureText(test).width > maxWidth && line) {
      ctx.fillText(line, x, y + lines * lineHeight);
      line = word;
      lines += 1;
      if (lines > 2) break;
    } else {
      line = test;
    }
  }
  if (line && lines <= 2) ctx.fillText(line, x, y + lines * lineHeight);
}

function hexToRgba(hex, alpha) {
  const value = hex.replace("#", "");
  const r = parseInt(value.slice(0, 2), 16);
  const g = parseInt(value.slice(2, 4), 16);
  const b = parseInt(value.slice(4, 6), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function updatePanel(node) {
  if (!node) {
    titleEl.textContent = "选择一个节点";
    typeEl.textContent = "点击文章、判断、概念或主题节点查看它在知识网络中的位置。";
    summaryEl.textContent = "";
    linkEl.hidden = true;
    return;
  }

  titleEl.textContent = node.label;
  typeEl.textContent = `${typeLabel[node.type] || node.type} · weight ${node.weight || 1}`;
  summaryEl.textContent = node.summary || node.stance || "";
  if (node.url) {
    linkEl.href = withSiteRoot(node.url);
    linkEl.textContent = "打开文章";
    linkEl.hidden = false;
  } else {
    linkEl.hidden = true;
  }
}

function findNode(x, y) {
  return nodes
    .filter(visibleNode)
    .slice()
    .reverse()
    .find((node) => Math.hypot(node.x - x, node.y - y) <= node.radius + 8);
}

function loop() {
  if (running) simulate();
  draw();
  requestAnimationFrame(loop);
}

canvas.addEventListener("pointermove", (event) => {
  const rect = canvas.getBoundingClientRect();
  pointer.x = event.clientX - rect.left;
  pointer.y = event.clientY - rect.top;
  if (pointer.dragging) {
    pointer.dragging.x = pointer.x;
    pointer.dragging.y = pointer.y;
    pointer.dragging.vx = 0;
    pointer.dragging.vy = 0;
    return;
  }
  hovered = findNode(pointer.x, pointer.y);
  canvas.style.cursor = hovered ? "grab" : "default";
});

canvas.addEventListener("pointerdown", (event) => {
  const rect = canvas.getBoundingClientRect();
  const node = findNode(event.clientX - rect.left, event.clientY - rect.top);
  if (!node) return;
  pointer.down = true;
  pointer.dragging = node;
  selected = node;
  updatePanel(node);
  canvas.setPointerCapture(event.pointerId);
});

canvas.addEventListener("pointerup", (event) => {
  pointer.down = false;
  pointer.dragging = null;
  canvas.releasePointerCapture(event.pointerId);
});

canvas.addEventListener("dblclick", () => {
  if (selected?.url) window.location.href = withSiteRoot(selected.url);
});

filters.forEach((button) => {
  button.addEventListener("click", () => {
    filter = button.dataset.filter;
    filters.forEach((item) => item.classList.toggle("is-active", item === button));
    selected = null;
    updatePanel(null);
  });
});

window.addEventListener("resize", () => {
  resize();
  resetPositions();
});

async function boot() {
  resize();
  const response = await fetch(root.dataset.graphSrc || "graph/knowledge-graph.json");
  graph = await response.json();
  document.querySelector("[data-stat='articles']").textContent = graph.stats.articles;
  document.querySelector("[data-stat='nodes']").textContent = graph.stats.nodes;
  document.querySelector("[data-stat='links']").textContent = graph.stats.links;

  nodes = graph.nodes.map((node) => ({ ...node }));
  const byId = new Map(nodes.map((node) => [node.id, node]));
  links = graph.links
    .map((link) => ({ ...link, source: byId.get(link.source), target: byId.get(link.target) }))
    .filter((link) => link.source && link.target);

  resetPositions();
  updatePanel(null);
  loop();
}

function withSiteRoot(url) {
  if (/^https?:\/\//.test(url) || url.startsWith("/")) return url;
  return `${siteRoot.replace(/\/$/, "")}/${url.replace(/^\//, "")}`;
}

boot().catch((error) => {
  panel.innerHTML = `<h2>图谱加载失败</h2><p>${error.message}</p>`;
});
