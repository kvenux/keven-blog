import { mkdir, readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const articleDir = path.join(root, "data", "graph", "articles");
const bridgePath = path.join(root, "data", "graph", "bridges.json");
const outputDir = path.join(root, "static", "graph");
const outputPath = path.join(outputDir, "knowledge-graph.json");

const nodeMap = new Map();
const links = [];

const types = {
  article: { level: 4, color: "#f25f4c" },
  topic: { level: 3, color: "#2cb67d" },
  concept: { level: 2, color: "#7f5af0" },
  claim: { level: 3, color: "#00a6fb" },
  keyword: { level: 1, color: "#faae2b" },
};

function addNode(node) {
  const existing = nodeMap.get(node.id);
  if (existing) {
    existing.weight = Math.max(existing.weight || 1, node.weight || 1);
    existing.refs = Array.from(new Set([...(existing.refs || []), ...(node.refs || [])]));
    return existing;
  }
  const typed = types[node.type] || { level: 1, color: "#94a1b2" };
  const next = { ...typed, weight: 1, ...node };
  nodeMap.set(next.id, next);
  return next;
}

function addLink(source, target, type, reason, weight = 1) {
  if (!source || !target || source === target) return;
  links.push({ source, target, type, reason: reason || "", weight });
}

function normalizeId(prefix, value) {
  return `${prefix}:${String(value).toLowerCase().trim().replace(/[^\p{L}\p{N}]+/gu, "-").replace(/^-|-$/g, "")}`;
}

const files = (await readdir(articleDir)).filter((file) => file.endsWith(".json")).sort();
const articles = [];

for (const file of files) {
  const graph = JSON.parse(await readFile(path.join(articleDir, file), "utf8"));
  const articleId = `article:${graph.article.slug}`;
  articles.push(graph.article);

  addNode({
    id: articleId,
    type: "article",
    label: graph.article.title,
    title: graph.article.title,
    summary: graph.article.summary,
    stance: graph.article.stance,
    url: `posts/${graph.article.slug}/`,
    weight: 10,
    refs: [graph.article.slug],
  });

  for (const topic of graph.topics || []) {
    const id = `topic:${topic.id}`;
    addNode({ id, type: "topic", label: topic.name, summary: "专题入口", weight: topic.weight, refs: [graph.article.slug] });
    addLink(articleId, id, "belongs_to", `${graph.article.title} 属于 ${topic.name}`, topic.weight);
  }

  for (const concept of graph.concepts || []) {
    const id = `concept:${concept.id}`;
    addNode({ id, type: "concept", label: concept.name, role: concept.role, summary: concept.summary, weight: concept.weight, refs: [graph.article.slug] });
    addLink(articleId, id, concept.role === "central" ? "centers_on" : "mentions", concept.summary, concept.weight);
  }

  for (const claim of graph.claims || []) {
    const id = `claim:${claim.id}`;
    addNode({ id, type: "claim", label: claim.text, summary: claim.text, importance: claim.importance, confidence: claim.confidence, status: claim.status, weight: claim.importance === "core" ? 10 : 7, refs: [graph.article.slug] });
    addLink(articleId, id, "makes", claim.text, claim.importance === "core" ? 10 : 7);
    for (const concept of claim.concepts || []) {
      addLink(id, `concept:${concept}`, "uses_concept", "这个判断依赖该概念", 5);
    }
  }

  for (const keyword of graph.keywords || []) {
    const id = normalizeId("keyword", keyword);
    addNode({ id, type: "keyword", label: keyword, summary: "检索关键词", weight: 2, refs: [graph.article.slug] });
    addLink(articleId, id, "has_keyword", keyword, 1);
  }

  for (const relation of graph.relations || []) {
    const source = relation.source.includes(":") ? relation.source : guessNodeId(relation.source);
    const target = relation.target.includes(":") ? relation.target : guessNodeId(relation.target);
    addLink(source, target, relation.type, relation.reason, 4);
  }
}

try {
  const bridges = JSON.parse(await readFile(bridgePath, "utf8"));
  for (const bridge of bridges) {
    addLink(bridge.source, bridge.target, bridge.type, bridge.reason, bridge.weight || 5);
  }
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}

function guessNodeId(id) {
  if (nodeMap.has(`article:${id}`)) return `article:${id}`;
  if (nodeMap.has(`claim:${id}`)) return `claim:${id}`;
  if (nodeMap.has(`concept:${id}`)) return `concept:${id}`;
  if (nodeMap.has(`topic:${id}`)) return `topic:${id}`;
  return id;
}

const graph = {
  generatedAt: new Date().toISOString(),
  stats: {
    articles: articles.length,
    nodes: nodeMap.size,
    links: links.length,
  },
  nodes: Array.from(nodeMap.values()),
  links,
};

await mkdir(outputDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(graph, null, 2)}\n`);
console.log(`Wrote ${outputPath} with ${graph.stats.nodes} nodes and ${graph.stats.links} links.`);
