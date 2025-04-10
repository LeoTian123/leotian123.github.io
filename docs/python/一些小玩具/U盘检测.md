# U盘检测

这也是一个神奇的功能，核心是psutil的disk_partitions函数，获取所有的磁盘分区，然后判断是否是U盘。

```python
import time
import psutil

iffind = False

while True:
    # 寻找可移动驱动器
    while not iffind:
        #  设置休眠时间
        time.sleep(5)
        #  检测所有的驱动器，进行遍历寻找
        for item in psutil.disk_partitions():
            if 'removable' in item.opts:
                driver, opts = item.device, item.opts
                #  输出可移动驱动器符号
                # print('发现usb驱动：', driver)
                iffind = True
                break

    '''这里放入核心逻辑'''

    # 检测可移动驱动器是否断开
    while iffind:
        lis = []
        #  设置休眠时间
        time.sleep(5)
        #  检测所有的驱动器，进行遍历寻找
        for item in psutil.disk_partitions():
            lis.append(('removable' in item.opts))
        if not any(lis):
            iffind = False
``` 

当时我用这个干什么？其实中学时候我还负责教室电脑的管理，还有投影仪啊什么的。有一个很烦的任务是记录投影仪的使用记录。这可得想个办法。

我发现每次老师用投影必然会用U盘，因为里面有他们的课件。所以并不需要检测投影仪如何如何，只需要检测老师插入了U盘即可。这样程序自动按照课程表、当时时间等信息维护一个记录，每次到了提交时间拷下来抄一遍就行了。