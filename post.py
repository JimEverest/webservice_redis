import requests
from lxml import etree
import redis
import logging
import sys
import time

redis_port = 2017
url = 'http://127.0.0.1:8080/test'

logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                    filename='post.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志  #a是追加模式，默认如果不写的话，就是追加模式
                    format= '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s' #日志格式
                    )

def on_message(message):
    logging.debug("......... Got Redis Signal Workdone .........")
    data = message["data"]
    ID = redis_server.get('String301')
    X1= redis_server.get('Float124')
    Y1= redis_server.get('Float123')
    X2= redis_server.get('Float126')
    Y2= redis_server.get('Float125')
    X3= redis_server.get('Float128')
    Y3= redis_server.get('Float127')

    # create XML 
    root = etree.Element('result')
    child = etree.Element('ID')
    child.text = ID
    root.append(child)
    child = etree.Element('X1')
    child.text = X1
    root.append(child)
    child = etree.Element('Y1')
    child.text = Y1
    root.append(child)
    child = etree.Element('X2')
    child.text = X2
    root.append(child)
    child = etree.Element('Y2')
    child.text = Y2
    root.append(child)
    child = etree.Element('X3')
    child.text = X3
    root.append(child)
    child = etree.Element('Y3')
    child.text = Y3
    root.append(child)
    # s = etree.tostring(root, pretty_print=True)
    s = etree.tostring(root)
    logging.debug(f"....... xml orgnized ....... \n {s}")

    #post it
    # xml = """<?xml version='1.0' encoding='utf-8'?>""" + s.decode()
    xml = s.decode()

    headers = {'Content-Type': 'application/xml'} # set what your server accepts
    resp = requests.post(url, data=xml, headers=headers).text
    logging.debug(f"Posted---- Response: \n {resp}")
    redis_server.set('String301', '') 

def on_selfcheck_message(message):
    global redis_server
    redis_server.publish('checked_inference' ,'OK')

def on_exit_message(message):
    print('enter exit pid ',os.getpid())
    os.kill(os.getpid(), signal.SIGKILL)


def run_redis(channelname):
    print(f"...... subscribe {channelname} ........")
    try:
        global redis_server 
        redis_server = redis.Redis(host='127.0.0.1', port=redis_port)
        logging.debug("Connected to redis... Wait for signal.")
        pubsub = redis_server.pubsub()
        sub = pubsub.subscribe(**{channelname:on_message})        
        # sub = pubsub.subscribe(**{'exit':on_exit_message})
        # sub = pubsub.subscribe(**{'selfcheck_inference':on_selfcheck_message})
        thread = pubsub.run_in_thread(sleep_time=.5)
        thread.run()

    except (KeyboardInterrupt, SystemExit):
        logging.debug("**In except")
        thread.release()
        thread.stop()

if __name__ == "__main__":
    logging.debug("post running.. waiting redis signal (workdone). ")
    run_redis("workdone")


    # <result>
    #     <ID>1234567890123</ID>
    #     <X1>0.0</X1>
    #     <Y1>0.0</Y1>
    #     <X2>0.0</X2>
    #     <Y2>0.0</Y2>
    #     <X3>0.0</X3>
    #     <Y3>0.0</Y3>
    # </result>
#https://stackoverflow.com/questions/12509888/how-can-i-send-an-xml-body-using-requests-library
