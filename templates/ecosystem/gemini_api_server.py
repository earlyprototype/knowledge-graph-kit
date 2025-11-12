"""
Gemini Chat API Server for Knowledge Graph Viewer

Provides REST API endpoints for chat functionality with Gemini 2.5 Pro,
including context management, session persistence, and intelligent summarization.

Author: Research Paper Analysis System
Version: 1.0.0
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
BASE_DIR = Path(__file__).parent.parent.parent  # AI/_Research directory
CONFIG_FILE = Path(__file__).parent / "gemini_config.json"
ENTITIES_FILE = Path(__file__).parent / "entities.json"
CHAT_SESSIONS_DIR = BASE_DIR / ".lia" / "chat_sessions"
PAPER_ANALYSIS_DIR = BASE_DIR / ".lia" / "paper"
RESEARCH_PAPERS_DIR = BASE_DIR / "@Research" / "papers"

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


def load_paper_context(paper_id: str) -> Dict[str, str]:
    """Load all markdown files for a specific paper."""
    context_files = {}
    
    # Load from .lia/paper/{paper_id}/
    paper_dir = PAPER_ANALYSIS_DIR / paper_id
    if paper_dir.exists():
        # Standard analysis files
        analysis_files = [
            '0-source-document.md',
            '0-notepad.md',
            '1-context.md',
            '2-structure.md',
            '3-methodology.md',
            '4-evidence.md',
            '5-contribution.md',
            '6-synthesis.md',
            '7-citations.md',
            '8-integration.md'
        ]
        
        for filename in analysis_files:
            file_path = paper_dir / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        context_files[filename] = f.read()
                except Exception as e:
                    print(f"Warning: Could not read {file_path}: {e}")
        
        # Load any ANALYSIS_*.md files
        for file_path in paper_dir.glob('ANALYSIS_*.md'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    context_files[file_path.name] = f.read()
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")
    
    # Load summary from @Research/papers/
    summary_path = RESEARCH_PAPERS_DIR / f"{paper_id}_summary.md"
    if not summary_path.exists():
        # Try without _summary suffix
        summary_path = RESEARCH_PAPERS_DIR / f"{paper_id}.md"
    
    if summary_path.exists():
        try:
            with open(summary_path, 'r', encoding='utf-8') as f:
                context_files['paper_summary.md'] = f.read()
        except Exception as e:
            print(f"Warning: Could not read {summary_path}: {e}")
    
    return context_files


def create_system_prompt(paper_context: Optional[Dict[str, str]] = None) -> str:
    """Create system prompt with entities and optional paper context."""
    prompt_parts = []
    
    # Base system prompt
    prompt_parts.append("""You are a research assistant helping analyze academic papers on Design Thinking, Human-AI Collaboration, and Innovation. You have access to a knowledge graph containing concepts, papers, and researchers.

Your role is to:
- Answer questions about research papers with academic rigour
- Explain concepts and their relationships
- Help synthesise insights across multiple papers
- Provide critical analysis and identify research gaps
- Suggest connections between ideas

Always:
- Cite specific papers and sections when making claims
- Acknowledge limitations and uncertainties
- Use UK English spelling
- Be concise but thorough
- Focus on actionable insights for research
""")
    
    # Add entities.json context
    if entities_content:
        # Truncate if too large (keep first 50KB for now)
        entities_truncated = entities_content[:50000]
        if len(entities_content) > 50000:
            entities_truncated += "\n\n[... entities.json truncated for context window ...]"
        
        prompt_parts.append(f"""
# Knowledge Graph Context

You have access to the following knowledge graph (entities.json):

{entities_truncated}

Use this to understand relationships between concepts, papers, and researchers.
""")
    
    # Add paper-specific context if provided
    if paper_context:
        prompt_parts.append("\n# Current Paper Context\n")
        prompt_parts.append("The user is currently viewing a specific paper. Here are all the analysis documents:\n")
        
        # Add files in logical order
        file_order = [
            'paper_summary.md',
            '0-source-document.md',
            '0-notepad.md',
            '1-context.md',
            '2-structure.md',
            '3-methodology.md',
            '4-evidence.md',
            '5-contribution.md',
            '6-synthesis.md',
            '7-citations.md',
            '8-integration.md'
        ]
        
        for filename in file_order:
            if filename in paper_context:
                # Truncate very large files
                content = paper_context[filename]
                if len(content) > 30000:
                    content = content[:30000] + "\n\n[... file truncated ...]"
                
                prompt_parts.append(f"\n## {filename}\n\n{content}\n")
        
        # Add any remaining ANALYSIS_*.md files
        for filename, content in paper_context.items():
            if filename not in file_order and filename.startswith('ANALYSIS_'):
                if len(content) > 30000:
                    content = content[:30000] + "\n\n[... file truncated ...]"
                prompt_parts.append(f"\n## {filename}\n\n{content}\n")
    
    return "\n".join(prompt_parts)


def save_session(session_id: str, session_data: Dict[str, Any]):
    """Save chat session to disk."""
    try:
        paper_id = session_data.get('paper_id', 'general')
        session_dir = CHAT_SESSIONS_DIR / paper_id
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
        paper_id = data.get('paper_id')  # None for general chat
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get or create session
        if not session_id or session_id not in current_sessions:
            session_id = str(uuid.uuid4())
            current_sessions[session_id] = {
                'thread_id': session_id,
                'paper_id': paper_id or 'general',
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
        
        # Load paper context if paper_id provided and not already loaded
        paper_context = None
        if paper_id and paper_id != 'general':
            paper_context = load_paper_context(paper_id)
            if paper_context and not session['context_files']:
                session['context_files'] = list(paper_context.keys())
        
        # Create system prompt
        system_prompt = create_system_prompt(paper_context)
        
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
        data = request.json
        paper_id = data.get('paper_id')
        
        session_id = str(uuid.uuid4())
        current_sessions[session_id] = {
            'thread_id': session_id,
            'paper_id': paper_id or 'general',
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
        data = request.json
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


@app.route('/api/chat/load-context/<paper_id>', methods=['GET'])
def load_context(paper_id: str):
    """Load paper context files."""
    try:
        context_files = load_paper_context(paper_id)
        
        return jsonify({
            'paper_id': paper_id,
            'files_loaded': list(context_files.keys()),
            'file_count': len(context_files),
            'message': f'Loaded {len(context_files)} context files for {paper_id}'
        })
        
    except Exception as e:
        print(f"Error loading context: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat/generate-summary', methods=['POST'])
def generate_summary():
    """Generate summary of conversation using Gemini."""
    try:
        data = request.json
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
        summary_prompt = f"""Please provide a concise summary of this research conversation. 
Include:
- Main topics discussed
- Key insights and findings
- Any questions that remain unanswered
- Suggested next steps for research

Conversation:
{conversation_str}

Summary:"""
        
        response = gemini_model.generate_content(summary_prompt)
        summary = response.text
        
        # Save summary to file
        paper_id = session.get('paper_id', 'general')
        session_dir = CHAT_SESSIONS_DIR / paper_id
        session_dir.mkdir(parents=True, exist_ok=True)
        
        thread_id = session['thread_id']
        summary_file = session_dir / f"thread_{thread_id}_summary.md"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"# Chat Session Summary\n\n")
            f.write(f"**Session ID**: {thread_id}\n")
            f.write(f"**Paper**: {paper_id}\n")
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
        'gemini_initialized': gemini_model is not None,
        'entities_loaded': entities_content is not None,
        'active_sessions': len(current_sessions)
    })


def main():
    """Start the Flask API server."""
    print("=" * 60)
    print("Gemini Chat API Server")
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

