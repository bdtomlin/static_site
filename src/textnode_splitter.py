from textnode import TextNode, TextType


def splitter(node, delimiter, text_type):
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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        delims = node.text.count(delimiter)
        if (delims % 2) != 0:
            raise Exception(
                "Unbalanced delimiters. If your are nesting delimiters, it is unsupported."
            )

        new_nodes.extend(splitter(node, delimiter, text_type))

    return new_nodes
