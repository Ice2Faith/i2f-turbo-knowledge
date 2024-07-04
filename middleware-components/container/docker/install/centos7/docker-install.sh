# install docker for syetm
# author i2f

echo uninstall old docker
yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine

echo install drivers
yum install -y yum-utils \
  device-mapper-persistent-data \
  lvm2

echo set repository
yum-config-manager \
    --add-repo \
    http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

echo install docker community
yum install docker-ce docker-ce-cli containerd.io

echo set autorun-boot
systemctl enable docker

echo start docker
systemctl start docker

echo test by hello-world
docker search hello-world
docker pull hello-world
docker run --rm hello-world

echo docker has installed.

