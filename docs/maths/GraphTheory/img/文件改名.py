import os

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 列出目录中的所有文件和文件夹
files = os.listdir(current_dir)

# 打印文件名
for file in files:
    if file[:2] == 'T3':
        if file[-2-4] == ' ':
            new_name = 'GNN的数学基础' + '0' + file[-1-4:]
        else:
            new_name = 'GNN的数学基础' + file[-2-4:]
        print(new_name)
        os.rename(file, new_name)
