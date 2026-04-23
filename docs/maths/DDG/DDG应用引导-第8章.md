## 0 一个基本观点与相关算子

一个连续事物的函数，存不下所有值。然而，一个离散事物的函数，可以存下。假设班里每一个同学具有一个固定顺序，那么从人类到数字的一个函数，就可以表示为一个向量，同学在这个固定顺序的位置作为这个向量的索引值。

其实这没什么难以理解了，我们就是用一个列表/数组存储数列的，当然矩阵也是。只是说，这些东西有个“自然顺序”，有些事物则没有。

所以，点的函数（0-form）、边的函数（1-form）、面的函数（2-form）都可以用一个向量进行表示——**离散的函数，在自变量固定顺序的要求下，可以表示为一个向量**。

函数的变化，就变为了一些矩阵——微分、霍奇星，都是矩阵——它们作用在一个向量上。

这个观点还是比较伟大的，图论中也是这么干的，固定点的某种顺序，那么点上函数就是一个向量，函数的变化（例如图上拉普拉斯）就是一个矩阵。

之后出现了这样一页，不用理解意义，就关注微分和霍奇星从连续到离散的处理：

![图片](https://pic1.zhimg.com/v2-d87c13774aaec63fd1f4c2fb6a819080.jpg)

微分和霍奇星是可以用在随便一个form上的，那么这里就有具体含义的问题，这两个东西抽象能力太强了，编程的时候就得变成多个。那么这三个 $\star$ ，两个 $d$ 具体是什么呢？这就用到了第4章的知识。

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

$(\star _0)_{vv} = \frac{1}{3} \sum_{毗邻面}  [毗邻面的面积]$

那么这就是选择了重心连线了。

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
@property
    def star_0(self):
        if self._star_0 is None:
            vals = []
            rows = []
            cols = []

            for i in range(self.V):
                rows.append(i)
                cols.append(i)

                total_area = 0.0
                link = self._get_link_fast(i)
                link.append(link[0])
                for index_j in range(len(link) - 1):
                    j = link[index_j]
                    k = link[index_j + 1]
                    total_area += self.get_area(i, j, k)
                vals.append(total_area / 3)

            self._star_0 = sp.csr_matrix((vals, (rows, cols)), shape=(self.V, self.V))

        return self._star_0

    @property
    def star_1(self):
        if self._star_1 is None:
            vals = []
            rows = []
            cols = []

            for i, edge in enumerate(self.edges):
                rows.append(i)
                cols.append(i)

                opposite = self.edge_to_opposite[edge]

                if len(opposite) != 2:
                    vals.append(1)
                    continue

                cot_alpha = self.get_angle_cot(opposite[0], *edge)
                cot_beta = self.get_angle_cot(opposite[1], *edge)
                vals.append(0.5 * (cot_alpha + cot_beta))

            self._star_1 = sp.csr_matrix((vals, (rows, cols)), shape=(self.E, self.E))

        return self._star_1

    @property
    def star_2(self):
        if self._star_2 is None:
            vals = []
            rows = []
            cols = []

            for i, face in enumerate(self.faces):
                rows.append(i)
                cols.append(i)
                vals.append(1 / self.get_area(*face))

            self._star_2 = sp.csr_matrix((vals, (rows, cols)), shape=(self.F, self.F))

        return self._star_2

    @property
    def d_0(self):
        if self._d_0 is None:
            vals = []
            rows = []
            cols = []

            for i, edge in enumerate(self.edges):
                rows.append(i)
                cols.append(edge[0])
                vals.append(1)

                rows.append(i)
                cols.append(edge[1])
                vals.append(-1)

            self._d_0 = sp.csr_matrix((vals, (rows, cols)), shape=(self.E, self.V))

        return self._d_0

    @property
    def d_1(self):
        if self._d_1 is None:
            vals = []
            rows = []
            cols = []

            for i, face in enumerate(self.faces):
                v0, v1, v2 = face

                for vi, vj in [(v0, v1), (v1, v2), (v2, v0)]:
                    rows.append(i)
                    if vi < vj:
                        cols.append(self.edge_to_index[(vi, vj)])
                        vals.append(1)
                    else:
                        cols.append(self.edge_to_index[(vj, vi)])
                        vals.append(-1)

            self._d_1 = sp.csr_matrix((vals, (rows, cols)), shape=(self.F, self.E))

        return self._d_1
```

可以直接print(sp.linalg.norm(d1 @ d0))验证是不是等于0.


## 1 霍奇分解

![图片](https://pic3.zhimg.com/v2-58c269f5ec1ceaff5bb95dffc396d412.jpg)

链复形相关的理论不多说了，那么霍奇分解数学上的表述还是比较复杂的：

![图片](https://pic4.zhimg.com/v2-af73e05ddf5c038e67e2bee86f22ac0f.jpg)

![图片](https://pic2.zhimg.com/v2-175d416eb8cf58aef73a936c2e55a9df.jpg)

看最后的表述，对应到二维流形上的向量场，就是说：

![图片](https://pica.zhimg.com/v2-817f579a2df6f7e902531453eaf68d04.jpg)

那么怎么求解导出了梯度部分的 $\alpha$ 以及导出了旋度部分的 $\beta$ 呢？看这一页就行了：

![图片](https://pica.zhimg.com/v2-2fce9370884841cdbee17d3e5574ec58.jpg)

就是把外代数上的理论离散化。请注意这个 $\delta$ 的离散化有两种情况一种是 $\star_0^{-1} d_0 ^T \star_1$ ，另一种是 $\star_1^{-1} d_0 ^T \star_2$ 。怎么理解呢？首先熟悉的定义是 $\delta = \star d \star$ ，有定理：

![图片](https://pic3.zhimg.com/v2-27593d8aacc08bab47bf04510b780b34.jpg)

内积是：

![图片](https://pica.zhimg.com/v2-85b7e309f440a13b6e43728515dbb80a.jpg)

就可以得到这个结果：

![图片](https://pic3.zhimg.com/v2-87255bb5ad52323908c85d514b98275a.jpg)

现在来写霍奇分解，生成随机一个场，按照公式得到结果：

```python
from closed_surface import *
from pyvista_wrapped import *

cs = ClosedSurface('input/double-torus.obj')

d0 = cs.d_0  # (|E| × |V|)
d1 = cs.d_1  # (|F| × |E|)
star0 = cs.star_0  # (|V| × |V|) diag
star1 = cs.star_1  # (|E| × |E|) diag
star2 = cs.star_2  # (|F| × |F|) diag
star0_inv = sp.diags(1.0 / star0.diagonal())
star1_inv = sp.diags(1.0 / star1.diagonal())
star2_inv = sp.diags(1.0 / star2.diagonal())

print("||d^2|| =", sp.linalg.norm(d1 @ d0))

L_by_operators = - d0.T @ star1 @ d0
L = cs.laplacian_matrix

print("compare d0.T @ star1 @ d0:", sp.linalg.norm(L_by_operators - L))
print("compare star0_inv @ d0.T @ star1 @ d0:", sp.linalg.norm(star0_inv @ L_by_operators - L))

omega = np.random.randn(cs.E)

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

form_1_list = [omega, grad_part, curl_part, gamma]
pyvista_multiple_edge_1_forms(cs.verts, cs.faces, cs.edges, form_1_list)
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

可视化直接用写好的模版函数：

```python
form_1_list = [omega, grad_part, curl_part, gamma]
pyvista_multiple_edge_1_forms(verts, faces, edges, form_1_list)
```

兔子结果，随机杂乱的场：

![图片](https://picx.zhimg.com/v2-9471840c0da5e05deb1ef8029422448b.jpg)

梯度部分：

![图片](https://pic2.zhimg.com/v2-172bbc0fe26e764f7292c970c68cd14d.jpg)

放大看一下表面：

![图片](https://pic4.zhimg.com/v2-ee3384640a86d9fae6d4d5efc7a7a769.jpg)

旋量部分：

![图片](https://pic3.zhimg.com/v2-f7a92304e942386af36b813aa1f1d072.jpg)

调和部分非常非常小，兔子这个规模的可视化都看不见。

这里看一下soccerball.obj的，请注意这东西的 $\chi=-60$ ，三个分量的大小对比：

![图片](https://pic2.zhimg.com/v2-7547253bcb6fdf7e5f81c90d4fbdf86d.jpg)

还有就是这东西可以验证拉普拉斯矩阵。

我们知道 $\Delta = d\delta + \delta d$ ，我们要的是**作用到0-form的**拉普拉斯，那么我们只能先升维（ $d$ ）、再降维（ $\delta$ ），因为零维降维就没了，所以前面那一项没了。那么我们得到：

$L = \star_0^{-1}  d_0^T  \star_1 d_0$

不过呢，拉普拉斯这个东西，本书介绍的，其实是

$L =  d_0^T  \star_1 d_0$

本书的拉普拉斯，不除以自己的对偶面积。所以没有前面那一个霍奇星了。

可以代码验证：

```text
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

  

## 2 generators的求解与调和基

generators是第一同调群 $H_1$ 的生成元，可以看做是曲面上“本质不同的非平凡环路”。亏格为 $g$ 的封闭曲面，有 $2g$ 个同调生成元， $2g$ 个线性无关的调和1-form。

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

当然也可以自己复合自己：

![图片](https://pic2.zhimg.com/v2-812c62ef0f933f0db6686f5ba0137123.jpg)

使用tree-cotree算法找这些东西。

![图片](https://picx.zhimg.com/v2-d11e6f2186242a4b7eccfd96f7122379.jpg)

大致意思是，我们可以做一颗生成树（tree），还可以做一颗对偶图形的生成树（cotree），要求两个树的边不能交叉。tree占据了 $V-1$ 个边，cotree占据了 $F-1$ 个边，剩下的边数量是

$E-(V-1)-(F-1) = 2-\chi=2g$ 

这 $2g$ 个对偶边，每一个都对应了一个生成元，这个对偶边加入到cotree里，会得到唯一一个环路，生成元就是这个环路。注意是对偶边，这个环路是面的列表。

![图片](https://pic2.zhimg.com/v2-ddf9c5571d2b7d633f786e342ad2fe6f.jpg)

这个东西图片看不出来，即便这样大伙看出第一个似乎有点奇怪，不过应该没问题，线性无关还是保证了，因为：

-   第一个似乎不是“最简形式”，似乎是“上大+下大+下小”的复合，
-   第二个是“上小”，
-   第三个是“上大”
-   第四个是“下小”

这个甜甜圈就很好：

![图片](https://pic2.zhimg.com/v2-ae72524a4cb63275f4ed209418fa281d.jpg)

  

小猫也是：

![图片](https://pic4.zhimg.com/v2-add227bae2d7faae4eb01bbac3519497.jpg)

代码，都是经典算法：

```python
def get_generators(self, root=0, co_root=0):
        if not (0 <= root < self.V):
            raise IndexError(f"root index out of bounds: {root}")
        if not (0 <= co_root < self.F):
            raise IndexError(f"co_root index out of bounds: {co_root}")

        # cotree
        covertex_visited = [False] * self.F  # covertex is just face
        cotree_edges = set()

        q = deque([co_root])
        covertex_visited[co_root] = True

        while q:
            f = q.popleft()
            for neighbor in self.co_adj_mat[f]:
                if not covertex_visited[neighbor]:
                    covertex_visited[neighbor] = True
                    cotree_edges.add((min(f, neighbor), max(f, neighbor)))
                    q.append(neighbor)

        # tree的边不能和cotree的对偶边交叉，即对偶回来不能相同
        edge_selected = [self.dual_edge_to_edge[dual_edge] for dual_edge in list(cotree_edges)]
        edge_selected = set(edge_selected)

        # tree
        vertex_visited = [False] * self.V  # vertex is just vertex
        tree_edges = set()

        q = deque([root])
        vertex_visited[root] = True

        while q:
            v = q.popleft()
            for neighbor in self.adj_mat[v]:
                current_edge = (min(v, neighbor), max(v, neighbor))
                if current_edge not in edge_selected:
                    if not vertex_visited[neighbor]:
                        vertex_visited[neighbor] = True
                        tree_edges.add(current_edge)
                        q.append(neighbor)

        # 得到剩余边
        all_edge_selected = edge_selected | tree_edges
        left_edges = list(set(self.edges) - all_edge_selected)
        left_dual_edges = [self.edge_to_dual_edge[edge] for edge in left_edges]

        # 构建cotree的邻接表
        cotree_adj_mat = defaultdict(set)
        for dual_edge in cotree_edges:
            f0, f1 = dual_edge
            cotree_adj_mat[f0].add(f1)
            cotree_adj_mat[f1].add(f0)

        # 经典算法题，其实就是图中寻路
        def get_generator(left_dual_edge):
            (u, v) = left_dual_edge

            parent = dict()  # parent[x] = x 在 BFS/DFS 树中的父节点
            visited = set()
            stack = [u]
            visited.add(u)
            parent[u] = None

            # 在树里找 u 到 v 的路径
            while stack:
                x = stack.pop()
                if x == v:
                    break
                for y in cotree_adj_mat[x]:
                    if y not in visited:
                        visited.add(y)
                        parent[y] = x
                        stack.append(y)

            # 回溯 v -> u
            path = []
            cur = v
            while cur is not None:
                path.append(cur)
                cur = parent[cur]

            path.append(v)
            return path

        generators = []
        for left_dual_edge in left_dual_edges:
            generators.append(get_generator(left_dual_edge))

        return generators
```

对应的1-form：

![图片](https://pic3.zhimg.com/v2-a870db205c6879e07175c1a4a04b2604.jpg)

这个其实对应了为啥没有亏格的图形的场没有调和分量。代码如下：

```python
def order_of_dual_edge(self, edge):
        two_neighbor_faces = self.edge_to_dual_edge[edge]
        a_neighbor_face = two_neighbor_faces[0]
        a, b, c = self.faces[a_neighbor_face]
        u, v = edge

        if (a, b) == (u, v) or (b, c) == (u, v) or (c, a) == (u, v):
            left_face = a_neighbor_face
            right_face = two_neighbor_faces[1]
        else:
            left_face = two_neighbor_faces[1]
            right_face = a_neighbor_face

        return left_face, right_face    

    def get_harmonic_bases(self, generators):
        omegas = []
        for generator in generators:
            omega = np.zeros(self.E)
            for u, v in pairwise(generator):
                # u, v：path order
                order_by_indices = (min(u, v), max(u, v))  # to find corresponding edge
                edge = self.dual_edge_to_edge[order_by_indices]

                index_dual_edge = self.dual_edge_to_index[order_by_indices]

                left_face, right_face = self.order_of_dual_edge(edge)
                if left_face == u:
                    omega[index_dual_edge] = 1
                else:
                    omega[index_dual_edge] = -1

            omegas.append(omega)

        d0 = self.d_0
        star1 = self.star_1

        gammas = []
        for omega in omegas:
            A = d0.T @ star1 @ d0  # (|V| × |V|) , namely laplacian
            b = d0.T @ star1 @ omega  # (|V|) , namely co-differential
            alpha = spla.spsolve(A, b)
            gamma = omega - d0 @ alpha
            gammas.append(gamma)

        return gammas, omegas
```

看着简单，关于定向其实还挺麻烦的...我们的edge是按照索引序定向的，这边dual edge我不太清楚能不能随意指定，我这边指定的顺序是我们面向edge指向的方向，然后**左边的面指向右边的面**。

双甜甜圈，正确性验证与绘图：

```python
print('关于omega是closed的：')
for omega in omegas:
    print("||d omega|| =", np.linalg.norm(d1 @ omega))
print('关于gamma是harmonic的：')
for gamma in gammas:
    print("||dγ|| =", np.linalg.norm(d1 @ gamma))
    print("||δγ|| =", np.linalg.norm(star0_inv @ d0.T @ star1 @ gamma))

pyvista_multiple_edge_1_forms(verts, faces, edges, gammas, factor=3)
```

验证：

![图片](https://picx.zhimg.com/v2-ae1dda34ee09bd61ebd0537a2afa7d8f.jpg)

图：

![图片](https://pic4.zhimg.com/v2-c8b31b5a64c6ab86772516af5a2d2783.jpg)

![图片](https://pic2.zhimg.com/v2-0c3ee4cb1fac381741838882fc6acb43.jpg)

![图片](https://pic4.zhimg.com/v2-c304e5112926d09cd6f46b19afb89bd1.jpg)

![图片](https://pica.zhimg.com/v2-0e9fb0a498526732da1efbb3aeef2ea8.jpg)

可以看到后三个对应了“上上下”，相比第一个减去后三者的线性组合会得到看起来干净一些的一个“下”，事实上确实如此：

![图片](https://pic4.zhimg.com/v2-2990aba4662f3d6a962fa22b182d480b.jpg)

还有一件事，验证这些基的线性无关的一个方法，是看矩阵 $P$ 是不是满秩：

```python
P = cs.get_P(generators, gammas)
print('关于gammas是线性无关的：')
print("2g =", len(generators))
if P.shape == (0, 0):
    print("rank(P) = 0")
else:
    print("rank(P) =", np.linalg.matrix_rank(P))
```

矩阵 $P$ ：

```python
def get_P(self, generators, gammas):
        two_g = len(generators)
        P = np.zeros(shape=(two_g, two_g))
        for i in range(two_g):
            for j in range(two_g):
                P[i, j] = self.integral_dual_path_dual_1_form(generators[i], gammas[j])
        return P
```

会得到这样的结果：

```text
关于gammas是线性无关的：
2g = 4
rank(P) = 4
```

其中这个线积分：

```python
def integral_dual_path_dual_1_form(self, dual_path, dual_1_form):
        res = 0
        for u, v in pairwise(dual_path):
            # u, v：path order
            order_by_indices = (min(u, v), max(u, v))  # to find corresponding edge
            edge = self.dual_edge_to_edge[order_by_indices]

            index_dual_edge = self.dual_edge_to_index[order_by_indices]

            left_face, right_face = self.order_of_dual_edge(edge)

            if left_face == u:
                sign = 1
            else:
                sign = -1

            res += sign * dual_1_form[index_dual_edge]
        return res
```

一定要注意线积分关于对偶边的顺序。

  

## 3 求解connection

老算法：

![图片](https://picx.zhimg.com/v2-961ff708a19e3942371518ccdaed9487.jpg)

我们用的是：

![图片](https://pic3.zhimg.com/v2-be1e413156de5c60fb010bf8e7df0c9e.jpg)

这东西经过推导继续化简，说白了就是我们让梯度部分为零，只有后两个部分贡献力量：

![图片](https://picx.zhimg.com/v2-472adc2be5c5aa93a963ec2f638c7823.jpg)

证明：

-   梯度部分、旋度部分、调和部分是正交的， $\phi$ 范数平方就是这三个部分的范数平方和。
-   第一个约束中， $d$ 分配进去， $d^2=0$ ，梯度部分没了， $d$ 调和部分，也没了。
-   第二个约束中，积分分配进去，梯度部分的环路积分，由于Stokes公式，没了。
-   也就是说两个约束都约束不到梯度部分，既然要最小，直接让梯度部分为0，得证。

那么求解算法是：

![图片](https://pic3.zhimg.com/v2-ba72a391cb075fc05960042f22781596.jpg)

其中，矩阵 $P$

![图片](https://picx.zhimg.com/v2-d7da71250338a513d25053014ef720cb.jpg)

求解 $\gamma $

![图片](https://pic1.zhimg.com/v2-509c1c7542a19ed5cbf1b2587dbf4d64.jpg)

现在来写一下这个东西。

函数前半部分求解 $\delta \beta$ ，后半部分求解 $\gamma$ ：

```python
def get_trivial_connection(self, generators, gammas, point_indices, singularity_type_input):

        two_g = len(generators)
        euler_chi = 2 - two_g

        if sum(singularity_type_input) != euler_chi:
            raise ValueError("sum(singularity_type_input) != euler_chi")

        singularity_type = np.zeros(self.V)
        singularity_type[point_indices] = singularity_type_input

        d0 = self.d_0
        d1 = self.d_1
        star0 = self.star_0
        star1 = self.star_1
        star2 = self.star_2

        u = - self.angle_defects + 2 * pi * singularity_type

        A = d0.T @ star1 @ d0  # (|V| × |V|)
        b = u  # (|V|)
        beta_tilde = spla.spsolve(A, b)
        delta_beta = star1 @ d0 @ beta_tilde

        if two_g == 0:
            phi = delta_beta

        else:
            v_tilde = np.zeros(two_g)
            for i in range(two_g):
                vi = self.get_holonomy_of_levi_civita_connection_on_generator(generators[i])
                v_tilde[i] = vi - self.integral_dual_path_dual_1_form(generators[i], delta_beta)

            P = self.get_P(generators, gammas)
            z = np.linalg.lstsq(P, v_tilde, rcond=None)[0]

            gammas_arr = np.array(gammas)
            harmonic = z @ gammas_arr

            phi = delta_beta + harmonic

        return phi, delta_beta
```

这个vi是一个额外约束，是Levi Civita connection在generators上的holonomy。这东西我让ai写的，有点复杂：

```python
def get_holonomy_of_levi_civita_connection_on_generator(self, generator):
        """ This function is implemented by AI. """

        if len(generator) < 2:
            return 0.0

        def _normalize(x, eps=1e-12):
            n = np.linalg.norm(x)
            if n < eps:
                return x.copy()
            return x / n

        def _rotate_about_axis(v, axis, angle):
            # Rodrigues formula, axis must be unit
            c = math.cos(angle)
            s = math.sin(angle)
            return (
                    v * c
                    + np.cross(axis, v) * s
                    + axis * np.dot(axis, v) * (1 - c)
            )

        # ---- choose an initial tangent vector on the first face ----
        f0 = generator[0]
        n0 = _normalize(self.get_normal(*self.faces[f0]))

        # pick one edge direction in the first face as initial tangent vector
        a, b, c = self.faces[f0]
        w0 = self.verts[b] - self.verts[a]
        w0 = w0 - np.dot(w0, n0) * n0
        w0 = _normalize(w0)

        w = w0.copy()

        # ---- parallel transport the SAME vector across each adjacent face pair ----
        for u, v in pairwise(generator):
            order_by_indices = (min(u, v), max(u, v))
            edge = self.dual_edge_to_edge[order_by_indices]

            # shared primal edge direction
            axis = self.verts[edge[1]] - self.verts[edge[0]]
            axis = _normalize(axis)

            n_u = _normalize(self.get_normal(*self.faces[u]))
            n_v = _normalize(self.get_normal(*self.faces[v]))

            # signed angle rotating normal_u to normal_v around the shared edge axis
            phi = math.atan2(
                np.dot(axis, np.cross(n_u, n_v)),
                np.dot(n_u, n_v)
            )

            # transport the vector by rotating it around the shared edge
            w = _rotate_about_axis(w, axis, phi)

            # numerical cleanup: re-project to the tangent plane of face v
            w = w - np.dot(w, n_v) * n_v
            w = _normalize(w)

        # ---- compare final vector with initial vector in the initial tangent plane ----
        w = w - np.dot(w, n0) * n0
        w = _normalize(w)

        holonomy = math.atan2(
            np.dot(n0, np.cross(w0, w)),
            np.dot(w0, w)
        )

        return holonomy
```

关于 $\phi$ 和其生成的向量场的可视化见前面的总览吧。phi生成向量场的代码来自ai，这里不放了。