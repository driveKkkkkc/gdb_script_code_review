import gdb
import json

"""_summary_
gdb脚本，用于调试可执行文件，获取栈帧信息
这个脚本是通过gdb调用时执行的，与web应用跑在两个进程中
"""

list = []
filter_line_list = [
    # 只包含这些字符的行会被过滤（空格和缩进不影响）
    "{",
    "}",
]
filter_str_list = [
    "return 0",
    "int main",
    "int argc",
    "char *argv[]"
    "return",
]

# 需要步入的函数参数，默认为空
step_into = step_into
# 输出json文件的路径
ouput_file = ouput_file

def is_filter_code(code):
    for filter in filter_line_list:
        # 相等则过滤
        if filter == code.strip():
            return True
    for filter in filter_str_list:
        # 包含则过滤
        if filter in code:
            return True
    return False


def is_step_into(frame):
    for func in step_into:
        if func in frame.split("\n")[1]:
            return True
    return False

def main():
    # 设置断点在主函数的入口处
    gdb.execute('break main')
    # 启动程序
    gdb.execute('run')
    # 记录步数
    step = 0
    frame = gdb.execute('frame', to_string=True)
    info = frame.split("\n")[1]
    code = info.split("\t")[1].replace(" ", "")
    if not is_filter_code(code):
        line = info.split("\t")[0]
        code_dict = {
            "step": step,
            "line": line,
            "code": code
        }
        list.append(code_dict)
    # 进入单步执行循环
    while True:
        execute_flag = False
        # 判断是否步入
        if is_step_into(frame):
            gdb.execute('step')
            execute_flag = True
        # 判断是否步过
        if not execute_flag:
            gdb.execute('next')
            
        frame = gdb.execute('frame', to_string=True)
        # 获取frame的第二行，代表行号和具体代码
        info = frame.split("\n")[1]
        code = info.split("\t")[1].replace(" ", "")
        line = info.split("\t")[0]
        #  过滤无意义代码
        if is_filter_code(code):
            continue
        
        step += 1
        # 构造为dict，包括行号和指令
        code_dict = {
            "step": step,
            "line": line,
            "code": code
        }
        list.append(code_dict)
        
        # 判断是否在主函数中
        if 'main' in frame and "return 0" in frame:
            break
        # 可以添加其他条件来跳出单步执行循环

if __name__ == '__main__':
    main()
    # 把list 转换为json写入文件
    with open(ouput_file, 'w') as f:
        json.dump(list, f)
    # 重置参数
    step_into = []
    gdb.execute('quit')
    gdb.execute('y')