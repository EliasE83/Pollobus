#Importacion del framework
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

#Inicializacion del Servidor
app=Flask(__name__,)

#Configuracion de la conexion
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='pi'
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
    cop = mysql.connection.cursor()
    cop.execute('select * nombre operadores')
    consultaop = cop.fetchone()

    cautobus = mysql.connection.cursor()
    cautobus.execute('select matricula from autobuses')
    consultaautobus = cautobus.fetchone()

    return render_template('ruta.html', lsOp = consultaop, lsAut = consultaautobus)


@app.route('/rutaForm', methods=['POST'])
def rutaForm():
        if request.method == 'POST':
        
            vruta= request.form['ruta']
            voperador= request.form['operador']
            vbus= request.form['autobus']
            vsalida= request.form['salida']
            vhora= request.form['hora']
            vparadas= request.form['paradas']
            
            cs = mysql.connection.cursor()
            cs.execute('insert into rutas (ruta, operador, autobus, horasalida, horallegada, noparadas) values (%s,%s,%s,%s,%s,%s)', (vruta,voperador,vbus,vsalida,vhora,vparadas))
            mysql.connection.commit()
        
        return render_template('ventanaemergente.html')

@app.route('/autobus')
def autobus():
    return render_template('autobus.html')

#para asignar datos en bus
@app.route('/busform', methods=['POST'])
def busform():
    if request.method == 'POST':
        
        vmarca= request.form['marca']
        vmodelo= request.form['modelo']
        vmatricula= request.form['matri']
        vasientos= request.form['asientos']
        vtanque= request.form['tanque']
        
        cs = mysql.connection.cursor()
        cs.execute('insert into autobuses (marca, modelo, matricula, noasientos, capacidadtanque) values (%s,%s,%s,%s,%s)', (vmarca,vmodelo,vmatricula,vasientos,vtanque))
        mysql.connection.commit()
        
    return render_template('ventanaemergente.html')

@app.route('/operador')
def operador():
    return render_template('operador.html')

#form para datos en operador
@app.route('/operadorForm', methods=['POST'])
def operadorForm():
    if request.method == 'POST':
        
        vnombreo = request.form['nombre']
        voperadoro = request.form['ap']
        vamo = request.form['am']
        vlic = request.form['licencia']
        vVigencia = request.form['vigencia']
        vnempleado = request.form.get('nempleado', False)
        
        cs = mysql.connection.cursor()
        cs.execute('insert into operadores (nombre, apellidop, apellidom, numeroempleado, licencia, vigencia) values (%s,%s,%s,%s,%s,%s)', (vnombreo,voperadoro,vamo,vnempleado,vlic,vVigencia))
        mysql.connection.commit()
        
    return render_template('ventanaemergente.html')

@app.route('/alumno')
def alumno():
    return render_template('alumnno.html')

#form para insercion de datos alumno
@app.route('/alumnoForm', methods=['POST'])
def alumnoForm():
    if request.method == 'POST':
        
        vnombre= request.form['nombre']
        vap= request.form['ap']
        vam= request.form['am']
        vcarrera= request.form['carrera']
        vmatri= request.form['matri']
        vruta= request.form['ruta']
        vturno= request.form['turno']
        vTipo= request.form['tipo-viaje']
        
        cs = mysql.connection.cursor()
        cs.execute('insert into alumnos(nombre, apellidop, apellidom, carrera, matricula, ruta, turno, tipodeviaje) values (%s,%s,%s,%s,%s,%s,%s,%s)', (vnombre,vap,vam,vcarrera,vmatri,vruta,vturno,vTipo))
        mysql.connection.commit()
        
    
    return render_template('ventanaemergente.html')

@app.route('/consulta')
def consulta():
    return render_template('ventanaconsulta.html')

@app.route('/eliminar')
def eliminar():
    return render_template('elimin.html')

#Ejecucion de nuestro programa
if __name__ == '__main__':
    app.run(port=5000, debug=True)