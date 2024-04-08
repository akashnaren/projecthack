from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    address = ""
    if request.method == 'POST':
        address = request.form['address']
        # Here, you would typically geocode the address to get coordinates
        # For simplicity, we're just passing the raw address to the template
    return render_template('index.html', address=address)

if __name__ == '__main__':
    app.run(debug=True)