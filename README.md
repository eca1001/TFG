# TFG

Este repositorio abarca todo el proceso que he llevado a cabo para realizar el Trabajo de Fin de Grado (TFG) del grado en Ingeniería Informática.

## Descripción del TFG
Se va a implementar un sistema de recomendación de tecnologías (lenguajes de programación, bases de datos, plataformas, entre otras.) para desarroladores utilizando los datos de la encuesta de Stack Overflow.

## Autor: 
- Enrique Camarero Alonso

## Tutores:
- José Ignacio Santos Martín
- Virginia Ahedo García

## Página web
El proyecto se encuentra desplegado en la siguiente página web: https://tfg-enriquecamareroalonso.herokuapp.com/

## Instalación:
- VirtualBox: https://www.virtualbox.org/wiki/Downloads
- Ubuntu: https://ubuntu.com/download/desktop
- Visual Studio: https://code.visualstudio.com/download

## Ejecución en local:
### Primera instalación
- Python3: sudo apt-get install python3-venv
- Entorno virtual de Python: python3 -m venv deploy
- Librerías (se encuentra dentro de deploy/proyecto): pip install -r requirements.txt

### Ejecución:
- Activar entorno virtual: . deploy/bin/activate
- Cambiar a directorio deploy: cd deploy
- Cambiar a directorio proyecto: cd proyecto
- Ejecutar código: python main.py
