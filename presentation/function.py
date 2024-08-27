import msvcrt;
import sys
from time import time;
from config import TIMEOUT
import time;
import datetime;
def masked_input(prompt):
        password = ''
        sys.stdout.write(prompt)
        sys.stdout.flush()
        while True:
            ch = msvcrt.getch().decode('utf-8')
            if ch == '\r' or ch == '\n':
                sys.stdout.write('\n')
                break
            elif ch == '\x03': 
                raise KeyboardInterrupt
            elif ch == '\b':
                if password:
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
                    password = password[:-1]
            else:
                sys.stdout.write('*')
                sys.stdout.flush()
                password += ch
        return password
    
def options():
    print(f"{change_color.BOLD}Menú: {change_color.ENDC}");
    print(f"{change_color.OKBLUE}1. Realizar un déposito en su cuenta en ARS.{change_color.ENDC}");
    print(f"{change_color.OKCYAN}2. Realizar una Transacción de una cuenta a otra.{change_color.ENDC}");
    # print(f"{change_color.OKBLUE}3. Agregar cuenta.{change_color.ENDC}");
    print(f"{change_color.OKCYAN}3. Visualizar historial de transacciones.{change_color.ENDC}");
    print(f"{change_color.HEADER}4. Salir{change_color.ENDC}");
    
def timer():
    timeNow = time.time();

    x=input(f'{change_color.WARNING}Está seguro que desea realizar dicha operación?{change_color.ENDC}');

    if((time.time() - timeNow)<TIMEOUT):
        #print("Ok");
        return True;
    else:
        #print("Timeout");
        return False;
def getTime(timestamp):
        date_time = datetime.datetime.fromtimestamp(timestamp)
        date_str = date_time.strftime('%Y-%m-%d %H:%M:%S')
        return(date_str);
    
class change_color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    
   
