import re

from textnode import TextNode, TextType


def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "*", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    return text_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        delims = node.text.count(delimiter)
        if (delims % 2) != 0:
            raise Exception(
                "Unbalanced delimiters. If your are nesting delimiters, it is unsupported."
            )

        new_nodes.extend(__splitter(node, delimiter, text_type))

    return new_nodes


def extract_markdown_images(text):
    image_pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(image_pattern, text)


def extract_markdown_links(text):
    link_pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(link_pattern, text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        images = extract_markdown_images(text)
        for image in images:
            first, text = text.split(f"![{image[0]}]({image[1]})", 1)
            if first != "":
                new_nodes.append(TextNode(first, TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text)
        for link in links:
            first, text = text.split(f"[{link[0]}]({link[1]})", 1)
            if first != "":
                new_nodes.append(TextNode(first, TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def __splitter(node, delimiter, text_type):
    if node.text_type != TextType.TEXT:
        return [node]

    new_list = []
    split = node.text.split(delimiter)

    for i in range(len(split)):
        if split[i] == "":
            continue
        if i % 2 == 0:
            new_list.append(TextNode(split[i], TextType.TEXT))
        else:
            new_list.append(TextNode(split[i], text_type))

    return new_list
