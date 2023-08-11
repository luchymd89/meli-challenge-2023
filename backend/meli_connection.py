import logging
import requests

from datetime import datetime
from utils import getConfig
from multiprocessing import Pool

# initialize the log settings
logger = logging.getLogger('__meli_connection__')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('app.log')
logger.addHandler(fh)

URL_API_MELI = str(getConfig().get("MeliSection", "api.url"))
NUM_PROCESSES = int(getConfig().get('MeliSection', 'num.processes'))
NUM_CHUNK = int(getConfig().get('MeliSection', 'num.chunk'))


# Obtiene nombre de categoria
# URL_API_MELI/categories/$category_id
def getCategory(category_id):
    global logger
    category_name = ""
    if category_id:

        logger.info('getCategory : ' + str(category_id))
        url_categories = URL_API_MELI + "/categories/"
        headers = {
            'Authorization': 'Bearer ' + str(getConfig().get("MeliSection", "authorization.token"))
        }

        response = requests.get(url_categories + str(category_id), headers=headers)

        if response.status_code == 200:
            content_json = response.json()
            category_name = content_json['name']

    return category_name


# Obtiene descripción de moneda
# URL_API_MELI/currencies/$currency_id
def getDescription(currency_id):
    global logger
    currency_description = ""
    if currency_id:
        logger.info('getDescription : ' + str(currency_id))
        url_currencies = URL_API_MELI + "ption"
        headers = {
            'Authorization': 'Bearer ' + str(getConfig().get("MeliSection", "authorization.token"))
        }

        response = requests.get(url_currencies + str(currency_id), headers=headers)

        if response.status_code == 200:
            content_json = response.json()
            currency_description = content_json['description']

    return currency_description


# Obtiene nickname de usuario
# URL_API_MELI/users/$seller_id
def getNickName(seller_id):
    global logger
    nickname = ""
    if seller_id:
        logger.info('getNickName : ' + str(seller_id))
        url_users = URL_API_MELI + "/users/"
        headers = {
            'Authorization': 'Bearer ' + str(getConfig().get("MeliSection", "authorization.token"))
        }

        response = requests.get(url_users + str(seller_id), headers=headers)

        if response.status_code == 200:
            content_json = response.json()
            nickname = content_json['nickname']

    return nickname


# noinspection PyUnresolvedReferences
def getProduct(item):
    global logger
    logger.info('getProduct : ' + str(item))
    if item['code'] == 200:

        body = item['body']

        # Se obtiene id de item_id quitando las 3 primeras letras correspondientes a site
        id = body['id'][3:]
        site = body['site_id']
        if 'price' in body:
            price = float(body['price'])
        else:
            price = 0.0

        if 'start_time' in body:
            start_time = datetime.strptime(body['start_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            start_time = datetime.now()

        if 'category_id' in body:
            category_id = body['category_id']
            # Se obtiene nombre de categoria a partir de category_id
            name = getCategory(category_id)
        else:
            name = ""

        if 'currency_id' in body:
            currency_id = body['currency_id']
            # Se obtiene descripcion de moneda a partir de currency_id
            description = getDescription(currency_id)
        else:
            description = ""

        if 'seller_id' in body:
            seller_id = body['seller_id']
            # Se obtiene nickname de usuario a partir de seller_id
            nickname = getNickName(seller_id)
        else:
            nickname = ""

        # coros = [getCategory(body['category_id']), getDescription(body['currency_id']), getNickName(body['seller_id'])]
        # [name, description, nickname] = await asyncio.gather(*coros)
        # logger.info('name : ' + str(name))
        # logger.info('description : ' + str(description))
        # logger.info('nickname : ' + str(nickname))
        # se genera tupla de producto con los datos obtenidos
        product = (id, site, price, start_time, name, description, nickname)

        return product


# Obtiene los items de la lista, máximo 20 items.
# Se asume site de 3 caracteres.
# Se obtienen unicamente los atributos a utilizar de cada item, modificable de variable attributes.
# URL_API_MELI/items?ids=items_id&attributes=attributes
def getItems(items_id):
    global logger
    logger.info('getItems : ' + str(items_id))
    url_items = URL_API_MELI + "/items"
    # Se obtienen para cada item unicamente los atributos a utilizar.
    attributes = "id,site_id,price,start_time,category_id,currency_id,seller_id"
    headers = {
        'Authorization': 'Bearer ' + str(getConfig().get("MeliSection", "authorization.token"))
    }
    params = {'ids': items_id, 'attributes': attributes}
    response = requests.get(url_items, headers=headers, params=params)
    products = []
    if response.status_code == 200:
        content_json = response.json()
        products = [p for p in Pool(NUM_PROCESSES).map(getProduct, content_json, NUM_CHUNK) if p is not None]
        logger.info('products : ' + str(products))
        # for item in content_json:

        # products.append(product)

    return products

# product = {
#    "id": id,
#    "site": site,
#    "price": price,
#    "start_time": start_time,
#    "name": name,
#    "description": description,
#    "nickname": nickname
# }

# products.append(product)
