# xor-decode

El script permite decodificar de forma interactiva valores protegidos mediante la codificación XOR, como los utilizados por algunas aplicaciones para ofuscar contraseñas en archivos de configuración. La herramienta recibe un valor en formato {xor}, elimina el identificador, decodifica el contenido en Base64, aplica la operación XOR con la clave correspondiente y finalmente muestra el texto plano. Además, presenta cada etapa del proceso de forma visual y ofrece ayuda para facilitar su uso durante ejercicios de análisis de configuraciones y pruebas de seguridad.

<img width="1442" height="913" alt="Image" src="https://github.com/user-attachments/assets/b90ee473-091d-441a-ad85-8acb1632f6a0" />

## Comandos:

chmod +x xor-decode.py

python3 xor-decode.py
