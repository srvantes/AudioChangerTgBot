from pydub import AudioSegment

def cut_audio(input_file, start_ms, end_ms,output_file):
    audio = AudioSegment.from_file(input_file)
    clip = audio[start_ms:end_ms]
    clip.export(output_file, format="mp3")