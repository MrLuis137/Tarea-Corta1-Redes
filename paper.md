# ¿Por qué las voces de los integrantes son diferentes?


##  Introducción
El presente paper analiza los diferentes factores que inciden en las variables de sonido estudiadas por medio de las transformadas de fourier y cómo se relacionan con el sonido de las voces. Dicho análisis se realiza mediante el módulo analizador del software de aplicación Autrum, el cual tiene como propósito grabar y reproducir audios y generar los gráficos correspondientes en dominio del tiempo y en dominio de frecuencia (mediante las transformadas de Fourier). 
La estructura de este documento consiste en una recopilación de información que sirve como base teórica al análisis posterior, que muestra todas las pruebas realizadas y las observaciones necesarias para justificar las conclusiones. Finalmente, se muestra una sección que recopila toda la conclusiones obtenidas del análisis. 

El objetivo de la realización de este paper es mejorar el entendimiento del rango de frecuencias en el que se encuentra la voz humana, el concepto de sus armónicos principales y las diferencias observables que afectan cómo la percibimos.

##  Marco Teórico

Para el correcto entendimiento de este análisis y las pruebas realizadas, se debe comprender la labor de las transformadas de Fourier y los componentes  de esta. 
Según Tanenbaum, el análisis de Fourier es una función periódica de comportamiento razonable la cual se construye sumando una cantidad de senos y cosenos y sucede sobre un periodo de tiempo. Uno de los componentes de las series de Fourier son los armónicos, que son proporcionales a la energía transmitida en la frecuencia correspondiente y nos permiten reconstruir el audio para transmitir la información. Estos, al ser transmitidos por señales, pierden cierta potencia en el proceso y disminuyen en diferentes proporciones. Se distingue un primer armónico o armónico fundamental que identifica al tono principal que se está transmitiendo y es el que predomina sobre los otros.

Además, es importante conocer detalles relevantes sobre la voz humana, para así darle una interpretación más razonable a los gráficos obtenidos.

Según Vozalia (2020), la voz humana es medida, por lo general, en hercios(Hz), y se tiene un rango de frecuencias que está entre 250 y 3000, donde algunos fonemas incluso llegan entre 4000 y 8000 Hz.

Que un sonido se perciba como grave o agudo depende del número de vibraciones que realice por unidad de tiempo. Cuanto más frecuentes sean las vibraciones (alta frecuencia) más agudo será el sonido. Si las vibraciones son menos frecuentes (baja frecuencia) el sonido será más grave. Por lo general, la voz femenina tiene un timbre más agudo debido a que las cuerdas vocales de la mujer son más cortas que las masculinas, mientras que el timbre de voz masculino suele ser más grave. 





## Análisis de los resultados

Para el análisis de las voces de los integrantes del grupo se utilizó el programa en python realizado por el equipo, con el cual cada miembro grabó el sonido de la letra “a” con su voz de modo que los audios fueran similares y nos pudiéramos centrar en la voz de los integrantes. Estos audios se almacenaron en los archivos de formato .atm los cuales son leídos por el programa y contienen todos los datos necesarios para el correspondiente análisis.

Es importante denotar las posibles variables fuera del control del equipo: Micrófonos, ruidos ambientales, entre otros. Estas variables pueden afectar reduciendo el ancho de banda o variar algunos de los armónicos de uno de los miembros con respecto a los otros, ya que fueron grabados en locaciones distintas utilizando equipos distintos. Además todos los audios a excepción del de Luis fueron enviados a través de telegram, lo cual puede agregar alguna compresión extra.

Para analizar las voces humanas se recortó el rango de frecuencias hasta los 8000 hz, de este modo se reduce el ruido en la gráfica y permite concentrarse solo en los detalles importantes para el propósito del documento.

Antes de mostrar e interpretar los resultados obtenidos, es importante aclarar que el eje “y” corresponde a la cantidad de veces que se repite dicha frecuencia, mientras que, el eje “x” representan los componentes de frecuencia en Hz (se decide una escala que llega hasta 8000, debido a que por lo general no hay componentes de frecuencia en la voz humana que sobrepasen dicho rango) . 

Además, es relevante conocer que en el equipo se cuenta con una voz femenina y cuatro voces masculinas, por lo que, con el fin de comparar los gráficos de los integrantes y responder a la pregunta “¿Por qué las voces de los integrantes son diferentes?” en la sección de conclusiones, se decidió agregar primero la voz femenina y luego las voces masculinas para primero realizar comparaciones entre voces femenina y masculinas, entre las 4 voces masculinas, y luego entre las voces de los 5 integrantes en general.


## Resultados

### Fiorella

