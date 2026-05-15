import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();

const posts = [
  {
    source: "C:/Users/kvenu/playground/sub-wiki/poddeck/claude-code-eggs.md",
    slug: "claude-code-eggs",
    title: "Claude Code 源码泄露里的彩蛋",
    date: "2026-05-15T00:10:00+08:00",
    description: "从 Claude Code 源码泄露里看到的内部模式、做梦、宠物、卧底模式和产品气质。",
  },
  {
    source: "C:/Users/kvenu/playground/claude-code/blog-cc-v2-new.md",
    slug: "claude-code-false-claims",
    title: "你的 Agent 总在报喜不报忧：看看 Claude Code 怎么纠偏",
    date: "2026-05-15T00:20:00+08:00",
    description: "从 False Claim、验证合约和运行时拦截看 Claude Code 怎么补偿模型弱点。",
  },
  {
    source: "C:/Users/kvenu/playground/sub-wiki/poddeck/blog-superpowers-management.md",
    slug: "superpowers-management",
    title: "如何管理一群聪明但缺乏判断力的实习生？",
    date: "2026-05-15T00:30:00+08:00",
    description: "Superpowers 把 coding agent 当作聪明但缺判断力的实习生来管理。",
  },
];

function stripTitle(markdown) {
  return markdown.replace(/^# .+?\r?\n+/, "");
}

function normalizeImages(markdown) {
  return markdown.replace(/!\[([^\]]*)\]\(([^)]*)\)/g, (match, alt, src) => {
    const value = src.trim();
    if (!value || value === "#" || value === "图片占位" || value.startsWith("./images/")) {
      return `![${alt}](/images/article-placeholder.svg)`;
    }
    return match;
  });
}

function frontMatter(post) {
  return `---\ntitle: "${post.title.replaceAll('"', '\\"')}"\ndate: ${post.date}\ndescription: "${post.description.replaceAll('"', '\\"')}"\ndraft: false\nslug: "${post.slug}"\n---\n\n`;
}

await rm(path.join(root, "content", "posts", "hello-blog.md"), { force: true });

for (const post of posts) {
  const targetDir = path.join(root, "content", "posts", post.slug);
  await mkdir(targetDir, { recursive: true });
  const source = await readFile(post.source, "utf8");
  const body = normalizeImages(stripTitle(source).trim());
  await writeFile(path.join(targetDir, "index.md"), `${frontMatter(post)}${body}\n`);
}
