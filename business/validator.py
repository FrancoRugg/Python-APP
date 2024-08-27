from data.data_helper import data_helper;
# from data.test import Bdd_methods;
from data.Bdd_methods import Bdd_methods;
import bcrypt;
# from flask import Flask
# from flask_bcrypt import Bcrypt as bcrypt
# app = Flask(__name__)
# bcrypt = bcrypt(app)
from decimal import Decimal, getcontext
getcontext().prec = 100
#pip install getch
# pip install bcrypt
conn = Bdd_methods();
# conn = data_helper();
class validator:
    
    def __init__(self,user,password):
        self.user = user;
        self.password = password;
        
    # def checkPass(self,password,hash):
    #     password = self.password;
    #     # return bcrypt.checkpw(password,hash);
    #     return bcrypt.check_password_hash(password.encode('utf-8'),hash.encode('utf-8'));
    def checkPass(self,password,hash):
        password = self.password;
        return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'));
    def userLoginValidate(self, user, password):
        password = self.password;
        validate = conn.getLogin(user);
        if validate != False:
            return self.checkPass(password,validate);
        
    # def userLoginValidate(self, user, password):
    #     conn = data_helper();
    #     validate = conn.getLogin(user);
    #     if validate != False:
    #         return self.checkPass(self.password, validate);
        
    def userRegisterValidate(self, user):
        # conn = data_helper();
        rv = conn.getRegister(user);
        if rv == False:
            raise ValueError()
    
    # def userRegisterValidate(self, user):
    #     conn = data_helper();
    #     rv = conn.getRegister(user);
    #     if rv == False:
    #         raise ValueError()
    
    # def newUser(self, user, password): #Llevar esta función al 
    #     if self.userRegisterValidate(user):
    #         password = self.hashPassword(password)
    #         conn = data_helper();
    #         conn.newUser(user,password);
    #     else:
    #         raise Exception("Usuario existente ＼（〇_ｏ）／ \n Elija otro nombre de usuario")
    def newUser(self, user, password): #Llevar esta función al 
        try:
            self.userRegisterValidate(user)
            password = self.hashPassword(password)
            conn.Register(user,"",password,0,"");
        except ValueError:
             raise Exception("Usuario existente ＼（〇_ｏ）／ \n Elija otro nombre de usuario")
    
    # def newUser(self, user, password): #Llevar esta función al 
    #     try:
    #         self.userRegisterValidate(user)
    #         password = self.hashPassword(password)
    #         conn = data_helper();
    #         conn.newUser(user,password);
    #     except ValueError:
    #          raise Exception("Usuario existente ＼（〇_ｏ）／ \n Elija otro nombre de usuario")
    def validate(self,user,password):
        user = self.user;
        password = self.password;
        # password = self.hashPassword(self.password);
        if self.userLoginValidate(user,password) == False:
            raise Exception("Usuario inexistente o contraseña incorecta");
        else:
            return True;
            # res = self.getAllAccounts(user);
    def getAllAccounts(self,user):
            getAllAccounts = conn.getAccouts(user);
            return getAllAccounts;
    # def validate(self,user,password):
    #     user = self.user;
    #     password = self.password;
    #     # password = self.hashPassword(self.password);
    #     if self.userLoginValidate(user,password) == False:
    #         raise Exception("Usuario inexistente o contraseña incorecta");
    #     else:
    #         conn = data_helper();
    #         conn.getAccount(user);
            
            #raise Exception("Bienvenido al Home");
        # if self.validatePassword(password) == False:
        #     raise Exception("Contraseña incorrecta");
    def addOrUpdateAccount(self, user, account_name, account_value):
        user = self.user;       
        # result = 
        conn.add_or_update_account(user,account_name,account_value);
        
        # if result:
        # conn.getAccouts(user);
        # res = self.getAllAccounts(user);
        
    # def addOrUpdateAccount(self, user, account_name, account_value):
    #     user = self.user;
    #     conn = data_helper();
        
    #     # result = 
    #     conn.add_or_update_account(user,account_name,account_value);
        
    #     # if result:
    #     conn.getAccount(user);
    
    def updateARS(self, user, account_value):
        user = self.user;
        
        # result = 
        conn.add_to_ars(user,account_value);
        
        # if result:
        # res = self.getAllAccounts(user);
        # conn.getAccouts(user);
        # else:
        #     raise Exception('No se pudieron obtener los datos actualizados de la cuenta.');
    def getTransactions(self,user):
        # res= conn.getTransactions(user);
        getAll = conn.getTransactions(user);
        
        return getAll;    
    def transaction(self, user, origin_account, origin_value, destiny_account):
        origin_account = origin_account.upper().strip();
        destiny_account = destiny_account.upper().strip();
        
        origin_value = Decimal(origin_value);
        getRates = data_helper();
        #Me traigo las tazas de cambio del API y valido que las mismas existan.
        rates = getRates.get_exchange_rates(origin_account,destiny_account);
        if origin_account not in rates or destiny_account not in rates:
            raise Exception('Imposible obtener las tazas de cambio solicitadas.');
        else:
            #Verifico que ambas cuentas existan, sinó las creo
            conn.add_or_update_account(user, origin_account, '0.00');
            conn.add_or_update_account(user, destiny_account, '0.00');
            #Confirmo que los saldos sean suficientes.
            originAmmount = conn.getAmmount(user,origin_account,origin_value);
            if not originAmmount:
                raise Exception('Saldos insuficientes en la cuenta origen.');
            
            originRate = Decimal(rates[origin_account]).quantize(Decimal('0.00'));
            destinyRate = Decimal(rates[destiny_account]).quantize(Decimal('0.00'));
            
            total = ((origin_value / originRate) * destinyRate).quantize(Decimal('0.00'));
            
            # totalAmmount = conn.getAmmount(user, origin_account, origin_value);
            # if not totalAmmount:
            #     raise Exception('Saldos insuficientes en la cuenta origen.');
            # else:
            #Agrego total en cuenta destino
            conn.add_or_update_account(user, destiny_account, total);
            #Resto total de la cuenta origen
            conn.update_origin_account(user, origin_account, origin_value);
            
            #Se crea la transacción
            transaction =conn.createTransaction(user,origin_account,origin_value,destiny_account,total);

            #Me traigo los saldos actualizados
            # res = self.getAllAccounts(user);
            # conn.getAccouts(user);
            
    # def transaction(self, user, origin_account, origin_value, destiny_account):
    #     origin_account = origin_account.upper().strip();
    #     destiny_account = destiny_account.upper().strip();
        
    #     origin_value = Decimal(origin_value);
    #     conn = data_helper();
    #     #Me traigo las tazas de cambio del API y valido que las mismas existan.
    #     rates = conn.get_exchange_rates(origin_account,destiny_account);
    #     if origin_account not in rates or destiny_account not in rates:
    #         raise Exception('Imposible obtener las tazas de cambio solicitadas.');
    #     else:
    #         #Verifico que ambas cuentas existan, sinó las creo
    #         conn.add_or_update_account(user, origin_account, '0.00');
    #         conn.add_or_update_account(user, destiny_account, '0.00');
    #         #Confirmo que los saldos sean suficientes.
    #         originAmmount = conn.getAmmount(user,origin_account,origin_value);
    #         if not originAmmount:
    #             raise Exception('Saldos insuficientes en la cuenta origen.');
            
    #         originRate = Decimal(rates[origin_account]).quantize(Decimal('0.00'));
    #         destinyRate = Decimal(rates[destiny_account]).quantize(Decimal('0.00'));
            
    #         total = ((origin_value / originRate) * destinyRate).quantize(Decimal('0.00'));
            
    #         # totalAmmount = conn.getAmmount(user, origin_account, origin_value);
    #         # if not totalAmmount:
    #         #     raise Exception('Saldos insuficientes en la cuenta origen.');
    #         # else:
    #         #Agrego total en cuenta destino
    #         conn.add_or_update_account(user, destiny_account, total);
    #         #Resto total de la cuenta origen
    #         conn.update_origin_account(user, origin_account, origin_value);
            
    #         #Me traigo los saldos actualizados
    #         conn.getAccount(user);
    
    
    def hashPassword(self,password):
        self.password = password.encode('utf-8');
        # self.password = password;
        sal = bcrypt.gensalt();
        
        # return bcrypt.generate_password_hash(password,10).decode('utf-8');
        return bcrypt.hashpw(self.password,sal).decode('utf-8');


    