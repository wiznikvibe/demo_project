import logging 
import os
from datetime import datetime

# log file holding the execution info 
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M')}.log"
logs_path = os.path.join(os.getcwd(),'log',LOG_FILE)
# append files inside the folder even if it exists
os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path,LOG_FILE)

logging.basicConfig(filename=LOG_FILE_PATH,format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
level=logging.INFO,
)

# # To check if loggin works
# if __name__=='__main__':
#     logging.info("Logging has started.")