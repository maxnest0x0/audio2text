import librosa
import noisereduce as nr
import soundfile as sf
import numpy as np

def reduce_noise(input_path, output_path, reduction_strength=0.7):
    try:
        audio, rate = librosa.load(input_path, sr=None)
        noisy_part = audio[:int(rate * 0.5)]
        
        reduced_noise = nr.reduce_noise(
            y=audio, 
            y_noise=noisy_part, 
            sr=rate,
            prop_decrease=reduction_strength,
            stationary=True
        )
        
        sf.write(output_path, reduced_noise, rate)
        
        print(f'Обработка завершена. Результат сохранен в {output_path}')
        
    except Exception as e:
        print(f'Ошибка: {str(e)}')

if __name__ == '__main__':
    input_file = ''
    output_file = ''
    
    print('Начало обработки аудио.')
    reduce_noise(input_file, output_file)
    print('Готово!')
