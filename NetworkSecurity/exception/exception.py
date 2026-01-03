import sys
import os
from NetworkSecurity.logging.logger import logging



class NetworkSecurityException(Exception): #error_detail is the traceback of the exception
    def __init__(self, error_message, error_detail: sys): #error_detail is the traceback of the exception
        super().__init__(error_message)
        self.error_message = error_message
        _,_,exc_tb= error_detail.exc_info() #error_detail.exc_info() returns a tuple of (type, value, traceback) so we are unpacking it and using traceback as exc_tb to get the line number and file name where the exception occurred
        self.line_no=exc_tb.tb_lineno #exc_tb.tb_lineno returns the line number where the exception occurred
        self.file_name=exc_tb.tb_frame.f_code.co_filename #exc_tb.tb_frame.f_code.co_filename returns the file name where the exception occurred
        

    def __str__(self):
        return "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.file_name,
            self.line_no,
            str(self.error_message),
            )
        
if __name__=="__main__":
    try:
        logging.info("Enter the try block")
        a=1/0
        print("this will not be printed as:",a)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


"""
exception.py file creation and usage:

You created a project-specific exception
You inherited from Python's built-in Exception class
Your class is a child, Exception is the parent
You use super().__init__(error_message) to pass the message to the base exception

"""
