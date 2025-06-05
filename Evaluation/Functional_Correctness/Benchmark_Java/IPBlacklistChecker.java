// Filename: IPBlacklistChecker.java

class IPAddress {
    String ip;

    public IPAddress(String ip) {
        this.ip = ip;
    }
}

class BlacklistChecker extends IPAddress {
    public BlacklistChecker(String ip) {
        super(ip);
    }

    public boolean isBlacklisted() {
        // Hardcoded blacklist
        return ip.equals("192.168.1.100") || ip.equals("10.0.0.5");
    }
}

public class IPBlacklistChecker {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Usage: java IPBlacklistChecker <ipAddress>");
            return;
        }
        String addr = args[0];
        BlacklistChecker checker = new BlacklistChecker(addr);
        System.out.println(checker.isBlacklisted() ? "Blacklisted" : "Allowed");
    }
}
