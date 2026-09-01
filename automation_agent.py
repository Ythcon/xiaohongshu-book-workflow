"""XHS workflow agent: scheduled generation, 24h review, approval and publishing.

The default mode is local and safe: generation runs existing scripts, review reads
local metrics, and publishing creates a ready-to-upload manifest. A real publisher
can be plugged in through the PUBLISHER_COMMAND environment variable.
"""
from __future__ import annotations
import argparse, datetime as dt, json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE = ROOT / ".agent-state.json"
CONFIG = ROOT / "automation.config.json"

DEFAULT = {
    "timezone": "Asia/Shanghai", "daily_generation_time": "08:30",
    "review_time": "09:30", "publish_time": "18:30", "require_approval": True,
    "generation": {"book_script": "generate_new_eight_books.py", "magazine_script": "generate_casabella_110_cards.py"},
    "model_router": {"extract": "qwen2.5-7b-instruct/local", "draft": "deepseek-chat", "editor": "gpt-4o-mini"},
    "publisher": {"mode": "manifest", "command": ""}
}

def load(path: Path, fallback):
    if not path.exists(): return fallback.copy()
    with path.open(encoding="utf-8") as f: return json.load(f)

def save_state(s):
    STATE.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")

def run_script(name):
    script = ROOT / name
    if not script.exists(): return {"ok": False, "error": f"missing script: {name}"}
    p = subprocess.run([sys.executable, str(script)], cwd=ROOT, capture_output=True, text=True)
    return {"ok": p.returncode == 0, "script": name, "stdout": p.stdout[-2000:], "stderr": p.stderr[-2000:]}

def latest_posts():
    items=[]
    for p in (ROOT / "posts").glob("*/post.json"):
        try:
            d=json.loads(p.read_text(encoding="utf-8")); d["_path"]=str(p); items.append(d)
        except Exception: pass
    return sorted(items, key=lambda x: Path(x["_path"]).stat().st_mtime, reverse=True)

def parse_metrics():
    files=sorted((ROOT/"output").glob("流量复盘-*.md"), key=lambda p:p.stat().st_mtime, reverse=True)
    if not files: return {"source": None, "posts": [], "note": "尚无本地复盘文件"}
    text=files[0].read_text(encoding="utf-8", errors="ignore")
    rows=[]
    for line in text.splitlines():
        if "|" not in line or re.match(r"^\s*\|?\s*-", line): continue
        cells=[c.strip() for c in line.strip("|").split("|")]
        if len(cells)>=8 and cells[0].isdigit():
            rows.append({"title":cells[1],"views":cells[3],"likes":cells[4],"saves":cells[5],"shares":cells[6],"rate":cells[7]})
    return {"source":str(files[0]), "posts":rows}

def review():
    m=parse_metrics(); rows=m["posts"]
    rec=[]
    if rows:
        rec.append("保留单一命题、强明暗对比和可识别主轮廓；它们在当前样本中更容易获得点击。")
        rec.append("把‘可带走的观察框架’放入结尾，优先优化收藏率，而不是只增加装饰性细节。")
        rec.append("同系列发布间隔至少 3 小时，并在发布后 24 小时再比较互动率。")
    report={"created_at":dt.datetime.now().isoformat(timespec="seconds"),"metrics":m,"recommendations":rec,"model_router":load(CONFIG,DEFAULT)["model_router"]}
    out=ROOT/"output"/f"agent-review-{dt.date.today()}.json"; out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    return report

def approve(review_file):
    p=Path(review_file); approval=p.with_suffix(".approved")
    approval.write_text(dt.datetime.now().isoformat(timespec="seconds"), encoding="utf-8")
    return approval

def publish():
    cfg=load(CONFIG,DEFAULT); posts=latest_posts()[:1]
    manifest={"created_at":dt.datetime.now().isoformat(timespec="seconds"),"items":posts,"mode":cfg["publisher"]["mode"],"status":"ready-for-approval"}
    out=ROOT/"output"/"publish-manifest.json"; out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    cmd=cfg["publisher"].get("command") or os.getenv("PUBLISHER_COMMAND")
    if cmd:
        subprocess.run(cmd, cwd=ROOT, shell=True, check=False)
        manifest["status"]="publisher-invoked"; out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    return manifest

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("action", choices=["generate","review","approve","publish","run-once"]); ap.add_argument("file", nargs="?"); a=ap.parse_args()
    cfg=load(CONFIG,DEFAULT); state=load(STATE,{})
    if a.action=="generate":
        result=[run_script(cfg["generation"][k]) for k in ("book_script","magazine_script")]; state["last_generate"]=dt.datetime.now().isoformat(); state["generation"]=result
    elif a.action=="review": state["last_review"]=review()
    elif a.action=="approve": state["approval_file"]=str(approve(a.file or (ROOT/"output"/f"agent-review-{dt.date.today()}.json")))
    elif a.action=="publish":
        if cfg.get("require_approval") and not state.get("approval_file"): raise SystemExit("需要先执行 approve")
        state["publish"]=publish()
    else:
        state["generation"]=[run_script(cfg["generation"][k]) for k in ("book_script","magazine_script")]
        state["last_generate"]=dt.datetime.now().isoformat(); state["last_review"]=review()
    save_state(state); print(json.dumps(state,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
