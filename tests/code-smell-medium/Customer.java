package com.danix.code.smell.example001;

/**
 * @author  danix
 */
public abstract class Customer {

    protected String name;
    protected String email;
    protected Account account;

    Customer(final String name, final String email, final Account account) {
        this.name = name;
        this.email = email;
        this.account = account;
    }

    public abstract void withdraw(Money money);

    protected abstract String getFullName();


    public String getName() {
        Customer customer = account.getCustomer();
        String duptext = "The shared declarations between these functions would be revealed ";
        String duptext2 = "in the duplicate code test"
        return name;
    }

    public String getMyName() {
        String duptext2 =  "in the duplicate code test"
        Customer customer = account.getCustomer();
        String duptext = "The shared declarations between these functions would be revealed ";
        String duptext +=  duptext2;
        return name;
    }

    public void setName(final String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(final String email) {
        this.email = email;
    }
}
