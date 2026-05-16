from pathlib import Path

ROOT = Path(".")
README = ROOT / "README.md"

IGNORE = {
    ".git",
    ".github",
    "__pycache__",
    ".DS_Store",
}

BOOK_EXTENSIONS = {
    ".pdf",
    ".epub",
    ".mobi",
    ".djvu",
    ".azw3",
}


def get_books():
    books = []

    for file in ROOT.rglob("*"):
        if (
            file.is_file()
            and file.suffix.lower() in BOOK_EXTENSIONS
            and not any(part in IGNORE for part in file.parts)
        ):
            relative_path = file.relative_to(ROOT)

            category = (
                relative_path.parts[0]
                if len(relative_path.parts) > 1
                else "General"
            )

            books.append((category, relative_path))

    return sorted(books)


def generate_book_section():
    books = get_books()

    if not books:
        return "No books available yet."

    output = []
    current_category = None

    for category, path in books:
        if category != current_category:
            current_category = category
            output.append(f"\n### {category}\n")

        file_name = path.stem
        encoded_path = str(path).replace(" ", "%20")

        output.append(
            f"- [{file_name}]({encoded_path})"
        )

    return "\n".join(output)


def update_readme():
    content = README.read_text(encoding="utf-8")

    start_marker = "<!-- BOOKS-LIST:START -->"
    end_marker = "<!-- BOOKS-LIST:END -->"

    generated_content = generate_book_section()

    start_index = content.index(start_marker)
    end_index = content.index(end_marker)

    new_content = (
        content[: start_index + len(start_marker)]
        + "\n\n"
        + generated_content
        + "\n\n"
        + content[end_index:]
    )

    README.write_text(new_content, encoding="utf-8")


if __name__ == "__main__":
    update_readme()
