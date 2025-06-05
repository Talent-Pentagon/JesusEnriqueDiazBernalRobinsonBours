// Filename: CSRFTokenGenerator.java

class Request {
    String userId;
    String sessionId;

    public Request(String userId, String sessionId) {
        this.userId = userId;
        this.sessionId = sessionId;
    }
}

class CSRFToken extends Request {
    public CSRFToken(String userId, String sessionId) {
        super(userId, sessionId);
    }

    public String generate() {
        // Simple concatenation: userId|sessionId
        return userId + "|" + sessionId;
    }
}

public class CSRFTokenGenerator {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java CSRFTokenGenerator <userId> <sessionId>");
            return;
        }
        String uid = args[0];
        String sid = args[1];
        CSRFToken token = new CSRFToken(uid, sid);
        System.out.println(token.generate());
    }
}