![](https://cdn.discordapp.com/attachments/462125259382849546/1089033531348504596/image10.png)

En este primer gráfico, podemos notar una menor presencia de frecuencias bajas y un par de picos alrededor en las frecuencias altas entre los 3000Hz y 4500Hz, estas frecuencias altas son atribuibles a la voz femenina.

### Esteban

![](https://cdn.discordapp.com/attachments/462125259382849546/1089033531147157556/image9.png)

La voz de Esteban tiene una fuerte presencia de componentes de baja frecuencia, mientras que en los componentes de alta frecuencia vemos una reducción bastante notoria lo cual corresponde a una voz masculina. La reducción en las bajas frecuencias en parte puede ser causada por algún tipo de compresión o limitante en el ancho de banda del equipo de grabación.


### Leonardo

![](https://cdn.discordapp.com/attachments/462125259382849546/1089033530933260378/image8.png)

En el caso de Leonardo, observamos que las bajas frecuencias predominan(al igual que en el caso de Esteban), pero también hay picos alrededor de los 4000 hz, aunque con menor potencia que las frecuencias más bajas.






### Luis

![](https://cdn.discordapp.com/attachments/462125259382849546/1089033532946534440/image6.png)

En el gráfico correspondiente a Luis, es importante mencionar que fué el único grabado directamente evitando posibles compresiones intermedias. Se observa una fuerte presencia de bajas frecuencias, sobre todo debajo de los 3000Hz, con un pico alrededor de los 2500hz, es apreciable la presencia de frecuencias más altas pero con picos más pequeños.

### Jarod 


![](https://cdn.discordapp.com/attachments/462125259382849546/1089033532447404052/image4.png)

En el caso de Jarod, podemos observar que destacan las frecuencias bajas, con pocos picos destacados en las frecuencias altas, se puede apreciar que hay menos variación a lo largo del gráfico, esto pudiendo ser causado por la calidad del audio. Nuevamente el patrón coincide con una voz masculina con una fuerte presencia de bajos.

Para analizar de forma comparativa los resultados anteriores, primero se comparará la voz de Fiorella con una de las voces masculinas, en este caso la de Esteban. Seguidamente, se comparan 3 voces masculinas(Leonardo, Luis y Jarod), y finalmente, se pondrán en contraste las 5 voces.

#### Comparación de la voz de Fiorella y la voz de Esteban.


![](https://cdn.discordapp.com/attachments/462125259382849546/1089033531570794536/image1.png)

Al comparar ambos gráficos, podemos ver que la voz femenina, presenta frecuencias altas en un mayor porcentaje que la voz masculina(en la cual predominan las frecuencias bajas), esto se hace evidente debido a los picos que se presentan en el gráfico de Fiorella entre los 3000Hz y 4500Hz, mientras que en el caso de Esteban, los en las frecuencias altas hay poca presencia, es decir, los picos se dan principalmente en frecuencias cercanas a cero. Esto se debe principalmente al tono de la voz, el cual es más agudo en la voz femenina y más grave en la masculina.

#### Comparación de las voces de Leonardo, Luis y Jarod


![](https://cdn.discordapp.com/attachments/462125259382849546/1089033531822440588/image2.png)

Al comparar estos gráficos, podemos ver que en los 3 predominan las frecuencias bajas, ya que las tres voces tienen un tono grave. 
Sin embargo, podemos ver que en el caso de Leonardo, se presentan algunos pequeños picos entre 2000Hz y 5000Hz (estas frecuencias altas se presentan con menor porcentaje que las frecuencias bajas predominantes); en el caso de Luis, ocurre algo similar, pero las frecuencias altas que se muestran, tienen picos más altos que los de Leonardo, es decir, presentan un porcentaje mayor de aparición de dicha frecuencia (de igual forma, siguen predominando las frecuencias bajas); en el caso de Jarod, el gráfico se ve distinto a los dos anteriores, en este, la predominancia de las frecuencias bajas es más notoria, ya que no presenta picos notables después de los 10000Hz.

Estas “anomalías” se pueden dar por influencia de ruidos externos a la voz en el audio, los cuales generan nuevos componentes distintos a los de la voz, o por el ancho de banda del medio de transmisión del audio.

#### Comparación de las 5 voces

![](https://cdn.discordapp.com/attachments/462125259382849546/1089033531570794536/image1.png)

![](https://cdn.discordapp.com/attachments/462125259382849546/1089033531822440588/image2.png)


En este caso podemos ver que en las voces masculinas tienen una predominancia en las frecuencias bajas, mientras que la voz femenina en las frecuencias altas, esto se debe en gran parte al tono de la voz, ya que las voces graves generan frecuencias bajas, y las agudas frecuencias altas.

## Conclusión 

Teniendo claros los resultados obtenidos al graficar las distintas voces de los integrantes del equipo de trabajo utilizando los datos de la transformada de fourier, podemos responder la pregunta ¿Por qué las voces de los integrantes son diferentes?

En conclusión la diferencia en las componentes de frecuencia de las voces entre cada miembro se da por varios factores, entre ellos el género, tal como se observó con Fiorella, la diferencia en los tonos de voz, lo cual aunque mantiene características en común, hay algunas frecuencias que resaltan. Además la influencia del ancho de banda de los micrófonos y ruidos externos afectan la precisión de estas comparaciones, de modo que los resultados expuestos no son del todo fiables, pero permiten ejemplificar la diferencia entre las voces de cada miembro.

## Referencias

Vozalia  (2020, 10 septiembre). La voz humana. Decibelios y frecuencia de la voz humana. Vozalia. https://www.vozalia.com/voces/la-voz-humana-decibelios-y-frecuencia-de-la-voz-humana/

Tanenbaum, A & Wetherall, D. (2011). Redes de computadoras (4ta edición). Pearson

10 Ejemplos de Sonidos Graves y Sonidos Agudos. (s. f.). ejemplos. https://www.ejemplos.co/ejemplos-de-sonidos-graves-y-sonidos-agudos/ 




