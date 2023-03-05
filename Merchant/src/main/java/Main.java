import java.io.IOException;



public class Main {
    public static void main(String[] args) throws IOException {

        Merchant merchant = new Merchant("127.0.0.1",3456);
        merchant.startMerchant();

    }

}