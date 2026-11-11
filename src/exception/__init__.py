import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.logger import logger

def error_message_detail(error: Exception, error_detail: sys) -> str:
   
   
    _, _, exc_tb = error_detail.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename

    line_number = exc_tb.tb_lineno
    error_message = f"Error occurred in python script: [{file_name}] at line number [{line_number}]: {str(error)}"
    
    logger.error(error_message)
    
    return error_message

class MyException(Exception):
   
    def __init__(self, error_message: str, error_detail: sys):
      
        super().__init__(error_message)

        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self) -> str:

        return self.error_message


if __name__ == "__main__":
    try:
        raise ValueError("Test error for MyException")
    except ValueError as error:
        custom_exception = MyException(str(error), sys)
        print(custom_exception)