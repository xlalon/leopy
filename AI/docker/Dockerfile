FROM python3.6:v.7
# 镜像工作目录
WORKDIR /data
# 当前目录内容复制到容器的/data目录
ADD . /data
RUN pip install -r requirements.txt --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
# 80端口供外部使用
EXPOSE 80
# 定义环境变量
ENV NAME Wrold
# 启动容器运行
CMD ["python", "app.py"]
