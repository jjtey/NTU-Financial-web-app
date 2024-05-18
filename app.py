from flask import Flask, render_template, request
import google.generativeai as palm
import replicate
import os

flag = 1 #global variable
name = ""

makersuite_api=os.getenv("MAKERSUITE_API_TOKEN")
palm.configure(api_key=makersuite_api)

model = {'model':"models/chat-bison-001"}
app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=['GET','POST'])
def main():
    global flag, name
    if flag == 1:
        name = request.form.get("q")
        flag = 0 #to lock in the initial name input (else will return as None)
    return(render_template("main.html", r=name)) #define frontend r as backend r (request.form.get("q"))

@app.route("/prediction",methods=['GET','POST'])
def prediction():
    return(render_template("prediction.html"))

@app.route("/dbs_price",methods=['GET','POST'])
def dbs_price():
    q = float(request.form.get("q"))
    return(render_template("dbs_price.html",r=(q*-50.6)+90.2)) #coefficient/intercept is from slide 13 of MM AI Deck 

@app.route("/generate_text",methods=['GET','POST'])
def generate_text():
    return(render_template("generate_text.html")) #to take in questions from user

@app.route("/text_result_makersuite",methods=['GET','POST'])
def text_result_makersuite():
    q = request.form.get("q")
    r = palm.chat(**model,messages=q)
    return(render_template("text_result_makersuite.html",r=r.last))

@app.route("/generate_image",methods=['GET','POST'])
def generate_image():
    return(render_template("generate_image.html")) #to take in prompt from user

@app.route("/image_result",methods=['GET','POST'])
def image_result():
    q = request.form.get("q")
    r = replicate.run("stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",input = {"prompt":q})
    return(render_template("image_result.html",r=r[0])) #r[0] to get first image, as an array of 5 images would be generated

@app.route("/end",methods=['GET','POST'])
def end():
    global flag
    flag = 1
    return(render_template("index.html"))

#double underline means a magic variable that cannot be defined elsewhere
if __name__ == "__main__":
    app.run()
