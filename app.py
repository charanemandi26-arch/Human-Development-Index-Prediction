import importlib.util
import os
import sys

# Get absolute paths
root_dir = os.path.dirname(os.path.abspath(__file__))
dev_dir = os.path.abspath(os.path.join(root_dir, "5. Project Development Phase"))
actual_app_path = os.path.join(dev_dir, "app.py")

# Change working directory and path so that model and utility paths resolve correctly
sys.path.insert(0, dev_dir)
os.chdir(dev_dir)

# Load the app module dynamically with a unique name 'actual_app' to avoid conflict
spec = importlib.util.spec_from_file_location("actual_app", actual_app_path)
actual_app = importlib.util.module_from_spec(spec)
sys.modules["actual_app"] = actual_app
spec.loader.exec_module(actual_app)

app = actual_app.app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port, debug=False)
