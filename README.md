# week7
## app.py
```python
#api
@app.route("/api/member",methods=["get","patch"])
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
```
## member.html
```html
        <div class="text">查詢會員姓名</div>
        <div  class="form">
            <div>
                <div class="input">查詢：<input type="text" id="username"/></div>
                <div class="button"><button onclick="get();">查詢</button></div>            
                <div class="getUsername"></div>
            </div>             
        </div>        
        <hr>
        <div class="text">更新我的姓名</div>
        <div  class="form">
            <div>
                <div class="input">更新：<input type="text" id="name"/></div>
                <div class="button"><button onclick="patch();">更新</button></div>            
                <div class="updateName"></div>
            </div>             
        </div>  
```
## js
```js
<script>
        function get(){
            let username=document.getElementById("username").value;
            let url="http://127.0.0.1:3000/api/member?username="+username;
            fetch(url)
            .then(function(response){
                return response.json();
            })
            .then(function(data){
                if (data.data!=null) {
                    let getUsernameText=data.data[0]["name"]+"("+data.data[0]["username"]+")";
                    let getUsername=document.querySelector(".getUsername");
                    getUsername.innerHTML=getUsernameText;
                } else {
                    let getUsernameText="找不到帳號";
                    let getUsername=document.querySelector(".getUsername");
                    getUsername.innerHTML=getUsernameText;                    
                };
            });
        };       
        function patch(){
            let username=document.getElementById("name").value;
            let url="http://127.0.0.1:3000/api/member";  
            let data={
                name : username
            };
            
            fetch(url,{
                method: "PATCH",
                body: JSON.stringify(data),
                cache: "no-cache",
                headers:{
                    "Accept":"application/json",
                    "Content-Type":"application/json"
                }               
            })       
            .then(function(response){
                return response.json();
            })
            .then(function(ok){
                if (ok.ok==true) {
                    let updateText="更新成功";
                    let update=document.querySelector(".updateName");
                    update.innerHTML=updateText;                      
                };
                if (error.error==true) {
                    let updateText="更新失敗";
                    let update=document.querySelector(".updateName");
                    update.innerHTML=updateText;                      
                };                
            });
        };       
    </script>
```
