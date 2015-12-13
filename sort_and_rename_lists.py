import os
import shutil

for subdir, dirs, files in os.walk('lists/'):
    for f in files:
        if f.endswith('.txt'):
            file_list = f.replace('[', '').replace(']', '').replace(',', '') \
                .replace('txt_included_sorted.txt', '').replace('\'', '').split(' ')
            # move kiap
            file_list[0] = round(float(file_list[0]), 3)
            file_list[1] = round(float(file_list[1]), 3)
            file_list[2] = round(float(file_list[2]), 3)
            shutil.copy('lists/' + f, 'lists_discipline')
            os.rename('lists/' + f, 'lists/' + str(file_list[0]) + '__' + str(file_list[0]) + '_' + str(
                file_list[1]) + '_' + str(file_list[2]) + '_' + str(file_list[3]) + '_' + str(file_list[4]) + '_' + str(
                file_list[5]) + '_' + str(file_list[6]) + 'txt')
