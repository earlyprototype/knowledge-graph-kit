"""
Gemini Chat API Server for the Evidence Graph Viewer

Provides REST API endpoints for graph-grounded chat via the Gemini API
(model set in gemini_config.json), with context management, session
persistence, and summarization.

Context for a conversation is assembled from:
  - _data/entities.json (the whole evidence graph)
  - optionally, one claim's documentation: its doc_ref file plus the paths of
    any sources documented-in / evidenced-by that claim.
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import traceback

from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Configuration
BASE_DIR = Path(__file__).parent  # the project directory
CONFIG_FILE = BASE_DIR / "gemini_config.json"
ENTITIES_FILE = BASE_DIR / "_data" / "entities.json"  # graph data lives in _data/ (see config.yaml)
CHAT_SESSIONS_DIR = BASE_DIR / ".chat_sessions"
# Optional per-claim context, loaded only if these directories exist:
DOCS_DIR = BASE_DIR / "docs"
OUTPUT_DIR = BASE_DIR / "output"

# Global state
gemini_model = None
entities_content = None
current_sessions = {}  # {session_id: session_data}


def load_config() -> Dict[str, Any]:
    """Load Gemini API configuration from config file."""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_FILE}\n"
            f"Please copy gemini_config.template.json to gemini_config.json "
            f"and add your API key."
        )

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)

    if not config.get('api_key') or config['api_key'] == 'YOUR_GEMINI_API_KEY':
        raise ValueError(
            "API key not configured. Please add your Gemini API key to "
            f"{CONFIG_FILE}"
        )

    return config


def initialize_gemini():
    """Initialize Gemini API with configuration."""
    global gemini_model, entities_content

    try:
        config = load_config()

        # Configure Gemini API
        genai.configure(api_key=config['api_key'])

        # Initialize model
        model_name = config.get('model', 'gemini-2.0-flash-exp')
        gemini_model = genai.GenerativeModel(model_name)

        # Load entities.json for system context
        if ENTITIES_FILE.exists():
            with open(ENTITIES_FILE, 'r', encoding='utf-8') as f:
                entities_content = f.read()
        else:
            entities_content = None
            print(f"Warning: entities.json not found at {ENTITIES_FILE}")

        print(f"✓ Gemini API initialized with model: {model_name}")
        return True

    except Exception as e:
        print(f"✗ Failed to initialize Gemini API: {e}")
        traceback.print_exc()
        return False


def _load_graph() -> Optional[Dict[str, Any]]:
    """Load the evidence graph from disk (fresh, so edits are picked up)."""
    if not ENTITIES_FILE.exists():
        return None
    try:
        with open(ENTITIES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: could not parse {ENTITIES_FILE}: {e}")
        return None


def _read_repo_file(rel_path: str) -> Optional[str]:
    """Read a repo-relative text file if it exists and is inside the project."""
    if not rel_path or rel_path.startswith(('http://', 'https://')):
        return None

    # doc_ref may carry a markdown anchor: docs/FINDINGS.md#f9-divine
    clean = rel_path.split('#', 1)[0].strip()
    if not clean:
        return None

    candidate = (BASE_DIR / clean).resolve()
    try:
        candidate.relative_to(BASE_DIR.resolve())
    except ValueError:
        print(f"Warning: refusing to read path outside project: {rel_path}")
        return None

    if not candidate.is_file():
        return None

    try:
        return candidate.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"Warning: Could not read {candidate}: {e}")
        return None


def load_claim_context(claim_id: str) -> Dict[str, str]:
    """Load documentation relevant to a single claim.

    Returns a {label: text} mapping covering:
      - the claim record itself
      - the file named by the claim's doc_ref
      - the runs listed in the claim's `evidence`
      - any sources linked to the claim by documented-in / evidenced-by edges
    """
    context_files: Dict[str, str] = {}
    graph = _load_graph()
    if graph is None:
        return context_files

    claims = {c['id']: c for c in graph.get('claims', [])}
    runs = {r['id']: r for r in graph.get('runs', [])}
    sources = {s['id']: s for s in graph.get('sources', [])}

    claim = claims.get(claim_id)
    if claim is None:
        return context_files

    context_files['claim.json'] = json.dumps(claim, indent=2, ensure_ascii=False)

    # The claim's own documentation
    doc_ref = claim.get('doc_ref')
    if doc_ref:
        text = _read_repo_file(doc_ref)
        if text:
            context_files[f"doc_ref:{doc_ref}"] = text

    # Runs cited as evidence
    evidence_runs = [runs[r] for r in claim.get('evidence', []) or [] if r in runs]

    # Edges touching this claim
    related_source_ids: List[str] = []
    edge_lines: List[str] = []
    for rel in graph.get('relationships', []):
        if rel.get('from') != claim_id and rel.get('to') != claim_id:
            continue
        edge_lines.append(
            f"- {rel.get('from')} --{rel.get('type')}--> {rel.get('to')}: "
            f"{rel.get('description', '')}"
        )
        for endpoint in (rel.get('from'), rel.get('to')):
            if endpoint in sources and endpoint not in related_source_ids:
                related_source_ids.append(endpoint)
            if endpoint in runs and runs[endpoint] not in evidence_runs:
                evidence_runs.append(runs[endpoint])

    if edge_lines:
        context_files['edges.md'] = "\n".join(edge_lines)

    if evidence_runs:
        context_files['runs.json'] = json.dumps(evidence_runs, indent=2, ensure_ascii=False)

    for source_id in related_source_ids:
        source = sources[source_id]
        context_files[f"source:{source_id}"] = json.dumps(source, indent=2, ensure_ascii=False)
        text = _read_repo_file(source.get('path', ''))
        if text:
            context_files[f"source-file:{source.get('path')}"] = text

    return context_files


def create_system_prompt(claim_context: Optional[Dict[str, str]] = None) -> str:
    """Create system prompt with the evidence graph and optional claim context."""
    prompt_parts = []

    # Base system prompt
    prompt_parts.append("""You are an evidence assistant working with an evidence graph.

