from jinja2 import Environment
from django.urls import reverse
from django.contrib.staticfiles.storage import staticfiles_storage

def jinja2_environment(**options):
    # 创建环境对象
    env = Environment(**options)
    # 自定义语法实现{{ static('静态文件路径找到静态文件') }}, {{ url('路由的命名空间') }}
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    # 返回环境对象
    return env
