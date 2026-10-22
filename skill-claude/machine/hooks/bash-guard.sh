#!/usr/bin/env bash
# PreToolUse guard for the Bash tool: denies commands that destroy data or
# escalate privileges. Everything else is allowed and logged.
#
# Denied:
#   - sudo, su, doas, pkexec (in any position after wrappers such as xargs)
#   - rm with -r, -R, -f, -d, --no-preserve-root, or a glob argument
#   - find with -delete, or -exec/-ok running a destructive program
#   - rsync with --delete* or --remove-source-files
#   - dd, shred, truncate, wipefs, mkfs*, mkswap, partitioning tools
#   - chmod, chown, chgrp on a path outside the working directory
#   - any reference to a block device under /dev
#   - writes to a .git directory (redirections, or any non read-only program
#     given a .git path)
#
# The command line is split coarsely into simple commands (see guard-lib.sh)
# and each is inspected after leading assignments and wrappers are removed.
# `sh -c` style strings are inspected recursively.

set -u
GUARD_NAME=bash-guard
GUARD_LOG_ALLOW=1
# shellcheck source=guard-lib.sh
. "$(dirname "$(readlink -f "$0")")/guard-lib.sh"

DESTRUCTIVE_TOOLS='dd|shred|truncate|wipefs|mkfs|mkfs\..*|mkswap|fdisk|sfdisk|cfdisk|sgdisk|parted|blkdiscard|losetup|cryptsetup'
ESCALATION_TOOLS='sudo|sudoedit|su|doas|pkexec'
READONLY_ON_GIT='git|gh|cat|ls|less|more|head|tail|grep|egrep|fgrep|rg|find|fd|stat|file|wc|du|tree|diff|cmp|md5sum|sha1sum|sha256sum|sha512sum|hexdump|xxd|strings|realpath|readlink|jq|awk|cut|sort|uniq|bat|cd|pushd|test|\[|echo|printf|type|which'
DEVICE_RE='(^|[[:space:]>=])/dev/(sd|hd|vd|xvd|nvme|mmcblk|loop[0-9]|md[0-9]|dm-|nbd|mapper/|disk/|block/)'
GIT_DIR_RE='(^|/)\.git(/|$)'

check_rm() {
  local a letters endopts=0 recursive=0 force=0 dir=0 paths=()
  for a in "$@"; do
    if [ $endopts = 1 ] || [[ $a != -* ]]; then
      paths+=("$a")
      continue
    fi
    case $a in
      --) endopts=1 ;;
      --recursive) recursive=1 ;;
      --force) force=1 ;;
      --dir) dir=1 ;;
      --no-preserve-root) guard_deny "rm --no-preserve-root is not allowed" ;;
      --*) ;;
      -*)
        letters=${a#-}
        [[ $letters == *[rR]* ]] && recursive=1
        [[ $letters == *f* ]] && force=1
        [[ $letters == *d* ]] && dir=1
        ;;
    esac
  done
  [ $recursive = 1 ] && guard_deny "rm -r is not allowed; remove files one by one, or ask the user to delete the directory"
  [ $force = 1 ] && guard_deny "rm -f is not allowed; use rm on explicit file names without -f"
  [ $dir = 1 ] && guard_deny "rm -d is not allowed; ask the user to remove directories"
  for a in "${paths[@]}"; do
    [[ $a == *[\*\?\[]* ]] && guard_deny "rm with a glob pattern is not allowed; name the files explicitly"
  done
  return 0
}

check_find() {
  local i n=$# args=("$@") next
  for ((i = 0; i < n; i++)); do
    case ${args[i]} in
      -delete) guard_deny "find -delete is not allowed" ;;
      -exec|-execdir|-ok|-okdir)
        next=${args[i + 1]:-}
        next=${next##*/}
        if [[ $next =~ ^(rm|shred|truncate|dd|mv|chmod|chown|chgrp|sh|bash|$ESCALATION_TOOLS)$ ]]; then
          guard_deny "find ${args[i]} $next is not allowed"
        fi
        ;;
    esac
  done
  return 0
}

check_rsync() {
  local a
  for a in "$@"; do
    case $a in
      --delete*|--remove-source-files) guard_deny "rsync $a is not allowed" ;;
    esac
  done
  return 0
}

check_ownership_change() {
  local prog=$1 a first=1
  shift
  for a in "$@"; do
    [[ $a == -* ]] && continue
    if [ $first = 1 ]; then
      first=0
      continue
    fi
    guard_inside_cwd "$a" || guard_deny "$prog on a path outside the working directory is not allowed ($a)"
  done
  return 0
}

check_shell_string() {
  local i n=$# args=("$@") inner
  for ((i = 0; i < n; i++)); do
    if [[ ${args[i]} =~ ^-[A-Za-z]*c[A-Za-z]*$ ]] || [ "${args[i]}" = --command ]; then
      inner="${args[*]:i+1}"
      inner=${inner//[\"\']/}
      check_command "$inner"
      return 0
    fi
  done
  return 0
}

check_git_dir_write() {
  local prog=$1 a prev=""
  shift
  [[ $prog =~ ^($READONLY_ON_GIT)$ ]] && return 0
  for a in "$@"; do
    if [[ $a =~ $GIT_DIR_RE ]]; then
      case $prev in
        --exclude|--exclude-dir|--ignore|-x) ;;
        *) guard_deny "writing inside a .git directory is not allowed ($prog $a); git operations that change repository state are run by the user" ;;
      esac
    fi
    prev=$a
  done
  return 0
}

check_segment() {
  local prog args
  guard_tokenize "$1"
  [ ${#GUARD_ARGV[@]} -gt 0 ] || return 0
  prog=${GUARD_ARGV[0]}
  args=("${GUARD_ARGV[@]:1}")
  if [[ $prog =~ ^($ESCALATION_TOOLS)$ ]]; then
    guard_deny "$prog is not allowed; give the command to the user to run"
  fi
  if [[ $prog =~ ^($DESTRUCTIVE_TOOLS)$ ]]; then
    guard_deny "$prog is not allowed"
  fi
  case $prog in
    rm) check_rm "${args[@]}" ;;
    find) check_find "${args[@]}" ;;
    rsync) check_rsync "${args[@]}" ;;
    chmod|chown|chgrp) check_ownership_change "$prog" "${args[@]}" ;;
    sh|bash|zsh|dash|ksh|fish) check_shell_string "${args[@]}" ;;
  esac
  check_git_dir_write "$prog" "${args[@]}"
}

check_command() {
  local cmd=$1 seg
  if [[ $cmd =~ $DEVICE_RE ]]; then
    guard_deny "referencing a block device under /dev is not allowed"
  fi
  if [[ $cmd =~ \>+[[:space:]]*[^[:space:]]*\.git(/|[[:space:]]|$) ]]; then
    guard_deny "redirecting output into a .git directory is not allowed"
  fi
  while IFS= read -r seg; do
    [ -n "${seg// /}" ] || continue
    check_segment "$seg"
  done < <(guard_segments "$cmd")
}

guard_read_input
check_command "$GUARD_CMD"
guard_allow
