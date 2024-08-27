import sqlobject as SO
import time;
import datetime;
from decimal import Decimal, getcontext

getcontext().prec = 100;

# pip install SQLObject[mysql]
database = 'mysql://root:root@localhost/prog2';

__connection__=SO.connectionForURI(database);

# def __init__(self,user, password):
# self.user = user;
# self.password = password;
# id = SO.IntCol(); #PK FK
class Clients(SO.SQLObject):
    user = SO.StringCol(length = 40, varchar = True);#UNIQUE
    surname = SO.StringCol(length = 40, varchar = True);
    password = SO.StringCol(length = 200, varchar = True);
    dni = SO.IntCol();#UNIQUE
    email = SO.StringCol(length = 120, varchar = True);
    since = SO.IntCol();
    active = SO.IntCol();
    client = SO.MultipleJoin('Account');
    # accounts = SO.MultipleJoin('Account');
class Exchange(SO.SQLObject):
    exchangeType = SO.StringCol(length=80, varchar=True)# Definiendo correctamente el tipo de cambio
    active = SO.IntCol()
    exchange = SO.MultipleJoin('Account');
class Account(SO.SQLObject):
    client = SO.ForeignKey('Clients',default = None, cascade = False);#UNIQUE
    # clientId = SO.ForeignKey('Clients',default = None, cascade = False);#UNIQUE
    exchange = SO.ForeignKey('Exchange',default = None, cascade = False);#UNIQUE
    # exchangeId = SO.ForeignKey('Exchange',default = None, cascade = False);#UNIQUE
    balance = SO.DecimalCol(size=12,precision=2);#Ver que onda esto
    active = SO.IntCol();
class Transactions(SO.SQLObject):
    create_by = SO.StringCol(length = 40, varchar = True)
    origin_acount = SO.StringCol(length = 80, varchar = True)
    origin_amount = SO.DecimalCol(size=12,precision=2);
    destination_acount = SO.StringCol(length = 80, varchar = True)
    destination_amount = SO.DecimalCol(size=12,precision=2);
    time = SO.IntCol()
    active = SO.IntCol()
    user = SO.MultipleJoin('Clients');
    
