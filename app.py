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
def login():
    return render_template('login.html')

#Ruta http://localhost:5000/guardar tipo POST para insert

@app.route('/index')
def inicio():
    con = pyodbc.connect(app.config['SQL_SERVER_URI'])
    cursor = con.cursor()
    cursor.execute('select id_registroautobus, Rutas.numero, Rutas.nombre, RegistroAutobuses.id_autobus, Cuatrimestres.periodo from RegistroAutobuses inner join Rutas on Rutas.id_ruta = RegistroAutobuses.id_ruta inner join Cuatrimestres on Cuatrimestres.id_cuatrimestre = RegistroAutobuses.id_cuatrimestre where RegistroAutobuses.Estatus = 1')
    consulta = cursor.fetchall()

    cursor.execute('select RegistroAutobuses.id_registroautobus ,Operadores.numeroempleado, RegistroAutobuses.id_autobus from RegistroOperadores inner join Operadores on Operadores.id_operador = RegistroOperadores.id_operador inner join RegistroAutobuses on RegistroAutobuses.id_registroautobus = RegistroOperadores.id_registroautobus where RegistroOperadores.Estatus = 1')
    consulta2 = cursor.fetchall()
    return render_template('index.html', lsConsulta = consulta, lsConsulta2 = consulta2)

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

@app.route('/asignarbus')
def asignarbus():
    con = pyodbc.connect(app.config['SQL_SERVER_URI'])
    cursor = con.cursor()
    cursor.execute('select id_autobus from Autobuses')
    consultas = cursor.fetchall()

    cursor.execute('select id_ruta, numero from Rutas')
    consultas2 = cursor.fetchall()    

    cursor.execute('select id_cuatrimestre, periodo from Cuatrimestres')
    consultas3 = cursor.fetchall()

    return render_template('autobuses/asignarbus.html', lsBus = consultas, lsRutas = consultas2, lsCuatri = consultas3)

@app.route('/asignarbusBD', methods=['POST'])
def asignarbusBD():
    if request.method == 'POST':
        vrcuatrimestre = request.form['asigper']
        vrruta = request.form['asigrut']
        vridbus = request.form['asigbus']

        con = pyodbc.connect(app.config['SQL_SERVER_URI'])
        cursor = con.cursor()
        cursor.execute('insert into RegistroAutobuses (id_cuatrimestre, id_ruta, id_autobus) values (?,?,?)', (vrcuatrimestre,vrruta,vridbus))
        con.commit()
        con.close()

    return render_template('ventanaemergente.html')

@app.route('/desactivaruta/<id>')
def desactivaruta(id):
    con = pyodbc.connect(app.config['SQL_SERVER_URI'])
    cursor = con.cursor()
    cursor.execute('update RegistroAutobuses set Estatus = 0 where id_registroautobus = ?', (id))
    con.commit()
    con.close()
    return redirect(url_for('inicio'))

#Operadores

@app.route('/registroperador')
def registroperador():
    return render_template('operadores/registroperador.html')

@app.route('/registroperadorBD', methods=['POST'])
def registroperadorBD():

    vonombre = request.form['onombre']
    voap = request.form['oap']
    voam = request.form['oam']

    volicencia = request.form['olicencia']
    vonumemp = request.form['onoemp']
    

    con = pyodbc.connect(app.config['SQL_SERVER_URI'])
    cursor = con.cursor()
    cursor.execute('insert into Personas (nombre, ap, am) values (?,?,?)', (vonombre,voap,voam))
    con.commit()
    con.close()
        
    con1 = pyodbc.connect(app.config['SQL_SERVER_URI'])
    cursor1 = con1.cursor()   
    cursor1.execute('select id_persona from Personas where nombre = ? and ap = ? and am = ?', (vonombre,voap,voam))
    idpersona = cursor1.fetchone()
    print(idpersona[0], vonombre, voap, voam, volicencia, vonumemp)

    cursor1.execute('insert into Operadores (id_persona, licencia, numeroempleado) values (?,?,?)', (idpersona[0],volicencia,vonumemp))
    con1.commit()
    con1.close()

    return render_template('ventanaemergente.html')

