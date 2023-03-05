import java.io.IOException;



public class Main {
    public static void main(String[] args) throws IOException {

        Customer customer = new Customer("127.0.0.1",3456);
        customer.startCustomer();

    }

}