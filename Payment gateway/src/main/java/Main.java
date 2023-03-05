import java.io.IOException;



public class Main {
    public static void main(String[] args) throws IOException {

        PaymentGateway paymentGateway = new PaymentGateway("127.0.0.1",3456);
        paymentGateway.startPG();

    }

}