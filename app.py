from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def homePage():
    """
    Returns the mobile view welcome message for the root route.
    """
    try:
        return "hello laturkars render mobil view"
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route("/aboutus")
def aboutUsPage():
    """
    Returns the about us page content for laturkars.
    """
    try:
        return "this is laturkars about us page"
    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

