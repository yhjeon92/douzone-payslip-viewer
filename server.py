#!/usr/bin/python3
from flask import Flask, request, Response, redirect
from decipher import *
import json


app = Flask(__name__, static_url_path='', static_folder='static')


def parse_error(status: int, code: int, message: str, detail: str):
    return Response(response=json.dumps({'code': code, 'message': message, 'detail': detail}), status=status, mimetype="application/json; charset=utf-8")


@app.route('/upload', methods=["POST"])
def upload_payslip():
    file = request.files.get("file")
    password = request.form.get("password")
    if file is None:
        return parse_error(400, 400, "Bad Request", "HTML 파일을 인식할 수 없습니다.")

    if password is None:
        return parse_error(400, 400, "Bad Request", "패스워드가 지정되지 않았습니다.")

    try:
        html_data = file.stream.read()
        result = from_string(html_data, password)
    except Exception as e:
        return parse_error(500, 500, "Internal Server Error", "복호화에 실패하였습니다.")

    return result


@app.route('/', methods=["GET"])
def index_page():
    return redirect('/index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
