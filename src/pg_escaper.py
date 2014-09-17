def __gen_mapping():
    escaped_chr = {
            '\b':r'\b',
            '\f':r'\f',
            '\n':r'\n',
            '\r':r'\r',
            '\t':r'\t',
            '\v':r'\v',
            '\\':r'\\'
        }

    def escape_chr(c):
        if c in escaped_chr:
            return escaped_chr[c]
        elif 32 <= ord(c) <= 126: # all the printables ASCII characters
            return c
        else:
            return r'\x%.2X' % ord(c)

    return tuple([escape_chr(chr(i)) for i in range(256)])
__escape_mapping = __gen_mapping()

def __escape(s, mapping):
    if s is None:
        return r'\N'
    elif isinstance(s, unicode):
        s = unicode(s).encode('UTF8')
    else:
        s = str(s)

    return ''.join([mapping[ord(c)] for c in s])

def escape_row(row):
    r"""\
    Escapes a row of values to write to a file for the copy_from function.
    The horizontal tab is used as the delimiter, and a newline is appended.
    Implemented with consultation from:
    http://www.postgresql.org/docs/8.2/interactive/sql-copy.htm

    >>> escape_row_for_copy_from([None])
    '\\N\n'
    >>> escape_row_for_copy_from((123213,))
    '123213\n'
    >>> escape_row_for_copy_from(["hello\f\b\v\r\t world\n"])
    'hello\\f\\b\\v\\r\\t world\\n\n'
    >>> escape_row_for_copy_from([1234, "\\n", u"\\.", r'\\', None])
    '1234\t\\\\n\t\\\\.\t\\\\\\\\\t\\N\n'
    >>> escape_row_for_copy_from(["\x00\x127"])
    '\\x00\\x127\n'
    """
    return '\t'.join([__escape(x, __escape_mapping) for x in row]) + '\n'

