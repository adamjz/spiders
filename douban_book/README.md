###注意事项及各文件作用
1、配置get_tag_url.py、master和slave中reids的配置，配置save_to_mysql.py中的redis和mysql的配置    
2、get_tag_url.py，获取tag标签    
3、master，获取tag标签中的所有图书url地址     
4、slave，获取图书信息    
5、save_to_mysql.py，将redis中的图书信息保存到mysql数据库     
6、books_structure.sql是books表结构，mysql需要先导入此表结构     
###运行顺序
先运行get_tag_url.py获取tag标签   
再运行master的scrapy项目获取所有图书url    
然后运行slave的scrapy项目获取图书信息  
最后运行save_to_mysql.py将数据存入mysql数据库