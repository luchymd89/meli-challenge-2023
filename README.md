# Desafío técnico Meli
Este repositorio contiene el código correspondiente al desafío propuesto.

El proyecto consta de dos contenedores docker:
- meli_mariabd_db, correspondiente a la base de datos, se opto por utilizar la base de datos relacional MariaDB.
- meli_backend, expone un servicio implementado en Python/Flask, que recibe un archivo stremeable y los parámetros opcionales: separador, encode.

Para ejecutar el proyecto se puede utilizar docker-compose, el cual está configurado para levantar ambos contenedore.

`docker-compose build`
`docker-compose up`

- El servicio queda expuesto en el puerto 5003 y la base de datos en el puerto 3310.
- En el archivo _ConfigFile.properties_ se encuentran las credenciales utilizadas para la conexión a la base de datos, así como diferentes parámetros configurables utilizados en el proyecto, por ejemplo los correspondientes a la comunicación con la api de MercadoLibre.
- En el archivo `schema.sql` se encuentra el script que crea la base de datos, el usuario con los permisos correspondientes y la tabla product con los atributos solicitados.

- En _App.py_ se encuentra el punto de inicio, así como los diferentes endpoints.
- Se creo el servicio principal para procesar el archivo [/uploadfile/](http://localhost:5003/uploadfile/) y otro servicio para consultar productos [/product/](http://localhost:5003/product/). 
- En el archivo `teorico/meli-challenge.postman_collection.json` se encuentran ejemplos de llamadas a los diferentes endpoints.

## [/uploadfile/](http://localhost:5003/uploadfile/):
- Recibe opcionalmente por parámetros separator para indicar un separador (default = ,) y encode para indicar el encode del archivo (por defecto lo detecta usando `chardet.detect()['encoding']`).
- La lectura del archivo se hace por stream, con un tamaño de `chunk = 1024` (configurable).
- Elimina la primer línea correspondiente al cabezal.
- Procesa las líneas realizando un split con separator para obtener el id y el site para luego concatenarlas para obtener el `product_id = site + id`.
- Cada 20 líneas hace una llamada al método addProducts con los 20 ids de productos obtenidos hasta el momento.
- `addProducts` se encarga obtener los datos faltantes de los productos (comunicación con api de Mercado Libre) y posteriormente persistirlos en la base de datos.

## Api de MercadoLibre
* Para obtener los datos de productos se realizan consultas a diferentes servicios de MercadoLibre.
* El código se encuentra en `meli_connection.py`
* Con los datos de products_id se consulta el servicio [/items/](https://api.mercadolibre.com/items/), pasando como parámetro `ids= products_id` (la lista de los 20 ids) y `attributes =  "id,site_id,price,start_time,category_id,currency_id,seller_id"`. De esta manera reducimos la cantidad de llamadas a este servicio, dado que se utiliza la cantidad máxima de ids, también se filtra por los atributos que se van a necesitar.
* Esta consulta se realiza utilizando multiprocessing con 4 procesos y chunk = 5 (parámetros configurables).
* Por cada producto obtenido (code = 200) se consultan los servicios:
  * [/categories/](https://api.mercadolibre.com/categories/), con category_id, para obtener el campo name.
  * [/currencies/](https://api.mercadolibre.com/currencies/), con currency_id, para obtener el campo description.
  * [/users/](https://api.mercadolibre.com/users/), con seller_id, para obtener el campo nickname.

## Persistencia en DB
- Se encuentra en los archivos `mariadb_connection.py` y `controller/mariadb_controller.py`
- La base de datos contiene una única tabla `product` con las columnas correspondientes a cada atributo: `id, site, price, start_time, name, description, nickname`.
- Como primary key se usa la tupla (id, site).
- En caso de que los datos para un producto ya existan no se vuelve a persistir.
- La persistencia de productos desde el método `addProducts` se realiza de a 20 productos.
- También se encuentran definidas otras operaciones para insertar, editar, consultar y borrar productos.

# Desafío Teórico
- Las respuestas al desafío teórico se encuentran en el archivo `/teorico/README.md` 

 





