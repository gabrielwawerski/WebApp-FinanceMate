import os

from flask import Flask, render_template, request
import ftplib
import jsonpickle
import service

app = Flask(__name__)

ftp_username = "epiz_27836100"
ftp_password = "agipcompany"
ftp_host = "ftp.epizy.com"
ftp = ftplib.FTP(ftp_host, ftp_username, ftp_password)

server_path = "/htdocs/data/"
local_path = "\\static\\"

ROOT = "/"
ACCOUNTS = ROOT + "acc"
TRANSACTIONS = ROOT + "trans"
ADD_TRANSACTION = ROOT + "addtrans"


@app.route(ROOT)
def root():
    return render_template("index.html", title="FinanceMate v0.3.2")


@app.route(ACCOUNTS)
def accounts():
    acc = getdatatype("accounts")
    return render_template("accounts.html", currency="£", accounts=acc, title="Accounts")


@app.route(TRANSACTIONS)
def transactions():
    trans = getdatatype("transactions")
    return render_template("transactions.html", transactions=trans, title="Transactions", currency="£")


@app.route("/response", methods=["POST"])
def response():
    servc = service.service
    tname = request.form.get("tname")
    tdescription = request.form.get("tdescription")
    tamount = request.form.get("tamount")
    print(f"{tname}, {tdescription}, for {tamount}")
    acc = servc.get_account("Gabriel Wawerski")
    print(acc)
    servc.new_transaction(acc, tamount, "pay", tname, tdescription)
    return transactions()


def getdatatype(datatype):
    data = ServerSerializer(datatype).load()
    alist = []
    for value in data.values():
        alist.append(value)
    return alist


def save_asset(filename, data):
    ServerSerializer(filename).save(data)


def load(filename, path=None):
    if path:
        fpath = os.path.join(app.static_folder + "/" + path, filename)
    else:
        fpath = os.path.join(app.static_folder, filename)
    with open(fpath, "r") as file:
        return dict(jsonpickle.decode(file.read()))


def ftp_retr(path, filename):
    fpath = os.path.join(app.static_folder, filename)
    with open(fpath, "wb") as server_file:
        return ftp.retrbinary(f"RETR {path}{filename}", server_file.write)


class ServerSerializer:
    def __init__(self, data_type):
        self.data_type = data_type

        self.file_name = data_type + ".json"
        self.path = app.static_folder + self.file_name

    def load(self):
        print(f"Fetching {self.data_type} ({ftp_host})... ", end=" ", flush=True)
        with open(f"{app.static_folder}/{self.file_name}", "wb") as server_file:
            ftp.retrbinary(f"RETR /{server_path}/{self.file_name}", server_file.write)
        with open(f"{app.static_folder}/{self.file_name}", "r") as file:
            print("Done.", flush=True)
            return dict(jsonpickle.decode(file.read()))

    def save(self, data):
        print(f"Uploading {self.data_type} ({ftp_host})...", end=" ", flush=True)
        with open(f"{app.static_folder}/{self.file_name}", "w") as local_file:
            local_file.write(jsonpickle.encode(data))

        with open(f"data/{self.file_name}", "rb") as server_file:
            ftp.storbinary(f"STOR /{server_path}/{self.file_name}", server_file)
        print("Done.", flush=True)
