// Filename: SQLInjectionDetector.java

class Input {
    String text;

    public Input(String text) {
        this.text = text;
    }
}

class SQLDetector extends Input {
    public SQLDetector(String text) {
        super(text);
    }

    public boolean isVulnerable() {
        String lower = text.toLowerCase();
        return lower.contains(" or ") || lower.contains("drop ") || lower.contains("'--");
    }
}

public class SQLInjectionDetector {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Usage: java SQLInjectionDetector <inputString>");
            return;
        }
        String input = args[0];
        SQLDetector detector = new SQLDetector(input);
        System.out.println(detector.isVulnerable() ? "Vulnerable" : "Safe");
    }
}
