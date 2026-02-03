import os

SANDBOX_ROOT = os.path.abspath("sandbox")


def _safe_path(path: str) -> str:
    if path.startswith("/"):
        path = path[1:]
    full = os.path.abspath(os.path.join(SANDBOX_ROOT, path))
    if not full.startswith(SANDBOX_ROOT):
        raise ValueError("Unsafe path detected")
    return full


def execute_step(step: dict) -> dict:
    tool = step.get("tool")

    try:
        if tool == "shell":
            cmd = step.get("command", "")

            if cmd.startswith("mkdir /employees"):
                rel = cmd.replace("mkdir /employees", "employees", 1)
                path = _safe_path(rel)
                os.makedirs(path, exist_ok=True)
                return {"tool": "shell", "status": "executed", "output": f"created {path}"}

            if cmd.startswith("ls -la /employees"):
                rel = cmd.replace("ls -la /employees", "employees", 1)
                path = _safe_path(rel)
                files = os.listdir(path)
                return {"tool": "shell", "status": "executed", "output": "\n".join(files)}

            return {"tool": "shell", "status": "ignored", "output": cmd}

        elif tool == "apply_patch":
            file_path = _safe_path(step["file"])
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(step["content"])

            return {
                "tool": "apply_patch",
                "status": "executed",
                "output": f"wrote {file_path}"
            }

        else:
            return {"tool": tool, "status": "error", "output": "Unknown tool"}

    except Exception as e:
        return {"tool": tool, "status": "error", "output": str(e)}