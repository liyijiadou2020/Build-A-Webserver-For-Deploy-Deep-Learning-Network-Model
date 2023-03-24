# Flask 项目部署 bilibili

地址

[05 服务器-端口和安全组_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV18M41127Mf/?p=6&spm_id_from=pageDriver&vd_source=e185ae5bd3b2892b1ad1a067375a6baa)

### 步骤

1. 租个服务器（含公网IP）
2. 代码放在服务器上
3. 让程序在服务器上运行起来

---

## 租用云服务器

腾讯云服务器 含有公网IP 可以让外地的计算机也访问你的程序

- 一般使用CentOS系统
- Windows连接远程服务器可以用xshell工具，通过SSH命令连接
    
    `ssh root@公网IP地址`
    
    - SSH的端口固定是22

### 关于端口

IP地址可以定位到一个主机，端口号可以定位到主机的一个服务（或程序）。

- 22端口：SSH服务。让别的电脑连接自己的服务器（同时还要启动SSH服务）
- 80端口：提供网络服务的的默认端口（http）
- 443端口：提供https服务的端口
- 3306：MySQL的端口

### 安全组

在安全组中配置服务器的哪些端口是开放的

## 环境

- `Git`
- MySQL（如果需要）
- Python
- virtual env（虚拟环境）
- `uwsgi`  作为socket接收用户的请求，运行Python代码，把结果拿到，返回给用户浏览器
- `nginx` 用于接收浏览器发送的请求，如果是python代码的请求则交给uwsgi，如果是文件请求则直接返回（监听80端口）

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/00df294b-847f-4248-95a8-0e306c500900/Untitled.png)

第一层：Nginx，监听所有请求

第二层：uwsgi

第三层：虚拟环境+python+代码

---

### 安装Python

1. 安装gcc（Python的底层是C语言写的）
2. 安装python依赖
3. 下载python源码（`Python 3.9.5`）
4. 解压、编译、安装
5. Python解释器配置豆瓣源

---

### 虚拟环境

步骤：

1. 安装virtual env `pip install virtualenv`
2. 基于virtual env创建虚拟环境
    
    比如代码放在 `/data/www/day28`
    
    环境 `nb`放在这里 `/envs/nb`
    
    `mkdir /envs`
    
    `virtualenv /envs/nb --python=python3.9`
    
3. 激活虚拟环境
    
    `source /envs/bin/activate`
    
    激活了之后 命令行的前面会出现一个 内有你环境名的括号
    

---

### uWSGI （Web Server G- Interface）

步骤

1. 先激活虚拟环境，然后安装uwsgi
    
    `pip install uwsgi`
    
