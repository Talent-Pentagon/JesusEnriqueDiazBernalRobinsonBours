// Filename: TokenGenerator.java

class Token {
    String user;
    String timestamp;

    public Token(String user, String timestamp) {
        this.user = user;
        this.timestamp = timestamp;
    }
}

class SimpleTokenGenerator extends Token {
    public SimpleTokenGenerator(String user, String timestamp) {
        super(user, timestamp);
    }

    public String generate() {
        // Deterministic “token” format: user_timestamp (no separators changed)
        return user + "_" + timestamp;
    }
}

public class GenerateToken {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java GenerateToken <username> <timestamp>");
            return;
        }
        String user = args[0];
        String ts = args[1];
        SimpleTokenGenerator gen = new SimpleTokenGenerator(user, ts);
        System.out.println(gen.generate());
    }
}
