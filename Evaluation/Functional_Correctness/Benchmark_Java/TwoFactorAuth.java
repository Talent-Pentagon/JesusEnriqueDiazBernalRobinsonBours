// Filename: TwoFactorAuth.java

class OTP {
    String user;
    String code;

    public OTP(String user, String code) {
        this.user = user;
        this.code = code;
    }
}

class TimeBasedOTP extends OTP {
    public TimeBasedOTP(String user, String code) {
        super(user, code);
    }

    public boolean validate() {
        // For simplicity, assume the only valid code is "123456"
        return code.equals("123456");
    }
}

public class TwoFactorAuth {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java TwoFactorAuth <username> <otpCode>");
            return;
        }
        String user = args[0];
        String code = args[1];
        TimeBasedOTP tfa = new TimeBasedOTP(user, code);
        System.out.println(tfa.validate() ? "OTP Valid" : "OTP Invalid");
    }
}
