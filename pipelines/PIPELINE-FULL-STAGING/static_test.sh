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
##el propio flake8 imprimirá por std output los nombres de los ficheros que tienen algún problema
flake8 src/*.py
if [[ $? -ne 0 ]]
then
    exit 1
fi

#El alumno deberá de validar que no existen fallas de seguridad en el código de Python desarrollado.
#Para ello se usará la librería bandit. En caso de haber fallos de nivel alto el pipeline debe fallar indicando qué líneas de código tienen potenciales riesgos de seguridad
bandit src/*.py
if [[ $? -ne 0 ]]
then
    exit 1
fi



##limpieza
rm /tmp/unir-radon