from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def Main():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/registro")
def registro():
    return render_template('registro.html')

@app.route('/menu')
def registro():
    return render_template('menu.html')


if __name__=='__main__':
    app.run(debug=True)

