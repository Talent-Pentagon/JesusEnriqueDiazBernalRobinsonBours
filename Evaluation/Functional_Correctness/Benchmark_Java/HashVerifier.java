// Filename: HashVerifier.java

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

class Data {
    String message;
    String hash;

    public Data(String message, String hash) {
        this.message = message;
        this.hash = hash;
    }
}

class SHA256Verifier extends Data {
    public SHA256Verifier(String message, String hash) {
        super(message, hash);
    }

    public boolean verify() {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] computedBytes = digest.digest(message.getBytes());
            StringBuilder sb = new StringBuilder();
            for (byte b : computedBytes) {
                sb.append(String.format("%02x", b));
            }
            String computedHash = sb.toString();
            return computedHash.equalsIgnoreCase(hash);
        } catch (NoSuchAlgorithmException e) {
            return false;
        }
    }
}

public class HashVerifier {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java HashVerifier <message> <sha256Hash>");
            return;
        }
        String msg = args[0];
        String hsh = args[1];
        SHA256Verifier verifier = new SHA256Verifier(msg, hsh);
        System.out.println(verifier.verify() ? "Match" : "No Match");
    }
}
