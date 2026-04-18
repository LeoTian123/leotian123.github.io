# 第6章 拉普拉斯 The Laplacian

前文已经介绍，这东西最后结果和面积梯度就差了一个符号：

![图片](https://pic3.zhimg.com/v2-501e3e6bbd2242dad586fcbe7b9f0c9e.jpg)

请注意这个 $u$ 是点上的一个函数，这个函数可以不是实数，可以是奇奇怪怪的东西，所以他当然可以是三维数组——也就是说，它可以是点本身的三维坐标——这时候，拉普拉斯结果也是一个三维数组。那么，“自己和邻居的”差异就变为了**平滑程度**。而且，**拉普拉斯结果的方向指出了你应该向哪边移动，才能更加平滑，模长则告诉你移动的强度**。

我想我们还是先直观理解一下，通过两种我这边提供的方式。

1.  首先，拉普拉斯可以做平滑，也就是让点朝着邻居移动。这意味着什么？意味着**表面积的降低**。这就是为什么拉普拉斯结果和面积梯度符号相反。
2.  第二，还是通过图论进行理解。直觉上，离我越近的邻居应该对我影响大，离我远的邻居应该影响小。离得近或者远，通过其所对的角的大小进行表示，那么我们把它映射到一个指标上。$cot$ 是一个把 $[0,\pi]$ 映射到 $[\infty, -\infty]$ 的函数，就选它了。

然后我们通过数学的方法看一看更深刻的道理。

## 1 离散版的推导

其实就是找函数基，然后给函数做线性分解。这个线性空间的内积是这样的：

![图片](https://pic2.zhimg.com/v2-982f07f5816e29d279d38e2e7f014bb7.jpg)

![图片](https://picx.zhimg.com/v2-d2283e3597fc4087ea402dc66fa458db.jpg)

基是帽子函数：

![图片](https://pic2.zhimg.com/v2-3e06a392931fba350f8f4d713129ed5b.jpg)

这东西挺好的，把函数 $u$ 分解为了：

$u =\sum_i u_i \phi_i$ 

$\phi_i$ 是只在点 $i$ 取 $1$ 的基。 $u_i$ 说的是 $u$ 在 $i$ 的取值。然后吧，书上实在是高屋建瓴，ai指出这个过程其实就是：

![图片](https://pica.zhimg.com/v2-a31350e8e6bcb786a6e331806238d484.jpg)

![图片](https://pic2.zhimg.com/v2-3d1170d3edeb843ccc9fca20f8b4e6c1.jpg)

这就很简单了，而且我们还很顺利地得到一个矩阵：

![图片](https://picx.zhimg.com/v2-f3edfe0e2db77b932313633418754e4b.jpg)

下面求一下这个东西，帽子函数的梯度，是一个定值：

![图片](https://pic1.zhimg.com/v2-63aa8fa2b6644df4b20908776e8464ca.jpg)

然后是自己和自己的内积：

![图片](https://pic3.zhimg.com/v2-af26edfea91e69ddb7ed488066d02de6.jpg)

然后是两两内积：

![图片](https://pic1.zhimg.com/v2-044c243976282809d090243e96e388e6.jpg)

还是看一个点，即 $(\Delta u)_i$ ，有结果：

![图片](https://pica.zhimg.com/v2-e80ae5b5db0cca204d5a36fb6fd9fb4a.jpg)

这就给了cotan定理一个理论保证。

## 2 代码与可视化

先看一下这东西是不是表示了凹凸性，代码如下，在“laplacian.py”：

```python
from basictools import *
import scipy.sparse as sp

def get_angle_cot(verts, p, a, b):
    p, a, b = verts[p], verts[a], verts[b]
    pa = a - p
    pb = b - p

    # 计算叉积的模 (对应 sin) 和 点积 (对应 cos)
    pa_pb_cos = np.dot(pa, pb)
    pa_pb_sin = np.linalg.norm(np.cross(pa, pb))

    # 避免零向量导致的除以零错误
    if pa_pb_sin < 1e-12 and abs(pa_pb_cos) < 1e-12:
        return 0.0
    if pa_pb_sin < 1e-12:
        return float('inf') if pa_pb_cos > 0 else float('-inf')

    return pa_pb_cos / pa_pb_sin

def get_laplacian(verts, adj_mat, i):
    res = np.zeros(3, dtype=np.float32)
    link = get_link(adj_mat, i)
    for index_j in range(len(link)):
        index_prev = (index_j-1) % len(link)
        index_next = (index_j+1) % len(link)
        prev = link[index_prev]
        j = link[index_j]
        next = link[index_next]

        w = get_angle_cot(verts, prev, i, j) + \
            get_angle_cot(verts, next, i, j)
        res += w * (verts[j] - verts[i])
    return res / 2

def _get_link_fast(edge_to_opposite, adj_mat, p):
    res = []
    unordered_link = deepcopy(adj_mat[p])

    q = unordered_link.pop()
    res.append(q)

    nxt = edge_to_opposite[(min(p, q), max(p, q))][0]
    res.append(nxt)
    while unordered_link:
        unordered_link.remove(nxt)
        if not unordered_link:
            break
        for opposite in edge_to_opposite[(min(p, nxt), max(p, nxt))]:
            if opposite in unordered_link:
                nxt = opposite
        res.append(nxt)
    return res

def get_laplacians(verts, faces, adj_mat):
    n_verts = len(verts)
    laplacians = np.zeros((n_verts, 3), dtype=np.float32)

    # 预处理
    edge_to_opposite = get_edge_to_opposite(faces)

    for i in range(n_verts):
        res = np.zeros(3, dtype=np.float32)
        link = _get_link_fast(edge_to_opposite, adj_mat, i)
        n = len(link)

        for index_j in range(n):
            index_prev = (index_j - 1) % n
            index_next = (index_j + 1) % n
            prev = link[index_prev]
            j = link[index_j]
            next = link[index_next]

            w = get_angle_cot(verts, prev, i, j) + \
                get_angle_cot(verts, next, i, j)
            res += w * (verts[j] - verts[i])
        laplacians[i] = res / 2

    return laplacians

def get_laplacian_matrix(verts, adj_mat):
    vals = []
    rows = []
    cols = []

    V = len(verts)
    for i in range(V):
        link = get_link(adj_mat, i)
        w_sum = 0.0

        for index_j in range(len(link)):
            index_prev = (index_j - 1) % len(link)
            index_next = (index_j + 1) % len(link)
            prev = link[index_prev]
            j = link[index_j]
            next = link[index_next]

            w_ij = get_angle_cot(verts, prev, i, j) + \
                   get_angle_cot(verts, next, i, j)
            w_ij *= 0.5

            # 非对角项
            rows.append(i)
            cols.append(j)
            vals.append(w_ij)

            w_sum += w_ij

        # 对角项
        rows.append(i)
        cols.append(i)
        vals.append(-w_sum)

    L = sp.coo_matrix((vals, (rows, cols)), shape=(V, V))

    # 确认对称 是一种优化
    L = 0.5 * (L + L.T)

    return L.tocsr()
```

请注意这个get\_angle\_cot()，这东西稳定写法就是点积除以叉积模，不要 $cot(arccos(x)) = \pm \frac{\sqrt{1-x^2}}{x}$ 。

颜色这样准备，用到了一个粗糙的点法线判断内外：

```python
laplacians = get_laplacians(verts, faces, adj_mat)

scale = np.empty(len(verts), dtype=np.float32)

# 1. 先计算面法线，再平均得到顶点法线
def get_vertex_normals(verts, faces):
    v_normals = np.zeros_like(verts)
    for f in faces:
        v0, v1, v2 = verts[f]
        # 叉积得到面法线
        face_normal = np.cross(v1 - v0, v2 - v0)
        # 累加到三个顶点上（可以按面积加权，这里简化处理）
        v_normals[f] += face_normal

    # 归一化
    norms = np.linalg.norm(v_normals, axis=1, keepdims=True)
    return v_normals / (norms + 1e-9)
vertex_normals = get_vertex_normals(verts, faces)

# 2. 判断方向
for p in range(len(verts)):
    scale[p] = np.linalg.norm(laplacians[p])
    # 如果拉普拉斯向量与法线方向相反（点积为负），则设为负值
    if np.dot(laplacians[p], vertex_normals[p]) < 0:
        scale[p] *= -1

scale_abd_max = np.abs(scale).max()
normed_scale = scale / scale_abd_max
def blue_gray_red(t):
    if t < 0:
        a = -t
        return (0.5-0.5*a, 0.5-0.5*a, 0.5+0.5*a)
    else:
        a = t
        return (0.5+0.5*a, 0.5-0.5*a, 0.5-0.5*a)
colors = np.array([blue_gray_red(t) for t in normed_scale], dtype=np.float32)
```

看一下石像鬼，确实蓝色是突出的，红色是凹陷的：

![图片](https://pica.zhimg.com/v2-a10a33a2ff6d5a76fd985ccb3e12afbe.jpg)

和

![图片](https://pic4.zhimg.com/v2-921392e2a75b4647e4498d6714f7e111.jpg)

小猫：

![图片](https://pic1.zhimg.com/v2-ca534c2f01b164238b05db01968bf214.jpg)

## 3 拉普拉斯平滑

其实就是扩散方程，下一步等于这一步加上扩散强度乘以拉普拉斯。有前向和后向，也分别叫显式和隐式：

![图片](https://pic2.zhimg.com/v2-0564288ef9341509a3079e18e1b081bb.jpg)

前向欧拉不稳定，如果不去每步迭代修改最新的拉普拉斯，效果会很差。如果每一步修改拉普拉斯，那么结果还是可以的，但是会奇慢无比。后向则一直用老的，又快效果又好。为什么？涉及矩阵论的知识，ai这里有个说明：

![图片](https://pic3.zhimg.com/v2-da5488b8ab8534eb8ba858a5104d459a.jpg)

![图片](https://pica.zhimg.com/v2-4ba130201cb5ba46cdfbbbbd7f52ecd2.jpg)

前向我实现两种，后向只有一种，第二个其实是快速版本，预先做一个矩阵分解：

```python
def forward_euler_smooth_stable(verts, adj_mat, steps=50, lam=0.1):
    v = verts.copy()
    for i in tqdm(range(steps), desc="Forward Euler Smooth"):
        lplc = get_laplacians(v, faces, adj_mat)
        v = v + lam * lplc
    return v

def forward_euler_smooth_origin(verts, adj_mat, steps=50, lam=0.1):
    v = verts.copy()
    laplacians = get_laplacians(v, faces, adj_mat)

    for i in tqdm(range(steps), desc="Forward Euler Smooth"):
        v = v + lam * laplacians

    return v

def backward_euler_smooth(verts, adj_mat, steps=10, lam=0.1):
    v = verts.copy()
    L = get_laplacian_matrix(v, adj_mat)
    n = L.shape[0]
    I = sp.eye(n)
    A = I - lam * L

    for _ in tqdm(range(steps)):
        v_new = np.zeros_like(v)
        for d in range(3):
            v_new[:, d] = sp.linalg.spsolve(A, v[:, d])
        v = v_new

    return v

def backward_euler_smooth_fast(verts, adj_mat, steps=10, lam=0.1):
    v = verts.copy()
    L = get_laplacian_matrix(v, adj_mat)
    n = L.shape[0]
    I = sp.eye(n)
    A = (I - lam * L).tocsc()
    solver = sp.linalg.factorized(A)

    for _ in tqdm(range(steps)):
        for d in range(3):
            v[:, d] = solver(v[:, d])

    return v
```

这是前向20步不每次计算新拉普拉斯的效果，这就叫所谓“不稳定”：

![图片](https://pic4.zhimg.com/v2-d4c3c4290c34e6962b07d1eb6dddf08f.jpg)

更多步数会特别吓人，这里不放了。

这是20步每次计算新拉普拉斯的效果，很慢，效果好多了：

![图片](https://pic2.zhimg.com/v2-f1ad838d6b318d6ecd42b911708f0349.jpg)

![图片](https://pic1.zhimg.com/v2-32adb12937eaeaab8263b89c6dbd7166.jpg)

但是太慢了好几分钟：

![图片](https://pic2.zhimg.com/v2-869d775bdd987d402d3ae461279f8149.jpg)

这是20步后向：

![图片](https://picx.zhimg.com/v2-b1ad41f583aca9bbbe16b0a4416075d7.jpg)

速度直接起飞了...：

![图片](https://pic4.zhimg.com/v2-a9acdabe1f30b129465d31616a54df73.jpg)

我还让ai给了一个“62-拉普拉斯平滑-2.py”，这东西滚轮控制迭代步数，效果非常赞！

![图片](https://pic4.zhimg.com/v2-ab555fe3d80f355bc94654e668efc273.jpg)

![图片](https://pic4.zhimg.com/v2-45cb8b32c09fc7d4ce5b5eb078f96273.jpg)

![图片](https://pic4.zhimg.com/v2-bfac6b7076d8e0830444a87bbe8f33bd.jpg)

![图片](https://picx.zhimg.com/v2-4a63fdbb930d7fe0c024f060ab7d61b1.jpg)

另外，以上图的染色都是当时图形的拉普拉斯结果。

拉普拉斯先到这里。