The graph contains:
- claims: hypotheses, findings and concepts. Each has a status (supported, refuted,
  qualified, retired, corrected, open, untested), an `asserted` date and optionally a
  `retired` date, so its standing can be read at any point in time.
- runs: experiments, models and null models that produce evidence.
- sources: docs, artefacts and prior work.
- relationships: signed epistemic edges (supports, refutes, qualifies, corrects,
  retires, supersedes, tests), structural edges (produced-by, run-on, evidenced-by,
  documented-in) and associative edges (analogous-to, breaks-down-at, builds-on,
  cites, relates-to). Every edge carries a description saying why it holds.

Your role is to:
- Report where a claim stands now, and what changed it and when
- Trace the chain of runs and artefacts that support or refute a claim
- Surface contradictions: claims carrying both supporting and refuting edges
- Point out open or untested claims that no run has yet addressed
- Reconstruct the state of the graph as of a given date or phase

Always:
- Cite the run ids, artefact paths or doc_refs that back what you say
- Distinguish "supported" from "not yet tested" - absence of evidence is not refutation
- Respect the direction of edges: A supports B is not B supports A
- Say "not recorded in the graph" rather than guessing; never invent runs or results
- Use UK English spelling
- Be concise but precise
""")

    # Add entities.json context
    if entities_content:
        # Truncate if too large (keep first 50KB for now)
        entities_truncated = entities_content[:50000]
        if len(entities_content) > 50000:
            entities_truncated += "\n\n[... entities.json truncated for context window ...]"

        prompt_parts.append(f"""
# Evidence Graph Context

You have access to the following evidence graph (entities.json):

{entities_truncated}

