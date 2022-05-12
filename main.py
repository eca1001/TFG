from flask import Flask, render_template, request, session
from codigos.codigoLenguajes import ejecutar as ejecutarLen
from codigos.codigoDatabases import ejecutar as ejecutarDb
from codigos.codigoEntornos import ejecutar as ejecutarEnt
from codigos.codigoHerramientas import ejecutar as ejecutarHerr
from codigos.codigoPlataformas import ejecutar as ejecutarPlat
from codigos.codigoWebFrames import ejecutar as ejecutarWf

app = Flask(__name__)
app.secret_key = b'Esto deberia ser un texto unico y secretisimo'
PORT = 5000
DEBUG = False

@app.errorhandler(404)
def not_found(error):
    return "Not Found."

@app.route('/', methods=["GET"])
def index():
    return render_template("inicio.html")

@app.route('/lenguajes', methods=["GET", "POST"])
def indexL():
    if "user_umbral" not in session:
        session["user_umbral"] = 30

    if request.method == "GET":
        user_umbral = request.args.get("user_umbral")
    elif request.method == "POST":
        user_umbral = request.form['user_umbral']
        session["user_umbral"] = int(user_umbral)

    ejecutarLen(session["user_umbral"])
    return render_template("lenguajes.html", name=session["user_umbral"])

@app.route('/databases', methods=["GET", "POST"])
def indexD():
    if "user_umbral" not in session:
        session["user_umbral"] = 30
    
    if request.method == "GET":
        user_umbral = request.args.get("user_umbral")
    elif request.method == "POST":
        user_umbral = request.form['user_umbral']
        session["user_umbral"] = int(user_umbral)

    ejecutarDb(session["user_umbral"])
    return render_template("databases.html", name=session["user_umbral"])

@app.route('/entornos', methods=["GET", "POST"])
def indexE():
    if "user_umbral" not in session:
        session["user_umbral"] = 30
    
    if request.method == "GET":
        user_umbral = request.args.get("user_umbral")
    elif request.method == "POST":
        user_umbral = request.form['user_umbral']
        session["user_umbral"] = int(user_umbral)

    ejecutarEnt(session["user_umbral"])
    return render_template("entornos.html", name=session["user_umbral"])

@app.route('/herramientas', methods=["GET", "POST"])
def indexH():
    if "user_umbral" not in session:
        session["user_umbral"] = 30
    
    if request.method == "GET":
        user_umbral = request.args.get("user_umbral")
    elif request.method == "POST":
        user_umbral = request.form['user_umbral']
        session["user_umbral"] = int(user_umbral)

    ejecutarHerr(session["user_umbral"])
    return render_template("herramientas.html", name=session["user_umbral"])

@app.route('/plataformas', methods=["GET", "POST"])
def indexP():
    if "user_umbral" not in session:
        session["user_umbral"] = 30
    
    if request.method == "GET":
        user_umbral = request.args.get("user_umbral")
    elif request.method == "POST":
        user_umbral = request.form['user_umbral']
        session["user_umbral"] = int(user_umbral)

    ejecutarPlat(session["user_umbral"])
    return render_template("plataformas.html", name=session["user_umbral"])

@app.route('/webframes', methods=["GET", "POST"])
def indexW():
    if "user_umbral" not in session:
        session["user_umbral"] = 30
    
    if request.method == "GET":
        user_umbral = request.args.get("user_umbral")
    elif request.method == "POST":
        user_umbral = request.form['user_umbral']
        session["user_umbral"] = int(user_umbral)

    ejecutarWf(session["user_umbral"])
    return render_template("webframes.html", name=session["user_umbral"])


@app.route('/about', methods=["GET"])
def about():
    return render_template(
        "about.html", 
        name="Trabajo de Fin de Grado - Grado Ingeniería Informática", 
        autor=["Enrique Camarero Alonso"], 
        profesores=["José Ignacio Santos Martín", "Virginia Ahedo García"], 
        objetivo=["Diseñar e implementar un sistema de recomendación de tecnologías para desarrolladores (lenguaje de programación, base de datos, plataformas, etc) utilizando la información recogida en la encuesta que Stack Overflow realiza todos los años entre desarrolladores.)"],
        manual=["Seleccionar la tecnología deseada.", "Indicar el umbral que más se adapte a sus necesidades en el formulario de la esquina superior izquierda.", "En caso de querer cambiar el umbral repetir el paso anterior.", "Visualizar los resultados. Se puede filtrar cada una de las tecnologías a través del filtro ofrecido en el sistema de recomendación (tabla que se encuentra con el nombre de 'RECOMENDADOR DE' + el nombre de la tecnología), para una búsqueda más rápida de los resultdos."]
    )


if __name__ == '__main__':
    app.run(port = PORT, debug = DEBUG)