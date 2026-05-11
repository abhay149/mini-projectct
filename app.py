from flask import Flask, request, jsonify, render_template, send_file
import requests
import threading
import time
import uuid
import logging
import json
import os
from datetime import datetime
from functools import wraps
from collections import defaultdict, deque

import torch
from diffusers import StableDiffusionPipeline

# 🔥 OFFLINE WAKE ENGINE
from wake_word_engine import start_wake_word

# 🧠 BRAIN CORE IMPORTS
from brain.memory import MemoryManager
from brain.reasoning import ReasoningEngine
from brain.planner import Planner
from brain.personality import Personality
from brain.tools import ToolExecutor
from brain.automation import Automation
from brain.emotions import EmotionEngine
from brain.context_manager import ContextManager
from brain.learning import LearningEngine


# ─────────────────────────────────────────────
# 🏗️ APP SETUP
# ─────────────────────────────────────────────
app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "llama3"

MAX_HISTORY = 10

RATE_LIMIT = 20


# ─────────────────────────────────────────────
# 🧠 INITIALIZE BRAIN CORE
# ─────────────────────────────────────────────
memory = MemoryManager()

reasoning = ReasoningEngine()

planner = Planner()

personality = Personality()

tools = ToolExecutor()

automation = Automation()

emotions = EmotionEngine()

context_manager = ContextManager()

learning = LearningEngine()


# ─────────────────────────────────────────────
# 📝 LOGGING
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("NOVA")


def log_event(event: str, **kwargs):

    payload = {
        "event": event,
        "ts": datetime.utcnow().isoformat(),
        **kwargs
    }

    logger.info(json.dumps(payload))


# ─────────────────────────────────────────────
# 🎨 AI IMAGE GENERATOR
# ─────────────────────────────────────────────
IMAGE_FOLDER = "generated_images"

os.makedirs(IMAGE_FOLDER, exist_ok=True)

logger.info("🎨 Loading Stable Diffusion model...")

try:

    image_pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )

    if torch.cuda.is_available():

        image_pipe = image_pipe.to("cuda")

        logger.info("⚡ Using GPU for image generation")

    else:

        image_pipe = image_pipe.to("cpu")

        logger.info("💻 Using CPU for image generation")

    logger.info("✅ AI Image Generator Ready")

except Exception as e:

    logger.error(f"❌ Failed loading image model: {e}")

    image_pipe = None


# ─────────────────────────────────────────────
# 🧠 SESSION MEMORY
# ─────────────────────────────────────────────
sessions = defaultdict(lambda: deque(maxlen=MAX_HISTORY))


def get_session_history(session_id):

    return list(sessions[session_id])


def push_to_session(session_id, role, content):

    sessions[session_id].append({
        "role": role,
        "content": content
    })


# ─────────────────────────────────────────────
# 🛡️ RATE LIMITER
# ─────────────────────────────────────────────
_rate_buckets = defaultdict(list)


def is_rate_limited(ip):

    now = time.time()

    bucket = _rate_buckets[ip]

    _rate_buckets[ip] = [
        t for t in bucket if now - t < 60
    ]

    if len(_rate_buckets[ip]) >= RATE_LIMIT:
        return True

    _rate_buckets[ip].append(now)

    return False


def rate_limit(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        ip = request.remote_addr

        if is_rate_limited(ip):

            log_event("rate_limited", ip=ip)

            return jsonify({
                "response": "⚠️ Too many requests.",
                "action": None,
                "error": "rate_limit"
            }), 429

        return f(*args, **kwargs)

    return decorated


# ─────────────────────────────────────────────
# 🗂️ TOOL REGISTRY
# ─────────────────────────────────────────────
TOOLS = [

    {
        "triggers": ["open youtube", "youtube"],
        "action": "youtube",
        "response": "🎬 Opening YouTube"
    },

    {
        "triggers": ["open spotify", "spotify", "play music"],
        "action": "spotify",
        "response": "🎵 Opening Spotify"
    },

    {
        "triggers": ["open gmail", "gmail"],
        "action": "gmail",
        "response": "📧 Opening Gmail"
    },

    {
        "triggers": ["open maps", "maps"],
        "action": "maps",
        "response": "🗺️ Opening Maps"
    },

    {
        "triggers": ["what time is it"],
        "action": None,
        "response": lambda: f"🕐 {datetime.now().strftime('%I:%M %p')}"
    },

]


def match_tool(msg):

    for tool in TOOLS:

        if any(trigger in msg for trigger in tool["triggers"]):
            return tool

    return None


# ─────────────────────────────────────────────
# 🤖 PROMPT BUILDER
# ─────────────────────────────────────────────
def build_prompt(history, user_msg):

    base_prompt = personality.build_prompt()

    lines = [base_prompt]

    emotion = emotions.detect_emotion(user_msg)

    lines.append(f"Assistant emotion state: {emotion}")

    for turn in history:

        role_tag = (
            "User"
            if turn["role"] == "user"
            else "Assistant"
        )

        lines.append(
            f"{role_tag}: {turn['content']}"
        )

    lines.append(f"User: {user_msg}")

    lines.append("Assistant:")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# 🤖 LLM CALLER
# ─────────────────────────────────────────────
def call_llm(prompt, timeout=30):

    try:

        res = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=timeout
        )

        res.raise_for_status()

        output = res.json()

        return (
            output.get("response")
            or output.get("message", {}).get("content")
            or "No AI response"
        )

    except requests.exceptions.ConnectionError:

        return "⚠️ Ollama is not running."

    except requests.exceptions.Timeout:

        return "⚠️ AI timeout."

    except Exception as e:

        logger.error(f"LLM error: {e}")

        return f"⚠️ Error: {str(e)}"


