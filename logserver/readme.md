Log Server
==========
直接运行 logserver.exe
配置文件 logserver.ini 与 logserver.exe放于同一目录下
其中
[log]
maxfilesize =  25*1024*1024 每个日志文件最大大小
maxbackup   =  20           日志备份个数 
separator          = \n     日志换行分隔符
bufsize = 4*1024            收到bufsize大小后进行处理
cleanlog = 0                运行前是否日志目录中的所有文件
[std]
show = 0                    是否在控制台把收到的日志打印出来
