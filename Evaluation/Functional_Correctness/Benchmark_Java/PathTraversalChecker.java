// Filename: PathTraversalChecker.java

class FilePath {
    String path;

    public FilePath(String path) {
        this.path = path;
    }
}

class TraversalChecker extends FilePath {
    public TraversalChecker(String path) {
        super(path);
    }

    public boolean isUnsafe() {
        return path.contains("../") || path.contains("..\\");
    }
}

public class PathTraversalChecker {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Usage: java PathTraversalChecker <filePath>");
            return;
        }
        String fp = args[0];
        TraversalChecker checker = new TraversalChecker(fp);
        System.out.println(checker.isUnsafe() ? "Unsafe" : "Safe");
    }
}
