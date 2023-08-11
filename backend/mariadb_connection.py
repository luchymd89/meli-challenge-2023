from controller.mariadb_controller import mariadbController

from utils import getConfig
import logging

# initialize the log settings
logger = logging.getLogger('__mariadb_connection__')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('app.log')
logger.addHandler(fh)


def drop_create_tables():
    print("--> Obtengo conexion")
    mariadb_connection = mariadbController(getConfig().get('DatabaseSection', 'database.dbServerMariadb'),
                                           int(getConfig().get('DatabaseSection', 'database.dbServerMariadbPort')),
                                           getConfig().get('DatabaseSection', 'database.dbServerMariadbUser'),
                                           getConfig().get('DatabaseSection', 'database.dbServerMariadbPassword'),
                                           getConfig().get('DatabaseSection', 'database.dbServerMariadbDatabasename'))
    print("--> Drop table")
    mariadb_connection.drop_tables()
    print("--> Create table")
    mariadb_connection.create_tables()

    mariadb_connection.close()


def add_products_to_db(products):
    global logger
    logger.info('add_products_to_db')
    mariadb_connection = mariadbController(getConfig().get('DatabaseSection', 'database.dbServerMariadb'),
                                           int(getConfig().get('DatabaseSection', 'database.dbServerMariadbPort')),
                                           getConfig().get('DatabaseSection', 'database.dbServerMariadbUser'),
                                           getConfig().get('DatabaseSection', 'database.dbServerMariadbPassword'),
                                           getConfig().get('DatabaseSection', 'database.dbServerMariadbDatabasename'))

    mariadb_connection.add_products(products)

    mariadb_connection.close()


def get_product_from_db(id, site):
    global logger
    logger.info('get_product_from_db')
    mariadb_connection = mariadbController(getConfig().get('DatabaseSection', 'database.dbServerMariadb'),
                                           int(getConfig().get('DatabaseSection', 'database.dbServerMariadbPort')),
                                           getConfig().get('DatabaseSection', 'database.dbServerMariadbUser'),
                                           getConfig().get('DatabaseSection', 'database.dbServerMariadbPassword'),
                                           getConfig().get('DatabaseSection', 'database.dbServerMariadbDatabasename'))

    product = mariadb_connection.get_product(id, site)

    mariadb_connection.close()

    return product


def get_all_products_from_db():
    global logger
    logger.info('get_all_products_from_db')
    mariadb_connection = mariadbController(getConfig().get('DatabaseSection', 'database.dbServerMariadb'),
                                           int(getConfig().get('DatabaseSection', 'database.dbServerMariadbPort')),
                                           getConfig().get('DatabaseSection', 'database.dbServerMariadbUser'),
                                           getConfig().get('DatabaseSection', 'database.dbServerMariadbPassword'),
                                           getConfig().get('DatabaseSection', 'database.dbServerMariadbDatabasename'))

    products = mariadb_connection.get_all_product()

    mariadb_connection.close()

    return products
