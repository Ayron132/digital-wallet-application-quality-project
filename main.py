from account import Account 

def display_menu():
    print("Selecione uma opção:")
    print("1. Criar Conta")
    print("2. Selecionar Conta")
    print("3. Consultar Saldo")
    print("4. Consultar Crédito (conta)")
    print("5. Consultar Crédito do Celular")
    print("6. Depositar")
    print("7. Recarga de Celular")
    print("8. Realizar Pagamento")
    print("9. Transferência Entre Contas")
    print("10. Ver Histórico")
    print("11. Vincular Conta")
    print("Q. Sair")

def create_account():
    name = input("Digite seu nome: ")
    cpf = input("Digite seu CPF: ")
    password = input("Digite sua senha: ")
    balance = float(input("Digite seu saldo inicial: "))
    credit = float(input("Digite seu crédito inicial: "))
    phone_credit = float(input("Digite seu crédito de celular inicial: "))

    new_account = Account(name, cpf, password, balance, credit, phone_credit)
    accounts.append(new_account)
    print(f"Conta criada com sucesso para {name}!")

def select_account():
    print("Selecione uma conta:")
    for i, account in enumerate(accounts):
        print(f"{i + 1}. {account.name}")

    choice = int(input("Digite o número da conta: "))
    if 1 <= choice <= len(accounts):
        return accounts[choice - 1]
    else:
        print("Escolha inválida. Retornando ao menu principal.")
        return None

def main():
    while True:
        display_menu()
        option = input("Digite sua escolha: ").upper()

        if option == '1':
            create_account()

        elif option == '2':
            selected_account = select_account()
            if selected_account is not None:
                account_menu(selected_account)

        elif option == 'Q':
            print("Encerrando o programa.")
            break

        else:
            print("Opção inválida. Por favor, tente novamente.")

def account_menu(account):
    while True:
        print(f"\nMenu da Conta - {account.name}")
        display_menu()
        option = input("Digite sua escolha: ").upper()

        if option == '3':
            password = input("Digite sua senha: ")
            balance = account.get_balance(password)
            if balance is not None:
                print(f"Seu saldo: {balance}")

        elif option == '4':
            password = input("Digite sua senha: ")
            credit = account.credit if not account.wrong_password(password) else None
            if credit is not None:
                print(f"Seu crédito: {credit}")

        elif option == '5':
            password = input("Digite sua senha: ")
            phone_credit = account.phone_credit if not account.wrong_password(password) else None
            if phone_credit is not None:
                print(f"Seu crédito de celular: {phone_credit}")

        elif option == '6':
            password = input("Digite sua senha: ")
            amount_to_deposit = float(input("Digite o valor do depósito: "))
            account.deposit(amount_to_deposit, password)

        elif option == '7':
            password = input("Digite sua senha: ")
            amount = float(input("Digite o valor para recarga de celular/pagamento de conta: "))
            payment_type = input("Digite o tipo de pagamento (crédito/débito): ").lower()
            account.mobile_recharge_and_bill_payment(amount, password, payment_type)

        elif option == '8':
            password = input("Digite sua senha: ")
            amount_to_pay = float(input("Digite o valor para realizar o pagamento: "))
            account_to_pay_name = input("Digite o nome da conta para realizar o pagamento: ")
            account_to_pay = find_account_by_name(account_to_pay_name)
            if account_to_pay is not None:
                account.make_payment(amount_to_pay, account_to_pay, password)
            else:
                print("Conta não encontrada.")

        elif option == '9':
            password = input("Digite sua senha: ")
            amount_to_transfer = float(input("Digite o valor para transferência: "))
            recipient_account_name = input("Digite o nome da conta de destino: ")
            recipient_account = find_account_by_name(recipient_account_name)
            if recipient_account is not None:
                account.peer_to_peer_transfer(amount_to_transfer, recipient_account, password)
            else:
                print("Conta de destino não encontrada.")

        elif option == '10':
            password = input("Digite sua senha: ")
            account.get_historic(password)

        elif option == '11':
            password = input("Digite sua senha: ")
            account_to_link_name = input("Digite o nome da conta para vincular: ")
            account_to_link = find_account_by_name(account_to_link_name)
            if account_to_link is not None:
                account.link_account(account_to_link, password)
                print("Conta vinculada com sucesso.")
            else:
                print("Conta não encontrada.")

        elif option == 'Q':
            print("Retornando ao menu principal.")
            break

        else:
            print("Opção inválida. Por favor, tente novamente.")

def find_account_by_name(account_name):
    for acc in accounts:
        if acc.name == account_name:
            return acc
    return None

if __name__ == "__main__":
    accounts = [] 
    main()
