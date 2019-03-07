# Bike Rental API

## Consideraciones en el diseño y buenas prácticas 

* Se tomaron el consideración los patrones de diseño Strategy y Factory para la realización de este proyecto.

* Cada clase corresponde a una estrategia del modelo de negocios que puede ser renta tradicional y renta familiar.

* En la clase de renta familiar se tomaron en consideración cosas como la lista de miembros de la familia y errores que pueden presentarse. 

* Ambas clases heredan de una clase padre que contiene los parámetros del negocio.

* Se pretende que el diseno sea lo mas DRY posible.

* La interfaz esta pensada de una forma tal que permita arrendar cualquier objeto por hora, días y semanas

* Doy cumplimiento a la guia de estilo PEP8.

* El código python se ha escrito lo mas idiomático (pythonico) posible.


## Pruebas
1. Clonar
2. Activar venv
3. Instalar requirements.txt


```bash
coverage run --source="rental" -m pytest test_rental.py
coverage report
```
