# Script para transcribir audios con Whisper y TorchAudio

Este script transcribe audios usando el modelo de reconocimiento de voz Whisper y la biblioteca TorchAudio.
También extrae fragmentos de audio basados en un patrón regex especificado y los transcribe nuevamente.
Los resultados se comparan y guardan en un archivo CSV.

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
  * poetry update 
  * poetry build

Este comando instalará las dependencias necesarias en su sistema.
- Con pip:
  * pip install -r requirements.txt
  
## Uso

Para usar el script, siga estos pasos:

1. Coloque los audios que desea transcribir en la misma carpeta que el script.
2. Ejecute el script con el siguiente comando:

```bash
python transcribe_audio.py --model_type <model_type> --regex <regex> --format <audio_format> --language <language>
```

Reemplace `<model_type>` con el tipo de modelo deseado (por ejemplo, `base` o `large`), `<regex>` con el patrón regex para filtrar las transcripciones,
 `<audio_format>` con el formato de archivo de audio (por ejemplo, `wav` o `mp3`), y `<language>` con el idioma de destino.

Por ejemplo, para transcribir todos los audios con una extensión `.wav` usando el modelo Whisper `base`,
 filtrar las transcripciones para la frase "hola" y guardar los resultados en español, ejecutarías el siguiente comando:
```bash
python transcribe_audio.py --model_type base --regex "hola" --format wav --language es
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
python transcribe_audio.py --model_type base --regex "hola" --format wav --language es
```
```
El script creará el siguiente archivo CSV:
audio_name_original,original_transcription,audio_name_result,result_transcription
hola.wav,hola,hola_result.wav,hola
```


El archivo CSV contendrá las siguientes filas:

* La primera fila indica que el archivo original se llama `hola.wav` y la transcripción original es `hola`.
* La segunda fila indica que el archivo resultante se llama `hola_result.wav` y la transcripción resultante es también `hola`.

Este es solo un ejemplo de cómo se puede utilizar el script. El script se puede personalizar para satisfacer las necesidades específicas del usuario.

Espero que esta explicación sea de ayuda.



