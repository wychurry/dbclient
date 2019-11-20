
import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Function
from sqlparse.tokens import Keyword, DML, Punctuation

def extract_tables(sql):
    """Extract the table names from an SQL statment.

    Returns a list of (schema, table, alias) tuples

    """
    parsed = sqlparse.parse(sql)
    if not parsed:
        return []

    # INSERT statements must stop looking for tables at the sign of first
    # Punctuation. eg: INSERT INTO abc (col1, col2) VALUES (1, 2)
    # abc is the table name, but if we don't stop at the first lparen, then
    # we'll identify abc, col1 and col2 as table names.
    insert_stmt = parsed[0].token_first().value.lower() == 'insert'
    stream = extract_from_part(parsed[0], stop_at_punctuation=insert_stmt)
    return list(extract_table_identifiers(stream))

def is_subselect(parsed):
    if not parsed.is_group:
        return False
    for item in parsed.tokens:
        if item.ttype is DML and item.value.upper() in ('SELECT', 'INSERT',
                'UPDATE', 'CREATE', 'DELETE'):
            return True
    return False

def extract_from_part(parsed, stop_at_punctuation=True):
    tbl_prefix_seen = False
    for item in parsed.tokens:
        if tbl_prefix_seen:
            if is_subselect(item):
                for x in extract_from_part(item, stop_at_punctuation):
                    yield x
            elif stop_at_punctuation and item.ttype is Punctuation:
                return
            # An incomplete nested select won't be recognized correctly as a
            # sub-select. eg: 'SELECT * FROM (SELECT id FROM user'. This causes
            # the second FROM to trigger this elif condition resulting in a
            # StopIteration. So we need to ignore the keyword if the keyword
            # FROM.
            # Also 'SELECT * FROM abc JOIN def' will trigger this elif
            # condition. So we need to ignore the keyword JOIN and its variants
            # INNER JOIN, FULL OUTER JOIN, etc.
            elif item.ttype is Keyword and (
                    not item.value.upper() == 'FROM') and (
                    not item.value.upper().endswith('JOIN')):
                return
            else:
                yield item
        elif ((item.ttype is Keyword or item.ttype is Keyword.DML) and
                item.value.upper() in ('COPY', 'FROM', 'INTO', 'UPDATE', 'TABLE', 'JOIN',)):
            tbl_prefix_seen = True
        # 'SELECT a, FROM abc' will detect FROM as part of the column list.
        # So this check here is necessary.
        elif isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                if (identifier.ttype is Keyword and
                        identifier.value.upper() == 'FROM'):
                    tbl_prefix_seen = True
                    break


def extract_table_identifiers(token_stream):
    """yields tuples of (schema_name, table_name, table_alias)"""

    for item in token_stream:
        if isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                # Sometimes Keywords (such as FROM ) are classified as
                # identifiers which don't have the get_real_name() method.
                try:
                    schema_name = identifier.get_parent_name()
                    real_name = identifier.get_real_name()
                except AttributeError:
                    continue
                if real_name:
                    yield (schema_name, real_name, identifier.get_alias())
        elif isinstance(item, Identifier):
            real_name = item.get_real_name()
            schema_name = item.get_parent_name()

            if real_name:
                yield (schema_name, real_name, item.get_alias())
            else:
                name = item.get_name()
                yield (None, name, item.get_alias() or name)
        elif isinstance(item, Function):
            yield (None, item.get_name(), item.get_name())


print(extract_tables('select * from `user`'))
print(extract_tables('SELECT * FROM abc JOIN def'))
print(extract_tables('SELECT * FROM (SELECT id FROM `user`)'))
print(extract_tables('insert into abc.cc z VALUES (12,3)'))
print(extract_tables('''
CREATE
TABLE `user` (`id` int(10) unsigned NOT NULL AUTO_INCREMENT,user int(11) unsigned DEFAULT NULL,`created_at` timestamp NULL DEFAULT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=962 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
'''))