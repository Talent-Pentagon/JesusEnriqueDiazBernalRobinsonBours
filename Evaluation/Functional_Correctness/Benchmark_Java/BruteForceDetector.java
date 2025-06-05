// Filename: BruteForceDetector.java

class Attempt {
    String ipAddress;
    int attempts;

    public Attempt(String ipAddress, int attempts) {
        this.ipAddress = ipAddress;
        this.attempts = attempts;
    }
}

class BruteForce extends Attempt {
    public BruteForce(String ipAddress, int attempts) {
        super(ipAddress, attempts);
    }

    public boolean isSuspected() {
        // If attempts exceed 5, flag as suspected
        return attempts > 5;
    }
}

public class BruteForceDetector {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java BruteForceDetector <ipAddress> <attemptCount>");
            return;
        }
        String ip = args[0];
        int count;
        try {
            count = Integer.parseInt(args[1]);
        } catch (NumberFormatException e) {
            System.out.println("AttemptCount must be an integer.");
            return;
        }
        BruteForce bf = new BruteForce(ip, count);
        System.out.println(bf.isSuspected() ? "Suspected" : "Normal");
    }
}
