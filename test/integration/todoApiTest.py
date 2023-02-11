import http.client
import os
import unittest
from urllib.request import urlopen
import requests
import json

import pytest

BASE_URL = os.environ.get("BASE_URL")
#BASE_URL = "https://m0qwfec693.execute-api.us-east-1.amazonaws.com/Prod"
print(BASE_URL)
DEFAULT_TIMEOUT = 2  # in secs


@pytest.mark.api
class TestApi(unittest.TestCase):
    
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_listtodos(self):
        print('---------------------------------------')
        print('Starting - integration test List TODO')
        #Add TODO
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add Todo: '+ str(json_response))
        jsonbody= json.loads(json_response['body'])
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            jsonbody['text'], "Integration text example", "Error en la petición API a {url}"
        )
        #List
        url = BASE_URL+"/todos"
        response = requests.get(url)
        print('Response List Todo:' + str(response.json()))
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertTrue(response.json())
        
        print('End - integration test List TODO')
    def test_api_addtodo(self):
        print('---------------------------------------')
        print('Starting - integration test Add TODO')
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add Todo: '+ json_response['body'])
        jsonbody= json.loads(json_response['body'])
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            jsonbody['text'], "Integration text example", "Error en la petición API a {url}"
        )
        url = url+"/"+ID_TODO
        response = requests.delete(url)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        print('End - integration test Add TODO')
    def test_api_gettodo(self):
        print('---------------------------------------')
        print('Starting - integration test Get TODO')
        #Add TODO
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example - GET"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add Todo: '+ str(json_response))
        jsonbody= json.loads(json_response['body'])
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            jsonbody['text'], "Integration text example - GET", "Error en la petición API a {url}"
        )
        #Test GET TODO
        url = BASE_URL+"/todos/"+ID_TODO
        response = requests.get(url)
        json_response = response.json()
        print('Response Get Todo: '+ str(json_response))
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            json_response['text'], "Integration text example - GET", "Error en la petición API a {url}"
        )
        #Delete TODO to restore state
        response = requests.delete(url)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        print('End - integration test Get TODO')
    
    def test_api_updatetodo(self):
        print('---------------------------------------')
        print('Starting - integration test Update TODO')
        #Add TODO
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example - Initial"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add todo: ' + json_response['body'])
        jsonbody= json.loads(json_response['body'])
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            jsonbody['text'], "Integration text example - Initial", "Error en la petición API a {url}"
        )
        #Update TODO
        url = BASE_URL+"/todos/" + ID_TODO
        data = {
         "text": "Integration text example - Modified",
         "checked": "true"
        }
        response = requests.put(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Update todo: ' + str(json_response))
        #jsonbody= json.loads(json_response['body'])
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            json_response['text'], "Integration text example - Modified", "Error en la petición API a {url}"
        )
        #Test GET TODO
        url = BASE_URL+"/todos/"+ID_TODO
        response = requests.get(url)
        json_response = response.json()
        print('Response Get Todo: '+ str(json_response))
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            json_response['text'], "Integration text example - Modified", "Error en la petición API a {url}"
        )
        #Delete TODO to restore state
        response = requests.delete(url)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        print('End - integration test Update TODO')
    def test_api_deletetodo(self):
        print('---------------------------------------')
        print('Starting - integration test Delete TODO')
        #Add TODO
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example - Initial"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add todo: ' + json_response['body'])
        jsonbody= json.loads(json_response['body'])
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            jsonbody['text'], "Integration text example - Initial", "Error en la petición API a {url}"
        )
        #Delete TODO to restore state
        response = requests.delete(url + '/' + ID_TODO)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        print ('Response Delete Todo:' + str(response))
        #Test GET TODO
        url = BASE_URL+"/todos/"+ID_TODO
        response = requests.get(url)
        print('Response Get Todo '+ url+': '+ str(response))
        self.assertEqual(
            response.status_code, 404, "Error en la petición API a {url}"
        )
        print('End - integration test Delete TODO')
        
    def test_bateria_pruebas_enunciado(self):
        print('Start - test_bateria_pruebas_enunciado')
        url = BASE_URL+"/todos"
        data = {
         "text": "example_test"
        }
        #Prueba que haga una llamada a la función create y el resultado de la respuesta http sea un 200 
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add Todo: '+ str(json_response))
        jsonbody= json.loads(json_response['body'])
        #y que al consultar directamente contra la base de datos sea correcto.
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        self.assertEqual(
            response.status_code, 200, "test_bateria_pruebas_enunciado Error en la petición API a {url}"
        )
        self.assertEqual(
            jsonbody['text'], "example_test", "test_bateria_pruebas_enunciado Error en la petición API a {url}"
        )
        #Prueba que haga una llamada a la función list y el resultado de la respuesta http sea un 200 
        response = requests.get(url)
        print('Response List Todo:' + str(response.json()))
        self.assertEqual(
            response.status_code, 200, "test_bateria_pruebas_enunciado Error en la petición API a {url}"
        )
        #y que al consultar que el número de ítems sea distinto de cero.
        self.assertTrue(response.json())
        
        #•	Prueba que haga una llamada a la función get/{id}, tomando como referencia el identificador id generado en el punto a) de este apartado y validando que sea el mismo resultado del payload que el payload que se usó originalmente en el punto a) 
        
        url = BASE_URL+"/todos/"+ID_TODO
        response = requests.get(url)
        json_response = response.json()
        print('Response Get Todo: '+ str(json_response))
        #y que la respuesta http sea un 200.
        self.assertEqual(
            response.status_code, 200, "test_bateria_pruebas_enunciado Error en la petición API a {url}"
        )
        self.assertEqual(
            json_response['text'], "example_test - GET", "test_bateria_pruebas_enunciado Error en la petición API a {url}"
        )
        #Prueba que haga una llamada a la función update/{id} 
        url = BASE_URL+"/todos/" + ID_TODO
        data = {
         "text": "example_test_m",
         "checked": "true"
        }
        response = requests.put(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Update todo: ' + str(json_response))
        #y el resultado de la respuesta http un 200         
        self.assertEqual(
            response.status_code, 200, "test_bateria_pruebas_enunciado Error en la petición API a {url}"
        )
        #y que el valor actualizado sea exactamente el mismo, invocando a la función get/{id} y comparado los valores.

        self.assertEqual(
            json_response['text'], "example_test_m", "test_bateria_pruebas_enunciado Error en la petición API a {url}"
        )
        url = BASE_URL+"/todos/"+ID_TODO
        response = requests.get(url)
        json_response = response.json()
        print('Response Get Todo: '+ str(json_response))
        self.assertEqual(
            response.status_code, 200, "test_bateria_pruebas_enunciado Error en la petición API a {url}"
        )
        self.assertEqual(
            json_response['text'], "example_test_m", "test_bateria_pruebas_enunciado Error en la petición API a {url}"
        )
        
        #Prueba que haga una llamada a la función delete/{id}, tomando como referencia el identificador id generado en el punto a) de este apartado 

        #Delete TODO to restore state
        url = BASE_URL+"/todos/"+ID_TODO
        response = requests.delete(url)
        #y devuelva una respuesta 200. 
        self.assertEqual(
            response.status_code, 200, "test_bateria_pruebas_enunciado Error en la petición API a {url}"
        )
        #Después se debe de hacer una llamada get/{id} nuevamente con el id original para validar que ya no existe esa entrada en la tabla de la base de datos.
        url = BASE_URL+"/todos/"+ID_TODO
        print('Response Get Todo '+ url+': '+ str(response))
        self.assertEqual(
            response.status_code, 404, "test_bateria_pruebas_enunciado Error en la petición API a {url}"
        )
        
        print('End - test_bateria_pruebas_enunciado')
