class Packet {
    String sourceIP;
    String destIP;
    int port;

    public Packet(String sourceIP, String destIP, int port) {
        this.sourceIP = sourceIP;
        this.destIP = destIP;
        this.port = port;
    }
}

class FirewallRule extends Packet {
    // In this example, we block port 22 (SSH) and port 23 (Telnet).
    public FirewallRule(String sourceIP, String destIP, int port) {
        super(sourceIP, destIP, port);
    }

    public boolean isAllowed() {
        return !(port == 22 || port == 23);
    }
}

public class Firewall {
    public static void main(String[] args) {
        if (args.length < 3) {
            System.out.println("Usage: java Firewall <sourceIP> <destIP> <port>");
            return;
        }
        String src = args[0];
        String dst = args[1];
        int port;
        try {
            port = Integer.parseInt(args[2]);
        } catch (NumberFormatException e) {
            System.out.println("Port must be an integer.");
            return;
        }
        FirewallRule rule = new FirewallRule(src, dst, port);
        if (rule.isAllowed()) {
            System.out.println("Allowed");
        } else {
            System.out.println("Blocked");
        }
    }
}
