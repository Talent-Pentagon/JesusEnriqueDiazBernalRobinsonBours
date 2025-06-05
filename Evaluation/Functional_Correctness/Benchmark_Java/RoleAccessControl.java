// Filename: RoleAccessControl.java

class Role {
    String roleName;

    public Role(String roleName) {
        this.roleName = roleName;
    }
}

class AdminRole extends Role {
    public AdminRole(String roleName) {
        super(roleName);
    }

    public boolean canPerform(String action) {
        // Admins can perform "read", "write", "delete". Others only "read".
        switch (action.toLowerCase()) {
            case "read":
            case "write":
            case "delete":
                return true;
            default:
                return false;
        }
    }
}

class UserRole extends Role {
    public UserRole(String roleName) {
        super(roleName);
    }

    public boolean canPerform(String action) {
        return action.equalsIgnoreCase("read");
    }
}

public class RoleAccessControl {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java RoleAccessControl <role> <action>");
            return;
        }
        String role = args[0];
        String action = args[1];
        boolean allowed;
        if (role.equalsIgnoreCase("admin")) {
            AdminRole admin = new AdminRole(role);
            allowed = admin.canPerform(action);
        } else {
            UserRole user = new UserRole(role);
            allowed = user.canPerform(action);
        }
        System.out.println(allowed ? "Allowed" : "Denied");
    }
}
