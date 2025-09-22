import os, json, time
from datetime import datetime
from google.adk.runtime import Callback, CallbackContext

class MonitorCallback(Callback):
  def _now(self): return datetime.utcnow().isoformat() + "Z"

  async def before_run(self, ctx: CallbackContext):
    s = ctx.session
    s.state.setdefault("logs", []).append({"ts": self._now(), "event": "before_run", "input": ctx.input})

  async def after_tool(self, ctx: CallbackContext):
    s = ctx.session
    s.state.setdefault("logs", []).append({
      "ts": self._now(), "event": "after_tool", "tool": ctx.tool_name,
      "args": ctx.tool_args, "ok": ctx.tool_error is None,
      "error": str(ctx.tool_error) if ctx.tool_error else None
    })

  async def after_agent(self, ctx: CallbackContext):
    os.makedirs("run_logs", exist_ok=True)
    fp = os.path.join("run_logs", f"adk_run_{int(time.time())}.jsonl")
    with open(fp, "a", encoding="utf-8") as f:
      for row in ctx.session.state.get("logs", []):
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    ctx.session.state["memory_summary"] = f"Last turn {self._now()}."
    ctx.session.state["logs"] = []
