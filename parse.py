#!/usr/bin/env python
# This is on its way out in favor of a PLY-based implementation.
"""What will eventually become a MediaWiki parser.

Based on the work at http://www.mediawiki.org/wiki/Markup_spec/BNF

"""

from pyparsing import *
import string


# Different from html5lib.constants.entities in that (1) some of these are supported in multiple cases, (2) this lacks &apos, for which there's a complicated discussion at http://www.mail-archive.com/mediawiki-cvs@lists.wikimedia.org/msg01907.html.
_htmlEntities = {
    u'Aacute': 193,    u'aacute': 225, u'Acirc': 194, u'acirc': 226, u'acute': 180,
    u'AElig': 198, u'aelig': 230, u'Agrave': 192, u'agrave': 224, u'alefsym': 8501,
    u'Alpha': 913, u'alpha': 945, u'amp': 38, u'and': 8743, u'ang': 8736, u'Aring': 197,
    u'aring':      229,
    u'asymp':      8776,
    u'Atilde':     195,
    u'atilde':     227,
    u'Auml':       196,
    u'auml':       228,
    u'bdquo':      8222,
    u'Beta':       914,
    u'beta':       946,
    u'brvbar':     166,
    u'bull':       8226,
    u'cap':        8745,
    u'Ccedil':     199,
    u'ccedil':     231,
    u'cedil':      184,
    u'cent':       162,
    u'Chi':        935,
    u'chi':        967,
    u'circ':       710,
    u'clubs':      9827,
    u'cong':       8773,
    u'copy':       169,
    u'crarr':      8629,
    u'cup':        8746,
    u'curren':     164,
    u'dagger':     8224,
    u'Dagger':     8225,
    u'darr':       8595,
    u'dArr':       8659,
    u'deg':        176,
    u'Delta':      916,
    u'delta':      948,
    u'diams':      9830,
    u'divide':     247,
    u'Eacute':     201,
    u'eacute':     233,
    u'Ecirc':      202,
    u'ecirc':      234,
    u'Egrave':     200,
    u'egrave':     232,
    u'empty':      8709,
    u'emsp':       8195,
    u'ensp':       8194,
    u'Epsilon':    917,
    u'epsilon':    949,
    u'equiv':      8801,
    u'Eta':        919,
    u'eta':        951,
    u'ETH':        208,
    u'eth':        240,
    u'Euml':       203,
    u'euml':       235,
    u'euro':       8364,
    u'exist':      8707,
    u'fnof':       402,
    u'forall':     8704,
    u'frac12':     189,
    u'frac14':     188,
    u'frac34':     190,
    u'frasl':      8260,
    u'Gamma':      915,
    u'gamma':      947,
    u'ge':         8805,
    u'gt':         62,
    u'harr':       8596,
    u'hArr':       8660,
    u'hearts':     9829,
    u'hellip':     8230,
    u'Iacute':     205,
    u'iacute':     237,
    u'Icirc':      206,
    u'icirc':      238,
    u'iexcl':      161,
    u'Igrave':     204,
    u'igrave':     236,
    u'image':      8465,
    u'infin':      8734,
    u'int':        8747,
    u'Iota':       921,
    u'iota':       953,
    u'iquest':     191,
    u'isin':       8712,
    u'Iuml':       207,
    u'iuml':       239,
    u'Kappa':      922,
    u'kappa':      954,
    u'Lambda':     923,
    u'lambda':     955,
    u'lang':       9001,
    u'laquo':      171,
    u'larr':       8592,
    u'lArr':       8656,
    u'lceil':      8968,
    u'ldquo':      8220,
    u'le':         8804,
    u'lfloor':     8970,
    u'lowast':     8727,
    u'loz':        9674,
    u'lrm':        8206,
    u'lsaquo':     8249,
    u'lsquo':      8216,
    u'lt':         60,
    u'macr':       175,
    u'mdash':      8212,
    u'micro':      181,
    u'middot':     183,
    u'minus':      8722,
    u'Mu':         924,
    u'mu':         956,
    u'nabla':      8711,
    u'nbsp':       160,
    u'ndash':      8211,
    u'ne':         8800,
    u'ni':         8715,
    u'not':        172,
    u'notin':      8713,
    u'nsub':       8836,
    u'Ntilde':     209,
    u'ntilde':     241,
    u'Nu':         925,
    u'nu':         957,
    u'Oacute':     211,
    u'oacute':     243,
    u'Ocirc':      212,
    u'ocirc':      244,
    u'OElig':      338,
    u'oelig':      339,
    u'Ograve':     210,
    u'ograve':     242,
    u'oline':      8254,
    u'Omega':      937,
    u'omega':      969,
    u'Omicron':    927,
    u'omicron':    959,
    u'oplus':      8853,
    u'or':         8744,
    u'ordf':       170,
    u'ordm':       186,
    u'Oslash':     216,
    u'oslash':     248,
    u'Otilde':     213,
    u'otilde':     245,
    u'otimes':     8855,
    u'Ouml':       214,
    u'ouml':       246,
    u'para':       182,
    u'part':       8706,
    u'permil':     8240,
    u'perp':       8869,
    u'Phi':        934,
    u'phi':        966,
    u'Pi':         928,
    u'pi':         960,
    u'piv':        982,
    u'plusmn':     177,
    u'pound':      163,
    u'prime':      8242,
    u'Prime':      8243,
    u'prod':       8719,
    u'prop':       8733,
    u'Psi':        936,
    u'psi':        968,
    u'quot':       34,
    u'radic':      8730,
    u'rang':       9002,
    u'raquo':      187,
    u'rarr':       8594,
    u'rArr':       8658,
    u'rceil':      8969,
    u'rdquo':      8221,
    u'real':       8476,
    u'reg':        174,
    u'rfloor':     8971,
    u'Rho':        929,
    u'rho':        961,
    u'rlm':        8207,
    u'rsaquo':     8250,
    u'rsquo':      8217,
    u'sbquo':      8218,
    u'Scaron':     352,
    u'scaron':     353,
    u'sdot':       8901,
    u'sect':       167,
    u'shy':        173,
    u'Sigma':      931,
    u'sigma':      963,
    u'sigmaf':     962,
    u'sim':        8764,
    u'spades':     9824,
    u'sub':        8834,
    u'sube':       8838,
    u'sum':        8721,
    u'sup':        8835,
    u'sup1':       185,
    u'sup2':       178,
    u'sup3':       179,
    u'supe':       8839,
    u'szlig':      223,
    u'Tau':        932,
    u'tau':        964,
    u'there4':     8756,
    u'Theta':      920,
    u'theta':      952,
    u'thetasym':   977,
    u'thinsp':     8201,
    u'THORN':      222,
    u'thorn':      254,
    u'tilde':      732,
    u'times':      215,
    u'trade':      8482,
    u'Uacute':     218,
    u'uacute':     250,
    u'uarr':       8593,
    u'uArr':       8657,
    u'Ucirc':      219,
    u'ucirc':      251,
    u'Ugrave':     217,
    u'ugrave':     249,
    u'uml':        168,
    u'upsih':      978,
    u'Upsilon':    933,
    u'upsilon':    965,
    u'Uuml':       220,
    u'uuml':       252,
    u'weierp':     8472,
    u'Xi':         926,
    u'xi':         958,
    u'Yacute':     221,
    u'yacute':     253,
    u'yen':        165,
    u'Yuml':       376,
    u'yuml':       255,
    u'Zeta':       918,
    u'zeta':       950,
    u'zwj':        8205,
    u'zwnj':       8204
}


