# run_import.py
import traceback
try:
    import app
    print("app imported OK")
except Exception:
    traceback.print_exc()
