class Message {
    String text;

    public Message(String text) {
        this.text = text;
    }
}

class CaesarCipher extends Message {
    public CaesarCipher(String text) {
        super(text);
    }

    public String encrypt(int shift) {
        StringBuilder sb = new StringBuilder();
        for (char c : text.toCharArray()) {
            if (Character.isLetter(c)) {
                char base = Character.isLowerCase(c) ? 'a' : 'A';
                int offset = (c - base + shift) % 26;
                if (offset < 0)
                    offset += 26;
                sb.append((char) (base + offset));
            } else {
                sb.append(c);
            }
        }
        return sb.toString();
    }
}

public class Encryptor {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java Encryptor <text> <shift>");
            return;
        }
        String text = args[0];
        int shift;
        try {
            shift = Integer.parseInt(args[1]);
        } catch (NumberFormatException e) {
            System.out.println("Shift must be an integer.");
            return;
        }
        CaesarCipher cipher = new CaesarCipher(text);
        System.out.println(cipher.encrypt(shift));
    }
}
