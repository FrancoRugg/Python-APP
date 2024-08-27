import json;
from decimal import Decimal, getcontext
import requests as rq 
# from requests import Request as rq 
#pip install requests
getcontext().prec = 100
class data_helper:
    
    def __init__(self):
        pass;
    # def serialize(self):
    #     with open('users.json', 'w') as f:
    #         f.write(json.dumps(self.toDict(),indent=4)); #f.write es lo mismo que print, en json es más amigable pq no hay que pasarlo a modo de tupla. indent=4, usa la indentación de 4 espacios.
    # def deserialize(self):
        # with open('users.json', 'r') as f:
        #     aux = json.loads(f.read());#Te devuelve todo lo que encuentre.
        # return self.fromDict(aux); #
                
    # def toDict(self):
        # rv = {}; #Return Value, valor de retorno.
        # for attr in self.dictattributes:
        #     aux = getattr(self, attr, 'null');#Necesita 3 params, obj, el nombre de lo que quieras obtener y un valor por defecto. Se le dice reflection a dicha técnica.
        #     rv.update({attr:aux});
        # return rv;
    # def fromDict(self,dataDict):
        # for attr in self.dictattributes:
        #     setattr(self, attr, dataDict[attr]);
        # return self;
    # def newUserInJson(self,user,password):
    #     try:
    #         with open('users.json', 'r') as f:
    #                 data = json.load(f)
    #     except (FileNotFoundError, json.decoder.JSONDecodeError):
    #             data = []
    #     data.append({'user': user.lower().strip(), 'password': password.decode('utf-8')})
        
    #     with open('users.json', 'w') as f:
    #         json.dump(data, f, indent=4)
    def get_exchange_rates(self, org, dst):
        symbols = f"{org},{dst}"
        url = f"http://data.fixer.io/api/latest?access_key=f3a24b68620fab1336ea9d8b2b6fcbf4&symbols={symbols}"
        res = rq.get(url)
        x = res.json()
        l = x['rates'];
        return l
        # return res.json().get('rates', {});
    
    def newUserInJson(self, user, password):
        try:
            with open(user + '.json', 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = []

        data.append({
            'user': user.lower().strip(),
            'password': password.decode('utf-8'),
            'accounts': [
                {
                'name': "ARS",
                'value': "0.00"}
            ]
        })

        with open(user + '.json', 'w') as f:
            json.dump(data, f, indent=4)
    def getAccount(self, user):
        try:
            with open(user+'.json','r') as f:
                data = json.load(f);
                # print(data);
                print(40*'-');
                print('Listado de cuentas: ');
                for elem in data:
                    accounts = elem['accounts'];
                    for e in accounts:
                        print(e['name'],e['value']);
                print(40*'-');
                        
        except FileNotFoundError:
            return False;
    def getAmmount(self, user, account_name, account_value):
        account_name = account_name.upper().strip();
        account_decimal_value = Decimal(account_value).quantize(Decimal('0.00'));
        try:
            with open(user+'.json', 'r') as f:
                data = json.load(f);
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = [];
        for account in data[0]['accounts']:                
            if account['name'] == account_name:
                if account_decimal_value <= Decimal(account['value']):
                    return True;
                else:
                    return False;
    def add_or_update_account(self, user, account_name, account_value):
        account_name = account_name.upper().strip();
        account_decimal_value = Decimal(account_value).quantize(Decimal('0.00'));
        try:
            with open(user+'.json', 'r') as f:
                data = json.load(f);
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = [];
        account_exist = False;
        for account in data[0]['accounts']:                
            if account['name'] == account_name:
                account['value'] = str(Decimal(account['value']) + account_decimal_value);
                account_exist = True;
                break;

        if not account_exist:
            data[0]['accounts'].append({'name': account_name, 'value': str(Decimal(account_value))});

        with open(user + '.json', 'w') as f:
            json.dump(data, f, indent=4);
    def update_origin_account(self, user, account_name, account_value):
        account_name = account_name.upper().strip();
        account_decimal_value = Decimal(account_value).quantize(Decimal('0.00'));
        try:
            with open(user+'.json', 'r') as f:
                data = json.load(f);
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = [];
        for account in data[0]['accounts']:                
            if account['name'] == account_name:
                account['value'] = str(Decimal(account['value']).quantize(Decimal('0.00')) - account_decimal_value);
                break;

        with open(user + '.json', 'w') as f:
            json.dump(data, f, indent=4);
    def add_to_ars(self, user, account_value):
        account_decimal_value = Decimal(account_value).quantize(Decimal('0.00'));
        try:
            with open(user + '.json', 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = [{'accounts': [{'name': 'ARS', 'value': '0.00'}]}];

        for account in data[0]['accounts']:
            if account['name'] == "ARS":
                account['value'] = str(Decimal(account['value']).quantize(Decimal('0.00')) + account_decimal_value)
                break

        with open(user + '.json', 'w') as f:
            json.dump(data, f, indent=4)
    def getRegister(self,user):
        try:
            with open(user+".json", "r") as f:
                data = json.load(f)
                for elem in data:
                    if elem['user'] == user.lower().strip():
                        return False;
        except FileNotFoundError:
            return True
    def getLogin(self,user):
        with open(user+".json", "r") as f:
            data = json.load(f)
            for elem in data:
                if elem['user'] == user:
                    return elem['password'];
            return False;
    
    def newUser(self,user,password):
        self.newUserInJson(user,password)