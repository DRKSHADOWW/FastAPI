INSTALACIÓN DE ENTORNO VIRTUAL
py -m venv (nombre_del_proyecto)
cd (nombre_del_proyecto)
cd Scripts
activate (se debe estar en el cmd)
"Luego salir con "cd .." hasta llegar al archivo del proyecto"


#fastapi
-pip install "fastapi[all]"
python.exe -m pip install --upgrade pip

#Iniciar el server
uvicorn main:app --reload
uvicorn users:app --reload

#dependecias para encriptar
pip install "python-jose[cryptography]"
pip install "passlib[bcrypt]"
openssl rand -hex 32 # gererador de contraseñas ramdon

#documentación
Documentación con Swagger: http://127.0.0.1:8000/docs
Documentación con Redocly: http://127.0.0.1:8000/redoc

#Extensiones
Thunder Client

filter
lambda
ndex
async
