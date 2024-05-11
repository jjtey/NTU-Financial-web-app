from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=['GET','POST'])
def main():
    r = request.form.get("q")
    return(render_template("main.html", r=r)) #define frontend r as backend r (request.form.get("q"))

#double underline means a magic variable that cannot be defined elsewhere
if __name__ == "__main__":
    app.run()
