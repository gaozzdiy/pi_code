from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    ip = request.remote_addr
    return  render_template('index.html',user_ip=ip)
    #return  ip

@app.route('/test')
def test():
    return "Hello World!" 


if __name__  == '__main__':
    app.run(host='0.0.0.0')
