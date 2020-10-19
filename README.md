# intro 
Repositorio en construcción y continua adaptación. 

# instrucciones de instalación
descargar requerimientos
- clonar el repositorio
- Instalar anaconda o miniconda 
- correr los siguientes comando en la terminal  
```shell script
conda env create --file ./requirements.txt --name ebol20
conda activate ebol20
cd path_to_ebol20
```
instalar ebol20 en modo desarollo
```shell script 
pip intall -e . 

```  
- instalar el programa cart de [acá](http://www.umich.edu/~mejn/cart/)
  - copiar el binario a ./cart/cart
  
# contenidos
- elec_bol20
    - README
    - cart  
    ejecutable del programa cart
        - cart
    - datos_0_crudos  
    datos de entreada para ser procesados
        - 2019
        - 2020
    - datos_1_intermedios
    - datos_2_finales
    - nb_2019    
    notebook con código para procesar los datos del 2019 
    - nb_2020  
    notebook con código para procesar los datos del 2020 
    - util.pyb 
    funciones reusables  


# hoja de ruta 
nb_2020 -> elecciones del 2020  
nb_2019 -> prototipo elecciones 2019 

- z010_carto_nac.py  
crear cartogramas nacionales
- z015_carto_ext.py  
crear cartogramas internacionales

- z020_procesador_datos  
libreria agnóstica para transformar datos crudos de entrada, combinarlos con output de z010,z015 
y crear un file standard
  - definir cual va a ser el estandard de file i.e que columnas, convención de nombres y identificadores (id)
  
- z050_predictor  
tomar los datos de z020 y predecir posibles resultdos

- z070_visualizador
tomar los datos de z020 y visualizar y ademas subir las graficas internet


