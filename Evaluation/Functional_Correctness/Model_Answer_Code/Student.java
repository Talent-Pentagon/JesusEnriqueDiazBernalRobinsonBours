class Student {
    private String name;
    private int[] grades;

    public Student(String name, int[] grades) {
        this.name = name;
        this.grades = grades;
    }

    public double average() {
        int sum = 0;
        for (int grade : grades)
            sum += grade;
        return grades.length == 0 ? 0 : (double) sum / grades.length;
    }

    public void printInfo() {
        System.out.printf("Student: %s, Average: %.2f%n", name, average());
    }

    public static void main(String[] args) {
        int[] grades = {90, 80, 70, 85};
        Student student = new Student("Alice", grades);
        student.printInfo();
    }
}