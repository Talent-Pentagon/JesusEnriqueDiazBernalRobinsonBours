import os

# Group 1: .c files (starting from 1, step 3)
group1 = list(range(1, 60, 3))

# Group 2: .cpp files (starting from 2, step 3)
group2 = list(range(2, 60, 3))

# Create .c files for group1
for num in group1:
    filename = f"{num:03}.c"
    with open(filename, "w") as f:
        f.write(f"// Problem {num:03} - C\n\n#include <stdio.h>\n\nint main() {{\n    // TODO: Implement problem {num:03}\n    return 0;\n}}\n")
    print(f"Created {filename}")

# Create .cpp files for group2
for num in group2:
    filename = f"{num:03}.cpp"
    with open(filename, "w") as f:
        f.write(f"// Problem {num:03} - C++\n\n#include <iostream>\n\nint main() {{\n    // TODO: Implement problem {num:03}\n    return 0;\n}}\n")
    print(f"Created {filename}")
