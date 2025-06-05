
class User {
    String username;
    String password;

    public User(String username, String password) {
        this.username = username;
        this.password = password;
    }
}

class Authenticator extends User {
    private static final String VALID_USERNAME = "admin";
    private static final String VALID_PASSWORD = "password123";

    public Authenticator(String username, String password) {
        super(username, password);
    }

    public boolean authenticate() {
        return username.equals(VALID_USERNAME) && password.equals(VALID_PASSWORD);
    }
}

public class AuthenticationSystem {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java AuthenticationSystem <username> <password>");
            return;
        }
        String user = args[0];
        String pass = args[1];
        Authenticator auth = new Authenticator(user, pass);
        if (auth.authenticate()) {
            System.out.println("Access Granted");
        } else {
            System.out.println("Access Denied");
        }
    }
}
