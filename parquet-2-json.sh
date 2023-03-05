#!/usr/bin/env bash

cmd="$1"; shift
path="$1"; shift

parquet2json "$path" "$cmd" "$@"
