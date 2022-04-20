from flask import Flask, render_template, request, session
from finalCode import ejecutar

app = Flask(__name__)
app.secret_key = b'Esto deberia ser un texto unico y secretisimo'
PORT = 5000
DEBUG = False

@app.errorhandler(404)
def not_found(error):
    return "Not Found."


@app.route('/', methods=["GET", "POST"])
def index():
    if "user_umbral" not in session:
        session["user_umbral"] = 30
    
    if request.method == "GET":
        user_umbral = request.args.get("user_umbral")
    elif request.method == "POST":
        user_umbral = request.form['user_umbral']
        session["user_umbral"] = int(user_umbral)

    ejecutar(session["user_umbral"])
    return render_template("principal.html", name=session["user_umbral"])


@app.route('/about', methods=["GET"])
def about():
    return render_template("about.html", name="Trabajo de Fin de Grado", autor=["Enrique Camarero"], profesores=["José Ignacio Santos Martín", "Virginia Ahedo García"])


if __name__ == '__main__':
    app.run(port = PORT, debug = DEBUG)