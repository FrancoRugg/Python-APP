from business.validator import validator;
from presentation.function import masked_input, options, timer, change_color, getTime;
class app:        
    def main(self):
        print(f'{change_color.WARNING}\n Bienvenido!\n {change_color.ENDC}{change_color.BOLD}\n Si cuenta con usuario ingrese L, sinó registrarse ingresando R \n{change_color.ENDC}');
        entry = input(f"{change_color.HEADER}Ingrese L o R: {change_color.ENDC}").upper().strip();
        try:
            if entry != "L" and entry != "R":
                raise Exception("Ingrese un valor correcto para proceder con su registro o logueo");
            else:
                if entry == "L":
                    user = input("Ingrese su usuario: ");
                    # password = input("Ingrese su contraseña: ");
                    password = masked_input("Ingrese su contraseña: ");
                    
                    valid = validator(user,password);
                    
                    valid.validate(user,password);
                    getAllAccounts = valid.getAllAccounts(user)
                    print(40*'-');
                    
                    print('Listado de cuentas: ');
                    
                    for account in getAllAccounts:
                        print(f"Exchange Type: {account.exchange.exchangeType}, Balance: {account.balance}")
                    
                    print(40*'-');
                    option = '';
                    while option != 4:
                        options();
                        opcion = input("Elige una opción: ")

                        if opcion == '1':
                            print(f"{change_color.BOLD}Elegiste la Opción 1 \n{change_color.ENDC}")
                            account_value = input("Ingrese su depósito: ");
                            if float(account_value) < 0:
                                print(f"{change_color.FAIL}Ingrese un importe >= 0.\n{change_color.ENDC}");
                            else:
                                timeout = timer();
                                if(timeout):
                                    valid.updateARS(user, account_value);
                                    getAllAccounts = valid.getAllAccounts(user)
                                    print(40*'-');
                                    
                                    print('Listado de cuentas: ');
                                    
                                    for account in getAllAccounts:
                                        print(f"Exchange Type: {account.exchange.exchangeType}, Balance: {account.balance}")
                                    
                                    print(40*'-');
                                else:
                                    raise Exception('Tiempo Excedido.\nImposible realizar la operación.');
                        elif opcion == '2':
                            print(f"{change_color.BOLD}Elegiste la Opción 2\n{change_color.ENDC}")
                            origin_account = input("Ingrese nombre de la cuenta origen: ");
                            origin_value = input("Ingrese el valor a convertir nuevo valor: ");
                            destiny_account = input("Ingrese nombre de la cuenta destino: ");
                            if float(origin_value) < 0:
                                print(f"{change_color.FAIL}Ingrese un importe >= 0.\n{change_color.ENDC}");
                            else:
                                timeout = timer();
                                if(timeout):
                                    valid.transaction(user, origin_account, origin_value, destiny_account);
                                    getAllAccounts = valid.getAllAccounts(user)
                                    print(40*'-');
                                    
                                    print('Listado de cuentas: ');
                                    
                                    for account in getAllAccounts:
                                        print(f"Exchange Type: {account.exchange.exchangeType}, Balance: {account.balance}")
                                    
                                    print(40*'-');
                                else:
                                    raise Exception('Tiempo Excedido.\nImposible realizar la operación.');
                        # elif opcion == '3':
                        #     print(f"{change_color.BOLD}Elegiste la Opción 3\n{change_color.ENDC}")
                        #     account_name = input("Ingrese nombre de la cuenta a crear: ");
                        #     print(f"{change_color.BOLD}(El valor de la misma se iniciará en 0) \n{change_color.ENDC}");
                        #     #account_value = input("Ingrese un nuevo valor: ");
                        #     # if float(account_value) < 0:
                        #     #     print(f"{change_color.FAIL}Ingrese un importe >= 0.\n{change_color.ENDC}");
                        #     # else:
                        #     timeout = timer();
                        #     if(timeout):
                        #         valid.addOrUpdateAccount(user, account_name, '0.00');
                        #     else:
                        #         raise Exception('Tiempo Excedido.\nImposible realizar la operación.');
                        elif opcion == '3':
                            print(f"{change_color.BOLD}Elegiste la Opción 3\n{change_color.ENDC}")
                            getAll = valid.getTransactions(user);
                            print('Transacciones realizadas: ');
                            print(40*'-');
                            for transaction in getAll:
                                times = getTime(transaction.time);
                                print(f"-Realizada por: {transaction.create_by}, Cuenta origen: {transaction.origin_acount}, Cuenta destino: {transaction.destination_acount} \n Monto enviado de la cuenta origen: {transaction.origin_amount}, Monto ingresado a la cuenta destino: {transaction.destination_amount} el día {times}. \n")                            
                            print(40*'-');
                            
                        elif opcion == '4':
                            print(f"{change_color.WARNING}Saliendo del programa...{change_color.ENDC}");
                            break;
                        else:
                            print(f"{change_color.FAIL}Elija una opción correcta (╬▔皿▔)╯ \n{change_color.ENDC}");
                    
                if entry == "R":
                    user = input("Elija su usuario: ");
                    password = masked_input("Elija su contraseña: ");
                    
                    if user != '' and password != '':
                        User = validator(user,password);
                        # password = User.hashPassword(password);
                        
                        User.newUser(user,password)
                        print(f"{change_color.OKGREEN}New User!{change_color.ENDC}")

                    else:
                        raise Exception('Ingrese datos en ambos campos');
                    
                    
        # except ZeroDivisionError as e: #para debuguear mejor los errores.
        except Exception as e:
            print(e.args[0]);
            
                
                
            