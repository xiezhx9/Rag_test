# Python 编程语言

## 什么是 Python？

Python 是一种高级、解释型、面向对象的编程语言。由 Guido van Rossum 于 1991 年首次发布。

## Python 的特点

- **简洁易读**：Python 的语法设计让代码更易读、更易维护
- **多范式支持**：支持面向对象、命令式、函数式编程
- **丰富的标准库**：内置了大量标准库，覆盖各种任务
- **跨平台**：可在 Windows、Linux、macOS 等系统运行
- **强大的生态系统**：拥有丰富的第三方库

## Python 应用领域

| 领域 | 说明 |
|------|------|
| Web 开发 | Django、Flask、FastAPI |
| 数据科学 | Pandas、NumPy、Matplotlib |
| 机器学习 | TensorFlow、PyTorch、scikit-learn |
| 自动化脚本 | 系统管理、测试自动化 |
| 游戏开发 | Pygame |
| 网络爬虫 | Scrapy、Beautiful Soup |

## 快速开始

### 安装 Python

```bash
# macOS / Linux
brew install python3

# Windows
# 从 python.org 下载安装
```

### 第一个程序

```python
# hello.py
print("Hello, World!")

# 运行
python hello.py
```

### 变量和数据类型

```python
# 整数
age = 25

# 浮点数
price = 19.99

# 字符串
name = "Python"

# 列表
fruits = ["apple", "banana", "cherry"]

# 字典
person = {"name": "Alice", "age": 30}

# 布尔值
is_active = True
```

### 函数定义

```python
def greet(name):
    """问候函数"""
    return f"Hello, {name}!"

# 调用
message = greet("World")
print(message)  # 输出: Hello, World!
```

### 类和对象

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def bark(self):
        return f"{self.name} says Woof!"

# 创建实例
my_dog = Dog("Buddy", 3)
print(my_dog.bark())  # 输出: Buddy says Woof!
```

## 虚拟环境

建议使用虚拟环境管理项目依赖：

```bash
# 创建虚拟环境
python -m venv myenv

# 激活虚拟环境
# Linux/macOS
source myenv/bin/activate
# Windows
myenv\Scripts\activate

# 安装依赖
pip install package_name

# 退出虚拟环境
deactivate
```

## 包管理

使用 pip 管理 Python 包：

```bash
# 安装包
pip install package_name

# 卸载包
pip uninstall package_name

# 列出已安装的包
pip list

# 导出依赖
pip freeze > requirements.txt

# 从文件安装
pip install -r requirements.txt
```

## 常用库推荐

### Web 框架
- **Django**：全功能 Web 框架
- **Flask**：轻量级 Web 框架
- **FastAPI**：现代高性能 Web 框架

### 数据处理
- **Pandas**：数据分析
- **NumPy**：数值计算
- **Matplotlib**：数据可视化

### 机器学习
- **TensorFlow**：Google 开发的机器学习框架
- **PyTorch**：Facebook 开发的机器学习框架
- **scikit-learn**：机器学习库

## 进一步学习

- 官方文档：https://docs.python.org
- Python 教程：https://docs.python.org/3/tutorial/
- 编程之道：https://peps.python.org/

---

*Python 让编程变得有趣！*
