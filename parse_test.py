
import sqlparse
from sqlparse.tokens import Whitespace

parsed = sqlparse.parse('''CREATE
TABLE `faults` (`id` int(10) unsigned NOT NULL AUTO_INCREMENT,user int(11) unsigned DEFAULT NULL,`created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `notify_at` timestamp NULL DEFAULT NULL,
  `inspection_id` int(11) DEFAULT NULL,
  `equip_id` int(11) NOT NULL,
  `check_item_id` int(11) DEFAULT NULL,`info` varchar(2000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_repair` int(11) DEFAULT '0',
  `is_process` int(11) DEFAULT '0',
  `process` varchar(2000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `level` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=962 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci''')
# parsed = sqlparse.parse('select a as f,b,c from `user` where c = 2')

# for i in parsed[0].tokens:
#     print(i.get_type())

# print(type(parsed[0].get_sublists()))
# for i in parsed[0]:
#     print(type(i), i, '\r\n')
    # for j in parsed[0].get_sublists():
    #     print(type(j), j, '\r\n')
# print(parsed[0].get_sublists())


def walk(node, level):
    for i in node.tokens:
        print('-' * level, type(i), '\t\t', i.ttype, '\t\t', i.value)
        # for child in node.get_sublists():
        #     walk(child, level + 1)

    # if node.get_sublists():
    # for n in node.get_sublists():
    #     walk(n, level)


# walk(parsed[0].tokens[6].tokens[9], 0)
# for i in parsed[0].flatten():
#     print(i)

def p(t, level=0):
    # print(str(t.ttype), type(Whitespace))
    # if not str(t.ttype).startswith('Token.Text.Whitespace'):
    if str(type(t)) == "<class 'sqlparse.sql.Token'>" and not str(t.ttype).startswith('Token.Text.Whitespace'):
        print('%s %-40s\t\t\t%-30s\t\t\t%s\t\t\t%s' % ('\t' * level, type(t), t.ttype, (t.value, ), (t.parent, )))

for i in parsed[0].tokens:
    # print(type(i), '\t\t\t', i.ttype, '\t\t\t', i.value, i.is_group)
    p(i)
    if i.is_group:
        for j in i.tokens:
            p(j, 1)
            if j.is_group:
                for x in j.tokens:
                    p(x, 2)
                    if x.is_group:
                        for y in x.tokens:
                            p(y, 3)

