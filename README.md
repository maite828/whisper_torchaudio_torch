# Script para transcribir audios con Whisper,Torch y TorchAudio
El código proporcionado es un programa de Python que transcribe y transforma archivos de audio utilizando las bibliotecas whisper, torchaudio y torch. A continuación se explica el código paso a paso: 
 
1. Importar las bibliotecas necesarias: csv, os, argparse, json, re, torch y torchaudio. 
2. Definir la ruta del script actual. 
3. Definir una función para analizar los argumentos de línea de comandos. 
4. Definir una función para transcribir un archivo de audio utilizando el modelo de whisper. 
5. Definir una función para excluir una porción de audio de un archivo. 
6. Definir una función para escribir en un archivo CSV. 
7. Definir la función principal del programa. 
8. Leer los argumentos de línea de comandos. 
9. Cargar el modelo de whisper según el tipo especificado en los argumentos. 
10. Ejecutar la función principal del programa. 
 
La función principal del programa realiza las siguientes acciones: 
 
1. Obtener el formato de audio, el patrón regex, el contexto y el idioma de los argumentos de línea de comandos. 
2. Crear un directorio de salida y un archivo CSV de resultados si no existen. 
3. Recorrer todos los archivos en el directorio del script. 
4. Si el archivo tiene el formato de audio especificado, realizar las siguientes acciones: 
   a. Obtener el nombre y la ruta del archivo de audio. 
   b. Transcribir el archivo de audio utilizando el modelo de whisper y el idioma especificado. 
   c. Encontrar todas las coincidencias del patrón regex en la transcripción original. 
   d. Para cada coincidencia, obtener el tiempo de inicio y fin de la palabra correspondiente. 
   e. Excluir la porción de audio correspondiente utilizándo la función exclude_audio_chunk. 
   f. Guardar el audio excluido en un nuevo archivo. 
   g. Transcribir el nuevo archivo utilizándo el modelo de whisper y el idioma especificado. 
   h. Escribir los resultados en el archivo CSV. 
   i. Imprimir la transcripción original y la transcripción después de recortar el audio. 
5. Imprimir un mensaje de finalización del proceso. 
 
En resumen, el código carga un modelo de whisper, transcribe archivos de audio, encuentra palabras que coinciden con un patrón regex, recorta el audio correspondiente a esas palabras y guarda los resultados en un archivo CSV.

## Dependencias

* Python 3.6 o superior
* PyTorch 1.8 o superior
* Modelo de reconocimiento de voz Whisper
* Biblioteca TorchAudio

## Instalación de dependencias

Para instalar las dependencias necesarias, siga estos pasos:

1. Abra una terminal o un símbolo del sistema.
2. Navegue a la carpeta donde se encuentra el script.
3. Ejecute el siguiente comando:
- Con Poetry:
  * poetry shell
  * poetry update 
  * poetry build
#### En caso de no tener instalado poetry, en mac sería:
- brew install poetry

Este comando instalará las dependencias necesarias en su sistema.
- Con pip:
  * pip install -r requirements.txt
  
## Uso

Para usar el script, siga estos pasos:

1. Coloque los audios que desea transcribir en la misma carpeta que el script.
2. Ejecute el script con el siguiente comando:
- python main.py <model_type> <regex> <audio_format> --language <language>

```bash
cd whisper-torchaudio-torch
python main.py base "\b\d{4}\b" .wav --language es
```

Reemplace `<model_type>` con el tipo de modelo deseado (por ejemplo, `base` o `large`), `<regex>` con el patrón regex para filtrar las transcripciones,
 `<audio_format>` con el formato de archivo de audio (por ejemplo, `wav` o `mp3`), y `<language>` con el idioma de destino.

Por ejemplo, para transcribir todos los audios con una extensión `.wav` usando el modelo Whisper `base`,
 filtrar las transcripciones para la frase "hola" y guardar los resultados en español, ejecutarías el siguiente comando:
```bash
cd whisper-torchaudio-torch
python main.py large "hola" .wav --language es
```

Este comando creará un archivo CSV llamado `output_results.csv` en la carpeta `output`. El archivo CSV contendrá las siguientes columnas:

* `audio_name_original`: El nombre del archivo de audio original
* `original_transcription`: La transcripción original del archivo de audio
* `audio_name_result`: El nombre del archivo de audio con el fragmento extraído
* `result_transcription`: La transcripción del fragmento extraído

El script también imprimirá las transcripciones originales y resultantes para cada archivo de audio con la coincidencia regex correspondiente.

## Explicación de la ejecución

El script funciona de la siguiente manera:

1. Primero, el script carga el modelo de reconocimiento de voz Whisper.
2. Luego, el script recorre todos los archivos de audio en la carpeta actual.
3. Para cada archivo de audio, el script realiza los siguientes pasos:
    * Transcribe el audio completo usando el modelo Whisper.
    * Busca coincidencias con el patrón regex especificado.
    * Si se encuentra una coincidencia, el script extrae un fragmento de audio del archivo original.
    * El script transcribe nuevamente el fragmento extraído.
    * El script guarda la transcripción original, la transcripción del fragmento extraído y el nombre del archivo de audio en un archivo CSV.

## Ejemplo de ejecución

Considere el siguiente ejemplo:
audios/
hola.wav
adios.wav

Si ejecuta el script con el siguiente comando:
```bash
cd whisper-torchaudio-torch
python main.py base "hola" --format .mp3 --language galician
```
```
El script creará el siguiente archivo CSV:
audio_name_original,original_transcription,audio_name_result,result_transcription
hola.wav,hola,hola_result.wav,hola
```


El archivo CSV contendrá las siguientes filas:

* La primera fila indica que el archivo original se llama `hola.wav` y la transcripción original es `hola`.
* La segunda fila indica que el archivo resultante se llama `hola_result.wav` y la transcripción resultante es también `hola`.


