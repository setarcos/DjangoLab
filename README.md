# 教学管理网站 
基于 Django 的教学/实验室管理

主要功能包括：
* 课程基本信息管理：时段报名，课程资料等
* 实验流程管理：实验进度记录，学生签到
* 实验室管理：设备情况
* 会议室预定
* 其它辅助教学的内容

## 设置方法

```Shell
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```
* 在管理页面建立 Teacher 和 Student 账号，本系统结合 IAAA 使用这两个用户分别代表教师和学生权限。
* 建立学年信息
* 在调试阶段可以绕过 IAAA 登陆，例如使用如下 URL
```
http://localhost:8000/auth/?token=Teacher
```
