# refjmp - 识别PDF论文中的引用并链接到参考文献

## 需求背景描述

读论文时，我们经常需要查看参考文献。如果论文本身的文献引用处有一个指向文末参考文献列表中对应项目的超链接，我们的阅读体验就会好很多——很多PDF阅读器（如PDF Expert），支持直接在引用处（如`[1]`）右键，然后选择在分屏中跳转到文末参考文献列表对应项目处显示。

然而，很多论文，尤其是发表时间比较早的论文，并没有在文献引用处设置超链接。对于这样的论文，我们如果想要查看参考文献，就需要手动翻到文献最底部，肉眼根据序号搜索参考文献，阅读，然后再翻到之前正在阅读的正文部分。毫无疑问，非常麻烦。

refjmp就是为了应对这种情况。它将自动解析PDF文件，识别出其中的文献引用，然后在文献引用标号处创建指向文末对应参考文献的超链接。

## 安装与使用

安装方法（建议按照如下方式设置独立环境）：

```bash
git clone https://github.com/brant-ruan/refjmp.git
cd refjmp/
virtualenv -p python3 venv
source venv/bin/activate
pip install -y requirements.txt
```

使用方法：

```bash
# 进入独立环境
cd refjmp/
source venv/bin/activate

# 参数1是输入文件名，参数2是输出文件名
python refjmp.py ./examples/ret2dir.pdf ./examples/ret2dir_linked.pdf
```

## 其他说明

目前，refjmp的文献引用判定逻辑还比较简单，会有漏标和误标，但是不影响阅读。后面我们将陆续丰富功能（欢迎提交PR）。另外，flask\_app目录下提供了一个简单的网页版refjmp应用，大家也可以自行搭建使用。

本项目由我和chatGPT在相互指导下共同完成 :)

祝论文阅读愉快！

