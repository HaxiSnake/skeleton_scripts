# Skeleton Scripts

## 预先准备

* 安装openpose的docker镜像
* 将本仓库和视频文件以数据卷方式挂载到openpose docker容器中
* 安装python相关包

pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple


## 主要脚本功能简介

### skating_convert.py:

调用openpose提取视频中的骨骼点并每个视频的结果打包成json文件

### skating_gendata.py

将json文件整理为npy文件并保存