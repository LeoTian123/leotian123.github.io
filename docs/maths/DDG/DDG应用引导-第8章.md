# 第8章 向量场分解与设计（部分）

这部分代码难度很高，后两节没做，看一下前两节，后两节做一个概念整理。

## 1 霍奇分解

![图片](https://pic3.zhimg.com/v2-58c269f5ec1ceaff5bb95dffc396d412.jpg)

链复形相关的理论不多说了，那么霍奇分解数学上的表述还是比较复杂的：

![图片](https://pic4.zhimg.com/v2-af73e05ddf5c038e67e2bee86f22ac0f.jpg)

![图片](https://pic2.zhimg.com/v2-175d416eb8cf58aef73a936c2e55a9df.jpg)

看最后的表述，对应到二维流形上的向量场，就是说：

![图片](https://pica.zhimg.com/v2-817f579a2df6f7e902531453eaf68d04.jpg)

那么怎么求解导出了梯度部分的 $\alpha$ 以及导出了旋度部分的 $\beta$ 呢？看这一页就行了：

![图片](https://pica.zhimg.com/v2-2fce9370884841cdbee17d3e5574ec58.jpg)

就是把外代数上的理论离散化。请注意这个 $\delta$ 的离散化有两种情况，

- 一种是 $\star_0^{-1} d_0 ^T \star_1$ ，
- 另一种是 $\star_1^{-1} d_0 ^T \star_2$ 。

怎么理解呢？首先熟悉的定义是 $\delta = \star d \star$ ，有定理：

![图片](https://pic3.zhimg.com/v2-27593d8aacc08bab47bf04510b780b34.jpg)

内积是：

![图片](https://pica.zhimg.com/v2-85b7e309f440a13b6e43728515dbb80a.jpg)

就可以得到这个结果：

![图片](https://pic3.zhimg.com/v2-87255bb5ad52323908c85d514b98275a.jpg)

那么这三个 $\star$ ，两个 $d$ 具体是什么呢？这就用到了第4章的知识。

4.8.4节提到了离散霍奇星的定义。怎么定义对偶元素？理论上可以有多种方法，最常用的是**正交对偶**，要求了元素和对偶元素正交。

这可以称之为“外心法”，来看看为什么。二维流形上，点和面互相对偶，点面正交不太好说，先不看了。看边和边的对偶，两个毗邻三角形的什么东西连在一起和公共边垂直？是外心，而且这个连线正是公共边的垂直平分线。

这件事在二维平面上可以得到顺畅的理解。假设有一个平面mesh，这个mesh是使用Delaunay剖分法生成的，但是任意的mesh都可以说明：

![图片](https://pic4.zhimg.com/v2-046357839c2ed178aa226fe44de2917b.jpg)

然后有几种想象方式，结果是一样的：

-   对于每个点，以它们为圆心，开始等速率地扩展出一个圆形，两个圆形的边界一旦相遇，相遇的地方就停止膨胀、贴在一起（必然在垂直平分线），还没有贴在一起的部分继续扩展、膨胀（最终在每个三角形的外心相碰）。得到了一些多边形。
-   找出每个边的中点，开始等速率扩展出垂直平分线，线段一旦互相遇到（必然在外心）就停下。得到了一些多边形。
-   找出每个三角形的外心，连接相邻三角形的外心。

得到的这些多边形，叫做Voronoi多边形，如下：

![图片](https://pic3.zhimg.com/v2-0e1f104ca64ca00e6d1910d450e7a20a.jpg)

![图片](https://pic1.zhimg.com/v2-e1dc990eca24ed2f761dfd22971f4c14.jpg)

这个网站参见：[Delaunay & Voronoi](https://leotian123.github.io/maths/delaunay-voronoi/delaunay-voronoi.html)

这就定义了对偶元素，那么对偶元素的**度量**也就定义出来了，这才能继续定义霍奇星。也就是说，霍奇星的定义和度量选择是有关系的，类似地 $\delta = \star d \star$ 也是度量诱导出来的，他们不同于 $d$ 的含义是确定的。

$n$ 维霍奇星对应的那个矩阵记作 $\star_n$ ，是一个**对角矩阵**。既然对于 $n$ 维霍奇星作用在 $n$ 维的元素上，那么这东西的行列数量就是对应维度元素的数量，前三个维度就是 $V,E,F$ 。还有不要忘了书上这个定义：

$\star \alpha = \frac{|\sigma ^ \star|}{|\sigma|} \alpha$

那个 $\sigma$ 就是元素， $\sigma ^ \star$ 是对偶元素，双竖线是度量的意思。一个点的度量就是 $1$ 。

**（0）**对于 $\star _0$ ，这东西对应的矩阵对角元素是

$(\star _0)_{vv} = [毗邻面外心连线的面积]=[Voronoi多边形面积]$

右边这个多边形我们给它限制在mesh表面，也就是给面做一个弯折。所以这东西不是很好求，我们做一个工程近似，变为

$(\star _0)_{vv} = \frac{1}{3} \sum_{毗邻面}  [毗邻面的面积]$那么这就是选择了重心连线了。

**（1）**对于 $\star _1$ ，这东西对应的矩阵对角元素是

$(\star _1)_{ee} = \frac{[对偶边长]}{[本边长]}$ 

同样限制在mesh上，线有一个弯折。这就又回到了cotan定理，是 $\frac{1}{2}(cot\alpha+cot\beta)$ ，证明如下：

![图片](https://pic4.zhimg.com/v2-f1663677130cd2a3fcb558e7ea272c63.jpg)

也可以进行工程近似，变为两个三角形重心连线，这东西我们知道是两个三角形中另外两个点的连线长的三分之一。

**（2）**对于 $\star _2$ ，这东西对应的矩阵对角元素是

$(\star _2)_{ff} = \frac{1}{[本三角形面积]}$ 

4.8.3节提到了离散外导数的定义。不要忘了Stokes公式，在一些元素上 $d\alpha$ 的积分就是边界上 $\alpha$ 的积分。那么离散化说的就是一些元素上 $d\alpha$ 的和就是边界上 $\alpha$ 的和，那么**一个**（而不是一些）元素的 $d\alpha$ 的和，也就是 $d\alpha$ 自己，就是该要素边界上 $\alpha$ 的和。总结起来就是“**外导数等于边界积分/边界和**”。

那么这里如何单独表达 $d$ 的矩阵形式呢？首先我们知道二维流形上只有两个 $d$ ，也就是作用在边上的 $d_0$ ，和作用在面上的 $d_1$ 。那么

-   这个 $d_0$ 要指导边如何如何，乘在 $\alpha$ 左边，所以它的行数是 $E$ 。指导的是什么？是边对应操作了哪些点、是加上这个点的值、还是减去这个点的值，值在后面那个 $\alpha$ 给出。所以它应该具有 $V$ 列，且取值就是0（对应不操作这个点）、1（加上这个点的值）、-1（减去这个点的值）。 $E\times V$
-   这个 $d_1$ 要指导面如何如何，乘在 $\alpha$ 左边，所以它的行数是 $F$ 。指导的是什么？是面对应操作了哪些边、是加上这个边的值、还是减去这个边的值，值在后面那个 $\alpha$ 给出。所以它应该具有 $E$ 列，且取值就是0（对应不操作这个边）、1（加上这个边的值）、-1（减去这个边的值）。 $F\times E$

而且这个形状对应了之前结论，即d一个form会把这个form升一个维度。对应到形状，承接低维度的度量（V、E），输出高纬度的度量（E、F）。

我们知道另一个重要定理 $d^2=0$ ，那么矩阵形式应该有 $d_1d_0=0$ ，可以做一个代码正确性验证。

定向很重要，边定向和面定向都有。定向可以随便给，但是要全局固定。也就是说其实不用额外处理。

-   对于d0，头部设置为1，尾部设置为0（当然也可以反过来，只要全局一致）。
-   对于d1，边定向顺着面定向的，设置为1，边定向逆着面定向的，设置为0。

面定向我用的默认数据的方向；边定向我要求两个点中，左边点的索引小于右边点的索引。

来写一下这5个矩阵，在“operators.py”：

```python
from laplacian import *

def get_hodge_star_0(verts, adj_mat):
    vals = []
    rows = []
    cols = []

    V = len(verts)
    for i in range(V):
        rows.append(i)
        cols.append(i)

        total_area = 0
        link = get_link(adj_mat, i)
        link.append(link[0])
        for index_j in range(len(link) - 1):
            index_k = index_j + 1
            j = link[index_j]
            k = link[index_k]
            total_area += get_area(verts, i, j, k)
        vals.append(total_area / 3)

    return sp.csr_matrix((vals, (rows, cols)), shape=(V, V))

def get_hodge_star_1_old(verts, edges, edge_to_opposite):
    vals = []
    rows = []
    cols = []

    E = len(edges)
    for i, edge in enumerate(edges):
        rows.append(i)
        cols.append(i)

        opposite = edge_to_opposite[edge]

        if len(opposite) != 2:
            vals.append(1)
            continue

        length_self = np.linalg.norm(verts[edge[0]] - verts[edge[1]])
        length_dual = np.linalg.norm(verts[opposite[0]] - verts[opposite[1]]) / 3
        vals.append(length_dual / length_self)

    return sp.csr_matrix((vals, (rows, cols)), shape=(E, E))

def get_hodge_star_1(verts, edges, edge_to_opposite):
    vals = []
    rows = []
    cols = []

    E = len(edges)
    for i, edge in enumerate(edges):
        rows.append(i)
        cols.append(i)

        opposite = edge_to_opposite[edge]

        if len(opposite) != 2:
            vals.append(1)
            continue

        cot_alpha = get_angle_cot(verts, opposite[0], *edge)
        cot_beta = get_angle_cot(verts, opposite[1], *edge)

        vals.append(0.5 * (cot_alpha + cot_beta))

    return sp.csr_matrix((vals, (rows, cols)), shape=(E, E))

def get_hodge_star_2(verts, faces):
    vals = []
    rows = []
    cols = []

    F = len(faces)
    for i, face in enumerate(faces):
        rows.append(i)
        cols.append(i)
        vals.append(1 / get_area(verts, *face))

    return sp.csr_matrix((vals, (rows, cols)), shape=(F, F))

def get_d_0(E, V, edges):
    vals = []
    rows = []
    cols = []

    for i, edge in enumerate(edges):
        rows.append(i)
        cols.append(edge[0])
        vals.append(1)

        rows.append(i)
        cols.append(edge[1])
        vals.append(-1)

    return sp.csr_matrix((vals, (rows, cols)), shape=(E, V))

def get_d_1(F, E, faces, edges):
    vals = []
    rows = []
    cols = []

    for i, face in enumerate(faces):
        v0, v1, v2 = face

        for vi, vj in [(v0, v1), (v1, v2), (v2, v0)]:
            rows.append(i)
            if vi < vj:
                cols.append(edges.index((vi, vj)))
                vals.append(1)
            else:
                cols.append(edges.index((vj, vi)))
                vals.append(-1)

    return sp.csr_matrix((vals, (rows, cols)), shape=(F, E))
```

可以直接print(sp.linalg.norm(d1 @ d0))验证是不是等于0.

现在来写霍奇分解，别忘了这一页：

![图片](https://pic1.zhimg.com/v2-d87c13774aaec63fd1f4c2fb6a819080.jpg)

生成随机一个场，按照公式得到结果：

```python
d0 = get_d_0(E, V, edges) # (|E| × |V|)
d1 = get_d_1(F, E, faces, edges) # (|F| × |E|)

print(sp.linalg.norm(d1 @ d0))

star0 = get_hodge_star_0(verts, adj_mat)  # (|V| × |V|) diag
star1 = get_hodge_star_1(verts, edges, edge_to_opposite)  # (|E| × |E|) diag
star2 = get_hodge_star_2(verts, faces)  # (|F| × |F|) diag
star0_inv = sp.diags(1.0 / star0.diagonal())
star1_inv = sp.diags(1.0 / star1.diagonal())
star2_inv = sp.diags(1.0 / star2.diagonal())

omega = np.random.randn(E)

A = d0.T @ star1 @ d0          # (|V| × |V|)
b = d0.T @ star1 @ omega       # (|V|)
alpha = spla.spsolve(A, b)

A = d1 @ star1_inv @ d1.T     # (|F| × |F|)
b = d1 @ omega                # (|F|)
beta_tilde = spla.spsolve(A, b)
beta = star2_inv @ beta_tilde

grad_part = d0 @ alpha
curl_part = star1_inv @ d1.T @ star2 @ beta
gamma = omega - grad_part - curl_part

print("||γ|| =", np.linalg.norm(gamma))
print("||dγ|| =", np.linalg.norm(d1 @ gamma))
print("||δγ|| =", np.linalg.norm(star0_inv @ d0.T @ star1 @ gamma))
print("⟨dα, δβ⟩ =", grad_part.T @ star1 @ curl_part)
print("⟨dα, γ⟩ =", grad_part.T @ star1 @ gamma)
print("⟨δβ, γ⟩ =", curl_part.T @ star1 @ gamma)
```

这个还真得是spla.spsolve，不能是spla.cg，不太收敛。“稀疏对称正定”条件似乎满足啊...可能是这个正定没满足，不管它了。其实spsolve也挺快（似乎更快）。

这边是双甜甜圈的结果：

```text
||γ|| = 2.3175715480953243
||dγ|| = 2.0296402451682708e-12
||δγ|| = 3.331306069347086e-11
⟨dα, δβ⟩ = 7.105427357601002e-14
⟨dα, γ⟩ = 7.321920847402907e-14
⟨δβ, γ⟩ = 9.814371537686384e-13
```

$\gamma$ 确实无源无旋，三个分量确实正交。

第一条打印 $\gamma$ 本身是为了验证 $g=0$ 的mesh上面没有这个分量。这边拿一个兔子看看效果，确实如此：

```text
||γ|| = 1.883434515210402e-13
||dγ|| = 1.591345815740438e-13
||δγ|| = 6.776420223534135e-11
⟨dα, δβ⟩ = -1.509903313490213e-14
⟨dα, γ⟩ = -1.3902748235112737e-13
⟨δβ, γ⟩ = 1.7984222529540056e-13
```

还有就是这东西可以验证拉普拉斯矩阵。

我们知道 $\Delta = d\delta + \delta d$ ，我们要的是**作用到0-form的**拉普拉斯，那么我们只能先升维（ $d$ ）、再降维（ $\delta$ ），因为零维降维就没了，所以前面那一项没了。那么我们得到：

$L = \star_0^{-1}  d_0^T  \star_1 d_0$

不过呢，拉普拉斯这个东西，本书介绍的，其实是

$L =  d_0^T  \star_1 d_0$

本书的拉普拉斯，不除以自己的对偶面积。所以没有前面那一个霍奇星了。

可以代码验证：

```python
K_dec = - d0.T @ star1 @ d0
L = get_laplacian_matrix(verts, adj_mat)

f = np.random.randn(V)
print("compare K:", np.linalg.norm(K_dec @ f - L @ f))
print("compare K:", sp.linalg.norm(K_dec - L))
print("compare star0_inv @ K_dec:", np.linalg.norm((star0_inv @ K_dec) @ f - L @ f))
print("compare star0_inv @ K_dec:", sp.linalg.norm(star0_inv @ K_dec - L))
```

结果：

```text
compare K: 0.0
compare K: 0.0
compare star0_inv @ K_dec: 375621.45768633706
compare star0_inv @ K_dec: 371124.0514661404
```

### 2 后续内容速览

首先是第一同调群 $H_1$ 的生成元，可以看做是曲面上“本质不同的非平凡环路”。亏格为 $g$ 的封闭曲面，有 $2g$ 个同调生成元， $2g$ 个线性无关的调和1-form。

“本质不同的非平凡环路”直观看上去就是那种不能通过连续变化缩为一个点的环路。那么甜甜圈上可以看出来两个，这两个：

![图片](https://pic4.zhimg.com/v2-ad0d346749c7f4034fd28f35032880ad.jpg)

接下来有点意思了，来看双甜甜圈这四个容易想到：

![图片](https://pic3.zhimg.com/v2-84cea65985345112323d4831c3183f06.jpg)

这个呢？：

![图片](https://pic1.zhimg.com/v2-6dafd9b66f7447bf7f150c982adc4d82.jpg)

被看做是这两个的复合：

![图片](https://picx.zhimg.com/v2-f0577eba58a8075278c117a84aa9e759.jpg)

类似这个也是：

![图片](https://pica.zhimg.com/v2-50ce786d50f30d349d62b03229eb90bc.jpg)

还有别的。其实甜甜圈本身也可以复合：

![图片](https://pic3.zhimg.com/v2-909ab3fcabbc91d7dad86dab75562e9a.jpg)

下一节的算法就是告诉我们怎么找这个东西。大致意思是，我们可以做一颗生成树（tree），还可以做一颗对偶图形的生成树（cotree）。tree占据了 $V-1$ 个边，cotree占据了 $F-1$ 个边，剩下的边数量是

$E-(V-1)-(F-1) = 2-\chi=2g$ 

这 $2g$ 个边，每一个都对应了一个生成元，这个边加入到tree里，会得到唯一一个环路，生成元就是这个环路。

我让ai写了个代码，用pyvista可视化了一下，似乎有点问题..但是确实只有四个。

![图片](https://pic3.zhimg.com/v2-a492e2d3104bb62ceab4ba696a95f23a.jpg)

对应的1-form：

![图片](https://pic3.zhimg.com/v2-a870db205c6879e07175c1a4a04b2604.jpg)

这个其实对应了为啥没有亏格的图形的场没有调和分量。

下一节谈到了homology、connection相关的事情，和计算出来的生成元也有很大关系。给定一个connection，要检测这种不一致的现象存在与否：

![图片](https://pic1.zhimg.com/v2-59a75e976ee6773ab9e2aba7de193c4e.jpg)

检测方法大致情况：

![图片](https://pic2.zhimg.com/v2-671b8d272b313d69b9df2341dc883d25.jpg)

以上这个图跳了一个步骤，他说 $holonomy \equiv 0\ mod\  2\pi$ 。其实一开始我们的思路是 $holonomy  = 0 $ 的。

但是，这样子的话，由于高斯博内定理，这东西只能是一个甜甜圈...曲率和是一个 $0 $ 。

所以必须要引入奇点，奇点在积分时贡献非零曲率。同时允许holonomy是 $2 \pi$ 的倍数。假设这个倍数是 $k$ ，称作它的指数，那么 $\sum_{奇点} k(奇点) = \chi$

最后的目标是什么呢？看一下这一章的标题，向量场设计。最后的效果是，只要按照上面这个式子的要求，指定奇点以及它的指数，就会生成一个connection。再随便指定一个单位向量，这个场就按照connection建立起来了。

那么这东西纹理、毛发、流动等等图像的生成都可以用上。