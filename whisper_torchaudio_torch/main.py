import argparse
import csv
import json
import os
import re

import torch
import torchaudio
import whisper_timestamped as whisper

script_path = os.path.dirname(os.path.realpath(__file__))


def parse_args():
    parser = argparse.ArgumentParser(description="Transcribe and transform audios with whisper, torchaudio, and torch.")
    parser.add_argument('model_type', help="Model type: base")
    parser.add_argument('regex', help="Regex: d{4}")
    parser.add_argument('format', help="Audio a_format: .wav")
    parser.add_argument('--language', default='es', help="Language:  es")
    return parser.parse_args()


def transcribe_audio(model, audio_file_path, language):
    try:
        transcription_result = whisper.transcribe_timestamped(
            model,
            audio_file_path,
            language=language,
            task="transcribe",
            remove_punctuation_from_words=True,
            fp16=False
        )
        return transcription_result
    except Exception as e:
        print(f"Error during audio processing: {e}")
        return None


def exclude_audio_chunk(audio_file_path, start, end):
    audio_tensor, sample_rate = torchaudio.load(audio_file_path)
    start_sample = int(start * sample_rate)
    end_sample = int(end * sample_rate)
    audio_excluded = torch.cat((audio_tensor[:, :start_sample], audio_tensor[:, end_sample:]), dim=1)
    return audio_excluded, sample_rate


def write_to_csv(csv_file_path, row):
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(row)


def main(model, regex, a_format, context, lan):
    try:
        audio_format = a_format
        regex_pattern = re.compile(regex)
        output_dir = os.path.join(script_path, "../output")
        os.makedirs(output_dir, exist_ok=True)

        csv_file_path = os.path.join(script_path, "../output/output_results.csv")
        header = ["audio_name_original", "original_transcription", "audio_name_result", "result_transcription"]

        if not os.path.exists(csv_file_path):
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(header)

        for entry in os.scandir(os.path.join(script_path, "../input")):
            if entry.is_file() and entry.name.endswith(audio_format):
                audio_name = entry.name
                audio_path = entry.path

                original_transcription = transcribe_audio(model, audio_path, language=lan)
                match = regex_pattern.findall(original_transcription["text"])
                data = json.loads(json.dumps(original_transcription, indent=2, ensure_ascii=False))
                for m in match:
                    word = next((t for t in data['segments'][0]['words'] if t['text'] == m), None)
                    if word:
                        start_time = word['start']
                        end_time = word['end'] + context
                        audio_excluded, sample_rate = exclude_audio_chunk(audio_path, start_time, end_time)
                        output_file = os.path.join(script_path, f"../output/new_{audio_name}")
                        torchaudio.save(output_file, audio_excluded, sample_rate=sample_rate)
                        result_transcription = transcribe_audio(model, output_file, language=lan)
                        csv_row = [audio_name, original_transcription["text"], os.path.basename(output_file),
                                   result_transcription["text"]]
                        write_to_csv(csv_file_path, csv_row)
                        print(f'Original transcription = {original_transcription["text"]}')
                        print(f'Transcription after audio cut = {result_transcription["text"]}')
                    else:
                        print(f"{data['segments'][0]['words']}\nNo matches with that regex pattern: {regex}")
        print("Process completed successfully.")
    except Exception as e:
        print(f"Error during audio processing: {e}")


if __name__ == '__main__':
    command_line_args = parse_args()
    if command_line_args.model_type == "base":
        ctxt = 0.6
    elif command_line_args.model_type == "large":
        ctxt = 1.1
    whisper_model = whisper.load_model(command_line_args.model_type, device="cpu")
    main(whisper_model, command_line_args.regex, command_line_args.format, ctxt, lan=command_line_args.language)
