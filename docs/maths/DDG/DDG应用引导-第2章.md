# 第2章 组合曲面 Combinatorial Surfaces

## 1 关于欧拉-庞加莱公式

欧拉-庞加莱公式：

$V-E+F=2-2g$

有好几个习题，差不多一个意思。valence其实就是度。假设平均度是 $x$ ，那么对于二维simplicial surface（后文直接叫mesh或者三角形mesh）有

$\frac{xV}{3} = \frac{2E}{3} = F$ 

这个可以解决好几个题：

![图片](https://pic3.zhimg.com/v2-7c85a56b2c091639e8ab7511a9c80540.jpg)

这个题说的就是 $x=6$ 的情况，有 $V-E+F=V-3V+2V=0=2-2g$ ，所以 $g=1$ 。

![图片](https://pic1.zhimg.com/v2-062e852efa2c101341af45005d190b52.jpg)

假设regular的点 $n$ 个，irregular的点 $m$ 个，irregular的点平均valence是 $x$ ，那么上面公式就是

$\frac{6n+xm}{3} = \frac{2E}{3} = F$ 

$V-E+F=2-2g$ 整理一下是

$m = \frac{2-2g}{1-\frac{x}{6}}$

我们发现很神奇，和regular的点没有关系。 

$m \geq 0$ ，一个正整数，求这个东西最小值。

-   $g=0$ ， $x $ 越小 $m$ 越小，不要忘了 $x$ 的意义， $x$ 最小是 $3$ ，整个图形也就是一个四面体。
-   $g=1$ 就是 $0$ 了。
-   $g\geq2$ ，一个负数除以 $6-x$ ， $x$ 可以很大使得这个东西作为一个正数很小，但是最小的只能是 $1 $ ，那就是 $1$ 了。

对于regular这个概念最重要的可能是这个习题：

![图片](https://pic4.zhimg.com/v2-e2060787c786915417961659695a722f.jpg)

这很显然， $\frac{xV}{3} = \frac{2E}{3} = F$ ，那么 $V-E+F=V-\frac{x}{2}V+\frac{x}{3}V =2-2g$ ，两边除以 $V$ 得到 $1-\frac{x}{2}+\frac{x}{3}=\frac{2-2g}{V}$ $V$ 趋于无穷大， $x$ 趋于 $6$ 。也就是说无限细的三角mesh上，每个点都是regular的。那么我们知道一个正三角形密铺中，每个三角形正好也是regular的，这里有一种对应。

关于其他种类的mesh的证明这里不写了，后面用不到。

## 2 关于link的实现

这一章我没按照他练习里说的写代码，练习里很多东西后来没用上。但是一个basictools.py还是必要的，详见仓库。

后来写拉普拉斯的时候，发现link还是得专门写一下。这东西值得说一下，对于单点link，我用的是：

```python
def get_link(adj_mat, p):
    res = []
    unordered_link = deepcopy(adj_mat[p])

    q = unordered_link.pop()
    res.append(q)

    # ... --- last --- q=first --- next=second --- ...
    # second, last = list(unordered_link & adj_mat[q])

    nxt = list(unordered_link & adj_mat[q])[0]
    res.append(nxt)
    try:
        while unordered_link:
            unordered_link.remove(nxt)
            if not unordered_link:
                break
            nxt = list(unordered_link & adj_mat[nxt])[0]
            res.append(nxt)
        return res
    except Exception as e:
        return res
```

这个try-except其实没必要加，如果数据良好，不会进入except。我这边有一个数据后来发现有点问题就加上了。

那么这个东西由于计算了集合的交集，假设平均度是 $x$ ，单点复杂度是 $O(x^2)$ ，整个mesh上就是 $O(Vx^2)$ 。

也可以预处理一下，得到一个edge到面上另一个点的映射，数据良好的话每个edge当然是有两个对面点。预处理过程是一个 $O(F)$ ，单点复杂度变为了 $O(2x)$ ，假设两个过程计算量相当，整个mesh上就是 $O(F+2Vx)$ ，而 $3F=xV$ ，也就是 $O(Vx)$ ，只能说是稍微变快了一点点，意义不是很大。

```python
def get_edge_to_opposite(faces):
    edge_to_opposite = defaultdict(list)

    for v0, v1, v2 in faces:
        v0, v1, v2 = sorted([v0, v1, v2])
        edge_to_opposite[(v0, v1)].append(v2)
        edge_to_opposite[(v0, v2)].append(v1)
        edge_to_opposite[(v1, v2)].append(v0)

    return edge_to_opposite

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
```