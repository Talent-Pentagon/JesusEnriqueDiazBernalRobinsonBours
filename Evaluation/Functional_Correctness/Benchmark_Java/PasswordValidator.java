// Filename: PasswordValidator.java

class Password {
    String password;

    public Password(String password) {
        this.password = password;
    }
}

class StrongPasswordChecker extends Password {
    public StrongPasswordChecker(String password) {
        super(password);
    }

    public boolean isStrong() {
        // For simplicity: must be at least 8 chars, contain a digit and an uppercase
        // letter.
        if (password.length() < 8)
            return false;
        boolean hasDigit = false, hasUpper = false;
        for (char c : password.toCharArray()) {
            if (Character.isDigit(c))
                hasDigit = true;
            if (Character.isUpperCase(c))
                hasUpper = true;
        }
        return hasDigit && hasUpper;
    }
}

public class PasswordValidator {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Usage: java PasswordValidator <password>");
            return;
        }
        String pw = args[0];
        StrongPasswordChecker checker = new StrongPasswordChecker(pw);
        System.out.println(checker.isStrong() ? "Strong" : "Weak");
    }
}
