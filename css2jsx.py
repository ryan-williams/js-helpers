#!/usr/bin/env python

from sys import stdin, stdout

import click
import regex as re


def kv_rgx(i=''):
    return f'(?P<k{i}>[\\w\\-]+):\\s*(?P<v{i}>[%#\\w\\-_ ]+)'


RGX = f'"{kv_rgx("0")}(?:;\\s*{kv_rgx("1")})*;?"'


def convert_css(css, string=True):
    m = re.fullmatch(RGX, css.rstrip('\n'))
    if not m:
        raise ValueError(f'Failed to parse {css} with {RGX}')

    kvs = { m['k0']: m['v0'], **{ k: v for k, v in zip(m.captures('k1'), m.captures('v1')) } }

    obj = {}
    for k, v in kvs.items():
        first, *rest = k.split('-')
        new_k = ''.join([
            first,
            *[
                (pc[0].upper() + pc[1:] if pc else '')
                for pc in rest
            ]
        ])
        obj[new_k] = v

    if string:
        return '{{ %s }}' % ', '.join([ f'"{k}": "{v}"' for k, v in obj.items() ])
    else:
        return obj


def convert_css_all(content):
    matches = re.finditer(RGX, content)
    if matches:
        idx = 0
        replaced = ''
        for m in matches:
            start, end = m.span()
            replaced += content[idx:start]
            replaced += convert_css(content[start:end])
            idx = end
        replaced += content[idx:]
    else:
        replaced = content
    return replaced

@click.command()
@click.option('-i', '--in-place', is_flag=True, help='Overwrite <path> in-place')
@click.argument('path', required=False)#, help='Read this path and convert inline styles (when absent, input is read from stdin)')
@click.argument('output', required=False)#, help='Optional path to write output to')
def main(path, in_place, output):
    if path:
        with open(path, 'r') as f:
            content = f.read()

        replaced = convert_css_all(content)

        if in_place:
            assert not output
            output = path
            in_place = False

        if output:
            assert not in_place
            with open(output, 'w') as f:
                f.write(replaced)
        else:
            stdout.write(replaced)
    else:
        assert not in_place
        css = stdin.read()
        obj_str = convert_css(css)
        if output:
            with open(output, 'w') as f:
                f.write(obj_str)
        else:
            stdout.write(obj_str)


if __name__ == '__main__':
    main()
