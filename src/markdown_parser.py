from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        split_node_texts = node.text.split(delimiter)

        if len(split_node_texts) % 2 == 0:
            raise Exception(f'"{node.text}" has invalid Markdown syntax!')

        for i in range(0, len(split_node_texts)):
            if split_node_texts[i] == '':
                continue

            new_nodes.append(
                TextNode(
                    split_node_texts[i],
                    TextType.TEXT if i % 2 == 0 else text_type
                )
            )
    
    return new_nodes









