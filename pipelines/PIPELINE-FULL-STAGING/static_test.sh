#!/bin/bash

source todo-list-aws/bin/activate
set -x
##guardo salida de radon en /tmp/unir-radon, por si no supera el umbral  (-nc) y tengo que imprimrir
radon cc src -nc > /tmp/unir-radon 2>&1
RAD_ERRORS=$(cat /tmp/unir-radon| wc -l)
##complejidad ciclomática de todos  los lambdas es mayor o igual que B
if [[ $RAD_ERRORS -ne 0 ]] 
then
    echo 'Ha fallado el análisis estatico de RADON - CC; complejidad ciclomática de alguno de los lambdas es igual o peor que C'
	##imprimo si error
	cat /tmp/unir-radon
	##limpio fichero
	rm /tmp/unir-radon  
    exit 1
fi

##el código desarrollado en Python cumple con las reglas de estilo definidas por pep8
##guardo salida de flake8 en /tmp/unir-flake8, por si no supera el quality gateway y tengo que imprimrir

flake8 --verbose src/*.py > /tmp/unir-flake8 2>&1
if [[ $? -ne 0 ]]
then
	##imprimo si error
	cat /tmp/unir-flake8
	##limpio fichero
	rm /tmp/unir-flake8
    exit 1
fi

#El alumno deberá de validar que no existen fallas de seguridad en el código de Python desarrollado.
#Para ello se usará la librería bandit. En caso de haber fallos de nivel alto el pipeline debe fallar indicando qué líneas de código tienen potenciales riesgos de seguridad

bandit src/*.py > /tmp/unir-bandit
if [[ $? -ne 0 ]]
then
	##imprimo líneas si error
	grep -i location /tmp/unir-bandit
	##limpio fichero
	rm /tmp/unir-bandit
    exit 1
fi



##limpieza
rm /tmp/unir-radon
rm /tmp/unir-flake8
rm /tmp/unir-bandit