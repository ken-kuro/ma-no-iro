#!/usr/bin/env bash
# Run in a terminal using a Ma no Iro port. Prints every ANSI colour and the
# output styles programs use most, so a port can be checked by eye.
set -u
esc=$'\033'

printf '\n  normal  '
for i in 0 1 2 3 4 5 6 7; do printf '%s[3%dm %2d ██ %s[0m' "$esc" "$i" "$i" "$esc"; done
printf '\n  bright  '
for i in 0 1 2 3 4 5 6 7; do printf '%s[9%dm %2d ██ %s[0m' "$esc" "$i" "$((i + 8))" "$esc"; done
printf '\n  on bg   '
for i in 0 1 2 3 4 5 6 7; do printf '%s[4%dm  %2d  %s[0m' "$esc" "$i" "$i" "$esc"; done
printf '\n\n'

printf '  %s[1mbold%s[0m  %s[2mdim%s[0m  %s[3mitalic%s[0m  %s[4munderline%s[0m  %s[7minverse%s[0m  %s[9mstrike%s[0m\n\n' \
  "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc"

# git status
printf '  On branch %s[1mmain%s[0m\n' "$esc" "$esc"
printf '  %s[32m\tmodified:   tools/derive.py%s[0m\n' "$esc" "$esc"
printf '  %s[31m\tdeleted:    NOTES%s[0m\n' "$esc" "$esc"
printf '  %s[31m\t?? samples/terminal.sh%s[0m\n\n' "$esc" "$esc"

# ls --color
printf '  %s[1;34mdocs%s[0m  %s[1;34msamples%s[0m  %s[1;32mrelease.sh%s[0m  %s[1;36mlatest -> v0.4.0%s[0m  palette.json  %s[1;35mhexagon.png%s[0m\n\n' \
  "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc"

# a test runner
printf '  %s[32m✓%s[0m derive  %s[2m(12 ms)%s[0m\n' "$esc" "$esc" "$esc" "$esc"
printf '  %s[31m✗%s[0m policy  %s[31mhl_high is only 0.030 from overlay%s[0m\n' "$esc" "$esc" "$esc" "$esc"
printf '  %s[33m!%s[0m %s[33m2 weak pairs under simulated protanopia%s[0m\n' "$esc" "$esc" "$esc" "$esc"
printf '  %s[36mhint:%s[0m run %s[1mpython3 tools/derive.py --write%s[0m\n' "$esc" "$esc" "$esc" "$esc"
printf '  %s[90m2 passed, 1 failed, 1 warning in 0.41 s%s[0m\n\n' "$esc" "$esc"

# a prompt
printf '  %s[35m~/ma-no-iro%s[0m %s[90mmain%s[0m %s[33m✱%s[0m ❯ %s[7m %s[0m\n\n' "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc" "$esc"
