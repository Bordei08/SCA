import java.io.IOException;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.*;


public class Server {

    private final int port = 3456;
    private ServerSocket serverSocket;
    private Boolean timeOut = true;
    private String [] inputs;

    private Server() throws IOException {
    }

    public static Server getServerInstance() throws IOException {
        return new Server();
    }


    public void startServer() throws IOException {
        serverSocket = new ServerSocket(port);

        System.out.println("Server started...");
        System.out.println("Wating for clients...");

        while (true) {
            Socket clientSocket = serverSocket.accept();
            System.out.println("New client!");
            clientSocket.setSoTimeout(6000000);

            Thread t = new Thread() {
                public void run() {
                    try (
                            PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
                            Scanner in = new Scanner(clientSocket.getInputStream());
                    ) {
                        String role = null;
                        role = in.nextLine();
                        if(Objects.equals(role, "M"))
                            timeOut = false;
                        out.println("");
                        while (in.hasNextLine()) {
                            String input = in.nextLine();
                            System.out.println(role + " : " + input);

                            if (input.equalsIgnoreCase("exit")) {
                                if(Objects.equals(role, "M")){
                                    timeOut = true;
                                }
                                System.out.println("Client disconnected!");
                                break;
                            }
                            if(Objects.equals(role, "M") && !timeOut){
                                out.println(input);
                            }
                            else{
                                out.println("");
                            }
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            };
            t.start();

        }
    }


}