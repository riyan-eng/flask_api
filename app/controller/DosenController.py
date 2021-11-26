import math
from os import name

from flask.json import jsonify
from app import response, cursor, db, request
from math import ceil

def index():
    try:
        query = "select * from public.dosen a"
        cursor.execute(query)
        data = cursor.fetchall()
        return response.success(data, "success")
    except Exception as e:
        print(e)

def detail(id):
    try:
        query = "select * from public.dosen a where a.id='{0}'"
        cursor.execute(query.format(id))
        dosen = cursor.fetchone()

        query = "select * from public.mahasiswa a where a.dosen_satu='{0}' or a.dosen_dua='{1}'"
        cursor.execute(query.format(id, id))
        mahasiswa = cursor.fetchall()

        if not dosen:
            return response.badRequest([], 'Tidak ada data dosen')

        datamahasiswa = formatMahasiswa(mahasiswa)
        data = singleDetailMahasiswa(dosen, datamahasiswa)
        return response.success(data, 'success')

    except Exception as e:
        print(e)

def singleDetailMahasiswa(dosen, mahasiswa):
    data = {
        'id': dosen['id'],
        'nidn': dosen['nidn'],
        'name': dosen['name'],
        'phone': dosen['phone'],
        'mahasiswa': mahasiswa,
    }
    return data

def singleMahasiswa(mahasiswa):
    data = {
        'id': mahasiswa['id'],
        'nim': mahasiswa['nim'],
        'name': mahasiswa['name'],
        'phone': mahasiswa['phone'],
    }
    return data

def formatMahasiswa(data):
    array = []
    for i in data:
        array.append(singleMahasiswa(i))
    return array

def create():
    try:
        nidn = request.form.get('nidn')
        name = request.form.get('name')
        phone = request.form.get('phone')
        alamat = request.form.get('alamat')

        query = "insert into public.dosen(nidn, name, phone, alamat) values('{0}','{1}','{2}','{3}')"
        cursor.execute(query.format(nidn, name, phone, alamat))
        db.commit()
        return response.success([], 'berhasil menambahkan data dosen')

    except Exception as e:
        print(e)

def update(id):
    try:
        nidn = request.form.get('nidn')
        name = request.form.get('name')
        phone = request.form.get('phone')
        alamat = request.form.get('alamat')

        query = "update public.dosen set nidn='{0}', name='{1}', phone='{2}', alamat='{3}' where id='{4}'"
        cursor.execute(query.format(nidn,name,phone,alamat,id))
        db.commit()
        return response.success([], 'berhasil mengubah data dosen')

    except Exception as e:
        print(e)

def delete(id):
    try:
        query = "delete from public.dosen where id='{0}'"
        cursor.execute(query.format(id))
        db.commit()
        return response.success([], 'berhasil menghapus data dosen')
    
    except Exception as e:
        print(e)
cek2 = "public.dosen"

def get_pagination(table, url, start, limit):
    #ambil data select
    query = "select * from " + str(table)
    cursor.execute(query)
    data = cursor.fetchall()
    #hitung jumlah data
    count = len(data)

    obj={}
    if count < start:
        obj['success'] = False
        obj['message'] = "Page yang dipilih melewati batas total data"
        return obj
    else:
        obj['success'] = True
        obj['start_page'] = start
        obj['per_page'] = limit
        obj['total_data'] = count
        obj['total_page'] = ceil(count/limit)

        #previous link
        if start == 1:
            obj['previous'] = ''
        else:
            start_copy = max(1, start-limit)
            limit_copy = start-1
            obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
        #next link
        if start+limit > count:
            obj['next'] = ''
        else:
            start_copy = start+limit
            limit_copy = start-1
            obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
        
        obj['results'] = data[(start-1): (start-1+limit)]
        return obj

def paginate():
    start = request.args.get('start')
    limit = request.args.get('limit')
    try:
        if start == None or limit == None:
            return jsonify(get_pagination(
                "public.dosen",
                "http://127.0.0.1:5000/api/dosen/page",
                start=request.args.get('start', 1),
                limit=request.args.get('limit', 3),
            ))
        else:
            return jsonify(get_pagination(
                "public.dosen",
                "http://127.0.0.1:5000/api/dosen/page",
                start=int(start),
                limit=int(limit),
            ))
    except Exception as e:
        print(e)