class Observer:
    def update(self, message):
        pass

class NotificationService(Observer):
    def update(self, message):
        print("Notificação:", message)

class TransactionLogger(Observer):
    def update(self, message):
        print("Registro de transação:", message)

class AccountManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._accounts = {} 
        return cls._instance

    def add_account(self, account):
        self._accounts[account.cpf] = account

    def get_account(self, cpf):
        return self._accounts.get(cpf)


class Person:
    def __init__(self, name, cpf):
        self._name = name
        self._cpf = cpf

    @property
    def name(self):
        return self._name

    @property
    def cpf(self):
        return self._cpf


class Account(Person):
    def __init__(self, name, cpf, password, balance, credit, phone_credit):
        super().__init__(name, cpf)
        self._password = password
        self._balance = int(balance)
        self._historic = []
        self._credit = int(credit)
        self._loyalty_points = 0
        self._phone_credit = int(phone_credit)
        self._linked_accounts = []
        AccountManager().add_account(self)  
        self._observers = [NotificationService(), TransactionLogger()] 
        
    @property
    def password(self):
        return self._password

    @property
    def historic(self):
        return self._historic

    @property
    def credit(self):
        return self._credit

    @property
    def loyalty_points(self):
        return self._loyalty_points

    @property
    def phone_credit(self):
        return self._phone_credit

    @property
    def linked_accounts(self):
        return self._linked_accounts

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value

    def get_balance(self, password):
        if self.wrong_password(password):
            return None
        return self._balance

    @phone_credit.setter
    def phone_credit(self, value):
        self._phone_credit = value

    @loyalty_points.setter
    def loyalty_points(self, value):
        self._loyalty_points = value

    @credit.setter
    def credit(self, value):
        self._credit = value

    def mobile_recharge_and_bill_payment(self, amount, password, payment_type):
        if self.wrong_password(password):
            return None

        if payment_type not in ['credit', 'debit']:
            print("Tipo de pagamento inválido")
            return None

        if payment_type == 'credit':
            self.credit -= amount
        elif payment_type == 'debit':
            self.balance -= amount

        self.phone_credit += amount
        self.historic.append(["Recarga de Celular/Pagamento de Conta", amount])
        self.notification(True, "Recarga de Celular/Pagamento de Conta")

    def wrong_password(self, password):
        return self.password != password

    def deposit(self, amount_to_deposit, password):
        if self.wrong_password(password):
            return None

        if amount_to_deposit < 0:
            print('Você não pode depositar um valor negativo')
            return None

        self.historic.append(["Depósito", amount_to_deposit])
        self.notification(True, "Depósito")
        self.balance += amount_to_deposit
        self.add_loyalty_points()
        return self.balance

    def get_payment(self, amount_to_deposit, who_sent):
        self.balance += amount_to_deposit
        self.historic.append(["Pagamento de " + who_sent, amount_to_deposit])
        self.notification(True, "Pagamento recebido")
        return self.balance

    def notification(self, notification_status, message):
        if notification_status:
            for observer in self._observers:
                observer.update(message)

    def make_payment(self, amount_to_deposit, account_to_pay, password):
        if self.wrong_password(password):
            return None

        self.historic.append(["Pagamento para " + account_to_pay.name, amount_to_deposit])
        account_to_pay.get_payment(amount_to_deposit, self.name)
        self.balance -= amount_to_deposit
        self.notification(True, "Pagamento")
        self.add_loyalty_points()
        return self.balance

    def get_historic(self, password):
        if self.wrong_password(password):
            return None

        if len(self.historic) == 0:
            print('Não há histórico')
            return None

        for x in range(len(self.historic)):
            print(self.historic[x][0], "----->", self.historic[x][1])

    def add_loyalty_points(self):
        self.loyalty_points += 1

    def link_account(self, account_to_link, password):
        if self.wrong_password(password):
            return None

        self.linked_accounts.append(account_to_link)

    def peer_to_peer_transfer(self, amount_to_transfer, recipient_account, password):
        if self.wrong_password(password):
            return None

        if amount_to_transfer < 0 or amount_to_transfer > self.balance:
            print('Valor de transferência inválido')
            return None

        self.balance -= amount_to_transfer
        recipient_account.balance += amount_to_transfer
        self.historic.append(["Transferência Peer-to-Peer para " + recipient_account.name, amount_to_transfer])
        self.notification(True, "Transferência Peer-to-Peer")
        recipient_account.notification(True, "Recebida Transferência Peer-to-Peer de " + self.name)
