from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json
from flask_cors import CORS 

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

app.secret_key = 'myawesomesecretkey'

app.config['MONGO_URI'] = 'mongodb://localhost:27017/pythonmongodb'

mongo = PyMongo(app)

#***************************users***************************************
@app.route('/api/user', methods=['POST'])
def create_user():
    # Receiving Data
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if username and email and password:
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert(
            {'username': username, 'email': email, 'password': hashed_password})
        response = jsonify({
            '_id': str(id),
            'username': username,
            'password': password,
            'email': email
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/api/user', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")


@app.route('/api/user/<id>', methods=['GET'])
def get_user(id):
    # print(id)
    user = mongo.db.users.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")


@app.route('/api/user/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/api/user/<_id>', methods=['PUT'])
def update_user(_id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    if username and email and password and _id:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'username': username, 'email': email, 'password': hashed_password}})
        response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()

#****************************aeropuertos*****************************
# Create
@app.route('/api/aero', methods=['POST'])
def create_aero():
    # Receiving Data
    codigo = request.json['codigo']
    nombre = request.json['nombre']
    ciudad = request.json['ciudad']
    pais = request.json['pais']
    image = request.json['image']

    if codigo and nombre and ciudad and pais and image:
        id = mongo.db.aeros.insert(
            {'codigo': codigo, 'nombre': nombre, 'ciudad': ciudad, 'pais': pais, 'image': image})
        response = jsonify({
            '_id': str(id),
            'codigo': codigo,
            'nombre': nombre,
            'ciudad': ciudad,
            'pais': pais,
            'image': image
        })
        response.status_code = 201
        return response
    else:
        return not_found()

# Get
@app.route('/api/aero', methods=['GET'])
def get_aeros():
    aeros = mongo.db.aeros.find()
    response = json_util.dumps(aeros)
    return Response(response, mimetype="application/json")

# Get one
@app.route('/api/aero/<id>', methods=['GET'])
def get_aero(id):
    aero = mongo.db.aeros.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(aero)
    return Response(response, mimetype="application/json")

# Delete
@app.route('/api/aero/<id>', methods=['DELETE'])
def delete_aero(id):
    mongo.db.aeros.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Aeropuerto' + id + ' eliminado exitosamente'})
    response.status_code = 200
    return response

# Update
@app.route('/api/aero/<_id>', methods=['PUT'])
def update_aero(_id):
    # Receiving Data
    codigo = request.json['codigo']
    nombre = request.json['nombre']
    ciudad = request.json['ciudad']
    pais = request.json['pais']
    if codigo and nombre and ciudad and pais and _id:
        mongo.db.aeros.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'nombre': nombre, 'codigo': codigo, 'ciudad': ciudad, 'pais': pais}})
        response = jsonify({'message': 'Aeropuerto' + _id + 'actualizado correctamente'})
        response.status_code = 200
        return response
    else:
      return not_found()


#***************************aviones***************************************
@app.route('/api/avion', methods=['POST'])
def create_avion():
    # Receiving Data
    modelo = request.json['modelo']
    capadidad = request.json['capacidad']
    
    if modelo and capadidad:
        id = mongo.db.aviones.insert(
            {'modelo': modelo, 'capacidad': capadidad})
        response = jsonify({
            '_id': str(id),
            'modelo': modelo,
            'capacidad': capadidad
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/api/aviones', methods=['GET'])
def get_aviones():
    aviones = mongo.db.aviones.find()
    response = json_util.dumps(aviones)
    return Response(response, mimetype="application/json")


@app.route('/api/avion/<id>', methods=['GET'])
def get_avion(id):
    avion = mongo.db.aviones.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(avion)
    return Response(response, mimetype="application/json")


@app.route('/api/avion/<id>', methods=['DELETE'])
def delete_avion(id):
    mongo.db.aviones.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Avion' + id + ' eliminado satisfactoriamente'})
    response.status_code = 200
    return response


@app.route('/api/avion/<_id>', methods=['PUT'])
def update_avion(_id):
    modelo = request.json['modelo']
    capacidad = request.json['capacidad']
    if modelo and capacidad and _id:
        mongo.db.aviones.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'modelo': modelo, 'capacidad': capacidad }})
        response = jsonify({'message': 'Avion ' + _id + ' actualizado exitosamente'})
        response.status_code = 200
        return response
    else:
      return not_found()

