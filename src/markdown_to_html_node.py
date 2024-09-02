import re
from inline_markdown import text_to_textnodes
from leafnode import LeafNode
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
)
from parentnode import ParentNode
from textnode import TextNode, TextType


def markdown_to_html_node(markdown):
    block_nodes = []

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_nodes.append(block_to_html_node(block))

    return ParentNode("div", block_nodes)


def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        return heading_html(block, block_type)

    match block_type:
        case "code":
            return code_html(block)
        case "quote":
            return quote_html(block)
        case "ul":
            return ul_html(block)
        case "ol":
            return ol_html(block)
        case _:
            return p_html(block)


def heading_html(block, block_type):
    stripped = re.sub(r"#{1,6}\s", "", block, count=1)
    text_nodes = text_to_textnodes(stripped)
    leaves = map(lambda tn: tn.to_html_node(), text_nodes)
    return ParentNode(block_type, leaves)


def code_html(block):
    stripped = block.strip("```")
    html_node = TextNode(stripped, TextType.TEXT).to_html_node()
    code_node = ParentNode("code", [html_node])
    pre_node = ParentNode("pre", [code_node])
    return pre_node


def quote_html(block):
    lines = block.split("\n")
    lines = map(lambda line: line.replace("> ", "", 1), lines)
    new_block = "\n".join(lines)

    text_nodes = text_to_textnodes(new_block)
    leaves = map(lambda tn: tn.to_html_node(), text_nodes)

    return ParentNode("blockquote", leaves)


def ul_html(block):
    lines = block.split("\n")
    lis = []
    for i in range(len(lines)):
        stripped = re.sub(r"^\*\s", "", lines[i])
        text_nodes = text_to_textnodes(stripped)
        html_nodes = map(lambda tn: tn.to_html_node(), text_nodes)
        lis.append(ParentNode("li", html_nodes))
    return ParentNode("ul", lis)


def ol_html(block):
    lines = block.split("\n")
    lis = []
    for i in range(len(lines)):
        stripped = re.sub(r"^d+\.\s", "", lines[i])
        text_nodes = text_to_textnodes(stripped)
        html_nodes = map(lambda tn: tn.to_html_node(), text_nodes)
        lis.append(ParentNode("li", html_nodes))
    return ParentNode("ol", lis)


def p_html(block):
    text_nodes = text_to_textnodes(block)
    html_nodes = map(lambda tn: tn.to_html_node(), text_nodes)
    return ParentNode("p", html_nodes)
