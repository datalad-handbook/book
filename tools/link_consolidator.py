#!/usr/bin/env python
#
# Use this with the output of the sphinx linkchecker
# $ make linkcheck | tee links.txt
# $ python tools/link_consolidator.py links.txt
#
# It provides a markdown-formatted list of issues, that can be posted
# to an issue tracker.
#
# The following issues are recognized:
#
# - `redundant-trailing-slash`
#     The URL has a trailing slash that is (likely) not needed.
#     (was: The same URL, but without the trailing slash, is used elsewhere
#     in the book).
# - unshorted-youtube-link
#     This could be a https://youto.be/ style short URL
# - needless-trailing-slash
#     A URL without a path component. It should need nbow trailing slash
# - permanent-redirect
#     A permanent redirect is reported for a URL
# - none-https
#     An link with an insecure protocol
# - needless-latest-handbook
#     The default handbook version served is 'en/latest'
# - long-kbi-link
#     KBI link with needless '/index.html' tail


from pathlib import Path
import re
import sys
from urllib.parse import urlparse


linkline_re = re.compile(
    '\((?P<use>.*): line[ ]+(?P<line>[0-9]+)\) (?P<status>[^ ]+) [ ]*(?P<link>[^ ]+)(?P<note>.*)'
)


def read_links(fpath):
    links = {}
    for line in fpath.open():
        m = linkline_re.match(line)
        if m is None:
            print(f'ignore line: {line!r}', file=sys.stderr)
            continue
        m = m.groupdict()
        link = m['link'].strip()
        link_rec = links.get(link, {})
        if not link_rec:
            link_rec['status'] = m['status']
            link_rec['note'] = m['note'].strip() if m['note'].strip() else None
        uses = link_rec.get('uses')
        if uses is None:
            use = {}
            uses = [use]
        else:
            # must be a list
            use = {}
            uses.append(use)
        use.update(
            file=m['use'],
            line=int(m['line']),
        )
        link_rec['uses'] = uses
        links[link] = link_rec
    return links


def _report_flaws(report, type_, uses, src):
    for u in uses:
        flaws = report.get(u['file'], [])
        flaws.append(dict(
            type=type_,
            line=u['line'],
            src=src,
        ))
        report[u['file']] = flaws


def report_redundant_trailing_slash(links, report):
    for link in links:
        if link.endswith('/'):
            _report_flaws(
                report, "redundant-trailing-slash", links[link]['uses'], link)


def report_unshortened_youtube(links, report):
    for link in links:
        if 'youtube.com/watch' in link:
            _report_flaws(
                report, "unshorted-youtube-link", links[link]['uses'], link)


def report_domainroot_trailing_slash(links, report):
    for link in links:
        p = urlparse(link)
        if p.path == '/' and not p.params and not p.query and not p.fragment:
            _report_flaws(
                report, "needless-trailing-slash", links[link]['uses'], link)


def report_permanent_redirects(links, report):
    for link, rec in links.items():
        if rec['status'] == 'redirect' and 'permanently to' in rec['note']:
            _report_flaws(
                report, "permanent-redirect", links[link]['uses'],
                f"{link} {rec['note']}")


def report_insecure_links(links, report):
    for link in links:
        if link.startswith('http://'):
            _report_flaws(
                report, "none-https", links[link]['uses'], link)


def report_needless_latest_handbook(links, report):
    for link in links:
        if 'handbook.datalad.org/en/latest/' in link:
            _report_flaws(
                report, "needless-latest-handbook", links[link]['uses'], link)


def report_long_kbi_link(links, report):
    for link in links:
        if 'knowledge-base.psychoinformatics.de/kbi' in link \
                and link.endswith('index.html'):
            _report_flaws(
                report, "long-kbi-link", links[link]['uses'], link)


def print_report(report):
    for f in sorted(report):
        print(f'- `docs/{f.strip()}.rst`:')
        for flaw in sorted(report[f], key=lambda x: x['line']):
            print(f"  - *line {flaw['line']}*: `{flaw['type']}` [{flaw['src']}]")


if __name__ == '__main__':
    links = read_links(Path(sys.argv[1]))
    report = {}
    report_redundant_trailing_slash(links, report)
    report_unshortened_youtube(links, report)
    report_domainroot_trailing_slash(links, report)
    report_permanent_redirects(links, report)
    report_insecure_links(links, report)
    report_needless_latest_handbook(links, report)
    report_long_kbi_link(links, report)
    print_report(report)
    #for l in sorted(links):
    #    print(l)
