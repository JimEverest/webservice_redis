from flask import Flask, jsonify, request
import xmltodict
import time
import redis
from werkzeug.wrappers import Response
import logging
import sys

app = Flask(__name__)
app.config["DEBUG"] = True
start = int(round(time.time()))
print("api running")
redis_port = 2017

logging.basicConfig(level=logging.DEBUG,
                    filename='web.log',
                    filemode='a',
                    format= '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s' 
                    )

@app.route("/", methods=['GET', 'POST'])
def parse_xml():
    logging.debug("........................ Service Getting in ........................")
    #xml_data = request.form['barcode']
    try:
        logging.debug("--- raw XML: \n" + request.data.decode() )
        content_dict = xmltodict.parse(request.data)
        logging.debug(content_dict)
        bar_id = content_dict['barcode']['MID']
        logging.debug(f"bar_id--->{bar_id}")
        redis_server.set('String301', bar_id) 
        resp = Response(response='ok',status=200,content_type='text/html;charset=utf-8')
        logging.debug(f"resp--->{resp}")
        return resp
    except:
        logging.error(f"Unexpected error: \n {sys.exc_info()}")
        resp = Response(response='error',status=500,content_type='text/html;charset=utf-8')
        return resp
    # return jsonify(content_dict)

@app.route("/test", methods=['GET', 'POST'])
def test():
    print("Getting in test........................................")
    #xml_data = request.form['barcode']
    try:
        content_dict = xmltodict.parse(request.data)
        print(content_dict)
        bar_id = content_dict['result']['ID']
        print("bar_id---> ", bar_id)
        # redis_server.set('String301', bar_id) 
        resp = Response(response='ok',status=200,content_type='text/html;charset=utf-8')
        return resp
    except expression as identifier:
        resp = Response(response='error',status=500,content_type='text/html;charset=utf-8')
        return resp

@app.route('/hello')
def hello():
    logging.debug("........................ HELLO ........................")
    return 'Hello, World'

def run_redis():
    try:
        global redis_server 
        redis_server = redis.Redis(host='127.0.0.1', port=redis_port)
        print("Connected to redis...")
        # pubsub = redis_server.pubsub()
        # sub = pubsub.subscribe(**{channelname:on_message})
        # sub = pubsub.subscribe(**{'exit':on_exit_message})
        # sub = pubsub.subscribe(**{'selfcheck_inference':on_selfcheck_message})
        # thread = pubsub.run_in_thread(sleep_time=.5)
        # thread.run()
    except (KeyboardInterrupt, SystemExit):
        print("**In except")

        # thread.release()
        # thread.stop()


if __name__ == '__main__':
    logging.debug("Starting web service.")
    run_redis()
    app.run(host='0.0.0.0', port=8080, debug=False)
    

# curl -X POST -d @barcode.xml  -H 'Accept: application/xml'  -H 'Content-Type: application/xml' http://192.168.50.100:8080/ 
#barcode.xml content:
# <barcode>
#     <MID>1234567890123</MID>
# </barcode>
#https://stackoverflow.com/questions/49901197/flask-api-to-parse-xml-post-requests-returning-errors
