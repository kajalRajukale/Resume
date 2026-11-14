Output assets/vhs/Django_Healthcare.webm
Output assets/vhs/Django_Healthcare.gif

Source vhs/_style.tape

Hide
Type `export PS1="\[\e[1;32m\]kajal\[\e[0m\]@\[\e[1;36m\]portfolio\[\e[0m\] \W \$ " BAT_THEME=OneHalfDark BAT_PAGER="" BASH_SILENCE_DEPRECATION_WARNING=1; command -v bat >/dev/null || alias bat=batcat; D="$(mktemp -d)/kajal"; mkdir "$D"; cd "$D"`
Enter
Type "clear"
Enter
Show
Type "git clone -q --depth 1 https://github.com/kajalRajukale/Django_Healthcare hc && cd hc"
Enter
Wait@90s /\$ *$/
Type "tree -d -L 1 -I '.venv*|static*|media|__pycache__'"
Enter
Sleep 2s
Type "bat appointments/models.py"
Enter
Sleep 5s
Screenshot assets/vhs/Django_Healthcare.png
Sleep 1s
