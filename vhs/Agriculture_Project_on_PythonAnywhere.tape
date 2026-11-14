Output assets/vhs/Agriculture_Project_on_PythonAnywhere.webm
Output assets/vhs/Agriculture_Project_on_PythonAnywhere.gif

Source vhs/_style.tape

Hide
Type `export PS1="\[\e[1;32m\]kajal\[\e[0m\]@\[\e[1;36m\]portfolio\[\e[0m\] \W \$ " BAT_THEME=OneHalfDark BAT_PAGER="" BASH_SILENCE_DEPRECATION_WARNING=1; command -v bat >/dev/null || alias bat=batcat; D="$(mktemp -d)/kajal"; mkdir "$D"; cd "$D"`
Enter
Type "clear"
Enter
Show
Type "git clone -q --depth 1 https://github.com/kajalRajukale/Agriculture_Project_on_PythonAnywhere agri && cd agri"
Enter
Wait@60s /\$ *$/
Type "ls"
Enter
Sleep 1.5s
Type "bat -r 9:27 App/ai_engine.py"
Enter
Sleep 4.5s
Type "clear && python3 -q"
Enter
Sleep 800ms
Type "from App.ai_engine import suggest_for_soil"
Enter
Type "from pprint import pprint"
Enter
Type "pprint(suggest_for_soil(soil_ph=5.2, moisture=18, crop='wheat'))"
Enter
Sleep 3.5s
Screenshot assets/vhs/Agriculture_Project_on_PythonAnywhere.png
Sleep 1s
Type "exit()"
Enter
Sleep 300ms
