# drawImageByWord
计算机根据文本描述，自动合成符合内容的图片
为了运行该项目，你需要安装 Torch, CuDNN, 和display 包.

训练模型的方法:
    首先下载对应的数据：
    描述数据：
    鸟类： https://drive.google.com/file/d/0B0ywwgffWnLLLUc2WHYzM0Q2eWc/view?usp=sharing
    花类： https://drive.google.com/file/d/0B0ywwgffWnLLMl9uOU91MV80cVU/view?usp=sharing
    coco: https://drive.google.com/open?id=0B0ywwgffWnLLamltREhDRjlaT3M
    对应的图片数据集：
    花类：http://www.robots.ox.ac.uk/%7Evgg/data/flowers/102
    鸟类：http://www.vision.caltech.edu/visipedia/CUB-200-2011.html
    coco:http://mscoco.org/dataset/#download
    下载对应的已经训练好的文本编码器模型：
    鸟：https://drive.google.com/open?id=0B0ywwgffWnLLU0F3UHA3NzFTNEE
    花：https://drive.google.com/open?id=0B0ywwgffWnLLZUt0UmQ1LU1oWlU
    coco:https://drive.google.com/open?id=0B0ywwgffWnLLeVNmVVV6OHBDUFE
然后修改config文件，将对应的路径指向自己本地的数据集
执行训练脚本示例： ./scripts/train_cub.sh

运行样例的方法:

    合成花在master目录下运行命令: ./scripts/demo_flowers.sh. 将对应的文本描述写在 scripts/flowers_queries.txt.文件中
    合成鸟: ./scripts/demo_cub.sh.
    coco数据集: ./scripts/demo_coco.sh.
    
训练新的文本编码器:

   训练鸟和花的文本编码器，参照网址：https://github.com/reedscot/cvpr2016
   训练coco数据集的文本编码器: ./scripts/train_coco_txt.sh.
