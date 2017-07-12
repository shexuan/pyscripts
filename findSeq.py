#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(
    description="Find the regex (Regular Expression) and return its span (start and end)")
parser.add_argument('--fasta', '-f', type=str,
                    help='Input a fasta file here.')
# parser.add_argument('--input', '-in', type=str,
#                     help='Read sequences from stdin.')
parser.add_argument('--regex', '-r', type=str,
                    help='Input a regex (Regular Expression) here.')

args = parser.parse_args()
res = defaultdict(str)


if args.fasta:
    with open(args.fasta, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith(">"):
                gene_id = line.strip()[1:]
            else:
                res[gene_id] += line.strip()

pattern = re.compile(args.regex)
for gene_id, seq in res.items():
    search = re.search(pattern, seq)
    if search.group() == "":
        continue
    else:
        match = re.finditer(pattern, seq)
        for p in match:
            print("{0:<20}{1:<20}{2:<8}{3:<8}".format(
                gene_id, p.group(), p.span()[0], p.span()[1]))

