#Importacion del framework
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

#Inicializacion del Servidor
app=Flask(__name__,)

#Configuracion de la conexion
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='dbflask'
app.secret_key='mysecretkey'
mysql=MySQL(app)

#Declaracion de la ruta http://localhost:5000
@app.route('/')
def index():
    return render_template('login.html')

#Ruta http://localhost:5000/guardar tipo POST para insert

@app.route('/ventana')
def inicio():
    return render_template('ventana.html')

@app.route('/ruta')
def ruta():
    return render_template('ruta.html')

@app.route('/autobus')
def autobus():
    return render_template('autobus.html')

@app.route('/operador')
def operador():
    return render_template('operador.html')

@app.route('/alumno')
def alumno():
    return render_template('alumnno.html')

@app.route('/consulta')
def consulta():
    return render_template('ventanaconsulta.html')

@app.route('/eliminar')
def eliminar():
    return render_template('elimin.html')

#Ejecucion de nuestro programa
if __name__ == '__main__':
    app.run(port=5000, debug=True)