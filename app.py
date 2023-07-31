#Importacion del framework
from flask import Flask, render_template, request, redirect, url_for, flash
#from flask_mysqldb import MySQL
import pyodbc

#Inicializacion del Servidor
app=Flask(__name__,)

#Configuracion de la conexion 
 
#app.config['MYSQL_HOST']='localhost'
#app.config['MYSQL_USER']='root'
#app.config['MYSQL_PASSWORD']=''
#app.config['MYSQL_DB']='pi'
#app.secret_key='mysecretkey'
#mysql=MySQL(app)


#Conexion a SQL Server

app.config['SQL_SERVER_URI']='Driver={SQL Server};Server=ELIAS;Database=ProyectoIntegrador;UID=DBA;PWD=1234;Trusted_Connection=yes;'

#Declaracion de la ruta http://localhost:5000
@app.route('/')
def index():
    return render_template('login.html')

#Ruta http://localhost:5000/guardar tipo POST para insert

@app.route('/index')
def inicio():
    return render_template('index.html')

#Rutas

@app.route('/registroruta')
def registroruta():
    return render_template('rutas/registroruta.html')

@app.route('/registrorutabs', methods=['POST'])
def registrorutabs():
    if request.method == 'POST':

        vrnombre = request.form['rnombre']
        vrnumero = request.form['rnumero']
        vrparadas = request.form['rparadas']
        
        con = pyodbc.connect(app.config['SQL_SERVER_URI'])
        cursor = con.cursor()
        cursor.execute('insert into Rutas (nombre, numero, noparadas) values (?,?,?)', (vrnombre,vrnumero,vrparadas))
        con.commit()
        con.close()
        
    return render_template('ventanaemergente.html')


@app.route('/consultaruta')
def consultaruta():
    con = pyodbc.connect(app.config['SQL_SERVER_URI'])
    cursor = con.cursor()
    cursor.execute('select * from Rutas')
    consultas = cursor.fetchall()
    return render_template('rutas/ruta.html', lsRutas = consultas)

@app.route('/editaruta/<id>')
def editaruta(id):
    con = pyodbc.connect(app.config['SQL_SERVER_URI'])
    cursor = con.cursor()
    cursor.execute('select * from Rutas where id_ruta = ?', (id))
    editaruta = cursor.fetchall()
    return render_template('rutas/editaruta.html', lscRutas = editaruta)

@app.route('/editarutaBD/<id>', methods=['POST'])
def editarutaBD(id):
    if request.method == 'POST':
        vrnombre = request.form['renombre']
        vrnumero = request.form['renumero']
        vrparadas = request.form['reparadas']

        con = pyodbc.connect(app.config['SQL_SERVER_URI'])
        cursor = con.cursor()
        cursor.execute('update Rutas set nombre = ?, numero = ?, noparadas = ? where id_ruta = ?', (vrnombre,vrnumero,vrparadas,id))
        print (vrnombre + ' ' + vrnumero + ' ' + vrparadas + ' ' + id)
        con.commit()
        con.close()
    return redirect(url_for('consultaruta'))

@app.route('/eliminaruta/<id>')
def eliminaruta(id):
    con = pyodbc.connect(app.config['SQL_SERVER_URI'])
    cursor = con.cursor()
    cursor.execute('delete from Rutas where id_ruta = ?', (id))
    con.commit()
    con.close()
    return redirect(url_for('consultaruta'))

#Autobuses

@app.route('/consultabus')
def consultabus():
    con = pyodbc.connect(app.config['SQL_SERVER_URI'])
    cursor = con.cursor()
    cursor.execute('select id_autobus, noasientos, capacidadtanque, Marcas.marca, Modelos.modelo  from Autobuses inner join Modelos on Modelos.id_modelo = Autobuses.id_modelo inner join Marcas on Marcas.id_marca = Modelos.id_marca')
    consultas = cursor.fetchall()
    return render_template('autobuses/consultabus.html', lsBus = consultas)

@app.route('/eliminarbus/<id>')
def eliminarbus(id):
    con = pyodbc.connect(app.config['SQL_SERVER_URI'])
    cursor = con.cursor()
    cursor.execute('delete from Autobuses where id_autobus = ?', (id))
    con.commit()
    con.close()
    return redirect(url_for('consultabus'))

@app.route('/registrarbus')
def registrarbus():
    con = pyodbc.connect(app.config['SQL_SERVER_URI'])
    cursor = con.cursor()
    cursor.execute('select id_modelo, modelo from Modelos')
    consultas2 = cursor.fetchall()

    return render_template('autobuses/registrarbus.html',  lsModelo = consultas2)

@app.route('/registrarbusBD', methods=['POST'])
def registrarbusBD():
    vmodelo = request.form['rmodelo']
    vnoasientos = request.form['asientos']
    vtanque = request.form['tanque']
    con = pyodbc.connect(app.config['SQL_SERVER_URI'])
    cursor = con.cursor()
    cursor.execute('insert into Autobuses (id_modelo, noasientos, capacidadtanque) values (?,?,?)', (vmodelo,vnoasientos,vtanque))
    con.commit()
    con.close()
    return render_template('ventanaemergente.html')

@app.route('/editabus/<id>')
def editabus(id):
    con = pyodbc.connect(app.config['SQL_SERVER_URI'])
    cursor = con.cursor()
    cursor.execute('select * from Autobuses where id_autobus = ?', (id))
    consultas = cursor.fetchall()
    return render_template('autobuses/editarbus.html', lscBus = consultas)

@app.route('/editarbusBD/<id>', methods=['POST'])
def editarbusBD(id):
    if request.method == 'POST':
        vrmodelo = request.form['remodelo']
        vrnoasientos = request.form['reasientos']
        vrtanque = request.form['retanque']

        con = pyodbc.connect(app.config['SQL_SERVER_URI'])
        cursor = con.cursor()
        cursor.execute('update Autobuses set id_modelo = ?, noasientos = ?, capacidadtanque = ? where id_autobus = ?', (vrmodelo,vrnoasientos,vrtanque,id))
        con.commit()
        con.close()
    return redirect(url_for('consultabus'))


#Ejecucion de nuestro programa
if __name__ == '__main__':
    app.run(port=5000, debug=True)