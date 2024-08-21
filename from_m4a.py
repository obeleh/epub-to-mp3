from pydub import AudioSegment

m4a_file = 'm4a/Akkerstraat.m4a'
wav_filename = 'm4a/Akkerstraat.wav'

sound = AudioSegment.from_file(m4a_file, format='m4a')
file_handle = sound.export(wav_filename, format='wav')