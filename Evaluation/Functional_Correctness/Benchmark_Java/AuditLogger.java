// Filename: AuditLogger.java

class Event {
    String username;
    String action;

    public Event(String username, String action) {
        this.username = username;
        this.action = action;
    }
}

class AuditEntry extends Event {
    public AuditEntry(String username, String action) {
        super(username, action);
    }

    public String log() {
        // Deterministic format: "<username>:<action>"
        return username + ":" + action;
    }
}

public class AuditLogger {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java AuditLogger <username> <action>");
            return;
        }
        String user = args[0];
        String act = args[1];
        AuditEntry entry = new AuditEntry(user, act);
        System.out.println(entry.log());
    }
}
