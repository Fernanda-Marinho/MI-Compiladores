import os
current = os.getcwd()
for file_path in (os.listdir(current)):
    if (not file_path.endswith(".txt")): continue
    with open(file_path, 'r') as file:
        with open(f'{current}/files/{os.path.splitext(os.path.basename(file.name))[0]}-saida.txt', 'w') as newfile:
            str = file.read()
            for letter in str:
                newfile.write(f'{letter}\n')
            newfile.close()
        file.close()