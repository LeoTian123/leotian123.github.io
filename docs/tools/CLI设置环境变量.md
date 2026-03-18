# CLI设置环境变量

这里只考虑Windows的cmd和Linux的bash。

环境变量，作为键值对，值本质上都是字符串，不论Windows还是Linux。如果想要用一个字符串表示“多值”，或者说模拟一个复合的数据结构，Linux使用冒号，Windows使用分号。

## 临时设置环境变量

这件事确实有需求，Windows 和 Linux 使用不同的两套指令：

| 行为 | Windows | Linux |
| :--- | :--- | :--- |
| 设置变量 | `set 变量名=值` | `export 变量名=值`|
| 查看变量 | `set` (查看所有) <br>或 `echo %变量名%` | `export` (查看所有) <br>或 `echo $变量名` |
| 删除变量 | `set 变量名=` | `unset 变量名` |

Linux中，set被用作设置shell变量。export这个关键字强调将shell变量导出为环境变量，使子进程也能访问到，因此得名。

等号两边不要有空格。

## 持久化设置环境变量

Windows：

```cmd
setx MY_VAR "my_value"
```
系统级后面加上 `/M` 即可。

Linux：

本质是修改~/.bashrc文件，建议
- 直接`nano ~/.bashrc`，
- 在文件末尾添加`export MY_VAR="my_value"`，
- 保存退出。
- 如果想要继续用刚才的窗口，使用`source ~/.bashrc`进行更新。

系统级，直接改具有风险，好在系统启动时，会自动运行`/etc/profile.d/`的所有 .sh 文件。
那么可以`sudo nano /etc/profile.d/my_global_vars.sh`，
在里面写入`export MY_VAR="my_value"`，保存退出。

## 引号问题

关于要不要引号有一些注意事项：

- Windows中，
    - set和setx命令，值若无空格，引号有无两可
    - set和setx命令，值若有空格，需要用**双引号**括起来
- Linux中，
    - export命令，值若无空格，引号有无两可
    - export命令，值若有空格，必须使用引号
    - 引号具有**两种形式**，有不同意义：
        - 单引号：引号中的内容会被原样输出，不进行变量替换，例如`export MY_VAR="hello world"`
        - 双引号：引号中的内容会进行变量替换，例如`export PATH="$PATH:/new/path"`以追加路径
