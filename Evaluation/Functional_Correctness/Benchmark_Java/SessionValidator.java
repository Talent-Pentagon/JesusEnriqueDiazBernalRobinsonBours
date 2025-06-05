// Filename: SessionValidator.java

class Session {
    String sessionId;
    long creationTime; // epoch seconds

    public Session(String sessionId, long creationTime) {
        this.sessionId = sessionId;
        this.creationTime = creationTime;
    }
}

class SecureSession extends Session {
    private static final long CURRENT_TIME = 1700000000L; // Hardcoded reference

    public SecureSession(String sessionId, long creationTime) {
        super(sessionId, creationTime);
    }

    public boolean isActive() {
        // Session is active if creationTime + 3600 > CURRENT_TIME
        return (creationTime + 3600) > CURRENT_TIME;
    }
}

public class SessionValidator {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java SessionValidator <sessionId> <creationTime>");
            return;
        }
        String sessionId = args[0];
        long creation;
        try {
            creation = Long.parseLong(args[1]);
        } catch (NumberFormatException e) {
            System.out.println("CreationTime must be a numeric epoch value.");
            return;
        }
        SecureSession ss = new SecureSession(sessionId, creation);
        System.out.println(ss.isActive() ? "Active" : "Expired");
    }
}
