import os
import shutil
import random

audio_train_dir = 'C:/Users/Di_Man/PP/Dataset/audio/train'
audio_test_dir = 'C:/Users/Di_Man/PP/Dataset/audio/test'
audio_validate_dir = 'C:/Users/Di_Man/PP/Dataset/audio/validate'

markups_train_dir = 'C:/Users/Di_Man/PP/Dataset/markups/train'
markups_test_dir = 'C:/Users/Di_Man/PP/Dataset/markups/test'
markups_validate_dir = 'C:/Users/Di_Man/PP/Dataset/markups/validate'

os.makedirs(audio_test_dir, exist_ok=True)
os.makedirs(audio_validate_dir, exist_ok=True)
os.makedirs(markups_test_dir, exist_ok=True)
os.makedirs(markups_validate_dir, exist_ok=True)

train_files = os.listdir(audio_train_dir)
random.shuffle(train_files)

total_files = len(train_files)
test_count = int(total_files * 0.15)
validate_count = int(total_files * 0.15)

test_files = train_files[:test_count]
validate_files = train_files[test_count:test_count + validate_count]


def move_files(files, source_audio_dir, target_audio_dir, source_markups_dir, target_markups_dir):
    for file in files:

        file_base = os.path.splitext(file)[0]

        audio_src = os.path.join(source_audio_dir, file)
        audio_dst = os.path.join(target_audio_dir, file)
        shutil.move(audio_src, audio_dst)

        for markup_file in os.listdir(source_markups_dir):
            if os.path.splitext(markup_file)[0] == file_base:
                markup_src = os.path.join(source_markups_dir, markup_file)
                markup_dst = os.path.join(target_markups_dir, markup_file)
                shutil.move(markup_src, markup_dst)
                break


move_files(test_files, audio_train_dir, audio_test_dir, markups_train_dir, markups_test_dir)

move_files(validate_files, audio_train_dir, audio_validate_dir, markups_train_dir, markups_validate_dir)

print(f"Перемещено {len(test_files)} файлов в test и {len(validate_files)} файлов в validate")
