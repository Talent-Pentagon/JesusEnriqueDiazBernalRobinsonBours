// Filename: AccountLockoutChecker.java

class LoginAttempt {
    String username;
    int failures;

    public LoginAttempt(String username, int failures) {
        this.username = username;
        this.failures = failures;
    }
}

class LockoutChecker extends LoginAttempt {
    public LockoutChecker(String username, int failures) {
        super(username, failures);
    }

    public boolean isLocked() {
        return failures >= 3;
    }
}

public class AccountLockoutChecker {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java AccountLockoutChecker <username> <failureCount>");
            return;
        }
        String user = args[0];
        int count;
        try {
            count = Integer.parseInt(args[1]);
        } catch (NumberFormatException e) {
            System.out.println("FailureCount must be an integer.");
            return;
        }
        LockoutChecker lockout = new LockoutChecker(user, count);
        System.out.println(lockout.isLocked() ? "Locked" : "Active");
    }
}
