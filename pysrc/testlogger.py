import logging
logging.basicConfig(filename='mylog.log', 
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s', 
                    datefmt='%m-%d-%Y %I:%M:%S')
logging.warning('This is a warning message.')
