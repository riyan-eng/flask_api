from app import response, cursor, db, request, app, uploadconfig
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import os
import uuid
from werkzeug.utils import secure_filename

def upload():
    try:
        judul = request.form.get('judul')
        if 'file' not in request.files:
            return response.badRequest([], 'File tidak tersedia')
        file = request.files['file']
        if file.filename == '':
            return response.badRequest([], 'File tidak tersedia')
        if file and uploadconfig.allowed_file(file.filename):
            uid = uuid.uuid4()
            filename = secure_filename(file.filename)
            renamefile = "flask-"+str(uid)+filename

            file.save(os.path.join(app.config["UPLOAD_FOLDER"], renamefile))

            query = "insert into public.picture(judul, path_name) values ('{0}', '{1}')"
            cursor.execute(query. format(judul, renamefile))
            db.commit()
            return response.success({
                "judul": judul,
                "pathname": renamefile
            }, "Sukses mengupload file")
        else:
            return response.badRequest([], 'File tidak diizinkan')

    except Exception as e:
        print(e)

def createAdmin():
    try:
        level = 1
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        query = "insert into public.user(level, name, email, password) values('{0}','{1}','{2}','{3}')"
        cursor.execute(query.format(level, name, email, str(generate_password_hash(password, "sha256"))))
        db.commit()
        return response.success([], 'berhasil menambahkan user')

    except Exception as e:
        print(e)

def login():
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        query = "select * from public.user where email='{0}'"
        cursor.execute(query.format(email))
        user = cursor.fetchone()

        if not user:
            return response.badRequest([], 'Email tidak terdaftar')

        if check_password_hash(user['password'], password) == False:
            return response.badRequest([], 'Kombinasi password salah')

        access_token = create_access_token(user)

        return response.success({"data": user,"access_token": access_token}, 'Sukses login!')
    
    except Exception as e:
        print(e)