# ─────────────────────────────────────────────
# 🌐 ROUTES
# ─────────────────────────────────────────────
@app.route("/")
def home():

    return render_template("index.html")


@app.route("/health")
def health():

    return jsonify({

        "status": "ok",

        "model": MODEL,

        "sessions": len(sessions),

        "brain": "online"
    })


# ─────────────────────────────────────────────
# 💬 CHAT ROUTE
# ─────────────────────────────────────────────
@app.route("/chat", methods=["POST"])
@rate_limit
def chat():

    request_id = str(uuid.uuid4())[:8]

    data = request.get_json(silent=True)

    if not data or "message" not in data:

        return jsonify({
            "response": "No message received"
        }), 400

    raw_msg = data["message"]

    msg = raw_msg.lower().strip()

    session_id = (
        data.get("session_id")
        or request.remote_addr
    )

    log_event(
        "user_message",
        req=request_id,
        msg=raw_msg
    )

    # 🧠 LEARNING
    learning.learn(msg)

    # 🧠 CONTEXT
    context_manager.set_context(
        "last_message",
        msg
    )

    # 🧠 MEMORY
    memory.remember(
        "last_user_message",
        raw_msg
    )

    # 🧠 REASONING
    decision = reasoning.analyze(msg)

    # 🧠 PLANNING
    if "plan" in msg or "schedule" in msg:

        plan = planner.create_plan(msg)

        return jsonify({

            "response": "\n".join(plan),

            "action": "planner",

            "request_id": request_id
        })

    # 🧠 TOOL MATCHING
    tool = match_tool(msg)

    if tool:

        resp_text = (
            tool["response"]()
            if callable(tool["response"])
            else tool["response"]
        )

        if tool["action"]:

            tools.execute(tool["action"])

        push_to_session(
            session_id,
            "user",
            raw_msg
        )

        push_to_session(
            session_id,
            "assistant",
            resp_text
        )

        log_event(
            "tool_match",
            action=tool.get("action")
        )

        return jsonify({

            "response": resp_text,

            "action": tool.get("action"),

            "request_id": request_id
        })

    # 🧠 BUILD AI PROMPT
    history = get_session_history(session_id)

    prompt = build_prompt(
        history,
        raw_msg
    )

    # 🤖 AI RESPONSE
    reply = call_llm(prompt)

    push_to_session(
        session_id,
        "user",
        raw_msg
    )

    push_to_session(
        session_id,
        "assistant",
        reply
    )

    log_event(
        "llm_response",
        reply_len=len(reply)
    )

    return jsonify({

        "response": reply,

        "action": decision,

        "emotion": emotions.state,

        "request_id": request_id,

        "session_id": session_id
    })


# ─────────────────────────────────────────────
# 🎨 GENERATE AI IMAGE
# ─────────────────────────────────────────────
@app.route("/generate-image", methods=["POST"])
@rate_limit
def generate_image():

    if image_pipe is None:

        return jsonify({
            "error": "AI image model not loaded"
        }), 500

    data = request.get_json(silent=True)

    if not data or "prompt" not in data:

        return jsonify({
            "error": "Prompt required"
        }), 400

    prompt = data["prompt"].strip()

    if not prompt:

        return jsonify({
            "error": "Empty prompt"
        }), 400

    try:

        logger.info(f"🎨 Generating image: {prompt}")

        image = image_pipe(prompt).images[0]

        filename = f"{uuid.uuid4().hex}.png"

        filepath = os.path.join(
            IMAGE_FOLDER,
            filename
        )

        image.save(filepath)

        logger.info(f"✅ Image saved: {filepath}")

        return send_file(
            filepath,
            mimetype="image/png"
        )

    except Exception as e:

        logger.error(f"❌ Image generation error: {e}")

        return jsonify({
            "error": str(e)
        }), 500


# ─────────────────────────────────────────────
# 🧹 CLEAR SESSION
# ─────────────────────────────────────────────
@app.route("/session/clear", methods=["POST"])
def clear_session():

    data = request.get_json(silent=True) or {}

    session_id = (
        data.get("session_id")
        or request.remote_addr
    )

    sessions.pop(session_id, None)

    log_event(
        "session_cleared",
        session=session_id
    )

    return jsonify({

        "status": "cleared",

        "session_id": session_id
    })


# ─────────────────────────────────────────────
# 📜 SESSION HISTORY
# ─────────────────────────────────────────────
@app.route("/session/history")
def session_history():

    session_id = (
        request.args.get("session_id")
        or request.remote_addr
    )

    return jsonify({

        "session_id": session_id,

        "history": get_session_history(session_id)
    })


# ─────────────────────────────────────────────
# 🚀 STARTUP
# ─────────────────────────────────────────────
if __name__ == "__main__":

    logger.info("=" * 52)

    logger.info("🚀 NOVA Assistant Starting")

    logger.info(f"🧠 Model: {MODEL}")

    logger.info(f"🌐 Ollama: {OLLAMA_URL}")

    logger.info(f"🔒 Rate Limit: {RATE_LIMIT}")

    logger.info("🧠 Brain Core: ONLINE")

    logger.info("🎨 AI Image Generator: ONLINE")

    logger.info("=" * 52)

    # 🔥 Disable temporarily if Picovoice key missing
    # threading.Thread(target=start_wake_word, daemon=True).start()

    app.run(
        debug=False,
        host="127.0.0.1",
        port=10000
    )