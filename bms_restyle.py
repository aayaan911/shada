# -*- coding: utf-8 -*-
"""Bring the four carried-over screens onto the current design system.

Inventory, Accounts, Reports and Settings were written against the first CSS
pass and kept its class names, so when the stylesheet was rewritten they
rendered as raw HTML. Rather than maintain two stylesheets, their markup is
translated once, here, into the classes the rest of the app uses. The build
then asserts that no undefined class survives anywhere.
"""
import re

IC_MARK = ''

PAGEHEAD = re.compile(
    r'<div class="top"><div><h1>(?P<t>.*?)</h1>\s*'
    r'<div class="sub">(?P<s>.*?)</div></div>\s*'
    r'<div class="sp">(?P<a>.*?)</div>\s*</div>', re.S)


def _head(m):
    return (f'<div class="ph"><div><h1>{m.group("t")}</h1><p>{m.group("s")}</p></div>'
            f'<div class="phact">{m.group("a")}</div></div>')


TABMSG = ('Filters this screen to {}. Wired to the live query in the build; '
          'the prototype ships the full list so nothing is hidden during review.')


TABMSG = ('Filters this screen to {}. Wired to the live query in the build; '
          'the prototype ships the full list so nothing is hidden during review.')

UNPRESSED = ' aria-pressed="false"'


def _tab(b):
    """Keep the tab bars clickable: pressing one moves the selection and says
    what it would filter, rather than sitting there doing nothing."""
    pressed = b.group(1) or UNPRESSED
    label = b.group(2)
    return ('<button data-tab' + pressed + ' data-soon="' + TABMSG.format(label) + '">'
            + label + '</button>')


def _chips(m):
    inner = re.sub(r'<button( aria-pressed="true")?>(.*?)</button>', _tab, m.group(1))
    return '<div class="seg">' + inner + '</div><div style="height:16px"></div>'


# Every action button on the carried-over screens, and what it will do.
ACTIONS = {
 'Stock in': 'Opens the stock-in form. Adds a movement row; current stock is the running total, never typed.',
 'New production batch': 'Opens the batch form. Consumes raw material and adds finished product in one write.',
 'Record expense': 'Opens the expense form. Posts against cash or bank and lands in this list immediately.',
 'Record collection': 'Opens the collection form. Reduces that customer\u2019s due the moment it is saved.',
 'Export Excel': 'Excel export is Phase 7. Every report reads the same ledger, so the file matches the screen exactly.',
 'Export PDF': 'PDF export is Phase 7, A4 and 80mm thermal.',
 'Print': 'Prints the report as shown, with the company header from Settings.',
 'Download backup': 'Exports the full database as SQL. Phase 9, on a schedule as well as on demand.',
 'Save changes': 'Saves every setting on this screen in one write, with the before and after recorded in the activity log.',
}
REPORTS = {
 'Daily report': 'Opens the daily report for a chosen date: every sale, collection and expense.',
 'Weekly report': 'Opens seven days against the week before.',
 'Monthly report': 'Opens the month, broken down by product and by district.',
 'Yearly report': 'Opens twelve months with growth and seasonality.',
 'Product-wise': 'Quantity and value for every pack size, any date range.',
 'Customer-wise': 'Purchases, payments and due for every customer.',
 'District-wise': 'All 64 districts ranked by value.',
}


# order matters: longer, more specific patterns first
SWAPS = [
    # KPI internals
    ('<span class="k">', '<span class="kl">'),
    ('<span class="v">', '<span class="kv">'),
    ('<div class="kpi alert">', '<div class="kpi due">'),
    # card chrome
    ('<div class="h"><h2>', '<div class="ch"><h3>'),
    ('</h2><span class="sp">', '</h3><span class="sub">'),
    ('</h2></div>', '</h3></div>'),
    ('<div class="b flush">', '<div class="cb flush">'),
    ('<div class="b" style="padding:6px 18px 14px">', '<div class="cb" style="padding:4px 16px 12px">'),
    ('<table class="tb">', '<table>'),
    # layout
    ('<div class="two">', '<div class="g2">'),
    ('<div class="wide">', '<div class="g13">'),
    # buttons and pills
    ('class="btn pri"', 'class="btn btn-p"'),
    ('class="pill crit"', 'class="pill bad"'),
    ('class="pill low"', 'class="pill due"'),
    ('var(--red)', 'var(--bad)'),
]


def restyle(html):
    html = PAGEHEAD.sub(_head, html)
    html = re.sub(r'<div class="chips">(.*?)</div>\s*(?=<div)',
                  _chips, html, flags=re.S)
    for a, b in SWAPS:
        html = html.replace(a, b)
    # pills carry a bare status word in inventory; normalise the remaining two
    html = html.replace('class="pill critical"', 'class="pill bad"')
    # tables sit inside a scroller everywhere else, so do the same here
    html = html.replace('<div class="cb flush"><table>',
                        '<div class="cb flush"><div class="tw"><table>')
    html = html.replace('</tbody></table></div></div>',
                        '</tbody></table></div></div></div>')
    # the closing note becomes a proper footnote block
    html = re.sub(r'<p class="note">(.*?)</p>',
                  lambda m: f'<div class="note">{m.group(1)}</div>', html, flags=re.S)
    # every action button says what it does
    def wire(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        label = re.sub(r'<[^>]+>', '', inner).strip()
        msg = ACTIONS.get(label) or REPORTS.get(label.split('\n')[0].strip())
        if not msg:
            for k, v in list(ACTIONS.items()) + list(REPORTS.items()):
                if label.startswith(k):
                    msg = v
                    break
        if not msg or 'data-soon' in attrs:
            return m.group(0)
        return '<' + tag + ' data-soon="' + msg + '"' + attrs + '>' + inner + '</' + tag + '>'

    html = re.sub(r'<(a|button)((?:(?!>).)*class="(?:btn|btn btn-p|rep)"(?:(?!>).)*)>'
                  r'((?:(?!</\1>).)*)</\1>', wire, html, flags=re.S)

    # cards need vertical rhythm between them when stacked
    html = html.replace('</div>\n<div class="card">', '</div>\n<div style="height:14px"></div>\n<div class="card">')
    html = html.replace('</div>\n<div class="g2">', '</div>\n<div style="height:14px"></div>\n<div class="g2">')
    html = html.replace('</div>\n<div class="note">', '</div>\n<div style="height:14px"></div>\n<div class="note">')
    return html
