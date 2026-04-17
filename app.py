from callbacks import app  # noqa: F401 — registers all callbacks + sets layout
import callbacks           # noqa: F401

if __name__ == "__main__":
    from server import app
    app.run(debug=False)