
# 解决NameError: name '_mysql' is not defined
# 原因Mysqldb不兼容python3.5以后的版本，使用pymysql代替

import pymysql
pymysql.version_info = (1, 4, 13, "final", 0)
pymysql.install_as_MySQLdb()