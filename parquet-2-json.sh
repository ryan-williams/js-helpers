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
# Either way, putting the arg last, and the cmd and its options first, makes lots of other piping and wrapping easier.
#
# Additionally, this wrapper supports reading input data from stdin (which parquet2json doesn't support).

set -e

last="${@:(($#))}"  # path
set -- "${@:1:$(($#-1))}"

if [ $# -eq 0 ]; then
    tmpfile="$(mktemp)"
    cat > "$tmpfile"
    parquet2json "$tmpfile" "$last"
    rv=$?
    rm "$tmpfile"
    exit $rv
elif [ "$last" == "-" ]; then
    tmpfile="$(mktemp)"
    cat > "$tmpfile"
    parquet2json "$tmpfile" "$@"
    rv=$?
    rm "$tmpfile"
    exit $rv
else
    parquet2json "$last" "$@"
    exit $rv
fi
