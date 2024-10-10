# Importing necessary libraries

import time

def get_current_time():
    return str(time.localtime().tm_mday) + '-' + str(time.localtime().tm_mon) + '-' + str(time.localtime().tm_year)
