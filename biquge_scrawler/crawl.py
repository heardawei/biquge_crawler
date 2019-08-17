from scrapy.cmdline import execute
import scrapy
import os
import sys


# 获取当前文件路径(当前文件放在工程根目录)
project_path = os.path.dirname(os.path.abspath(__file__))
print('{} is in dir {}'.format(__file__, project_path))

# 切换到scrapy项目路径下
os.chdir(project_path)

# 启动爬虫,第三个参数为爬虫name
# scrapy.cmdline.execute()
execute(['scrapy', 'crawl', 'fanren'])
