#!/usr/bin/env python
import requests as req
import re
import telegram as tel
import telegram.ext as tex
import logging
import Finder
import time
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

start = time.time()
result = Finder.Search("yavar hamishe momen")
end = time.time()
print("time taked: "+str(end-start))
print(result)
