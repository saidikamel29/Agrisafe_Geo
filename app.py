from flask import Flask,render_template,jsonify,request

app = Flask(__name__)

@app.route('/')
def pageprincipal():

    return render_template('pageprincipal.html')

@app.route('/conect')
def conect():

    return render_template('conect.html')

@app.route('/aboutus')
def aboutus():

    return render_template('aboutus.html')

@app.route('/media')
def media():

    return render_template('media.html')


@app.route('/service')
def service():

    return render_template('service.html') 

@app.route('/acount/<name>')
def profile(name):
    return "HELLO (name)"


@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.get_json()  # get JSON from request
    
    name = data.get('name')
    age = data.get('age')
    city = data.get('city')

    print(name, age, city)

    return jsonify({
        "status": "success",
        "message": "Data received"
    })

if __name__ == "__main__":
    app.run(debug=True)