# iptablogs
iptablogs is a short program written in Python as a student project. Its goal is to make it easier to filter and sort iptables logs contents on the filter table.

## Disclaimer
This program is released under the GNU v3 licence. As stated in the licence file, this program is not covered by any warranty and I shall not be held responsible for any problem that may arise from its use.

## Important notes
It is currently in alpha state and some of its features don't work yet. Please read the following instructions carefully.
Due to limitations of the test environment, this program needs to be run as root, as the log file belongs to root. At the moment it also needs to be executed from the same folder as the log. I'm working to change that.

## Configuration
To use this program, you need to do the followings :

First, create a file in your /etc/rsyslog.d/ named for instance 1-iptables.conf.
Inside, add the following line : 

    :msg,contains, "[netfilter-" /var/log/iptables.log

Then restart the rsyslog service (sudo service rsyslog restart).

Finally, execute the following commands to add iptables rules to each chain INPUT, OUTPUT, FORWARD (or only the ones you're interested in):
  
    sudo iptables -A INPUT -j LOG --log-prefix="[netfilter-INPUT] "
    sudo iptables -A OUTPUT -j LOG --log-prefix="[netfilter-OUTPUT] "
    sudo iptables -A FORWARD -j LOG --log-prefix="[netfilter-FORWARD] "
  
Note : the above configurations can be achieved from within the program but don't have failswitches (if you click twice on the button, it will add the log rules TWICE !).

## Usage
Read the log file :

Once you have launched the program, click on the button "Initialiser". If you correctly followed the previous steps, it will read the log file and display the logs in the table. You'll have to click on that button again if you want to refresh the table as well.

Change the columns you want to display : 

Just select the columns under "Colonnes à afficher" (you can use CTRL or drag the mouse to select several columns), then click on "Appliquer".

Sort the lines : 

Under the label "Afficher" is an entry box in which you can indicate how many lines you want to display. By default, it will display the X first lines of the file. You can also display the X last lines by simply checking the box "Dernières lignes ?".
Just above "Trier par" is a drop-down list you can use to select how you want to sort the list. You can also check the box "Inverser le tri" if you want to reverse the sorting.
Once you're done, click on "Filtrer et trier".

Filter the lines (not implemented yet) : 

In the middle of the screen, you'll find the "Filtres" frame in which you can add filters. You have to separate each filter by a comma followed by a space (or it just won't work). 
eg : filter1, filter2, filter3, etc...
Then just click on "Filtrer et trier".

Experimental (USE WITH CAUTION !) (not implemented yet) :

In the right bottom corner is a frame in which you can find special functions.
The button "Effacer le fichier de logs" simply deletes the current log file and restarts the rsyslog service.
The button "Rediriger les logs dans /var/logs/iptables.logs" creates the 1-iptables.conf file if you didn't manually do it.
The button "Ajouter les règles de logs iptables" adds the -j LOG rules with the appropriate parameters in your iptables.

## Contributing
You can contribute in any way you want (add features, optimize, translate, etc...).
