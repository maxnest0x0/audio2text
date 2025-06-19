import os


def compare_and_rename(folder1, folder2):
    files1 = [f for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f))]
    files2 = [f for f in os.listdir(folder2) if os.path.isfile(os.path.join(folder2, f))]

    names1 = {}
    names2 = {}

    for file in files1:
        name, ext = os.path.splitext(file)
        names1[name] = (file, ext)

    for file in files2:
        name, ext = os.path.splitext(file)
        names2[name] = (file, ext)

    common_names = set(names1.keys()) & set(names2.keys())

    print(f"Найдено {len(common_names)} пар файлов с одинаковыми именами")

    for i, name in enumerate(common_names, 1):
        file1, ext1 = names1[name]
        file2, ext2 = names2[name]

        new_name1 = f"{i}{ext1}"
        new_name2 = f"{i}{ext2}"

        old_path1 = os.path.join(folder1, file1)
        new_path1 = os.path.join(folder1, new_name1)

        old_path2 = os.path.join(folder2, file2)
        new_path2 = os.path.join(folder2, new_name2)

        try:

            os.rename(old_path1, new_path1)
            os.rename(old_path2, new_path2)
            print(f"Успешно: {file1} -> {new_name1}, {file2} -> {new_name2}")
        except Exception as e:
            print(f"Ошибка при переименовании {file1} или {file2}: {str(e)}")


folder1 = "C:/Users/Di_Man/PP/Dataset/audio"
folder2 = "C:/Users/Di_Man/PP/Dataset/markups"

compare_and_rename(folder1, folder2)
