#!/usr/bin/env bash
# PreToolUse guard for the Bash tool: restricts git and gh to read-only
# operations. Any invocation that would change repository state, the working
# tree, the index, refs, stashes, configuration, or remote GitHub state is
# denied with a message asking the model to hand the command to the user.
#
# Allowed git subcommands are listed in GIT_READONLY; a few subcommands with
# both read and write forms (branch, tag, remote, stash, reflog, config,
# worktree, notes, submodule, symbolic-ref, hash-object, bundle, fsck,
# sparse-checkout) are inspected argument by argument. Unknown subcommands and
# aliases are denied.
#
# gh is allowed for view, list, status, diff, checks, watch, search and
# GET-only api calls. Everything else is denied.

set -u
GUARD_NAME=git-guard
GUARD_LOG_ALLOW=0
# shellcheck source=guard-lib.sh
. "$(dirname "$(readlink -f "$0")")/guard-lib.sh"

GIT_READONLY='status|log|diff|show|blame|ls-files|rev-parse|describe|shortlog|grep|cat-file|ls-tree|ls-remote|rev-list|merge-base|name-rev|count-objects|check-ignore|check-attr|check-ref-format|diff-tree|diff-files|diff-index|for-each-ref|show-ref|var|help|version|whatchanged|range-diff|cherry|verify-commit|verify-tag|show-branch|request-pull|annotate|get-tar-commit-id|check-mailmap|column|stripspace|interpret-trailers|mailinfo|mailsplit|patch-id|rev-list|unpack-file'

deny_git() {
  guard_deny "git $1 changes repository state; propose the exact command and let the user run it"
}

# Sets GIT_SUB to the git subcommand after global options ("" when there is
# none) and GIT_SUBARGS to the arguments that follow it.
git_subcommand() {
  local i n=$# args=("$@")
  GIT_SUB=""
  GIT_SUBARGS=()
  for ((i = 0; i < n; i++)); do
    case ${args[i]} in
      -C|-c|--git-dir|--work-tree|--namespace|--exec-path|--super-prefix|--config-env|--list-cmds)
        ((i++)) ;;
      --version|--help|-h) GIT_SUB=version; return 0 ;;
      -*) ;;
      *)
        GIT_SUB=${args[i]}
        GIT_SUBARGS=("${args[@]:i+1}")
        return 0
        ;;
    esac
  done
}

# Positional arguments of a subcommand, skipping values of the listed
# value-taking options. Usage: positionals "opt1|opt2" args...
positionals() {
  local valued=$1 a skip=0
  shift
  POSITIONALS=()
  for a in "$@"; do
    if [ $skip = 1 ]; then skip=0; continue; fi
    if [[ $a =~ ^($valued)$ ]]; then skip=1; continue; fi
    [[ $a == -* ]] && continue
    POSITIONALS+=("$a")
  done
}

has_any() {
  local pattern=$1 a
  shift
  for a in "$@"; do
    [[ $a =~ ^($pattern)$ ]] && return 0
  done
  return 1
}