# id = SO.IntCol(); #PK FK
# origin_acount = SO.ForeignKey('Exchange',default = None, cascade = False); 
# destination_acount = SO.ForeignKey('Exchange',default = None, cascade = False); 
    
    
# id = SO.IntCol(); #PK FK
# Account.dropTable();
# Clients.dropTable();
# Exchange.dropTable();
# Transactions.dropTable();
Exchange.createTable(ifNotExists=True);
Clients.createTable(ifNotExists=True);
Account.createTable(ifNotExists=True);
Transactions.createTable(ifNotExists=True);
class Bdd_methods:

    def __init__(self):
        # self.ARS = Exchange(exchangeType='ARS', active=1);
        pass;
    # ARS = Exchange(exchangeType = 'ARS', active = 1);

    # def timestamp():
    #     since = datetime.datetime.now();
    #     timestamp = since.timestamp();
    #     return timestamp;
    def createTransaction(self, user, origin_account, origin_amount, destination_acount,destination_amount):
        since = datetime.datetime.now();
        timestamp = since.timestamp();
        origin_account = origin_account.upper().strip();
        origin_amount = Decimal(origin_amount).quantize(Decimal('0.00'));
        destination_acount = destination_acount.upper().strip();
        destination_amount = Decimal(destination_amount).quantize(Decimal('0.00'));
        
        transaction = Transactions(create_by = user, origin_acount = origin_account, origin_amount = origin_amount, destination_acount = destination_acount,destination_amount = destination_amount, time = timestamp, active = 1);
        if(transaction):
            return True;
        else:
            return False;
    def getTime(self, timestamp):
        date_time = datetime.datetime.fromtimestamp(timestamp)
        date_str = date_time.strftime('%Y-%m-%d %H:%M:%S')
        return(date_str);
    def getTransactions(self,user):
        user = user.lower().strip();
        
        getAll = Transactions.select(Transactions.q.create_by == user);
        return getAll;
            

    def getLogin(self, user):
    # def getLogin(self, user, password):
        # user = self.user;
        user = user.lower().strip();
            
        res = Clients.select(SO.AND(Clients.q.user == user, Clients.q.active == 1));
        if res:
            return res[0].password;
        else:
            return False;
    def getId(self, user):
        user = user.lower().strip();
            
        res = Clients.select(SO.AND(Clients.q.user == user, Clients.q.active == 1));
        
        if res.count() > 0:
            return res[0].id;
        else:
            return False;
    def getExchangeId(self, account_name):
        account_name = account_name.upper().strip();
            
        res = Exchange.select(SO.AND(Exchange.q.exchangeType == account_name, Exchange.q.active == 1));
        
        if res.count() > 0:
            return res[0].id;
        else:
            return False;
        
    def getRegister(self,user):
        user = user.lower().strip();
        
        res = Clients.select(SO.AND(Clients.q.user == user, Clients.q.active == 1));
        
        if res.count() > 0:
            return False;
        else:
            return True;
        
    def Register(self, user, surname, password, dni, email):
        user = user.lower().strip();
        surname = 'Test';
        dni = 11222333;
        email = 'test@gmail.com';
        since = datetime.datetime.now();
        timestamp = since.timestamp();
        
        if user == "" or surname == "" or password == "" or dni == "" or email == "" or since == "":
            raise Exception("Es necesario completar todos los campos.");
        # if not all([user, surname, password, dni, email, since]):
        #     raise Exception("Es necesario completar todos los campos.")
        else:
            newUser = Clients(user = f"{user}", surname = f"{surname}", password = f"{password}", dni = dni, email = f"{email}", since = timestamp,active = 1);
            newExchange = Exchange(exchangeType = "ARS", active = 1);
            
            getId = self.getId(user);
            selectUser = Clients.get(getId);
            userId = selectUser.id;
            getExchangeId = self.getExchangeId('ARS');
            
            newAccount = Account(client = userId, exchange = getExchangeId, balance = 0.00, active = 1);
            
            transaction = Transactions(create_by = user, origin_acount = 'ARS', origin_amount = '0.00', destination_acount = "",destination_amount = '0.00', time = timestamp, active = 1)
                        
            if newUser and newExchange and newAccount and transaction:
                return True;
            else:
                return False;
        
    def addAccount(self,user,account_name):
        account_name = account_name.upper().strip();
        getId = self.getId(user);
        selectUser = Clients.get(getId);
        userId = selectUser.id;
        getExchangeId = self.getExchangeId(account_name);
        
        newAccount = Account(client = userId, exchange = getExchangeId, balance = 0.00, active = 1);
        
        if newAccount:
            return True;
        else:
            return False;
        
    def add_to_ars(self, user, account_value):
        userId = self.getId(user);
        account = 'ARS';
        account_decimal_value = Decimal(account_value).quantize(Decimal('0.00'));
        getExchangeId = self.getExchangeId(account);
        since = datetime.datetime.now();
        timestamp = since.timestamp();
        
        getArsAccount = Account.select(SO.AND(Account.q.client == userId, Account.q.exchange == getExchangeId ))
    
        
        newValue = (Decimal(getArsAccount[0].balance).quantize(Decimal('0.00')) + account_decimal_value);
        
        getArsAccount[0].balance = newValue;
    
        transaction = Transactions(create_by = user, origin_acount = account, origin_amount = account_decimal_value, destination_acount = account,destination_amount = account_decimal_value, time = timestamp, active = 1)
        
        
    def updateAccountValue(self, user, account_name, account_value):
        
        userId = self.getId(user);
        account_name = account_name.upper().strip();
        getExchangeId = self.getExchangeId(account_name);
        account_decimal_value = Decimal(account_value).quantize(Decimal('0.00'));
        
        getArsAccount = Account.select(SO.AND(Account.q.client == userId, Account.q.exchange == getExchangeId ));
        
        newValue = (Decimal(getArsAccount[0].balance).quantize(Decimal('0.00')) + account_decimal_value);
        
        
        getArsAccount[0].balance = newValue;
    def add_or_update_account(self, user, account_name, account_value):
        
        userId = self.getId(user);
        account_name = account_name.upper().strip();
        getExchangeId = self.getExchangeId(account_name);
        account_decimal_value = Decimal(account_value).quantize(Decimal('0.00'));
        
        getArsAccount = Account.select(SO.AND(Account.q.client == userId, Account.q.exchange == getExchangeId ));
        
        if getArsAccount.count() > 0:
    
            newValue = (Decimal(getArsAccount[0].balance).quantize(Decimal('0.00')) + account_decimal_value);
            getArsAccount[0].balance = newValue;
            
        else:
            newExchange = Exchange(exchangeType = account_name, active = 1);
            getExchangeId = self.getExchangeId(account_name);
            newAccount = Account(client = userId, exchange = getExchangeId, balance = 0.00, active = 1);
    def update_origin_account(self, user, account_name, account_value):
        
        userId = self.getId(user);
        account_name = account_name.upper().strip();
        getExchangeId = self.getExchangeId(account_name);
        account_decimal_value = Decimal(account_value).quantize(Decimal('0.00'));
        
        getArsAccount = Account.select(SO.AND(Account.q.client == userId, Account.q.exchange == getExchangeId ));
        
        newValue = (Decimal(getArsAccount[0].balance).quantize(Decimal('0.00')) - account_decimal_value);
        
        getArsAccount[0].balance = newValue;
        
    def getAccouts(self,user):
        userId = self.getId(user);
        
        getAllAccounts = Account.select(SO.AND(Account.q.client == userId, Account.q.active == 1, Account.q.exchange == Exchange.q.id ));   
        
        return getAllAccounts;
        
    def getAmmount(self, user, account_name, account_value):
            account_name = account_name.upper().strip();    
            userId = self.getId(user);
            account_decimal_value = Decimal(account_value).quantize(Decimal('0.00'));
            getExchangeId = self.getExchangeId(account_name);

            getArsAccount = Account.select(SO.AND(Account.q.client == userId, Account.q.exchange == getExchangeId ))
            
            if account_decimal_value <= Decimal(getArsAccount[0].balance):
                return True;
            else:
                return False;