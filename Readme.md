# Skeleton Scripts

## 预先准备

### 安装openpose的docker镜像 
docker版本： 19.03.12   
如果版本不对，加载容器的时候会出错   
docker仓库：https://hub.docker.com/r/cwaffles/openpose   
docker常用指令：https://www.runoob.com/docker/docker-tutorial.html  
**step1:安装docker**  
使用官方安装脚本自动安装:   
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun   
手动安装   
参考链接：https://www.runoob.com/docker/ubuntu-docker-install.html   
  
**step2:安装NVIDIA CONTAINER RUNTIME** 
新建一个脚本文件 vim nvidia.sh 填入如下内容:   
sudo curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | \
  sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
sudo curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
sudo apt-get update

执行脚本 sh nvidia.sh

安装 nvidia-container-runtime:
sudo apt-get install nvidia-container-runtime

**step3:创建用户组，方便授权**

如果没有sudo权限，可以创建dockers权限组
sudo groupadd docker
sudo gpasswd -a ${USER} docker
sudo service docker restart
newgrp - docker    //将当前用户以docker用户组的身份再次登录系统

通过cat /etc/group可以查看用户组信息

**step4:下载镜像，对应cuda10.0,cudnn7.0**

docker pull cwaffles/openpose
通过镜像创建容器

sudo docker run --gpus all --name openpose -it cwaffles/openpose:latest /bin/bash
进入容器内部(创建成功会自动进入容器)

docker exec -it openpose /bin/bash
注：还可以使用以下命令一次删除所有停止的容器。docker rm $(docker ps -a -q)

**step5:测试openpose的demo**

＃only body   
./build/examples/openpose/openpose.bin --video examples/media/video.avi --write_json output/ --display 0 --render_pose 0   
#Body + face + hands   
./build/examples/openpose/openpose.bin --video examples/media/video.avi --write_json output/ --display 0 --render_pose 0 --face --hand
###  将本仓库和视频文件以数据卷方式挂载到openpose docker容器中
接下来可以看一下docker容器的共享文件夹来拷贝数据集

docker run -it -v  /宿主机绝对路径目录:  /容器内目录  镜像名
docker run -idt -v --name openpose  /home/$USER/share:/openpose/share cwaffles/openpose:latest    //后台运行
docker exec -it  openpose /bin/bash //进入容器

### 安装python相关包

pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple


## 主要脚本功能简介

### skating_convert.py:

调用openpose提取视频中的骨骼点并每个视频的结果打包成json文件

### skating_gendata.py

将json文件整理为npy文件并保存
