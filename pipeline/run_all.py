"""Run every puller; a failure in one source doesn't stop the others."""
import importlib, traceback, sys, os
sys.path.insert(0, os.path.dirname(__file__))

failed = []
for mod in ["pull_bls", "pull_fred", "pull_eia", "pull_kalshi", "pull_bls_files"]:
    try:
        importlib.import_module(mod).pull()
    except Exception:
        print(f"=== {mod} FAILED ===")
        traceback.print_exc()
        failed.append(mod)

if failed:
    print("Failed sources:", ", ".join(failed))
    # Exit 0 anyway so partial data still commits; the log shows what failed.
