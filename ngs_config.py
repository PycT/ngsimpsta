nginxLogPath="/var/log/nginx/access.log"

allowedURLs = [
    # "/", don't put root here! don't uncomment!
    "/rss/",
    "/robots.txt",
    "/favicon.ico"
]  # url not starting with any of the item from the list is considered to be suspicious


allowedFrequencyPerMinute = 40
frequencyBanDays = 10  # for how many days ban the ip address, which sends frequent requests; 0 = forever
frequencyViolationsMaxTries = 3  # how many bans will be temporary (next one is permanent)

ban4SuspiciousURLs = False  # NOT A FOOLPROOF FEATURE. Be sure allowedURLs list is correct! 
suspiciousURLsBanDays = 1  # for how many days ban the ip address, which visited suspicious url; 0 = forever
suspiciousURLsTolerance = 3  # how many URL errors are ok. 
suspiciousURLViolationsMaxTries = 3  # how many bans will be temporary (next one is permanent)


daysToLookBack = 30


infoFilePath = "./ngs_info.txt"  


dbPath = "./ngsimpsta.sqlite"
