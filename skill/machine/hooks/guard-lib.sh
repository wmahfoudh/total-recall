#!/usr/bin/env bash
# Shared helpers for the Claude Code PreToolUse guards.
# Sourced by bash-guard.sh and git-guard.sh. Not meant to be executed directly.
#
# Input: the hook JSON on stdin ({tool_name, tool_input: {command}, session_id, cwd}).
# Output: nothing when the command is allowed; a permissionDecision "deny"
# JSON document when it is not. Exit status is always 0 so that a failure of
# the guard itself never masquerades as a decision.

GUARD_LOG_DIR="${CLAUDE_GUARD_LOG_DIR:-${HOME:-/tmp}/.claude/logs}"
GUARD_LOG_FILE="$GUARD_LOG_DIR/claude-guard.log"
GUARD_NAME="${GUARD_NAME:-guard}"
GUARD_CMD=""
GUARD_SESSION="-"
GUARD_CWD=""
GUARD_ARGV=()

guard_log() {
  local level=$1 reason=$2 flat
  mkdir -p "$GUARD_LOG_DIR" 2>/dev/null || return 0
  flat=$(printf '%s' "$GUARD_CMD" | tr '\n\r\t' '   ' | cut -c1-500)
  printf '%s %s hook=%s session=%s cwd=%s reason="%s" cmd="%s"\n' \
    "$(date -Is)" "$level" "$GUARD_NAME" "$GUARD_SESSION" "$GUARD_CWD" "$reason" "$flat" \
    >> "$GUARD_LOG_FILE" 2>/dev/null
}

guard_deny() {
  local reason=$1
  guard_log DENY "$reason"
  reason=${reason//\\/\\\\}
  reason=${reason//\"/\\\"}
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"%s"}}\n' "$reason"
  exit 0
}

guard_allow() {
  [ "${GUARD_LOG_ALLOW:-0}" = 1 ] && guard_log ALLOW "-"
  exit 0
}

guard_read_input() {
  local input
  input=$(cat)
  if ! command -v jq >/dev/null 2>&1; then
    guard_deny "jq is not installed, the command guard cannot inspect commands"
  fi
  GUARD_CMD=$(printf '%s' "$input" | jq -r '.tool_input.command // empty' 2>/dev/null) || GUARD_CMD=""
  GUARD_SESSION=$(printf '%s' "$input" | jq -r '.session_id // "-"' 2>/dev/null) || GUARD_SESSION="-"
  GUARD_CWD=$(printf '%s' "$input" | jq -r '.cwd // empty' 2>/dev/null) || GUARD_CWD=""
  [ -n "$GUARD_CWD" ] || GUARD_CWD=$PWD
  [ -n "$GUARD_CMD" ] || guard_allow
}

# Prints the simple commands of a shell command line, one per line. Splitting
# is deliberately coarse: every control operator, pipe, subshell and group
# delimiter starts a new segment, and quoting is ignored. Over-splitting only
# makes the guard stricter.
guard_segments() {
  printf '%s\n' "$1" | sed -E 's/\|\||&&|;|\||&|\$\(|`|\(|\)|\{|\}/\n/g'
}

# Fills GUARD_ARGV with the words of one segment, minus leading variable
# assignments and transparent wrappers (env, xargs, nohup, ...), so that
# GUARD_ARGV[0] is the program that actually runs.
guard_tokenize() {
  local w
  read -r -a GUARD_ARGV <<< "$1"
  while [ ${#GUARD_ARGV[@]} -gt 0 ]; do
    w=${GUARD_ARGV[0]}
    w=${w#\\}
    w=${w#[\"\']}
    case $w in
      [A-Za-z_]*=*|'!'|if|then|elif|else|do|while|until)
        GUARD_ARGV=("${GUARD_ARGV[@]:1}")
        ;;
      command|exec|nohup|time|nice|ionice|builtin|env|xargs|timeout|stdbuf|unbuffer|watch|eval|chronic)
        GUARD_ARGV=("${GUARD_ARGV[@]:1}")
        while [ ${#GUARD_ARGV[@]} -gt 0 ] && [[ ${GUARD_ARGV[0]} == -* || ${GUARD_ARGV[0]} == '{}' ]]; do
          case ${GUARD_ARGV[0]} in
            -I|-n|-P|-L|-s|-d|-a|-E|-e|-u|-C|--chdir|-S|--split-string|-k|--kill-after|-c|--class|-o|-i|-p)
              GUARD_ARGV=("${GUARD_ARGV[@]:2}") ;;
            *) GUARD_ARGV=("${GUARD_ARGV[@]:1}") ;;
          esac
        done
        if [ "$w" = timeout ] && [ ${#GUARD_ARGV[@]} -gt 0 ]; then
          GUARD_ARGV=("${GUARD_ARGV[@]:1}")
        fi
        ;;
      *)
        GUARD_ARGV[0]=${w##*/}
        break
        ;;
    esac
  done
}

# Resolves a path argument of a command to an absolute, normalized path,
# relative to the tool's working directory.
guard_abspath() {
  local p=$1
  case $p in
    '~'|'~/'*) p="${HOME}${p#\~}" ;;
    '$HOME'|'$HOME/'*) p="${HOME}${p#\$HOME}" ;;
    '${HOME}'|'${HOME}/'*) p="${HOME}${p#\$\{HOME\}}" ;;
    /*) ;;
    *) p="$GUARD_CWD/$p" ;;
  esac
  realpath -m -- "$p" 2>/dev/null || printf '%s\n' "$p"
}

# True when the resolved path is the working directory or inside it.
guard_inside_cwd() {
  local abs cwd
  abs=$(guard_abspath "$1")
  cwd=$(realpath -m -- "$GUARD_CWD" 2>/dev/null || printf '%s' "$GUARD_CWD")
  [ "$abs" = "$cwd" ] || [[ $abs == "$cwd"/* ]]
}
