## CentOS下安装Python2.7

工作中需要使用python2.7, 而服务器自带了2.6版本的python; 我们安装新版本的python时需要保证不影响老版本, 使系统正常服务

### 机房环境如下:
1. 自带 python2.6
2. 自带 pip2.6
3. 自带 virtualenv12.1.0

#### 安装Python2.7
1. 下载源代码 Python-2.7.10.tgz
2. 解压缩
3. 配置安装选项
4. 使用 make altinstall 安装
>linux自带2.6版本的Python，所以安装2.7版本的时候使用make altinstall而不是make install。
这样系统中将同时保留这两种版本的Python，否则的话将会和系统自带的Python冲突。

安装过程如下，我们可以看到安装前，系统默认Python版本是2.6
安装结束后，可以通过Python2.7使用新版本的Python，同时没有影响系统自带Python
```bash
$ python -V
Python 2.6.6
$ tar -xvf Python-2.7.10.tgz
$ cd Python-2.7.10
$ ./configure --prefix=/usr/local --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
$ sudo make && make altinstall
$ which python2.7
/usr/local/bin/python2.7
$ python -V
Python 2.6.6
```

#### 安装Setuptools
由于自带virtualenv, 也可以不用安装新版本Setuptools
```bash
$ wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
$ sudo python2.7 ez_setup.py
```

#### 安装pip2.7

由于自带virtualenv, 也可以不用安装新版本pip
```bash
$ easy_install-2.7 pip
```

#### 安装virtualenv
阿里机房可以不用安装新版本virtualenv, 使用默认版本即可
```bash
pip2.7 install virtualenv
```

#### 建立虚拟环境

建立 python2.7 的虚拟环境，可以看到在虚拟环境中，使用的python和pip都是2.7版本
```bash
$ virtualenv -p /usr/local/bin/python2.7 py2.7
$ source py2.7/bin/activate
$ which python
~/py2.7/bin/python
$which pip
~/py2.7/bin/pip
```
将以下内容添加到 ~/.bashrc, 使虚拟环境自动启用
```bash
source $HOME/py2.7/bin/activate
```