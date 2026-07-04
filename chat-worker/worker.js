/**
 * kgk-practice-chat — Cloudflare Worker
 *
 * Server-side proxy for the "Ask about this practice" chat panel on the
 * practice-map demo: https://earlyprototype.github.io/knowledge-graph-kit/
 *
 * Holds the GEMINI_API_KEY secret server-side (added via the Cloudflare
 * dashboard or `wrangler secret put` — never committed to this repo) and
 * calls the Gemini API on the static frontend's behalf, grounded in a
 * fixed system prompt describing Thom Conaty's public projects.
 *
 * No message content is logged anywhere in this file. See README.md.
 */

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const GEMINI_MODEL = 'gemini-2.5-flash';
const GEMINI_URL = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent`;

const ALLOWED_ORIGIN = 'https://earlyprototype.github.io';
const LOCAL_ORIGIN_RE = /^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/;

const MAX_BODY_BYTES = 4096;
const MAX_MESSAGE_CHARS = 1500;
const MAX_HISTORY_MESSAGES = 8;
const MAX_OUTPUT_TOKENS = 512;

const QUOTA_REPLY =
  "I've hit my daily limit for now — the map itself still works, so feel free to keep exploring. Please try the chat again tomorrow.";
const UPSTREAM_ERROR_REPLY =
  "I'm having trouble answering right now — the map itself still works, so feel free to keep exploring. Please try again shortly.";

// Grounding data below is drawn directly from examples/practice-map/_data/entities.json
// (15 elements, 19 relationships) plus each project's real GitHub repo description,
// fetched at build time. Do not add projects, relationships, or claims that aren't
// backed by that data.
const SYSTEM_PROMPT = `You are the practice guide built into Thom Conaty's knowledge-graph practice-map demo, a live map of his public personal projects at https://earlyprototype.github.io/knowledge-graph-kit/.

Your job is to help visitors understand what's on THIS map: the projects, the three practice areas they sit within, and how they connect. You are friendly, plain-spoken, and concise — answer in 2 to 5 sentences by default, and only go longer if the visitor clearly asks for more depth.

THE THREE PRACTICE AREAS
- Service design: designing tools, workflows and interfaces that make complex work usable for people.
- AI systems: agentic tools, MCP servers and AI-integrated workflows.
- Research & play: open-ended experiments probing how models and ideas behave off the well-trodden path.

THE 12 PROJECTS ON THE MAP
(practice area(s) each one sits in, then what it is, then its repo)

1. knowledge-graph-kit — Service design
   A configurable, LLM-integrated knowledge graph toolkit with templates for Research, Systems Mapping and Ecosystem Mapping. It's the tool that generated this very map.
   Repo: https://github.com/earlyprototype/knowledge-graph-kit

2. FabLatticeGPT — Service design, AI systems
   An OpenAI-Accelerator-inspired custom GPT for FabLab users: it works through the core components of someone's idea with them and gives a structured plan for bringing it to life with digital fabrication, before they touch the machines.
   Repo: https://github.com/earlyprototype/FabLatticeGPT

3. kanbanger — AI systems, Service design
   An MCP-driven kanban board for mixed human/agent work, with a server-enforced human-approval gate before any task can be marked done, plus optional GitHub Projects sync.
   Repo: https://github.com/earlyprototype/kanbanger

4. thought_bubble — AI systems, Service design
   Turns dense documents into a visual webpage with logical flow — an MCP-connected tool for making long or boring documents easier to navigate.
   Repo: https://github.com/earlyprototype/thought_bubble

5. NotebookLM MCPs — AI systems
   MCP servers that put Google NotebookLM into agent workflows, built on the notebooklm-py library, including a workflow-tuned "diet" companion server for smoother setup.
   Repo: https://github.com/earlyprototype/notebooklm-py-MCP

6. hunch_kit — Research & play, AI systems
   A structured experimentation framework for testing hunches: human-in-the-loop evaluation, provider-agnostic execution, and MCP integration for AI-assisted experiment management.
   Repo: https://github.com/earlyprototype/hunch_kit

7. plugin marketplace — AI systems
   A Claude Code plugin marketplace (repo name: early-prototype) — installable with '/plugin marketplace add'.
   Repo: https://github.com/earlyprototype/early-prototype

8. lia-workflow-specs — AI systems
   Nicknamed "Slow-code" — a spec-driven framework for deliberate, understanding-first AI development, meant as a counterweight to vibe coding.
   Repo: https://github.com/earlyprototype/lia-workflow-specs

9. meTube — AI systems
   A YouTube content extractor: dual-layer transcripts (YouTube captions + Whisper), auto-extracted entities like repos, websites and topics, and interactive HTML reports. Built as a TypeScript Ink CLI.
   Repo: https://github.com/earlyprototype/meTube

10. plasticFlowers — AI systems, Research & play
    A local-first live mindmap that listens to speech and builds an emergent knowledge graph in real time via Gemini.
    Repo: https://github.com/earlyprototype/plasticFlowers

11. FALSE FLAG — Research & play
    An LLM-driven political-military crisis simulation with AI cabinet advisors and free-form, adjudicated decision-making.
    Repo: https://github.com/earlyprototype/false-flag

12. Activation Tensor Resonance — Research & play
    Inspired by Alvin Lucier's "I Am Sitting in a Room": GPT-2 Small's activation tensor is excited through 500 rounds of iterative feedback. As semantic content dissolves, dominant attractor states emerge — the model's own "naked inner voice."
    Repo: https://github.com/earlyprototype/lucier-gpt2-activ-tensor-reson-experiments

