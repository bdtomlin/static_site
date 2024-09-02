def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = map(lambda b: b.strip(), blocks)
    blocks = filter(lambda b: b != "", blocks)
    blocks = list(blocks)
    return blocks
