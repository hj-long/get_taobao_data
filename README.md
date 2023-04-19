*** get_taobao_data ***

##### 淘宝网站：

auto_taobao.py 是使用 selenium 框架直接操纵浏览器进行数据爬取,
在该文件的27行的函数参数需要自己手动填写需要进行搜索的商品名称，填完之后运行即可自动爬取~

./测试文件/requests_02.py 是使用 requests 框架进行数据的爬取，里面的 header 需要从自己的浏览器去复制粘贴过来

##### 1688网站：

在 ./sqlit_spider 文件夹下的 get_1688_to_sqlite3.py 是主体程序，直接运行就可以爬取数据

sqlite3_model.py 是 sqlite3 数据库模型文件

其他的是一些测试文件