Use this to reason about claim status, evidence chains and how claims changed over time.
""")

    # Add claim-specific context if provided
    if claim_context:
        prompt_parts.append("\n# Current Claim Context\n")
        prompt_parts.append("The user is currently looking at a specific claim. Here is its record, "
                            "its edges, and the documents and runs attached to it:\n")

        # Add files in logical order
        file_order = ['claim.json', 'edges.md', 'runs.json']

        for filename in file_order:
            if filename in claim_context:
                content = claim_context[filename]
                if len(content) > 30000:
                    content = content[:30000] + "\n\n[... file truncated ...]"
                prompt_parts.append(f"\n## {filename}\n\n{content}\n")

        # Add remaining doc_ref / source files
        for filename, content in claim_context.items():
            if filename in file_order:
                continue
            if len(content) > 30000:
                content = content[:30000] + "\n\n[... file truncated ...]"
            prompt_parts.append(f"\n## {filename}\n\n{content}\n")

    return "\n".join(prompt_parts)


def save_session(session_id: str, session_data: Dict[str, Any]):
    """Save chat session to disk."""
    try:
        claim_id = session_data.get('claim_id', 'general')
        session_dir = CHAT_SESSIONS_DIR / claim_id
        session_dir.mkdir(parents=True, exist_ok=True)

        thread_id = session_data.get('thread_id', session_id)
        session_file = session_dir / f"thread_{thread_id}.json"

        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

        print(f"✓ Session saved: {session_file}")
        return True

    except Exception as e:
        print(f"✗ Failed to save session: {e}")
        traceback.print_exc()
        return False


def estimate_token_count(text: str) -> int:
    """Rough estimate of token count (4 characters ≈ 1 token)."""
    return len(text) // 4


# API Endpoints

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint - send message and receive response."""
    try:
        data = request.json
        message = data.get('message', '').strip()
        session_id = data.get('session_id')
        claim_id = data.get('claim_id')  # None for general chat

        if not message:
            return jsonify({'error': 'Message is required'}), 400

        # Get or create session
        if not session_id or session_id not in current_sessions:
            session_id = str(uuid.uuid4())
            current_sessions[session_id] = {
                'thread_id': session_id,
                'claim_id': claim_id or 'general',
                'created_at': datetime.now().isoformat(),
                'messages': [],
                'context_files': [],
                'token_count': 0
            }

        session = current_sessions[session_id]

        # Add user message to history
        session['messages'].append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })

        # Load claim context if claim_id provided
        claim_context = None
        if claim_id and claim_id != 'general':
            claim_context = load_claim_context(claim_id)
            if claim_context and not session['context_files']:
                session['context_files'] = list(claim_context.keys())

        # Create system prompt
        system_prompt = create_system_prompt(claim_context)

        # Build conversation history for Gemini
        conversation_parts = []
        for msg in session['messages']:
            conversation_parts.append(f"{msg['role']}: {msg['content']}")

        full_prompt = f"{system_prompt}\n\n{''.join(conversation_parts)}\n\nassistant:"

        # Estimate token count
        session['token_count'] = estimate_token_count(full_prompt)

        # Check if approaching context limit (assuming 1M tokens for Gemini 2.0)
        needs_summary = session['token_count'] > 800000  # 80% of 1M

        # Generate response using Gemini
        try:
            response = gemini_model.generate_content(full_prompt)
            assistant_message = response.text

        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            traceback.print_exc()
            return jsonify({
                'error': 'Failed to generate response',
                'details': str(e)
            }), 500

        # Add assistant response to history
        session['messages'].append({
            'role': 'assistant',
            'content': assistant_message,
            'timestamp': datetime.now().isoformat()
        })

        # Auto-save session
        save_session(session_id, session)

        return jsonify({
            'response': assistant_message,
            'session_id': session_id,
            'token_count': session['token_count'],
            'needs_summary': needs_summary,
            'context_loaded': len(session['context_files']) > 0,
            'context_files': session['context_files']
        })

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat/new-thread', methods=['POST'])
def new_thread():
    """Start a new conversation thread."""
    try:
        data = request.json or {}
        claim_id = data.get('claim_id')

        session_id = str(uuid.uuid4())
        current_sessions[session_id] = {
            'thread_id': session_id,
            'claim_id': claim_id or 'general',
            'created_at': datetime.now().isoformat(),
            'messages': [],
            'context_files': [],
            'token_count': 0
        }

        return jsonify({
            'session_id': session_id,
            'message': 'New thread created'
        })

    except Exception as e:
        print(f"Error creating new thread: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat/save-session', methods=['POST'])
def save_session_endpoint():
    """Manually save current chat session."""
    try:
        data = request.json or {}
        session_id = data.get('session_id')

        if not session_id or session_id not in current_sessions:
            return jsonify({'error': 'Session not found'}), 404

        session = current_sessions[session_id]
        success = save_session(session_id, session)

        if success:
            return jsonify({'message': 'Session saved successfully'})
        else:
            return jsonify({'error': 'Failed to save session'}), 500

    except Exception as e:
        print(f"Error saving session: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat/load-context/<claim_id>', methods=['GET'])
def load_context(claim_id: str):
    """Load context files for a claim."""
    try:
        context_files = load_claim_context(claim_id)

        return jsonify({
            'claim_id': claim_id,
            'files_loaded': list(context_files.keys()),
            'file_count': len(context_files),
            'message': f'Loaded {len(context_files)} context files for {claim_id}'
        })

    except Exception as e:
        print(f"Error loading context: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat/generate-summary', methods=['POST'])
def generate_summary():
    """Generate summary of conversation using Gemini."""
    try:
        data = request.json or {}
        session_id = data.get('session_id')

        if not session_id or session_id not in current_sessions:
            return jsonify({'error': 'Session not found'}), 404

        session = current_sessions[session_id]

        # Build conversation text
        conversation_text = []
        for msg in session['messages']:
            conversation_text.append(f"**{msg['role'].title()}**: {msg['content']}\n")

        conversation_str = "\n".join(conversation_text)

        # Generate summary
        summary_prompt = f"""Please provide a concise summary of this evidence-graph conversation.
Include:
- Which claims were discussed, and their status
- What evidence (runs, artefacts, docs) was cited
- Any contradictions or open questions that remain
- Suggested next runs or checks

Conversation:
{conversation_str}

Summary:"""

        response = gemini_model.generate_content(summary_prompt)
        summary = response.text

        # Save summary to file
        claim_id = session.get('claim_id', 'general')
        session_dir = CHAT_SESSIONS_DIR / claim_id
        session_dir.mkdir(parents=True, exist_ok=True)

        thread_id = session['thread_id']
        summary_file = session_dir / f"thread_{thread_id}_summary.md"

        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"# Chat Session Summary\n\n")
            f.write(f"**Session ID**: {thread_id}\n")
            f.write(f"**Claim**: {claim_id}\n")
            f.write(f"**Date**: {session['created_at']}\n")
            f.write(f"**Messages**: {len(session['messages'])}\n\n")
            f.write(f"## Summary\n\n{summary}\n")

        print(f"✓ Summary saved: {summary_file}")

        return jsonify({
            'summary': summary,
            'summary_file': str(summary_file),
            'message': 'Summary generated and saved'
        })

    except Exception as e:
        print(f"Error generating summary: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'domain': 'evidence',
        'gemini_initialized': gemini_model is not None,
        'entities_loaded': entities_content is not None,
        'active_sessions': len(current_sessions)
    })


def main():
    """Start the Flask API server."""
    print("=" * 60)
    print("Evidence Graph - Gemini Chat API Server")
    print("=" * 60)

    # Initialize Gemini
    if not initialize_gemini():
        print("\n⚠️  Server starting without Gemini initialization")
        print("Please check your configuration and restart the server\n")

    print(f"\n📁 Base directory: {BASE_DIR}")
    print(f"📁 Sessions directory: {CHAT_SESSIONS_DIR}")
    print(f"\n🚀 Starting Flask server on http://localhost:8001")
    print("=" * 60 + "\n")

    # Create sessions directory
    CHAT_SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    # Start Flask server
    app.run(host='0.0.0.0', port=8001, debug=False, threaded=True)


if __name__ == '__main__':
    main()
