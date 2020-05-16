# TP de  simulacipon 1er cuatrimestre 2020

## Software necesario
* Python 3.6
* pip

## Instalar dependencias
`pip install -r requirements.txt`


Si el sistema lanza un error 

`Collecting pkg-resources==0.0.0 (from -r requirements.txt (line 14))
remote:          Could not find a version that satisfies the requirement pkg-resources==0.0.0 (from -r requirements.txt (line 14)) (from versions: )
remote:        No matching distribution found for pkg-resources==0.0.0 (from -r requirements.txt (line 14))
remote:  !     Push rejected, failed to compile Python app.`
Se debe remover de requirements.txt el paquete `pkg-resources==0.0.0`

y volver a correr el comando `pip install -r requirements.txt`

