def generate_ping_pong_text(filename="ping_pong.txt", num_lines=5000):
    """
    Generates a text file with alternating "ping" and "pong" lines,
    with a "pung" exception.

    Args:
        filename (str, optional): The name of the output text file.
            Defaults to "ping_pong.txt".
        num_lines (int, optional): The number of lines to generate.
            Defaults to 5000.
    """
    with open(filename, "w") as f:
        for i in range(num_lines):
            if i == 0:
                f.write("ping\n")
            elif i == 2501:
                f.write("pung\n")
            elif i % 2 == 0:
                f.write("ping\n")
            else:
                f.write("pong\n")

    print(f"Generated {num_lines} lines of text and saved to {filename}")

if __name__ == "__main__":
    generate_ping_pong_text()

