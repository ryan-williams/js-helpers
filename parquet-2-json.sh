#!/usr/bin/env bash
#
# Wrapper for parquet2json rearranges the arguments:
#
# $ parquet2json.sh <subcommand> [args...] <path>
#
# as opposed to the original, whose usage says:
#
# $ parquet2json [OPTIONS] <FILE> <SUBCOMMAND>
#
# but in reality requires:
#
# $ parquet2json <FILE> <SUBCOMMAND> [OPTIONS]
#
# EIther way, putting the arg last, and the cmd and its options first, makes lots of other piping and wrapping easier.

last="${@:(($#))}"  # path
set -- "${@:1:$(($#-1))}"

parquet2json "$last" "$@"
