// Filename: XSSDetector.java

class Content {
    String html;

    public Content(String html) {
        this.html = html;
    }
}

class XSSChecker extends Content {
    public XSSChecker(String html) {
        super(html);
    }

    public boolean hasXSS() {
        String lower = html.toLowerCase();
        return lower.contains("<script>") || lower.contains("javascript:");
    }
}

public class XSSDetector {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Usage: java XSSDetector <htmlString>");
            return;
        }
        String html = args[0];
        XSSChecker checker = new XSSChecker(html);
        System.out.println(checker.hasXSS() ? "XSSFound" : "Safe");
    }
}
