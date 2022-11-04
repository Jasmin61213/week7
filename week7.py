from ssl import ALERT_DESCRIPTION_BAD_RECORD_MAC
from flask import Flask
from flask import jsonify 
from flask import request 
from flask import redirect 
from flask import render_template 
from flask import session
from flask import url_for
from flask import make_response
from flask_restful import Api, Resource
import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="",
  database="website"
)

app=Flask(
    __name__,
    static_folder="public",
    static_url_path="/" 
)

api=Api(app)

app.secret_key="any string but secret"

#api
@app.route("/api/member",methods=["GET","PATCH"])
def api_member():
    if request.method=="GET":
        username=request.args.get("username",None)
        cursor=mydb.cursor(dictionary=True)
        data_select="SELECT id,name,username FROM member WHERE username=%s"
        value=(username,)
        cursor.execute(data_select,value)
        data=cursor.fetchall()
        try:
            if data!=[]:
                return make_response(jsonify({"data":data}),200)
            if "account" not in session:
                return jsonify({"data":None})
        except:
            print("Unexpected Error")

    if request.method=="PATCH":
        username=session["account"]
        name=request.get_json()
        name=name["name"]
        cursor=mydb.cursor(dictionary=True)
        name_update="UPDATE member SET name=%s WHERE username=%s"
        value=(name,username)
        cursor.execute(name_update,value)
        mydb.commit()
        try:
            return jsonify({"ok":True})
        except:
            return jsonify({"error":True})

# 首頁
@app.route("/")
def index():
    return render_template("main.html")

# 登入驗證 post方法 導向成功或失敗
@app.route("/signin",methods=["post"])
def signin():
    account=str(request.form["account"])
    secret=str(request.form["secret"])
    cursor=mydb.cursor(dictionary=True)
    account_sel="SELECT * FROM member WHERE username=%s"
    account_val=(account,)
    cursor.execute(account_sel,account_val)
    accountsql = cursor.fetchall()
    if accountsql!=[]:
        if accountsql[0]["username"]==account and accountsql[0]["password"]==secret:
            session["id"]=accountsql[0]["id"]
            session["account"]=accountsql[0]["name"]
            return redirect("/member")
        else:
            return redirect(url_for("error",message="帳號或密碼輸入錯誤"))   
    else:
        return redirect(url_for("error",message="帳號或密碼輸入錯誤"))   

# 成功頁面
@app.route("/member")
def member():
    if "account" in session:
        name=session["account"]
        cursor=mydb.cursor(dictionary=True)
        content_sel="SELECT name,content FROM member INNER JOIN message ON member.id=message.member_id"
        cursor.execute(content_sel)
        result=cursor.fetchall()
        row=result
        return render_template("member.html",name=name,data=row)
    else:
        return redirect("/")

# 失敗頁面
@app.route("/error")
def error():
    data=request.args.get("message","")
    data=str(data)
    return render_template("error.html",message=data)

# 登出頁面導向首頁
@app.route("/signout")
def signout():
    session.pop("account", None)
    return redirect("/")

# 註冊頁面
@app.route("/signup",methods=["post"])
def signup():
    name=request.form["name"]
    account=request.form["account"]
    secret=request.form["secret"]
    cursor=mydb.cursor(dictionary=True)
    sql="SELECT * FROM member WHERE username=%s"
    usn=(account,)
    cursor.execute(sql,usn)
    result = cursor.fetchall()
    if result!=[]:
        return redirect(url_for("error",message="帳號已有人註冊"))
    else:
        sql="INSERT INTO member(name,username,password) VALUES (%s,%s,%s)"
        val=(name,account,secret)
        cursor.execute(sql,val)
        mydb.commit()
        return redirect("/")

# 儲存留言頁面
@app.route("/message",methods=["post"])
def message():
    member_id=session["id"]
    message=request.form["message"]
    cursor=mydb.cursor(dictionary=True)
    sql="INSERT INTO message(member_id,content) VALUE (%s,%s)"
    val=(member_id,message)
    cursor.execute(sql,val)
    mydb.commit()
    return redirect("/member")

# 埠號
app.run(port=3000)
