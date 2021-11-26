from app import app, response, request, cursor
from app.controller import DosenController, UserController
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import get_jwt_identity, jwt_required

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return response.success(current_user, 'Sukses!')

@app.route('/')
def index():
    return "halo guys"

@app.route('/login', methods=['POST'])
def login():
    return UserController.login()
    
@app.route('/dosen', methods=['GET', 'POST'])
@jwt_required()
def dosens():
    if request.method == 'GET':
        return DosenController.index()
    else:
        return DosenController.create()

@app.route('/dosen/<id>', methods=['GET', 'PUT', 'DELETE'])
def dosenDetail(id):
    if request.method == 'GET':
        return DosenController.detail(id)
    elif request.method == 'PUT':
        return DosenController.update(id)
    elif request.method == 'DELETE':
        return DosenController.delete(id)

@app.route('/api/dosen/page', methods=['GET'])
def dosen_pagination():
    return DosenController.paginate()

@app.route('/create_admin', methods=['POST'])
def admins():
    return UserController.createAdmin()

@app.route('/file_upload', methods=['POST'])
def upload_gambar():
    return UserController.upload()