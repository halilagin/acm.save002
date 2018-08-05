
ssh halil@acm <<'ENDSSH'
sh $HOME/bin/desktopscreen.sh
ENDSSH

scp halil@acm:/tmp/desktop.jpg .
open desktop.jpg
