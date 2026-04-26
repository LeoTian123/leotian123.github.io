# DDG-应用引导-拾遗

本文内容则是对另外一些离散微分几何的常见话题进行补充与拾遗。

## 一、保持体积的平滑变化

原图：

![图片](https://pic4.zhimg.com/v2-904031a790a9542df0218cf51e55b023.jpg)

为了便于理解，我们使用这个稳定版本（每次迭代都计算对应的拉普拉斯，不使用陈旧拉普拉斯）的前向欧拉，加入打印体积的功能

```python
def get_volume(self):
        res = 0
        for i, j, k in self.faces:
            res += np.dot(self.verts[i], np.cross(self.verts[j], self.verts[k]))
        return res    

    def forward_euler_smooth_stable(self, steps=50, lam=0.1):
        v = self.verts.copy()
        # for _ in tqdm(range(steps), desc="Forward Euler Smooth Stable"):
        for i, _ in enumerate(list(range(steps))):
            tmp = ClosedSurface.from_surface_with_new_verts(self, v)
            print(i, tmp.get_volume())
            lplc = tmp.laplacians
            v = v + lam * lplc
        return v
```

另外每10轮还可视化一下：

```python
for _ in range(5):
    v = tmp.forward_euler_smooth_stable(steps=10)
    tmp = ClosedSurface.from_surface_with_new_verts(tmp, v)

    scale = tmp.get_laplacian_color_scale()
    normed_scale = scale / np.abs(scale).max()
    colors = np.array([blue_gray_red(t) for t in normed_scale], dtype=np.float32)
    vista_colored_mesh(tmp.verts, tmp.faces, colors, show_edges=False, opacity=1.0)
```

看一下情况：

```text
0 0.7253084307430073
1 0.7239211553164124
2 0.722558453862115
3 0.7212165525490085
4 0.7198927208329047
5 0.7185849288168916
6 0.7172916119954535
7 0.7160115098241766
8 0.7147435497539302
9 0.7134868137079119
0 0.7122405319371926
1 0.7110040485275844
2 0.7097767949036041
3 0.7085582732356986
4 0.7073480437895171
5 0.7061457152643159
6 0.7049509371602762
7 0.7037633936886877
8 0.7025827988275617
9 0.701408892276646
0 0.7002414361065342
1 0.6990802119681614
2 0.697925018743528
3 0.6967756705634133
4 0.6956319951148461
5 0.6944938322007475
6 0.6933610324910453
7 0.6922334564607783
8 0.691110973442841
9 0.6899934608504582
0 0.6888808034138834
1 0.6877728926743355
2 0.6866696262194576
3 0.6855709076639017
4 0.6844766452755364
5 0.6833867536118041
6 0.682301148966499
7 0.6812197578968875
8 0.6801424988335611
9 0.6790693182697893
0 0.6780001193791161
1 0.6769348957442941
2 0.6758734894639656
3 0.6748160017932053
4 0.6737621469728756
5 0.6727121735542818
6 0.6716657045957063
7 0.6706230173825234
8 0.6695837973199569
9 0.6685482172211434
```

如何修正，使得体积不变？最简单的方法是每一步都硬生生地乘一个比例，体积是线度的三次方，所以每个点按照质心为原点的坐标系，缩放体积比例的立方根：

```python
def volume_maintained_smooth_simple(self, steps=10, lam=0.1):
        v = self.verts.copy()
        tmp = ClosedSurface.from_surface_with_new_verts(self, v)
        volume0 = tmp.get_volume()
        for _ in tqdm(range(steps), desc="volume_maintained_smooth_simple"):
            shift = lam * tmp.laplacians
            v = v + shift

            tmp = ClosedSurface.from_surface_with_new_verts(self, v)
            volume = tmp.get_volume()

            bary_center = np.mean(tmp.verts, axis=0)
            v = bary_center + (volume0 / volume) ** (1 / 3) * (v - bary_center)

            tmp = ClosedSurface.from_surface_with_new_verts(self, v)

        return v
```

效果差不多：

![图片](https://pica.zhimg.com/v2-eab43aeaed79cc907daaf19db943315a.jpg)

更好的方法需要用到体积梯度，体积梯度这本书也讲了，之前没有提。正像是一个三角形（2-单形）上一个点关于这个面积的面积梯度是

$\frac{1}{2} [底边长度]\vec{[垂直底边指向点的法向量]}$ 

一个四面体/三角锥（3-单形）上一个点关于这个体积的体积梯度是

$\frac{1}{3} [底面面积]\vec{[垂直底面指向点的法向量]}$

然后我们要知道，求体积这件事，随便找一个点，把这个点和各个面连起来形成一个个条状的三角锥，把这些三角锥体积加起来就是总体积。那么请注意这个三角锥的体积当然是有方向的、有正负的。假设要求所有面从外面看都是逆时针定向的（正像是常见的坐标系的x,y,z那样），那么就让朝着这个点看，逆时针的面的锥形为正，顺时针的为负，体积就求出来了。

这个定向被一般定义的所谓向量的**混合积**表示出来： 

$[a b c]=a⋅(b×c)=(a×b)⋅c$

由于这个参考点随便选，一般是原点即可。混合积容易想到是三向量平行六面体的有向体积，除以六就是对应的三角锥的体积了。

回到体积梯度，mesh上一个点当然只影响相邻的面对应的三角锥，所以把这些三角锥的体积梯度加起来即可：

![图片](https://pic3.zhimg.com/v2-c1752f1cdd2ca82b1dc774891df35f00.jpg)

体积梯度可以看做是顶点法线的一种定义方法。右边这个 $\sum{A_i \vec{N_i}}$ 也被叫做**顶点面积向量**，也可以看做一种顶点发现，二者只是一个倍数关系。

体积梯度和顶点面积向量共线，体积梯度和面积梯度共线吗？连续情况是的，离散情况不是这样。连续情况：

![图片](https://pica.zhimg.com/v2-144f9148456b8a585946f0f4cd0ccfd0.jpg)

当然了可以预见的是，如果网格细腻，二者近似共线。

不管共不共线，不耽误继续分析。我们从拉普拉斯提供的位移中，减去某个倍数的体积梯度，要求这个新的小位移不再贡献体积变化，也就是说和体积梯度垂直：

![图片](https://pica.zhimg.com/v2-952b96cd2aa7ead160c2c13abf591f72.jpg)

这操作其实就是一个投影了，结果比较眼熟的：

![图片](https://pica.zhimg.com/v2-05be3f1d15ae35d16e2c9a0f426f8404.jpg)

代码：

```python
def volume_maintained_smooth(self, steps=10, lam=0.1):
        def get_one_step_shift(cs):
            ui = cs.laplacians
            gradient_volume = np.zeros_like(cs.verts)
            for i, j, k in cs.faces:
                gradient_volume[i] += np.cross(cs.verts[j], cs.verts[k])
                gradient_volume[j] += np.cross(cs.verts[k], cs.verts[i])
                gradient_volume[k] += np.cross(cs.verts[i], cs.verts[j])
            gradient_volume /= 6

            projection_magnitude = (
                    np.sum(ui * gradient_volume) /
                    np.sum(gradient_volume * gradient_volume)
            )

            return lam * (ui - projection_magnitude * gradient_volume)

        v = self.verts.copy()
        tmp = ClosedSurface.from_surface_with_new_verts(self, v)
        volume0 = tmp.get_volume()
        for _ in tqdm(range(steps), desc="volume_maintained_smooth"):
            shift = get_one_step_shift(tmp)
            v = v + shift

            tmp = ClosedSurface.from_surface_with_new_verts(self, v)
            volume = tmp.get_volume()

            bary_center = np.mean(tmp.verts, axis=0)
            v = bary_center + (volume0 / volume) ** (1 / 3) * (v - bary_center)

            tmp = ClosedSurface.from_surface_with_new_verts(self, v)

        return v
```

可以看到是有点区别：

![图片](https://pic1.zhimg.com/v2-f12c205bb4c0c24343a7ae09ddfc7efc.jpg)

另外我这边打印了一些关于拉普拉斯结果和体积梯度的差别，是有效果的，那个mid就是(ui - projection\_magnitude \* gradient\_volume)：

```text
volume_maintained_smooth:   0%|          | 0/10 [00:00<?, ?it/s]
max sin: 0.9984480005459934
mean sin: 0.018581790025512145
95%: 0.07668897335539847
99%: 0.297063167130624
||ui - mid|| 0.13386585263311473
||ui|| 0.30586008669960674
volume_maintained_smooth:  10%|█         | 1/10 [00:04<00:41,  4.62s/it]
max sin: 0.9998063765112507
mean sin: 0.01685504960422279
95%: 0.06459640765545749
99%: 0.28658311339054554
||ui - mid|| 0.13359891490839795
||ui|| 0.2744442190161802
volume_maintained_smooth:  20%|██        | 2/10 [00:09<00:37,  4.72s/it]
max sin: 0.9999999469992552
mean sin: 0.016083544262112833
95%: 0.059325802489920476
99%: 0.2797438634649405
||ui - mid|| 0.13314914579454423
||ui|| 0.25576498995082586
```

## 二、真正的共形映射

之前简化了问题，没有实现把闭曲面剖开并共形映射的方法，而是做了另一种映射。

这里给一个正确版本。这个代码完全是ai写的，所以只在这里放一放结果。

### 具有亏格的

首先是甜甜圈：

![图片](https://pica.zhimg.com/v2-7ce017eb6db9633c15feeb268af19666.jpg)

拉普拉斯染色：

![图片](https://pic4.zhimg.com/v2-f49809f09abcf9c75032e22d3e0755d3.jpg)

原来的拉普拉斯染色：

![图片](https://pica.zhimg.com/v2-b2487e634bddf6943006c0f60e6d8c1c.jpg)

按照象限染色：

![图片](https://pic3.zhimg.com/v2-596280d7b3afa3d4b83668a42c0b4b66.jpg)

原来的象限颜色染色：

![图片](https://pica.zhimg.com/v2-b1b4bf435da51fd398e6f3f3a4dcb578.jpg)

还有所以ai代码看上去似乎是正确的。

然后是小猫：

![图片](https://pic2.zhimg.com/v2-3aab4a32f028e38ffae1a26385dae2dd.jpg)

小猫拉普拉斯染色，可以看到小猫的脸：

![图片](https://pic1.zhimg.com/v2-479d29a795284070e25a01f97e0f4dfa.jpg)

原来的拉普拉斯染色：

![图片](https://pic4.zhimg.com/v2-4b5f6e35eb479a078fc1427e94d455af.jpg)

按照象限染色：

![图片](https://pic2.zhimg.com/v2-c17c75b70bf1b661f40672e910d018e5.jpg)

原来的象限颜色染色：

![图片](https://pic2.zhimg.com/v2-4ff106d5178d94d97ac5c1deb8836115.jpg)

看起来也是对的...

这是单甜甜圈的：

![图片](https://pica.zhimg.com/v2-71a4488457a0c1f000d4f0a056322f6c.jpg)

拉普拉斯染色：

![图片](https://pica.zhimg.com/v2-bedf9023f68ae7fd77ae8e3998540db0.jpg)

按照象限染色：

![图片](https://picx.zhimg.com/v2-d9c0c4b153559a3dad49e7f6a923b3ed.jpg)

### 零亏格的

之后的都比较抽象，正像是我所说，接近一种球极投影，所以效果并不很好，这是一个兔子...嗯...：

![图片](https://pica.zhimg.com/v2-eddce43bedc484882e0221f9ad3fd3c0.jpg)

所以我让ai修改了一下，

![图片](https://pica.zhimg.com/v2-b3687d98acb9b1464c54932ea64211ba.jpg)

它现在是按照一个路径剖开：

![图片](https://pic4.zhimg.com/v2-9347055623ff3091fdfdbff044806a23.jpg)

拉普拉斯染色：

![图片](https://pic2.zhimg.com/v2-20d2889b51eec92ae8388b9c79f5c22d.jpg)

原来的拉普拉斯染色：

![图片](https://pic4.zhimg.com/v2-1d145f44aee31714c4ed14b0a26362af.jpg)

![图片](https://pica.zhimg.com/v2-30b784408477d18fc5386824cf102704.jpg)

按照象限染色：

![图片](https://pic3.zhimg.com/v2-d9d71078b3b63f12f4fa109ca5514366.jpg)

原来的象限颜色染色：

![图片](https://pic3.zhimg.com/v2-5c2474a5a366e92ba49ef48670838474.jpg)

![图片](https://picx.zhimg.com/v2-96dbb00aae793680e489f399f8da857b.jpg)

  

球：

![图片](https://pic3.zhimg.com/v2-999939e8a6106a925fe79cb42430fd7c.jpg)

按照象限染色：

![图片](https://pic1.zhimg.com/v2-02a1dc354d8937995f5b37807192a0ae.jpg)

这个石像鬼感觉是出了点问题啊（）：

![图片](https://pic1.zhimg.com/v2-d334c22a7a95e438429d30c0524d4ff4.jpg)

拉普拉斯染色：

![图片](https://picx.zhimg.com/v2-33bcd4ac45654ec3d294c57ba490be25.jpg)

原来的拉普拉斯染色：

![图片](https://pic3.zhimg.com/v2-628c3cf610fa6caeea3e556dcd53dd54.jpg)

按照象限染色：

![图片](https://pic4.zhimg.com/v2-ddb28e023280bdda225be8c678ed56e1.jpg)

原来的象限颜色染色：

![图片](https://pic1.zhimg.com/v2-cac266e1476dd65833833f45517e2dac.jpg)

先到这里吧，以后有时间再仔细看看啥情况。还会更新的，这几个文章即便到现在也是改了好几次（）
