# The watcher uses nodemon since more pythonic tools seem to restart too often which causes 
# telegram to detect that there is more than one instance of the bot open and crashing on start
nodemon interfaces\telegram_bot.py