check_git() {
  local sub
  git_subcommand "$@"
  sub=$GIT_SUB
  [ -n "$sub" ] || return 0
  [[ $sub =~ ^($GIT_READONLY)$ ]] && return 0
  case $sub in
    branch)
      has_any '-d|-D|-m|-M|-c|-C|-f|-u|-t|--delete|--move|--copy|--force|--set-upstream-to.*|--unset-upstream|--track|--edit-description|--create-reflog' "${GIT_SUBARGS[@]}" && deny_git branch
      positionals '--contains|--no-contains|--merged|--no-merged|--points-at|--format|--sort|--color|--abbrev|-l|--list' "${GIT_SUBARGS[@]}"
      [ ${#POSITIONALS[@]} -eq 0 ] && return 0
      has_any '-l|--list' "${GIT_SUBARGS[@]}" && return 0
      deny_git branch
      ;;
    tag)
      has_any '-a|-s|-u|-f|-d|-m|-F|-e|--annotate|--sign|--force|--delete|--message|--file|--edit|--local-user|--cleanup' "${GIT_SUBARGS[@]}" && deny_git tag
      positionals '-n|-l|--list|--contains|--no-contains|--points-at|--merged|--no-merged|--format|--sort|--color|--column' "${GIT_SUBARGS[@]}"
      [ ${#POSITIONALS[@]} -eq 0 ] && return 0
      has_any '-l|--list' "${GIT_SUBARGS[@]}" && return 0
      deny_git tag
      ;;
    remote)
      positionals '' "${GIT_SUBARGS[@]}"
      [ ${#POSITIONALS[@]} -eq 0 ] && return 0
      [[ ${POSITIONALS[0]} =~ ^(show|get-url)$ ]] && return 0
      deny_git "remote ${POSITIONALS[0]}"
      ;;
    stash)
      positionals '' "${GIT_SUBARGS[@]}"
      [ ${#POSITIONALS[@]} -gt 0 ] && [[ ${POSITIONALS[0]} =~ ^(list|show)$ ]] && return 0
      deny_git stash
      ;;
    reflog)
      positionals '' "${GIT_SUBARGS[@]}"
      [ ${#POSITIONALS[@]} -eq 0 ] && return 0
      [[ ${POSITIONALS[0]} =~ ^(show|exists)$ ]] && return 0
      deny_git "reflog ${POSITIONALS[0]}"
      ;;
    config)
      has_any '--add|--unset|--unset-all|--replace-all|--rename-section|--remove-section|--edit|-e|set|unset|rename-section|remove-section|edit' "${GIT_SUBARGS[@]}" && deny_git config
      has_any '--get|--get-all|--get-regexp|--get-urlmatch|--list|-l|get|list|--show-origin|--show-scope|--get-colorbool|--get-color' "${GIT_SUBARGS[@]}" && return 0
      positionals '-f|--file|--blob|--type|--default' "${GIT_SUBARGS[@]}"
      [ ${#POSITIONALS[@]} -le 1 ] && return 0
      deny_git config
      ;;
    worktree|sparse-checkout)
      positionals '' "${GIT_SUBARGS[@]}"
      [ ${#POSITIONALS[@]} -gt 0 ] && [ "${POSITIONALS[0]}" = list ] && return 0
      deny_git "$sub"
      ;;
    notes)
      positionals '--ref' "${GIT_SUBARGS[@]}"
      [ ${#POSITIONALS[@]} -eq 0 ] && return 0
      [[ ${POSITIONALS[0]} =~ ^(list|show)$ ]] && return 0
      deny_git "notes ${POSITIONALS[0]}"
      ;;
    submodule)
      positionals '' "${GIT_SUBARGS[@]}"
      [ ${#POSITIONALS[@]} -eq 0 ] && return 0
      [[ ${POSITIONALS[0]} =~ ^(status|summary)$ ]] && return 0
      deny_git "submodule ${POSITIONALS[0]}"
      ;;
    symbolic-ref)
      has_any '-d|--delete|-m' "${GIT_SUBARGS[@]}" && deny_git symbolic-ref
      positionals '' "${GIT_SUBARGS[@]}"
      [ ${#POSITIONALS[@]} -le 1 ] && return 0
      deny_git symbolic-ref
      ;;
    hash-object)
      has_any '-w' "${GIT_SUBARGS[@]}" && deny_git "hash-object -w"
      return 0
      ;;
    bundle)
      positionals '' "${GIT_SUBARGS[@]}"
      [ ${#POSITIONALS[@]} -gt 0 ] && [[ ${POSITIONALS[0]} =~ ^(list-heads|verify)$ ]] && return 0
      deny_git bundle
      ;;
    fsck)
      has_any '--lost-found' "${GIT_SUBARGS[@]}" && deny_git "fsck --lost-found"
      return 0
      ;;
    *)
      deny_git "$sub"
      ;;
  esac
}

deny_gh() {
  guard_deny "gh $1 changes GitHub state; propose the exact command and let the user run it"
}

check_gh_api() {
  local a prev=""
  for a in "$@"; do
    case $prev in
      -X|--method)
        [ "${a^^}" = GET ] || deny_gh "api $prev $a"
        ;;
    esac
    case $a in
      --method=*|-X?*)
        [ "${a#*[=X]}" = GET ] || deny_gh "api $a"
        ;;
      -f|-F|--field|--raw-field|--input|-f?*|-F?*|--field=*|--raw-field=*|--input=*)
        deny_gh "api with request fields"
        ;;
    esac
    prev=$a
  done
  return 0
}

check_gh() {
  local i n=$# args=("$@") cmd="" sub="" rest=()
  for ((i = 0; i < n; i++)); do
    case ${args[i]} in
      -R|--repo|--hostname) ((i++)) ;;
      -*) ;;
      *)
        cmd=${args[i]}
        rest=("${args[@]:i+1}")
        break
        ;;
    esac
  done
  [ -n "$cmd" ] || return 0
  for ((i = 0; i < ${#rest[@]}; i++)); do
    case ${rest[i]} in
      -R|--repo|--hostname) ((i++)) ;;
      -*) ;;
      *) sub=${rest[i]}; break ;;
    esac
  done
  case "$cmd ${sub:--}" in
    "api "*) check_gh_api "${rest[@]}"; return 0 ;;
    "search "*|"browse "*|"status "*|"help "*|"version "*|"completion "*) return 0 ;;
    "pr view"|"pr list"|"pr status"|"pr diff"|"pr checks") return 0 ;;
    "issue view"|"issue list"|"issue status") return 0 ;;
    "repo view"|"repo list"|"repo clone") return 0 ;;
    "run list"|"run view"|"run watch"|"run download") return 0 ;;
    "workflow list"|"workflow view") return 0 ;;
    "release list"|"release view"|"release download") return 0 ;;
    "auth status") return 0 ;;
    "label list"|"gist list"|"gist view"|"cache list"|"secret list"|"variable list") return 0 ;;
    "ssh-key list"|"gpg-key list"|"extension list"|"alias list"|"org list") return 0 ;;
    "project list"|"project view"|"codespace list"|"ruleset list"|"ruleset view"|"ruleset check") return 0 ;;
    "config get"|"config list") return 0 ;;
  esac
  deny_gh "$cmd${sub:+ $sub}"
}

check_segment() {
  local prog
  guard_tokenize "$1"
  [ ${#GUARD_ARGV[@]} -gt 0 ] || return 0
  prog=${GUARD_ARGV[0]}
  case $prog in
    git) check_git "${GUARD_ARGV[@]:1}" ;;
    gh) check_gh "${GUARD_ARGV[@]:1}" ;;
    sh|bash|zsh|dash|ksh|fish)
      local i inner
      for ((i = 1; i < ${#GUARD_ARGV[@]}; i++)); do
        if [[ ${GUARD_ARGV[i]} =~ ^-[A-Za-z]*c[A-Za-z]*$ ]]; then
          inner="${GUARD_ARGV[*]:i+1}"
          inner=${inner//[\"\']/}
          check_command "$inner"
          break
        fi
      done
      ;;
  esac
}

check_command() {
  local seg
  while IFS= read -r seg; do
    [ -n "${seg// /}" ] || continue
    check_segment "$seg"
  done < <(guard_segments "$1")
}

guard_read_input
check_command "$GUARD_CMD"
guard_allow
