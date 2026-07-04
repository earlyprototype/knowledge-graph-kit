# kgk-practice-chat

Cloudflare Worker behind the "Ask about this practice" chat panel on the
[practice-map demo](https://earlyprototype.github.io/knowledge-graph-kit/).
It holds the Gemini API key server-side so the key is never exposed in the
static frontend.

## What it does

- Accepts a short chat history (`POST` only) from the demo page.
- Grounds every reply in a fixed system prompt describing the projects on
  the map, the three practice areas they sit in, and how they connect (see
  the `SYSTEM_PROMPT` constant in `worker.js` — built from
  `examples/practice-map/_data/entities.json` plus each project's real
  GitHub description).
- Calls the Gemini API (`gemini-2.5-flash` — see note below) and returns the
  reply as `{ "reply": "..." }`.
- If Gemini is out of quota, or any other upstream error occurs, it returns
  the same JSON shape with a friendly "I can't answer right now, but the
  map still works" message instead of a raw error, so the frontend always
  has something sensible to render.
- CORS is locked to `https://earlyprototype.github.io`, plus
  `http://localhost:*` / `http://127.0.0.1:*` for local testing. Requests
  from any other origin are rejected.

Model note: the task spec suggested `gemini-2.0-flash`, but that model is
now deprecated per Google's own docs. This worker uses `gemini-2.5-flash`
instead — the current stable "best price-performance" flash model and the
direct successor in spirit. If Google ships something cheaper/better later,
change the `GEMINI_MODEL` constant at the top of `worker.js`.

## Deploy

From this folder:

```bash
npx wrangler login       # once, if not already authenticated
npx wrangler deploy
```

This publishes to `https://kgk-practice-chat.<your-subdomain>.workers.dev`.
Wrangler prints the exact URL after deploy — copy it into the
`CHAT_WORKER_URL` constant near the top of the chat script in
`docs/index.html`.

## Add the API key (Cloudflare dashboard)

The worker needs one secret, `GEMINI_API_KEY`. It is never stored in this
repo — add it directly in Cloudflare:

1. Go to the [Cloudflare dashboard](https://dash.cloudflare.com) →
   **Workers & Pages**.
2. Open the **kgk-practice-chat** worker.
3. Go to **Settings → Variables and Secrets**.
4. Click **Add**:
   - Name: `GEMINI_API_KEY`
   - Value: your Gemini API key
   - Type: **Secret** (encrypted)
5. Save / Deploy to apply it.

Equivalent CLI, if you'd rather not use the dashboard:

```bash
npx wrangler secret put GEMINI_API_KEY
```

Until the key is set, the worker responds to every chat request with the
same graceful "unavailable" message — it won't error or crash, and the
rest of the demo is unaffected either way.

## Privacy

The worker never logs message content. Cloudflare's own platform-level
request logs (if enabled on the account) may capture standard metadata
(IP, timing, status code), but nothing in this code writes chat text to
any log, storage, or third party other than the single Gemini API call
needed to produce the reply.

## Limits enforced here

- Request body capped at 4KB.
- Individual messages capped at 1500 characters.
- Only the last 8 messages of history are sent to Gemini.
- Replies capped at ~512 output tokens.
