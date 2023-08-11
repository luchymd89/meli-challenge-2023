from flask import Flask, request, jsonify
from datetime import datetime
import logging
import datetime
import chardet

from meli_connection import getItems
from mariadb_connection import get_product_from_db, get_all_products_from_db, add_products_to_db

# initialize the log settings
logger = logging.getLogger('__backend__')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('app.log')
logger.addHandler(fh)

# Definicion de variables globales
app = Flask(__name__, instance_relative_config=True)


# usado al convertir en json, sino da error si es de tipo datetime
def defaultconverter(o):
    if isinstance(o, datetime.date):
        return o.__str__()
    if isinstance(o, datetime.datetime):
        return o.__str__()


def addProducts(products_id):
    coma = ','
    products = getItems(coma.join(products_id))
    add_products_to_db(products)


@app.route('/product/', methods=['GET'])
def getProduct():
    try:
        if request.method == 'GET':
            if request.args.get('id') and request.args.get('site'):
                id = str(request.args.get('id'))
                site = str(request.args.get('site'))
                product = get_product_from_db(id, site)
            else:
                product = get_all_products_from_db()
            return jsonify(product), 200
    except Exception as e:
        logger.error('Error occurred : ' + str(e), exc_info=True)
        return jsonify(str(e)), 500


@app.route('/', methods=['GET'])
@app.route('/index/', methods=['GET'])
def index():
    global logger
    logger.info('index')

    try:
        return jsonify("It Works!!"), 200

    except Exception as e:
        logger.error('Error occurred : ' + 'index().' + str(e), exc_info=True)
        return jsonify(str(e)), 500


@app.route('/uploadfile/', methods=['POST'])
def uploadfile():
    global logger
    logger.info('uploadfile')
    try:
        chunk_size = 1024
        # new_line = b'\r\n'
        separator = b','
        rest = b''
        products_id = []

        init = True
        if request.args.get('separator'):
            separator = str(request.args.get('separator')).encode('utf-8')
        if request.args.get('encode'):
            encoding = str(request.args.get('encode'))

        while True:
            chunk = request.stream.read(chunk_size)

            # Final del archivo, proceso los productos que pueden haber quedado sin  procesar
            if len(chunk) == 0:
                if len(products_id) > 0:
                    addProducts(products_id)
                    products_id = []
                return jsonify("Archivo procesado"), 200

            # Primeras lineas del archivo
            if init:
                # Si no se agrego el parámetro de encoding trato de detectarlo
                if not encoding:
                    encoding = chardet.detect(chunk)['encoding']

                # quito cabezal
                chunk_splitted = chunk.splitlines()
                lines = chunk_splitted[1:]

                init = False
            else:
                # Si al obtener el archivo quedaron restos de datos de la particion anterior las agrego
                chunk_res = chunk + rest
                # chunk_splitted = chunk_res.split(new_line)
                lines = chunk_res.splitlines()

            for line in lines:
                prod = line.split(separator)
                if len(prod) == 2:
                    rest = b''
                    id = prod[1].decode(encoding)
                    site = prod[0].decode(encoding)
                    product_id = site + id
                    products_id.append(str(product_id))
                    if len(products_id) == 20:
                        addProducts(products_id)
                        products_id = []

                else:
                    rest = line

        return jsonify("Archivo procesado"), 200

    except Exception as e:
        logger.error('Error occurred : ' + str(e), exc_info=True)
        return jsonify(str(e)), 500


app.run(host='0.0.0.0', debug=True)