#***************************aerolineas***************************************
@app.route('/api/aerolinea', methods=['POST'])
def create_aerolinea():
    # Receiving Data
    nombre = request.json['nombre']
    origen = request.json['origen']
    
    if nombre and origen:
        id = mongo.db.aerolineas.insert(
            {'nombre': nombre, 'origen': origen})
        response = jsonify({
            '_id': str(id),
            'nombre': nombre,
            'origen': origen
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/api/aerolineas', methods=['GET'])
def get_aerolineas():
    aerolineas = mongo.db.aerolineas.find()
    response = json_util.dumps(aerolineas)
    return Response(response, mimetype="application/json")


@app.route('/api/aerolinea/<id>', methods=['GET'])
def get_aerolinea(id):
    aerolinea = mongo.db.aerolineas.find_one({'_id': ObjectId(id) })
    response = json_util.dumps(aerolinea)
    return Response(response, mimetype="application/json")


@app.route('/api/aerolinea/<id>', methods=['DELETE'])
def delete_aerolineas(id):
    mongo.db.aerolineas.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Aerolinea' + id + ' eliminada satisfactoriamente'})
    response.status_code = 200
    return response


@app.route('/api/aerolinea/<_id>', methods=['PUT'])
def update_aerolinea(_id):
    nombre = request.json['nombre']
    origen = request.json['origen']
    if nombre and origen and _id:
        mongo.db.aerolineas.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'nombre': nombre, 'origen': origen }})
        response = jsonify({'message': 'Aerolinea' + _id + ' actualizada exitosamente'})
        response.status_code = 200
        return response
    else:
      return not_found()

#****************************programas*****************************
# Create
@app.route('/api/programa', methods=['POST'])
def create_programa():
    # Receiving Data
    numero = request.json['numero']
    aerolinea = request.json['aerolinea']
    dias = request.json['dias']
    origen = request.json['origen']
    destino = request.json['destino']
    escalas = request.json['escalas']

    if numero and aerolinea and dias and origen and destino and escalas:
        id = mongo.db.programas.insert(
            {'numero': numero, 'aerolinea': aerolinea, 'dias': dias, 'origen': origen, 'destino': destino, 'escalas': escalas})
        response = jsonify({
            '_id': str(id),
            'numero': numero,
            'aerolinea': aerolinea,
            'dias': dias,
            'origen': origen,
            'destino': destino,
            'escalas': escalas
        })
        response.status_code = 201
        return response
    else:
        return not_found()

# Get
@app.route('/api/programas', methods=['GET'])
def get_programas():
    programas = mongo.db.programas.find()
    response = json_util.dumps(programas)
    return Response(response, mimetype="application/json")

# Get one
@app.route('/api/programa/<id>', methods=['GET'])
def get_programa(id):
    programa = mongo.db.programas.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(programa)
    return Response(response, mimetype="application/json")

# Delete
@app.route('/api/programa/<id>', methods=['DELETE'])
def delete_programa(id):
    mongo.db.programas.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Programa ' + id + ' eliminado exitosamente'})
    response.status_code = 200
    return response

# Update
@app.route('/api/programa/<_id>', methods=['PUT'])
def update_programa(_id):
    # Receiving Data
    numero = request.json['numero']
    aerolinea = request.json['aerolinea']
    dias = request.json['dias']
    origen = request.json['origen']
    destino = request.json['destino']
    escalas = request.json['escalas']
    if numero and aerolinea and dias and origen and destino and escalas and _id:
        mongo.db.aeros.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'numero': numero, 'aerolinea': aerolinea, 'dias': dias, 'origen': origen, 'destino': destino, 'escalas': escalas}})
        response = jsonify({'message': 'Aeropuerto' + _id + 'actualizado correctamente'})
        response.status_code = 200
        return response
    else:
      return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)
