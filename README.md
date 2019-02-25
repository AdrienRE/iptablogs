# iptablogs
iptablogs is a short script/program written by me (Adrien REYNAUD) in Python 3.7.2 as a student project. Its goal is to make it easier to filter and sort the logs from iptables, specifically on the Filter table. For more details on how it works, take a look at the external_doc.pdf file.

## Disclaimer
This script/program is released under the GPL-3 licence. As stated in the licence file, this script/program is not covered by any warranty and I shall not be held responsible for any problem that may arise from its use.
Please read the LICENCE for more details.

## Important notes
Please read the following instructions carefully.
Iptablogs needs to be run as root, as the log file belongs to root and the functions described in the "special functions" part need root privileges as well. It has only be tested on Python 3.7.2 under Debian 9.5 (it won't work well on Python 3.5 FYI).

## Configuration
Before using this iptablogs, you need to do the following to enable iptables logging and redirect the log messages in a separate file :

###### The easy way : 
Launch iptablogs using **sudo iptablogs.py**, click on the buttons "Rediriger les logs dans /var/logs/iptables.log" and "Ajouter les règles de logs iptables". 
You can now start using it.

###### The less easy way :
First, create a file in your /etc/rsyslog.d/ named for instance 1-iptables.conf.
Inside, add the following line : 
```
:msg,contains, "[netfilter-" /var/log/iptables.log
```
Then restart the rsyslog service (sudo service rsyslog restart).

Finally, execute the following commands to add iptables rules to each chain INPUT, OUTPUT, FORWARD (or only the ones you're interested in):
```
sudo iptables -A INPUT -j LOG --log-prefix="[netfilter-INPUT] "
sudo iptables -A OUTPUT -j LOG --log-prefix="[netfilter-OUTPUT] "
sudo iptables -A FORWARD -j LOG --log-prefix="[netfilter-FORWARD] "
```

## How to use this program ?
###### Filling the table :
Once you have launched iptablogs, click on the button "Initialiser". If you correctly followed the previous steps, it will read the log file and display the logs in the table. You'll have to click on that button again if you want to refresh the table as well.

###### Change the columns you want to display : 
Just select the columns under "Colonnes à afficher" (you can use CTRL or drag the mouse to select several columns), then click on "Appliquer".

###### Sort the lines : 
Under the label "Afficher" is an entry box in which you can indicate how many lines you want to display. By default, it will display the X first lines of the file. You can also display the X last lines by simply checking the box "Dernières lignes ?".
Just above "Trier par" is a drop-down list you can use to select how you want to sort the list. You can also check the box "Inverser le tri" if you want to reverse the sorting.
Once you're done, click on "Filtrer et trier".

###### Filter the lines : 
In the middle of the screen, you'll find the "Filtres" frame in which you can add filters. You have to separate each filter by a comma followed by a space (or it just won't work). 
e.g. : "filter1, filter2, filter3" etc...
or "filter1, , filter2" (if you want to use blank filters).
Then just click on "Filtrer et trier".

###### Special functions (USE WITH CAUTION !) : 
In the right bottom corner is a frame in which you can find special functions.
- The button "Effacer le fichier de logs" simply deletes the current log file and restarts the rsyslog service.
- The button "Rediriger les logs dans /var/logs/iptables.logs" creates the 1-iptables.conf file if you didn't manually do it.
- The button "Ajouter les règles de logs iptables" adds the -j LOG rules with the appropriate parameters in your iptables.

## Contribute
You can contribute in any way you want (add features, optimize, translate, etc...).

## Contact
For more informations, feel free to contact me at undercover1[at]live.fr
