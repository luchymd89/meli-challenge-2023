from datetime import datetime
import logging
import mariadb

# initialize the log settings
logger = logging.getLogger('__mariadb_controller__')


class mariadbController(object):
    def __init__(self, uri, port, user, password, database):
        try:
            config = {
                'host': uri,
                'port': port,
                'user': user,
                'password': password,
                'database': database
            }

            # connection for MariaDB
            print("--> MariaDB connect")
            self.conn = mariadb.connect(**config)

            # create a connection cursor
            print("--> MariaDB create a connection cursor")
            self.cur = self.conn.cursor()
            print("--> MariaDB connection done")
        except mariadb.Error as e:
            ex = 'mariadbController.__init__():' + str(e)
            global logger
            logger.error(ex, exc_info=True)
            raise e

    def close(self):
        try:
            self.conn.close()
        except Exception as e:
            ex = 'mariadbController.close():' + str(e)
            global logger
            logger.error(ex, exc_info=True)
            raise e

    def drop_tables(self):
        try:
            statement = "DROP TABLE IF EXISTS test;"
            self.cur.execute(statement)
            self.conn.commit()

            statement = "DROP TABLE IF EXISTS product;"
            self.cur.execute(statement)
            self.conn.commit()

            print("Successfully deleted")
        except Exception as e:
            print(f"Error creating table: {e}")

    def create_tables(self):
        try:

            statement = ("CREATE TABLE product(id VARCHAR(128) NOT NULL, site VARCHAR(8) NOT NULL, "
                         "price DOUBLE(11,2) UNSIGNED, "
                         "start_time DATETIME, "
                         "name VARCHAR(128), "
                         "description TEXT, "
                         "nickname VARCHAR(128), "
                         "CONSTRAINT pk_id_site PRIMARY KEY (id, site));")
            self.cur.execute(statement)
            self.conn.commit()

            print("Successfully created")
        except Exception as e:
            print(f"Error creating table: {e}")

    def add_product(self, product):
        try:
            logger.info('add_product')
            statement = ("INSERT INTO product(id, site, price, start_time, name, description, nickname)"
                         " VALUES (?, ?, ?, ?, ?, ?, ?)")
            start_date = None
            if product['start_time']:
                start_date = datetime.strptime(product['start_time'], '%Y-%m-%dT%H:%M:%S.%fZ')

            data = (
                product['id'], product['site'], float(product['price']), start_date, product['name'], product['description'],
                product['nickname'])
            self.cur.execute(statement, data)
            self.conn.commit()

            logger.info('Successfully added product to database', product['id'])

        except Exception as e:
            print(f"Error adding product to database: {e}")

    def add_products(self, products):
        try:
            logger.info('add_product')
            statement = ("INSERT INTO product(id, site, price, start_time, name, description, nickname)"
                         " VALUES (?, ?, ?, ?, ?, ?, ?)")

            self.cur.executemany(statement, products)
            self.conn.commit()

            logger.info('Successfully added product to database', self.cur.rowcount)

        except Exception as e:
            print(f"Error adding product to database: {e}")

    def get_product(self, id, site):
        try:
            statement = ("SELECT id, site, price, start_time, name, description, nickname FROM product "
                         "WHERE id = ? AND site = ?")
            data = (id, site)
            self.cur.execute(statement, data)
            result = []
            for (id, site, price, start_time, name, description, nickname) in self.cur:
                p = {
                    "id": id,
                    "site": site,
                    "price": price,
                    "start_time": start_time,
                    "name": name,
                    "description": description,
                    "nickname": nickname
                }
                result.append(p)

            return result

        except Exception as e:
            print(f"get_product: Error retrieving entry from database: {e}")

    def get_all_product(self):
        try:
            statement = "SELECT id, site, price, start_time, name, description, nickname FROM product "

            self.cur.execute(statement)
            result = []
            for (id, site, price, start_time, name, description, nickname) in self.cur:
                p = {
                    "id": id,
                    "site": site,
                    "price": price,
                    "start_time": start_time,
                    "name": name,
                    "description": description,
                    "nickname": nickname
                }
                result.append(p)

            return result

        except Exception as e:
            print(f"get_all_product: Error retrieving entry from database: {e}")

    def edit_product(self, id, site, start_time, name, description, nickname):
        try:
            statement = ("UPDATE product SET start_time = ?, name = ?, description = ?, nickname = ? "
                         "WHERE id = ? AND site = ?")
            start_date = None
            if start_time:
                start_date = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')
            data = (start_date, name, description, nickname, id, site)
            self.cur.execute(statement, data)
            self.conn.commit()
            print("edit_product: Entry updated successfully")
            return True
        except Exception as e:
            print(f"edit_product: Error updating entry to database: {e}")
            return False

    def delete_product(self, id, site):
        try:
            logger.info('delete_product')
            statement = "DELETE FROM product WHERE id = ? AND site = ?"
            data = (id, site)
            self.cur.execute(statement, data)
            self.conn.commit()
            print(f"delete_product: Successfully deleted delete_product {id}")
            logger.info('delete_product: Successfully deleted delete_product ')
            return True
        except Exception as e:
            print(f"delete_product: Error deleting delete_product from database: {e}")
            return False
