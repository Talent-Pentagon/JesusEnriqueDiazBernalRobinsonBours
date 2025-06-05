// Filename: CertificateValidator.java

class Certificate {
    String domain;
    int expiryYear;

    public Certificate(String domain, int expiryYear) {
        this.domain = domain;
        this.expiryYear = expiryYear;
    }
}

class SSLValidator extends Certificate {
    private static final int CURRENT_YEAR = 2025;

    public SSLValidator(String domain, int expiryYear) {
        super(domain, expiryYear);
    }

    public boolean isValid() {
        return expiryYear >= CURRENT_YEAR;
    }
}

class CertChecker {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java CertChecker <domain> <expiryYear>");
            return;
        }
        String domain = args[0];
        int year;
        try {
            year = Integer.parseInt(args[1]);
        } catch (NumberFormatException e) {
            System.out.println("Expiry year must be an integer.");
            return;
        }
        SSLValidator validator = new SSLValidator(domain, year);
        if (validator.isValid()) {
            System.out.println("Valid");
        } else {
            System.out.println("Expired");
        }
    }
}
