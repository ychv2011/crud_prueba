## crud_prueba

### Instalación y Ejecución

- Crear el usuario crud_prueba en Postgresql y la base de datos crud_prueba asignandole el usuario crud_prueba como owner.

- De preferencia crear un entorno virtual para correr el proyecto:

    `python3 -m venv nombre_entorno`

- Activar el entorno virtual:

    `source nombre_entorno/bin/activate`

- Ingresar a la carpeta donde se ha clonado el proyecto.

    `cd crud_prueba`

- Instalar los paquetes de requirements.txt

    `pip install -r requirements.txt`

- Hacer las migraciones:

    `python manage.py migrate`

- Correr el proyecto:

    `python manage.py runserver`