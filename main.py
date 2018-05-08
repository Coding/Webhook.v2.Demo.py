from bottle import Bottle, run, request, abort
import hmac

app = Bottle()

SECRET_TOKEN='123'

@app.get('/')
def index():
	return 'hello world'

@app.post('/webhook')
def webhook():
	event = request.get_header('X-Coding-Event')
	delivery = request.get_header('X-Coding-Delivery')
	webHook_version = request.get_header('X-Coding-WebHook-Version')
	signature = request.get_header('X-Coding-Signature')
	content = request.body.read()
	sha1 = hmac.new(bytes(SECRET_TOKEN, encoding = "utf8"), content, 'sha1')
	sha1 = sha1.hexdigest()
	calculate_signature = 'sha1=' + sha1
	if not calculate_signature == signature:
		abort(400, 'signature failed.')

	json = request.json
	sender = json['sender']
	login = sender['login']
	print('webhook ' + event + ' event from ' + login)
	return json

run(app, host='0.0.0.0', port=8080, debug=True)