@app.route('/consultaroperador')
def consultaroperador():
    con = pyodbc.connect(app.config['SQL_SERVER_URI'])
    cursor = con.cursor()
    cursor.execute("select id_operador, (Personas.nombre+' '+Personas.ap+' '+Personas.am), licencia, numeroempleado from Operadores inner join Personas on Personas.id_persona = Operadores.id_persona")
    consultas = cursor.fetchall()
    return render_template('operadores/consultaroperador.html', lsOperador = consultas)

@app.route('/asignaroperador')
def asignaroperador():
    con = pyodbc.connect(app.config['SQL_SERVER_URI'])
    cursor = con.cursor()
    cursor.execute('select id_operador, numeroempleado from Operadores')
    consultas = cursor.fetchall()

    cursor.execute('select id_registroautobus, Rutas.numero from RegistroAutobuses inner join Rutas on Rutas.id_ruta = RegistroAutobuses.id_ruta where RegistroAutobuses.Estatus = 1')
    consultas2 = cursor.fetchall()

    return render_template('operadores/asignaroperador.html', lsOperadorAS = consultas, lsRegistro = consultas2)

@app.route('/asignaroperadorBD', methods=['POST'])
def asignaroperadorBD():
    if request.method == 'POST':
        vroperador = request.form['asigop']
        vrregistro = request.form['asigrutop']

        con = pyodbc.connect(app.config['SQL_SERVER_URI'])
        cursor = con.cursor()
        cursor.execute('insert into RegistroOperadores (id_registroautobus, id_operador) values (?,?)', (vrregistro,vroperador))
        con.commit()
        con.close()

    return render_template('ventanaemergente.html')

@app.route('/desactivarop/<id>')
def desactivarop(id):
    con = pyodbc.connect(app.config['SQL_SERVER_URI'])
    cursor = con.cursor()
    cursor.execute('update RegistroOperadores set Estatus = 0 where id_registroautobus = ?', (id))
    con.commit()
    con.close()
    return redirect(url_for('inicio'))

#Alumnos

@app.route('/consultalumno')
def consultalumno():
    con = pyodbc.connect(app.config['SQL_SERVER_URI'])
    cursor = con.cursor()
    cursor.execute("select id_alumno, (Personas.nombre +' '+ Personas.ap +' '+ Personas.am), matricula from Alumnos inner join Personas on Personas.id_persona = Alumnos.id_persona")
    consultas = cursor.fetchall()

    return render_template('alumnos/consultalumno.html', lsAlumno = consultas)

@app.route('/registroalumno')
def registroalumno():
    return render_template('alumnos/registroalumno.html')

@app.route('/registroalumnoBD', methods=['POST'])
def registroalumnoBD():
    if request.method == 'POST':
        vonombre = request.form['anombre']
        voaap = request.form['aap']
        voaam = request.form['aam']
        vomatricula = request.form['amatricula']
        vacarrera = request.form['acarrera']

        con = pyodbc.connect(app.config['SQL_SERVER_URI'])
        cursor = con.cursor()
        cursor.execute('insert into Personas (nombre, ap, am) values (?,?,?)', (vonombre,voaap,voaam))
        con.commit()
        cursor.execute('select id_persona from Personas where nombre = ? and ap = ? and am = ?', (vonombre,voaap,voaam))
        idpersona = cursor.fetchone()

        cursor.execute('insert into Alumnos (id_persona, matricula, id_carrera) values (?,?,?)', (idpersona[0],vomatricula,vacarrera))
        con.commit()
        con.close()

    return render_template('ventanaemergente.html')

#Ejecucion de nuestro programa
if __name__ == '__main__':
    app.run(port=5000, debug=True)