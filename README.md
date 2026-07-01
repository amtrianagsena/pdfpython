README - Instalación y ejecución del proyecto
📋 Requisitos
Python 3.x
pip
🚀 Instalación

Instala las dependencias necesarias:

python -m pip install django
python -m pip install reportlab
🗄️ Configuración de la base de datos

Crea las migraciones y aplica los cambios:

python manage.py makemigrations
python manage.py migrate
📊 Generar el diagrama de la base de datos
1. Instalar django-extensions
python -m pip install django-extensions
2. Agregar la aplicación a Django

En el archivo settings.py, agrega 'django_extensions' en la lista INSTALLED_APPS:

INSTALLED_APPS = [
    ...
    'django_extensions',
]

3. Instalar pydotplus:
python -m pip install pydotplus

4. Descargar Graphviz.

Descarga la versión ZIP desde el sitio oficial:

👉 https://graphviz.org/download/

Extrae el contenido en una carpeta de tu preferencia.

5. Agregar Graphviz al PATH (solo para la sesión actual)

En Windows (CMD):

set PATH=C:\Users\aprendiz\Downloads\Graphviz-15.0.0-win32\bin;%PATH%

Nota: Ajusta la ruta según la ubicación donde hayas descomprimido Graphviz.

6. Verificar la instalación:
dot -V

Si el comando muestra la versión de Graphviz, la instalación fue exitosa.

7. Generar el diagrama
python manage.py graph_models -a -o modelo.png

Al finalizar, se generará el archivo modelo.png en la carpeta principal del proyecto con el diagrama de la base de datos.
