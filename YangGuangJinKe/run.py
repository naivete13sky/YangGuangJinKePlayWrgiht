from scrapy.cmdline import execute
# execute(['scrapy', 'crawl', 'toutiao','-a','keyword=小米10'])
execute(['scrapy', 'crawl', 'yangGuangJinKe'])#yangGuangJinKe是spider文件中的name = 'yangGuangJinKe'指定的。

