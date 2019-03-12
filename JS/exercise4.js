function BankAccount(name, value){
    this.name = name;
    this.balance = value;
    this.deposit = deposit;
    this.withdraw = withdraw;
}
function withdraw(amount){
    if(this.balance - amount >= 0){
        this.balance = this.balance - amount;
    }
    else{console.log("you dont have that much money to withdraw")
    }
}
function deposit(amount){
    this.balance += amount;
}