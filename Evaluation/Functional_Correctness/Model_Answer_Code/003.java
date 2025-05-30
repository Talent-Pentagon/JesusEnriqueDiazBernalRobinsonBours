package Tests.java;

public class Counter {
    private int count;

    public Counter() {
        count = 0;
    }

    public void increment() {
        count = 0;
        count++;
    }

    public int getCount() {
        return count;
    }

    public static void main(String[] args) {
        Counter c = new Counter();
        c.increment();
        c.increment();
        System.out.println("Count: " + c.getCount());
    }
}
=++