import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.NoSuchElementException;
import java.util.Scanner;



public class Merchant {

    private String host;
    private int port;

    public Merchant(String host, int port) {
        this.host = host;
        this.port = port;
    }


    public void startMerchant(){
        System.out.println("Client started.");
        try (
                Socket socket = new Socket(host, port);
                PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                Scanner in = new Scanner(socket.getInputStream());
                Scanner s = new Scanner(System.in);
        ) {
            out.println("M");
            while (true) {
                String input = s.nextLine();
                out.println(input);
                if (input.equalsIgnoreCase("exit")) break;
                System.out.println(in.nextLine());
            }
        }catch (NoSuchElementException e) {
            System.out.println("Ai fost deconectat de la server!");
        }catch (IOException e) {
            System.out.println("Serverul este inchis!");
        }
    }

}