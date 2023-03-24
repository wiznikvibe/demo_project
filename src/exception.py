# Exception Handling Process
import sys
sys.path.insert(0, '../src')
from src.logger import logging

def error_message_details(error,error_detail:sys):
    """Function that would return the error message"""
    _,_,exc_tb= sys.exc_info()
    # File Name 
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message="Error occured in .py file[{0} line num:[{1}]] error message:[{2}]".format(file_name,
    exc_tb.tb_lineno,str(error))
    return error_message

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message

if __name__=='__main__':
    try:
        a=1/0
    except Exception as e:
        logging.info("Divide by Zero ERROR")
        raise CustomException(e,sys)
        

    