HOW PROJECTS CONNECT TO EACH OTHER (beyond just sharing a practice area)
- thought_bubble influences Activation Tensor Resonance: it visualises ATR's activation-tensor experiments as an interactive mind-map.
- kanbanger regulates plugin marketplace: it governs how plugin-marketplace tasks move through review before being marked done.

Every project above also "enables" (practices and builds out) the practice area(s) listed next to its name — that's the main way most projects relate to each other: through a shared practice area, not a direct link.

HOW TO ANSWER
- Only talk about what's listed above: these 12 projects, these 3 practice areas, and these connections. Never invent a project, feature, relationship, or detail that isn't stated here.
- If someone asks something unrelated to this practice map (general coding help, unrelated news, personal questions about Thom that aren't reflected here, etc.), politely decline and offer to help with the map instead.
- When it's useful, point people to the relevant repo link so they can read more.
- Keep answers short by default (2-5 sentences). Only go into more detail if the visitor asks for it.
- You only see the last few messages of this conversation — if something seems missing, that's why.`;

// ---------------------------------------------------------------------------
// CORS
// ---------------------------------------------------------------------------

function resolveAllowedOrigin(origin) {
  if (!origin) return null;
  if (origin === ALLOWED_ORIGIN) return origin;
  if (LOCAL_ORIGIN_RE.test(origin)) return origin;
  return null;
}

function corsHeaders(origin) {
  const allowed = resolveAllowedOrigin(origin);
  const headers = {
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
    Vary: 'Origin',
  };
  if (allowed) {
    headers['Access-Control-Allow-Origin'] = allowed;
  }
  return headers;
}

function jsonResponse(body, status, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders(origin),
    },
  });
}

// ---------------------------------------------------------------------------
// Input validation
// ---------------------------------------------------------------------------

function validateMessages(messages) {
  if (!Array.isArray(messages) || messages.length === 0) {
    return 'messages must be a non-empty array';
  }
  for (const m of messages) {
    if (!m || (m.role !== 'user' && m.role !== 'assistant')) {
      return 'each message needs role "user" or "assistant"';
    }
    if (typeof m.text !== 'string' || m.text.trim().length === 0) {
      return 'each message needs non-empty text';
    }
    if (m.text.length > MAX_MESSAGE_CHARS) {
      return `each message must be ${MAX_MESSAGE_CHARS} characters or fewer`;
    }
  }
  if (messages[messages.length - 1].role !== 'user') {
    return 'the last message must be from the user';
  }
  return null;
}

// ---------------------------------------------------------------------------
// Gemini call
// ---------------------------------------------------------------------------

function toGeminiContents(messages) {
  return messages.map((m) => ({
    role: m.role === 'assistant' ? 'model' : 'user',
    parts: [{ text: m.text }],
  }));
}

async function callGemini(apiKey, messages) {
  const payload = {
    systemInstruction: { parts: [{ text: SYSTEM_PROMPT }] },
    contents: toGeminiContents(messages),
    generationConfig: { maxOutputTokens: MAX_OUTPUT_TOKENS },
  };

  const response = await fetch(GEMINI_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-goog-api-key': apiKey,
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const status = data?.error?.status;
    const code = data?.error?.code ?? response.status;
    const isQuota = code === 429 || status === 'RESOURCE_EXHAUSTED';
    return { ok: false, quota: isQuota };
  }

  const text = (data?.candidates?.[0]?.content?.parts || [])
    .map((p) => p.text || '')
    .join('')
    .trim();

  if (!text) {
    return { ok: false, quota: false };
  }
  return { ok: true, text };
}

// ---------------------------------------------------------------------------
// Request handling
// ---------------------------------------------------------------------------

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin');

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders(origin) });
    }

    if (request.method !== 'POST') {
      return jsonResponse({ error: 'POST only' }, 405, origin);
    }

    if (!resolveAllowedOrigin(origin)) {
      return jsonResponse({ error: 'origin not allowed' }, 403, origin);
    }

    const rawBody = await request.text();
    const bodyByteLength = new TextEncoder().encode(rawBody).length;
    if (bodyByteLength > MAX_BODY_BYTES) {
      return jsonResponse({ error: 'request body too large' }, 413, origin);
    }

    let body;
    try {
      body = JSON.parse(rawBody);
    } catch {
      return jsonResponse({ error: 'invalid JSON' }, 400, origin);
    }

    const validationError = validateMessages(body && body.messages);
    if (validationError) {
      return jsonResponse({ error: validationError }, 400, origin);
    }

    const history = body.messages.slice(-MAX_HISTORY_MESSAGES);

    if (!env.GEMINI_API_KEY) {
      // Secret not configured yet — graceful, not a crash.
      return jsonResponse({ reply: UPSTREAM_ERROR_REPLY, limited: true }, 200, origin);
    }

    try {
      const result = await callGemini(env.GEMINI_API_KEY, history);
      if (!result.ok) {
        return jsonResponse(
          { reply: result.quota ? QUOTA_REPLY : UPSTREAM_ERROR_REPLY, limited: true },
          200,
          origin
        );
      }
      return jsonResponse({ reply: result.text }, 200, origin);
    } catch {
      return jsonResponse({ reply: UPSTREAM_ERROR_REPLY, limited: true }, 200, origin);
    }
  },
};
