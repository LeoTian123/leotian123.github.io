# 第5章 离散曲面的曲率 Curvature of Discrete Surfaces

## 1 表面积梯度

第3、4章这里跳过了，实践出真知，后面用到再谈。

三角形一个点的面积梯度

![图片](https://pic1.zhimg.com/v2-7eac5fa13bbd92140e5100cdf93b2d04.jpg)

这个题还是很显然的， $\frac{\Delta 面积}{\Delta 纵向位移} = \frac{1}{2} 底边长$ ，方向向上。

下一个很重要，mesh上点的表面积梯度（我怀疑这里符号可能反了，我感觉是自己减邻居，这样才是邻居指向自己）：

![图片](https://pic1.zhimg.com/v2-26456a2f669f8c947a02db9a00e2f562.jpg)

  

![图片](https://pic2.zhimg.com/v2-395d3dac6eaf3a241248eb0cad53bb5d.jpg)

  

这已经出现了我们之后要多次见到的“cotan定理”了。看一个三角形上的梯度，和刚才一样：

![图片](https://pic4.zhimg.com/v2-4b32f79eb933c72fde594ab11f2d7205.jpg)

都加起来，整理一下形式就OK了。

## 2 拉普拉斯前瞻

这东西下一章还会仔细说，这里作者是提前引入。核心就是时刻记住它表征了**周围点（取值）和自己点（取值）的差异**。

拉普拉斯有很多种理解方法了，我们最先接触这个概念，一般是数量场的二阶导数的和：

![图片](https://pic2.zhimg.com/v2-c8d20ef4cc2cbad77471ac335c1d3981.jpg)

图论中也有拉普拉斯，假设节点上有一个函数，那么这个函数在这个节点的拉普拉斯值，就是其邻居的函数值的和，减去度数倍自己的函数值。也就是说，拉普拉斯被理解为**自己与邻居函数值的差异**。为什么这样引入？看这个图论上的动机：

![图片](https://pic1.zhimg.com/v2-16de5d1640424ae9b69fdf1aae3c79fe.jpg)

（上图详细还可参见[图数据挖掘的数学基础](../GraphTheory/图数据挖掘的数学基础.md)）

也就是说二阶导数本来表示的就是**周围点和自己点的差异**，是啊，高数就是这么学的啊，二阶导数和凹凸性程度有关啊。

那么这本书是怎么提前介绍这个概念的？通过这个公式：

![图片](https://pic3.zhimg.com/v2-f23ab6a7eec1341cddacd23402e26a6e.jpg)

他是说这个概念和上面我们计算出的面积梯度形式一样（下一章仔细说，另外，我还是之前观点，疑似符号反了，二者其实是相反数的关系）。这个公式他提出来，是要说明我们刚才计算的这个东西（以及，差了一个符号的拉普拉斯）和**曲率**关系很大，**这东西大小就是平均曲率** $H$ **，方向就是法向量**。为什么？

其实大家仔细想想，为什么拉普拉斯可以是长这个样子，就是说，为什么是挑了x,y,z这仨方向？别的行不行？：

![图片](https://pic1.zhimg.com/v2-e08e8c3f17b18b1765a246a7fb17c0b0.jpg)

以及为什么我们的理解一直都是“周围点和自己点的差异”“梯度”“（后文的）光滑程度”等等这种和具体坐标轴无关的描写？原因就是不论哪一个坐标系，算出来的拉普拉斯值当然是一样的。

在一个二维流形上，我们使用坐标轴算拉普拉斯值，是 $f_{xx} + f_{yy}$ 。

而我们知道 $2H$ 就是两个主曲率的和。某个方向上的曲率（法曲率）是啥？是某个方向上切出来的曲线的二阶导数。主曲率是啥？是主方向上，切出来曲线的二阶导数。两个主方向是垂直的，我们记作 $m$ 和 $l$ ，两个曲率我们记作 $f_{mm}$ 和 $f_{ll}$ 。

那么定理告诉我们，

$f_{xx} + f_{yy} =  f_{mm} + f_{ll}$ 

这当然是成立的，事实上任意两个正交方向上的法曲率，和是一样的：

![图片](https://pic3.zhimg.com/v2-eff86eb72099626e4ee9639065d34310.jpg)

体积梯度，和其他一些定义**顶点法线**的方法就不提了。

## 3 离散版高斯博内定理

这东西连续版本是这样：

![图片](https://pic1.zhimg.com/v2-9eeb8e784ca9e2aa05670f7d7f99003c.jpg)

我们不管具有边界的曲面，那么这定理退化为“高斯曲率在封闭曲面上的积分是 $2\pi\chi$ ”。

好了怎么定义**点的离散高斯曲率**？这里其实有一个启发，看一下曲线的曲率的一种理解方法：

![图片](https://pic4.zhimg.com/v2-d6cd8f6a5988c86a5788803426ad91d3.jpg)

就是单位法向量扫过的微小弧长比上微小弧长。“单位法向量扫过的微小弧长”是一个在单位圆上的弧长，这里出现了曲率。**离散高斯曲率**是受到这个东西的启发去定义的，它是把点毗邻的那些面的单位法向量拼在一个单位球面上，认为高斯曲率就是这个**单位球面多边形的面积**。（那个微小弧长不管了）

![图片](https://pica.zhimg.com/v2-bf03a4ba2af1d94947fd9a67b5951e2c.jpg)

来求一下这个面积，首先，单位球面三角形的面积是：

![图片](https://pica.zhimg.com/v2-2b5796805810a52df8c03c18039b1c46.jpg)

因为

![图片](https://pic4.zhimg.com/v2-bd4850cff0b71cd18956e584c2c81117.jpg)

自然地有单位球面多边形的面积：

![图片](https://pic4.zhimg.com/v2-12ed61903b728bdad8caaab40f8858ff.jpg)

就是看做 $(n-2)$ 个三角形。

然后，**离散高斯曲率等于角亏**，角亏，是 $2 \pi$ 减去它所在的所有角：

![图片](https://pic4.zhimg.com/v2-0e34437fa1ed2d3c5331f518a15bd94b.jpg)

证明我是这样做的：

![图片](https://pic1.zhimg.com/v2-213a74e688338b67edfaf4e058c9324c.jpg)

第一步看左图，角上转一圈，和下面走一圈转过的角，应该是一样的。第二步，法向量夹角，是把一个法向量旋转到另一个法向量的转角，那么这也就是外角。代入公式即可。

离散版高斯博内定理就是**离散高斯曲率的和是** $2 \pi \chi$ ：

![图片](https://pic4.zhimg.com/v2-17161d238c87d5ec6e870fe7df80a833.jpg)

## 4 代码

非常简单，在“curvature.py”。写了获取一个角亏的函数，和获取所有角亏的函数，最后计算 $\chi$ ：

```python
from basictools import *

def get_angle_defect(verts, adj_mat, p):
    res = 0
    for neighbor1 in adj_mat[p]:
        for neighbor2 in adj_mat[p]:
            if neighbor1 in adj_mat[neighbor2]:
                res += get_angle(verts, p, neighbor1, neighbor2)
    res = 4 * pi - res
    return res/2

def get_angle_defects(verts, faces):
    n = len(verts)
    angle_defects = np.full(n, 2 * pi, dtype=np.float32)

    for i, j, k in faces:
        angle_defects[i] -= get_angle(verts, i, j, k)
        angle_defects[j] -= get_angle(verts, j, k, i)
        angle_defects[k] -= get_angle(verts, k, i, j)

    return angle_defects

def get_Euler_Chi(verts, faces):
    angle_defects = get_angle_defects(verts, faces)
    return round(angle_defects.sum()/2/pi)

if __name__ == '__main__':
    verts, faces = resolve_input('input/kitten.obj')
    print(get_Euler_Chi(verts, faces))
```

兔子没有洞， $2-2g=2$ ，小猫和甜甜圈有一个洞， $2-2g=0$ ，双甜甜圈有两个洞， $2-2g=-2$ ，代码都符合预期。

小猫确实有一个洞...：

![图片](https://pic3.zhimg.com/v2-4d507e06b86d5aecddf533ec04687620.jpg)

这张图按照角亏染色。蓝色为负，红色为正。鞍点的高斯曲率——正像是连续情况那样——倾向于是负的，凹点或者凸点，倾向于是正的。

染色逻辑：

```python
angle_defects = get_angle_defects(verts, faces)
scale = np.abs(angle_defects).max()
n_a_d = angle_defects / scale
def blue_gray_red(t):
    if t < 0:
        # 蓝 -> 灰
        a = -t
        # (a)(0,0,1) + (1-a)(0.5,0.5,0.5)
        return (0.5-0.5*a, 0.5-0.5*a, 0.5+0.5*a)
    else:
        # 灰 -> 红
        # (a)(1,0,0) + (1-a)(0.5,0.5,0.5)
        a = t
        return (0.5+0.5*a, 0.5-0.5*a, 0.5-0.5*a)

colors = np.array([blue_gray_red(t) for t in n_a_d], dtype=np.float32)
```