2. 基于uwsgi运行flask项目
    - 通过命令行运行
        
        `uwsgi --http :80 --wsgi-file [app.py](http://app.py) --callable app`
        
        这里的uwsgi监听的是80端口，但这不是最好的方式。一般不会让uwsgi直接监听80端口，而是另外一个比如8080
        
    - 通过配置文件（推荐）
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9ca81978-348c-4937-9aac-e7def2f4a872/Untitled.png)
        
        socket：走tcp协议
        
        virtualenv：帮你激活虚拟环境
        
        `source /env/nb/bin/activate`
        
        `uwsgi --ini nb_uwsgi.ini`
        
    
    注意！当你**更新了代码之后，要重启uwsgi**！
    
    ---
    
    ### Nginx
    
    1. 安装Nginx
        
        `yml install nginx -y`
        
    2. 配置（修改配置文件）
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/a874905b-8756-4cd1-b029-c7ce1a85b9ea/Untitled.png)
        
        - 普通请求 → 8001端口
        - /static/ → /data/www/day28/static（静态文件：找到对应的请求文件）
        
        nginx的默认配置文件在/etc/nginx/nginx.conf、
        
        2.1 首先删除默认的nginx配置文件 `rm nginx.conf`
        
        2.2 新建nginx.conf 同时把内容copy进去并保存 `cd /etc/nginx`
        
        2.3 `vim nginx.conf` 把要添加的内容拷贝进去，:wq，然后退出。
        
    3. 启动nginx
        - 临时启动
            
            `systemctl start nginx`
            
            `systemctl stop nginx`
            
            `systemctl restart nginx`
            
        - 开机启动
            
            `systemctl enable nginx`
            
    4. 访问
        
        
    
    ---
    
    ### 简化重启uwsgi的流程 - 做重启的shell脚本
    
    1. 我们制作两个脚本：停止 & 重启
    - 重启（杀掉 `kill`）
        
        `reboot.sh`
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/58135230-e15b-43bc-b40a-0185d12a2b61/Untitled.png)
        
    - 停止
        
        `stop.sh`
        
    1. 赋予可执行权限
        
        `chmod 755 stop.sh`
        
        `chmod 755 reboot.sh`
        
    2. 直接执行 `[reboot.sh](http://reboot.sh)` 他就可以帮你自动重启了
    
    ---
    
    ### 其他
    
    - MySQL
    - Redis
    - http和域名
    
    如果依赖MySQL，那么就需要（跳过了）
    
    1. 安装MySQL服务
    2. 配置
    3. 启动
    4. 连接
    
    如果依赖Redis，那么就需要
    
    1. 安装
    2. 配置
        - 密码
        - bind `vim /etc/redis.conf`
    3. 启动
        - 开机启动
    
    域名和https
    
    需要域名访问，就需要：
    
    1. 租域名（万网）
    2. 域名解析（域名→IP地址）
        
        例如 [www.5xclass.com](http://www.5xclass.com) → 82.156.54.134
        
        [www.study.5xclass.com](http://www.study.5xclass.com) → 82.156.54.135 （另一台服务器）
        
        [www.buy.5xclass.com](http://www.study.5xclass.com) → 82.156.54.135 （又另一台服务器）
        
    3. 备案
    
    http部署
    
    - 申请证书（1年免费）
    - 上传到服务器上
    - nginx中进行配置 开发443端口
    
    ---
    
    `环境`总结：
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/ed96d508-1f9b-48e4-a018-145bea617a43/Untitled.png)
    

# Flask教程-YouTube

[【Flask 教程】1 -  Flask 的简介](https://www.youtube.com/watch?v=RWviEK1Si68&list=PLDFBYdF-BxV1G4FBpG1EMyFtbsbZuJOvD)

****1 - Flask 的简介****

- 少代码量
- 简单，只包含最基础的需要的东西
- 插件很丰富

****2 - 第一个 Hello World 程序****

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, FLASK!!!"

if __name__=='__main__':
    # app.run() # 如果修改了文件，需要重新启动server
    # app.run(debug=True) # 修改文件不需要重启server也可以反映出代码的变化
    app.run(debug=True, host="0.0.0.0", port=3000)
```

****3 - 利用 render_template 渲染界面****

****4 - 利用循环和判断语句控制 template 的渲染****

判断：

```python
{% if title %}
  <title>{{ title }}</title>
{% else %}
  <title>DEFULT FLASK TITLE</title>
{% endif %}
```

循环：

```python
{% for p in data %}
	<p>{{ p }}</p>
{% endfor %}
```

****5 - 模板继承和引用****

网页经常会有共用的部分，可以抽取出来作为一个模板。

可以利用模板的基础来实现。

继承：`{% extends 'base.html' %}`

引用：`{% include 'navbar.html' %}`

****6 - 利用 flask bootstrap 来优化布局****

****flask bootstrap 是一个插件，是用于优化页面布局的。****

### 实战：用Flask开发一个比较大的博客网站

****7 - Flask-SQLAlchemy 简介和创建用户模型****

---

YOLOv5 + Flask - Object Detection
Aim: To detect in video and images, through Yolov5, with Flask at frontend to upload the files.

Requiments:
1. python
2. flask
3. YOLOv5(pytorch)


