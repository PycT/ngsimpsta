path="nginx/access.log"
dbPath = "ngsimpsta.sqlite"
tableName = "statistics"

badIPsFileName = "addresses2ban.txt"

allowedURLs = [
    "/",
    "/rss/",
    "/robots.txt",
    "/favicon.ico"
]

ban4SuspiciousURLs = False  # marks ip addresses for ban, if the request URL out of allowedURLs list
suspiciousURLsBanDays = 1  # for how many days ban the ip address, which visited suspicious url; 0 = forever
suspiciousURLViolationsMaxTries = 3  # how many bans will be temporary (next one is permanent)

allowedFrequencyPerMinute = 60
ban4Frequency = True  # marks ip address for ban, if requests frequency per minute is higher than allowedFrequencyPerMinute
frequencyBanDays = 10  # for how many days ban the ip address, which sends frequent requests; 0 = forever
frequencyViolationsMaxTries = 3  # how many bans will be temporary (next one is permanent)
