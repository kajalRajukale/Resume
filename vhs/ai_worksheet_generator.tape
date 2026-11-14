Output assets/vhs/ai_worksheet_generator.webm
Output assets/vhs/ai_worksheet_generator.gif

Source vhs/_style.tape

Hide
Type `export PS1="\[\e[1;32m\]kajal\[\e[0m\]@\[\e[1;36m\]portfolio\[\e[0m\] \W \$ " BAT_THEME=OneHalfDark BAT_PAGER="" BASH_SILENCE_DEPRECATION_WARNING=1; command -v bat >/dev/null || alias bat=batcat; D="$(mktemp -d)/kajal"; mkdir "$D"; cd "$D"`
Enter
Type "git clone -q --depth 1 https://github.com/kajalRajukale/ai_worksheet_generator ws && cd ws && python3 -m venv .venv && . .venv/bin/activate && pip -q install -r requirements.txt 2>/dev/null; clear"
Enter
Wait@300s /\$ *$/
Show
Type "ls"
Enter
Sleep 1.5s
Type "bat -r 1:14 tests/test_worksheet_generator.py"
Enter
Sleep 3.5s
Type "clear && python -m unittest discover -s tests -v 2>&1 | cut -d'(' -f1 | tail -n 16"
Enter
Wait@90s /\$ *$/
Sleep 2.5s
Screenshot assets/vhs/ai_worksheet_generator.png
Sleep 1s
