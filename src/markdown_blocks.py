import re


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = map(lambda b: b.strip(), blocks)
    blocks = filter(lambda b: b != "", blocks)
    blocks = list(blocks)
    return blocks


def block_to_block_type(block):
    if is_heading(block):
        return heading_type(block)
    elif is_code(block):
        return "code"
    elif is_quote(block):
        return "quote"
    elif is_ul(block):
        return "ul"
    elif is_ol(block):
        return "ol"
    else:
        return "p"


def strip_block(block):
    if is_heading(block):
        return strip_heading(block)
    elif is_code(block):
        return strip_code(block)
    elif is_quote(block):
        return strip_quote(block)
    elif is_ul(block):
        return strip_ul(block)
    elif is_ol(block):
        return strip_ol(block)
    else:
        return block


def is_heading(block):
    return len(re.findall(r"^#{1,6}\s", block))


def strip_heading(block):
    return re.sub(r"#{1,6}\s", "", block, count=1)


def heading_type(block):
    hashes = block.split(" ", 1)[0]
    level = len(hashes)
    return f"h{level}"


def is_code(block):
    return block.startswith("```") and block.endswith("```")


def strip_code(block):
    return block.strip("```")


def is_quote(block):
    lines = block.split("\n")
    filtered = filter(lambda line: line.startswith("> "), lines)
    return len(lines) == len(list(filtered))


def strip_quote(block):
    return re.sub(r"^>\s", "", block)


def is_ul(block):
    lines = block.split("\n")

    def filter_func(line):
        return line.startswith("* ") or line.startswith("- ")

    filtered = filter(filter_func, lines)
    return len(lines) == len(list(filtered))


def strip_ul(block):
    return re.sub(r"^\*\s", "", block, count=1)


def is_ol(block):
    lines = block.split("\n")

    for i in range(len(lines)):
        if lines[i].startswith(f"{i+1}. "):
            continue
        return False
    return True


def strip_ol(block):
    return re.sub(r"^\d+\.\s", "", block)

    return True
