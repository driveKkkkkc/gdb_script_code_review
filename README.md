+ 运行环境
  + Ubuntu22.04 + 对应的gcc 与 gdb
  + Python 3.10.12
+ review的核心代码
  + gdb_debugger.py 在实际项目里是接收请求后被调用的python函数，开启gdb进程的入口
  + gdb_script.py  在gdb进程中由gdb进程执行的python脚本
