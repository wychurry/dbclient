
import pymysql
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QFont, QBrush, QColor

from icon import icon_font
import re


class MysqlModel:

    def __init__(self, host, user, password, port=3306, charset='utf8mb4'):
        self.schema_model = QStandardItemModel()
        self.table_info_model = QStandardItemModel()
        self.data_model = QStandardItemModel()
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.charset = charset
        self.db_icon = icon_font.icon('database')
        self.table_icon = icon_font.icon('table')
        self.connection = None
        self.init_connection()

    def init_connection(self):
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            charset=self.charset,
            database='test',
            autocommit=True
        )
        with self.connection.cursor() as cursor:
            cursor.execute('USE `information_schema`')
            cursor.execute('SELECT `TABLE_SCHEMA`, `TABLE_NAME` FROM `information_schema`.`TABLES`;')
            res = cursor.fetchall()

        for r in res:
            db_name = r[0]
            table_name = r[1]
            db_item = self.schema_model.findItems(db_name)
            if len(db_item) > 0:
                table_item = QStandardItem(table_name)
                table_item.setIcon(self.table_icon)
                table_item.setEditable(False)
                table_item.setFont(QFont("微软雅黑"))
                db_item[0].appendRow(table_item)
            else:
                db_item = QStandardItem(db_name)
                db_item.setEditable(False)
                db_item.setIcon(self.db_icon)
                db_item.setFont(QFont("微软雅黑"))
                table_item = QStandardItem(table_name)
                table_item.setIcon(self.table_icon)
                table_item.setEditable(False)
                table_item.setFont(QFont("微软雅黑"))
                db_item.appendRow(table_item)
                self.schema_model.appendRow(db_item)

    def show_table_data(self, db_name, table_name, overview_filter=None):
        self.data_model.clear()
        with self.connection.cursor() as cursor:
            cursor.execute('use %s' % db_name)
            cursor.execute('desc `%s`.`%s`;' % (db_name, table_name))
            desc_table_res = cursor.fetchall()
            select_fields = []
            for index, r in enumerate(desc_table_res):
                print(r)
                self.data_model.setHorizontalHeaderItem(index, QStandardItem(r[0]))
                if r[1] == 'text':
                    select_fields.append('LEFT(`%s`, 128)' % r[0])
                else:
                    select_fields.append('`%s`' % r[0])
            if overview_filter is None or overview_filter == '':
                cursor.execute('select %s from `%s` limit 1000' % (', '.join(select_fields), table_name))
            else:
                cursor.execute('select %s from `%s` where %s limit 1000' % (', '.join(select_fields), table_name, overview_filter))
            select_res = cursor.fetchall()
            for row_index, row_data in enumerate(select_res):
                for col_index, r in enumerate(row_data):
                    # print(type(r))
                    if r is None:
                        self.data_model.setItem(row_index, col_index, QStandardItem('NULL'))
                        self.data_model.item(row_index, col_index).setForeground(QBrush(QColor(225, 225, 225)))
                    elif isinstance(r, int):
                        self.data_model.setItem(row_index, col_index, QStandardItem(str(r)))
                        self.data_model.item(row_index, col_index).setForeground(QBrush(QColor(10, 20, 225)))
                        self.data_model.item(row_index, col_index).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    else:
                        self.data_model.setItem(row_index, col_index, QStandardItem(str(r)))
                        self.data_model.item(row_index, col_index).setForeground(QBrush(QColor(80, 80, 80)))
                    self.data_model.item(row_index, col_index).setFont(QFont("微软雅黑"))

    def add_db(self):
        self.model.appendRow(QStandardItem('new db'))

    # def __parse_create_table(self, sql):
    #     sql = sql.replace('\n', ' ')
    #     print(sql)
    #     parten = re.compile('^CREATE\s+TABLE\s+`(.+?)`\s+\((\s+`(.+?)`.+){1,}\).*')
    #     match = parten.match(sql)
    #     print(match)
    #     if match:
    #         print(match.groups())


    def __del__(self):
        print("close connection===")
        if self.connection:
            self.connection.close()



if __name__ == '__main__':
    my = MysqlModel(host='127.0.0.1', user='admin', password='123456')
    my.show_table_data('a1', 'faults')
