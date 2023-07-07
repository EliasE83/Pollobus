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

@app.route('/route')
def route():
    return render_template('ruta.html')

#Código para agregar info
@app.route('/ruta')
def ruta():
    if request.method == 'POST':
        
        vruta= request.form['ruta']
        voperador= request.form['operador']
        vbus= request.form['autobus']
        vsalida= request.form['salida']
        vhora= request.form['hora']
        vparadas= request.form['paradas']
        
        cs = mysql.connection.cursor()
        #falta tabla
        #cs.execute('insert into (,artista,anio) values (%s,%s,%s)', (vtitulo,vartista,vanio))
        mysql.connection.commit()
        
    flash('El album fue agregado correctamente')
    return redirect(url_for('ruta'))

@app.route('/autobus')
def autobus():
    return render_template('autobus.html')

#para asignar datos en bus
@app.route('/busform')
def busform():
    if request.method == 'POST':
        
        vruta= request.form['marca']
        voperador= request.form['modelo']
        vbus= request.form['matri']
        vsalida= request.form['asientos']
        vhora= request.form['tanque']
        
        cs = mysql.connection.cursor()
        #falta tabla
        #cs.execute('insert into (,artista,anio) values (%s,%s,%s)', (vtitulo,vartista,vanio))
        mysql.connection.commit()
        
    flash('El album fue agregado correctamente')
    return redirect(url_for('autobus'))

@app.route('/operador')
def operador():
    return render_template('operador.html')

#form para datos en operador
@app.route('/operadorForm')
def operadorForm():
    if request.method == 'POST':
        
        vruta= request.form['nombre']
        voperador= request.form['ap']
        vbus= request.form['am']
        vsalida= request.form['N_empleado']
        vhora= request.form['licencia']
        vVigencia= request.form['vigencia']
        
        cs = mysql.connection.cursor()
        #falta tabla
        #cs.execute('insert into (,artista,anio) values (%s,%s,%s)', (vtitulo,vartista,vanio))
        mysql.connection.commit()
        
    flash('El album fue agregado correctamente')
    return redirect(url_for('operador'))

@app.route('/alumno')
def alumno():
    return render_template('alumnno.html')

#form para insercion de datos alumno
@app.route('/alumnoForm')
def alumnoForm():
    if request.method == 'POST':
        
        vruta= request.form['nombre']
        voperador= request.form['ap']
        vbus= request.form['am']
        vsalida= request.form['carrera']
        vhora= request.form['matri']
        vruta= request.form['ruta']
        vturno= request.form['turno']
        vTipo= request.form['tipo-viaje']
        
        cs = mysql.connection.cursor()
        #falta tabla
        #cs.execute('insert into (,artista,anio) values (%s,%s,%s)', (vtitulo,vartista,vanio))
        mysql.connection.commit()
        
    flash('El album fue agregado correctamente')
    return redirect(url_for('operador'))

@app.route('/consulta')
def consulta():
    return render_template('ventanaconsulta.html')

@app.route('/eliminar')
def eliminar():
    return render_template('elimin.html')

#Ejecucion de nuestro programa
if __name__ == '__main__':
    app.run(port=5000, debug=True)