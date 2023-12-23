# ngsimpsta: NGINX log based statistics

## Purposes

 * Collect incoming requests statistics
 * Ban IP addresses malicious requests are coming from.

 **ufw firewall is a prerequsite for ban functionality**


## The usage presumed (but not limited to)

The idea is to run scripts on schedule via **sudo** cron.

 * **ngs_collect.py** - collects the stats from nginx access.log. The path to log is specified in **ngs_config.py**
 * **ngs_mark.py** - reviews statistics and marks IP addresses to be banned or unbanned (when the ban time is over). It also detect how many times the address already was in the ban, and prescribes a long-term ban to those. (number of violations tolerable is configured in **ngs_config.py**
 * **ngs_execute.py** - runs `ufw deny from ...` and `ufw delete deny from ...` commands and updates the table with IP addresses status (banned/released)
 * **ngs_show.py** - extracts the data on ip addresses banned or marked to be banned with reason and the timeline, into `ngs_info.txt`. The output file name and path may be changed in **ngs_config.py**

 Statistics (unaggregated) and ban data is stored in the *sqlite3* db `ngsimpsta.sqlite`. The name and path may be changed in **ngs_config.py**

### Crontab records sample

```
59 23 * * * python /home/johndoe/ngsimpsta/ngs_collect.py
07 00 * * * python /home/johndoe/ngsimpsta/ngs_mark.py
15 00 * * * python /home/johndoe/ngsimpsta/ngs_execute.py
```

 ## Statistics visualisation
 TBD