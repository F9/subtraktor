subtraktor
==========

python script to download subtitle for tv-shows

This is a fork of this project:

HOW TO
======

Change the initial lines with your account info on opensubs and change the dir where you store your tv shows.
Then simply launch
<br>
<code> python subtraktor.py </code>
<br>
and enjoy the subs

Automatically work
------------------

To automatically start the script you can add a line to your crontab file. In UNIX sys write <br />
<code>crontab -e</code> <br />
and add <br />
<code>@hourly python /home/pi/Download/subtraktor.py</code> <br />
The script each hour will check if there is new subs for your tv shows and films.
