from app import app

@app.route('/')
@app.route('/index')
def index():
    #return "My Name Is Oshri :-)"
	return app.send_static_file('index.html')
@app.route('/about')
def about():
    return "about us"
