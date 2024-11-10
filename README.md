# 《黑神话：悟空》PS5 自动化提升面板属性

![GitHub License](https://img.shields.io/github/license/yu-zou/bmw_suiyuchi_automation)
![GitHub Repo stars](https://img.shields.io/github/stars/yu-zou/bmw_suiyuchi_automation)

## 简介

对于动作游戏入门玩家来说，《黑神话：悟空》的游戏难度并不低，通过适当地提升面板属性,
可以大大提升操作的容错性。
游戏中提升面板属性的方法主要有两种：

1. 通过升级获得灵光点，通过灵光点进行升级

<img src="doc/ling-guang-dian.jpg" width="500">

2. 第二章解锁戌狗后，通过玲珑内丹制作天上仙丹，从而提升属性

<img src="doc/ling-long-nei-dan.jpg" width="500">

无论哪一种都需要花时间刷属性。和 Steam 端不同，PS5 端由于机器的限制，并不能使用修改器进行属性的快速修改。

该方案借助 PS5 串流+键盘录制脚本+适合初期的装备+适合刷的地点，从而可以挂机一键自动化提升面板属性。

注：本项目仅限分享学习之用，禁止以任何方式进行商业传播

## 适用人群

该方案主要适合于如下人群：

1. 菜（如作者本人）。即便靠攻略也很难上手，需要通过增加面板属性提升容错率的玩家。
2. 强迫症患者。对于玲珑内丹，灵光点这些，有强迫症，不点满及其难受的玩家。

## Demo 演示

盘丝洞碎玉池刷灵光点：

Placeholder: 碎玉池 demo

小西天罪业塔林刷玲珑内丹：

Placeholder: zuiyetalin demo

## 快速开始

1. 需要软件：

- chiaki-ng：一个用于串流的软件，可以将 PS5 通过局域网串流到 PC
  上，在 PC 上远程游玩 PS5 的机器
- python: 用于运行键盘录制脚本

2. 测试环境：Windows 10

3. 安装 chiaki-ng 以及 配置 PS5 串流: https://github.com/streetpea/chiaki-ng

4. 确定串流网络稳定，注意由于按键脚本对于网络的要求比较高，请尽可能将 PS5 和 PC 均通过网线连接至同一路由器下

5. 打开 chiaki-ng 并且远程进入游戏

6. （可选）修改 chiaki-ng 的默认按键配置，如果希望直接使用仓库里自带的脚本，则需要修改 chiaki-ng 的默认键位，如果是希望自己录制，则可跳过这一步

7. 在 windows 命令行中运行屏幕录制 python 脚本，注意打开命令行请务必以管理员模式打开

```python
python automation_script.py chiaki-ng <file_name>
```

7. 首先脚本会确认窗口

## 方案思路

## 推荐装备以及地点

### 推荐装备

### 推荐刷玲珑内丹地点

### 推荐刷灵光点地点
