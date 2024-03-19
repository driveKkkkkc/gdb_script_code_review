import os
import sys
import subprocess
import json
import random
import string

# 同级目录下的cpp_files文件夹 和 executable_files文件夹的路径
executable_path = os.path.abspath(os.path.dirname(__file__)) + '/executable_files/'
cpp_file_path = os.path.abspath(os.path.dirname(__file__)) + '/cpp_files/'

# 进到当前脚本目录下
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(os.path.dirname(os.path.abspath(__file__)))


def compile(cpp_file_path, executable_file_path):
    # 编译cpp文件
    result = os.system('g++ -g -O0 ' + cpp_file_path + ' -o ' + executable_file_path)
    return result


def debug(executable_file_path, step_into):
    """ 根据可执行文件路径和要步入的函数列表调试可执行文件
    @param executable_file_path: 可执行文件路径
    @param step_into: 要步入的函数列表
    """
    # 生成一个随机字符
    random_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    # 输出文件路径
    output_file = random_str + "_frame.json"
    # 要步入的函数
    step_param = "py step_into = [" + ", ".join(["\"" + step + "\"" for step in step_into]) + "]"
    file_param = "py ouput_file = \"" + output_file + "\""
    
    gdb_commands = [
        # 设置参数，可在gdb_script.py中使用
        # "py step_into = [\"preOrder\"]",
        step_param,
        file_param,
        "source gdb_script.py",
        "quit"
    ]
    
    gdb_commands[0].replace("'", r"\'")
    
    # 拼接调试命令, 并携带step_into作为gdb_script.py的参数
    gdb_command = "gdb -batch -q {}".format(" ".join(["-ex '{}'".format(cmd) for cmd in gdb_commands])) + " " + executable_file_path
    # print("gdb_command:", gdb_command)
    # 运行gdb并将输出写入文件
    subprocess.run(gdb_command, shell=True)
    
    frame = ""
    try:
        with open(output_file, 'r') as f:
            frame = f.read()
    except Exception as e:
        frame = e
    finally:
        # 删除输出文件
        os.remove(output_file)
        return frame


def gdb_process(executable_file_name, cpp_file_name):
    """
    测试不指定步入的编译调试
    """
    global executable_file, cpp_file
    executable_file = executable_path + executable_file_name
    cpp_file = cpp_file_path + cpp_file_name

    # 编译cpp文件
    result = compile(cpp_file, executable_file)
    if result == 0:
        # 编译成功，启动gdb调试
        print('编译成功！')
        debug(executable_file)
        # 读取frame.json文件,并返回
        with open('frame.json', 'r') as f:
            frame = f.read()
            return frame
        
    else:
        # 编译失败，退出
        print('编译失败！')
        exit(1)
