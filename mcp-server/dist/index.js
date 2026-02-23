import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
const SITE_URL = "https://zatoima.github.io";
function parseLlmsFullTxt(text) {
    const posts = [];
    // Split by "---" separator between posts
    const sections = text.split(/\n---\n/);
    for (const section of sections) {
        const trimmed = section.trim();
        if (!trimmed || trimmed.startsWith("# "))
            continue; // skip header
        const titleMatch = trimmed.match(/^### (.+)$/m);
        const dateMatch = trimmed.match(/^date: (.+)$/m);
        const urlMatch = trimmed.match(/^url: (.+)$/m);
        const tagsMatch = trimmed.match(/^tags: (.+)$/m);
        if (!titleMatch)
            continue;
        // Extract content (everything after the metadata lines)
        const metaEnd = trimmed.lastIndexOf(tagsMatch ? tagsMatch[0] : urlMatch ? urlMatch[0] : dateMatch ? dateMatch[0] : titleMatch[0]);
        const afterMeta = trimmed.slice(metaEnd);
        const contentStart = afterMeta.indexOf("\n");
        const content = contentStart >= 0
            ? afterMeta.slice(contentStart).trim()
            : "";
        posts.push({
            title: titleMatch[1].trim(),
            date: dateMatch ? dateMatch[1].trim().slice(0, 10) : "",
            url: urlMatch ? urlMatch[1].trim() : "",
            tags: tagsMatch ? tagsMatch[1].split(",").map((t) => t.trim()) : [],
            content,
        });
    }
    posts.sort((a, b) => b.date.localeCompare(a.date));
    return posts;
}
let allPosts = [];
let lastFetch = 0;
const CACHE_TTL = 10 * 60 * 1000; // 10 minutes
async function getPosts() {
    const now = Date.now();
    if (allPosts.length > 0 && now - lastFetch < CACHE_TTL) {
        return allPosts;
    }
    try {
        const res = await fetch(`${SITE_URL}/llms-full.txt`);
        if (!res.ok)
            throw new Error(`HTTP ${res.status}`);
        const text = await res.text();
        allPosts = parseLlmsFullTxt(text);
        lastFetch = now;
        console.error(`Fetched ${allPosts.length} posts from ${SITE_URL}/llms-full.txt`);
    }
    catch (e) {
        console.error("Failed to fetch posts:", e);
        if (allPosts.length === 0) {
            throw new Error("記事データの取得に失敗しました。サイトに接続できません。");
        }
    }
    return allPosts;
}
// --- MCP Server ---
const server = new McpServer({
    name: "zatoima-blog",
    version: "1.0.0",
});
// Tool: search posts
server.tool("search_posts", "ブログ記事をキーワードで検索する。タイトルと本文を全文検索する。", {
    query: z.string().describe("検索キーワード"),
    limit: z.number().optional().default(10).describe("返す最大件数 (デフォルト10)"),
}, async ({ query, limit }) => {
    const posts = await getPosts();
    const q = query.toLowerCase();
    const results = posts
        .filter((p) => p.title.toLowerCase().includes(q) ||
        p.content.toLowerCase().includes(q) ||
        p.tags.some((t) => t.toLowerCase().includes(q)))
        .slice(0, limit);
    const text = results.length === 0
        ? `「${query}」に一致する記事は見つかりませんでした。`
        : results
            .map((p, i) => `${i + 1}. [${p.date}] ${p.title}\n   tags: ${p.tags.join(", ")}\n   url: ${p.url}`)
            .join("\n\n");
    return { content: [{ type: "text", text: `検索結果 (${results.length}件):\n\n${text}` }] };
});
// Tool: read a post
server.tool("read_post", "ブログ記事の全文を取得する。slug(ディレクトリ名)またはタイトルの一部を指定する。", {
    identifier: z.string().describe("記事のslug(ディレクトリ名)またはタイトルの一部"),
}, async ({ identifier }) => {
    const posts = await getPosts();
    const id = identifier.toLowerCase();
    const post = posts.find((p) => p.url.toLowerCase().includes(id) ||
        p.title.toLowerCase().includes(id));
    if (!post) {
        return { content: [{ type: "text", text: `記事が見つかりませんでした: ${identifier}` }] };
    }
    const header = [
        `# ${post.title}`,
        `date: ${post.date}`,
        `tags: ${post.tags.join(", ")}`,
        `url: ${post.url}`,
        `---`,
    ].join("\n");
    return { content: [{ type: "text", text: `${header}\n\n${post.content}` }] };
});
// Tool: list posts
server.tool("list_posts", "ブログ記事一覧を取得する。タグやカテゴリでフィルタ可能。", {
    tag: z.string().optional().describe("タグでフィルタ"),
    category: z.string().optional().describe("カテゴリでフィルタ"),
    year: z.string().optional().describe("年でフィルタ (例: 2024)"),
    limit: z.number().optional().default(20).describe("返す最大件数 (デフォルト20)"),
    offset: z.number().optional().default(0).describe("オフセット (デフォルト0)"),
}, async ({ tag, category, year, limit, offset }) => {
    let posts = await getPosts();
    if (tag) {
        const t = tag.toLowerCase();
        posts = posts.filter((p) => p.tags.some((pt) => pt.toLowerCase() === t));
    }
    if (category) {
        const c = category.toLowerCase();
        posts = posts.filter((p) => p.tags.some((pt) => pt.toLowerCase() === c));
    }
    if (year) {
        posts = posts.filter((p) => p.date.startsWith(year));
    }
    const total = posts.length;
    const paged = posts.slice(offset, offset + limit);
    const text = paged
        .map((p, i) => `${offset + i + 1}. [${p.date}] ${p.title}\n   tags: ${p.tags.join(", ")}`)
        .join("\n\n");
    return {
        content: [
            {
                type: "text",
                text: `記事一覧 (${total}件中 ${offset + 1}〜${offset + paged.length}件):\n\n${text}`,
            },
        ],
    };
});
// Tool: list tags
server.tool("list_tags", "ブログで使用されている全タグとその記事数を取得する。", {}, async () => {
    const posts = await getPosts();
    const tagCount = new Map();
    for (const p of posts) {
        for (const t of p.tags) {
            tagCount.set(t, (tagCount.get(t) ?? 0) + 1);
        }
    }
    const sorted = [...tagCount.entries()].sort((a, b) => b[1] - a[1]);
    const text = sorted.map(([tag, count]) => `${tag} (${count})`).join("\n");
    return { content: [{ type: "text", text: `タグ一覧 (${sorted.length}種):\n\n${text}` }] };
});
// Tool: get stats
server.tool("blog_stats", "ブログの統計情報を取得する(記事数、年別投稿数、人気タグなど)。", {}, async () => {
    const posts = await getPosts();
    const yearCount = new Map();
    const tagCount = new Map();
    for (const p of posts) {
        const y = p.date.slice(0, 4);
        yearCount.set(y, (yearCount.get(y) ?? 0) + 1);
        for (const t of p.tags) {
            tagCount.set(t, (tagCount.get(t) ?? 0) + 1);
        }
    }
    const yearStats = [...yearCount.entries()]
        .sort((a, b) => b[0].localeCompare(a[0]))
        .map(([y, c]) => `  ${y}: ${c}件`)
        .join("\n");
    const topTags = [...tagCount.entries()]
        .sort((a, b) => b[1] - a[1])
        .slice(0, 15)
        .map(([t, c]) => `  ${t}: ${c}件`)
        .join("\n");
    const text = [
        `総記事数: ${posts.length}`,
        `\n年別投稿数:\n${yearStats}`,
        `\nトップ15タグ:\n${topTags}`,
    ].join("\n");
    return { content: [{ type: "text", text }] };
});
// Resource: recent posts
server.resource("recent-posts", "blog://recent", async (uri) => {
    const posts = await getPosts();
    const recent = posts.slice(0, 10);
    const text = recent
        .map((p) => `[${p.date}] ${p.title} (tags: ${p.tags.join(", ")})`)
        .join("\n");
    return {
        contents: [
            {
                uri: uri.href,
                mimeType: "text/plain",
                text: `最近の記事 (10件):\n\n${text}`,
            },
        ],
    };
});
// Start
async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("zatoima-blog MCP server started (remote mode)");
}
main().catch(console.error);