def parsed_eq(expr, text, want):
    got = expr.parseString(text).asList()
    if got != want:
        raise AssertionError('%s != %s' % (got, want))


ParserElement.setDefaultWhitespaceChars('')  # Whitespace is significant.
ParserElement.enablePackrat()  # Enable memoizing.


# Fundamental elements (http://www.mediawiki.org/wiki/Markup_spec/BNF/Fundamental_elements):
# TODO: Put Group() around almost everything to shape the output into a parse tree. Assign setResultsName()s to everything so we can tell what kind of tokens they are.
newline = Literal('\r\n') | '\n\r' | '\r' | '\n'
newlines = Combine(OneOrMore(newline))
#newlines.verbose_stacktrace = True
bol = newline | StringStart()
eol = newline | StringEnd()

space = Literal(' ')
spaces = Combine(OneOrMore(space))
space_tab = (space | '\t').parseWithTabs()
space_tabs = OneOrMore(space_tab)

whitespace_char = (space_tab | newline).parseWithTabs()
whitespace = Combine(OneOrMore(whitespace_char) + Optional(StringEnd())).parseWithTabs()

hex_digit = oneOf(list(hexnums))
hex_number = Combine(OneOrMore(hex_digit))

decimal_digit = oneOf(list(nums))
decimal_number = Combine(OneOrMore(decimal_digit))

underscore = Literal('_')
html_unsafe_symbol = oneOf(list('<>&'))  # TODO: on output, escape
symbol = Regex('[^0-9a-zA-Z]')  # inferred from inadequate description
lcase_letter = Regex('[a-z]')
ucase_letter = Regex('[A-Z]')
letter = Regex('[a-zA-Z]')
non_whitespace_char = letter | decimal_digit | symbol  # Optimize all such combinations; they'd probably benefit from being collapsed into single regex alternations.

html_entity_char = letter | decimal_digit
html_entity_chars = OneOrMore(html_entity_char)
html_entity = (('&#x' + hex_number + ';') |
               ('&#' + decimal_number + ';') |
               ('&' + oneOf(_htmlEntities.keys()) + ';')).setResultsName('html_entity')  # 

character = html_entity | whitespace_char | non_whitespace_char


# (Temporary?) unit tests:
parsed_eq(OneOrMore(newline), '\r\r\n\n\r\n', ['\r', '\r\n', '\n\r', '\n'])
parsed_eq(newlines, '\r\r\n\n\r\n', ['\r\r\n\n\r\n'])
parsed_eq(bol + 'hi', 'hi', ['hi'])
parsed_eq(bol + 'hi', '\nhi', ['\n', 'hi'])
parsed_eq('hi' + eol, 'hi', ['hi'])
parsed_eq('hi' + eol, 'hi\n', ['hi', '\n'])
parsed_eq(spaces, '  ', ['  '])
parsed_eq(space_tab, '\t', ['\t'])
parsed_eq(whitespace_char, '\t', ['\t'])
parsed_eq(whitespace, ' \t\r', [' \t\r'])
parsed_eq(whitespace, ' hi', [' '])  # no StringEnd
parsed_eq(hex_number, '123DECAFBAD', ['123DECAFBAD'])
parsed_eq(decimal_number, '0123', ['0123'])
assert character.parseString('&#xdeadbeef;').getName() == 'html_entity'
assert character.parseString('&aring;').getName() == 'html_entity'
assert character.parseString('&bozo;').getName() != 'html_entity'


print "All's well!"

# try:
#     p = newlines.parseString(str)
# except ParseException, e:
#     print repr(e.msg)
#     raise
# else:
#     print p
