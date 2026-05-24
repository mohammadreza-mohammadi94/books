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
    books_dir = ROOT / "books"

    if not books_dir.exists():
        return books

    for file in books_dir.rglob("*"):
        if (
            file.is_file()
            and file.suffix.lower() in BOOK_EXTENSIONS
            and not any(part in IGNORE for part in file.parts)
        ):
            relative_path = file.relative_to(ROOT)

            if len(relative_path.parts) >= 2:
                category = relative_path.parts[1]
            else:
                category = "Uncategorized"

            books.append((category, relative_path))

    return sorted(books, key=lambda x: (x[0], x[1]))


def generate_book_section():
    books = get_books()

    if not books:
        return "No books available yet. Add PDF/EPUB files to the `books/` directory."

    output = []
    current_category = None

    for category, path in books:
        if category != current_category:
            current_category = category
            category_name = category.replace("-", " ").replace("_", " ").title()
            output.append(f"\n### {category_name}\n")

        file_name = path.stem
        encoded_path = str(path).replace(" ", "%20")

        file_ext = path.suffix.upper().lstrip(".")

        output.append(f"- [{file_name}]({encoded_path}) `.{file_ext}`")

    return "\n".join(output)


def update_readme():
    if not README.exists():
        initial_content = """# 📚 Book Collection

This repository contains my collection of technical books.

<!-- BOOKS-LIST:START -->
<!-- BOOKS-LIST:END -->

## About
Automatically updated book list.
"""
        README.write_text(initial_content, encoding="utf-8")

    content = README.read_text(encoding="utf-8")

    start_marker = "<!-- BOOKS-LIST:START -->"
    end_marker = "<!-- BOOKS-LIST:END -->"

    if start_marker not in content or end_marker not in content:
        content += f"\n\n{start_marker}\n{end_marker}\n"
        README.write_text(content, encoding="utf-8")
        content = README.read_text(encoding="utf-8")

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
