import re

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

def extract_markdown_images(text):
    return re.findall(r"(?<=\!)\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        
        extracted_images = extract_markdown_images(node.text)

        if (len(extracted_images) == 0):
            new_nodes.append(node)
            continue

        text = node.text
        for extracted_img in extracted_images:
            split_text = text.split(f"![{extracted_img[0]}]({extracted_img[1]})", maxsplit=1)
            
            if (split_text[0] != ''):
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))

            new_nodes.append(TextNode(extracted_img[0], TextType.IMAGE, extracted_img[1]))

            text = split_text[1]

        if text != '':
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        
        extracted_links = extract_markdown_links(node.text)

        if (len(extracted_links) == 0):
            new_nodes.append(node)
            continue

        text = node.text
        for extracted_link in extracted_links:
            split_text = text.split(f"[{extracted_link[0]}]({extracted_link[1]})", maxsplit=1)

            if split_text[0] != '':
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))

            new_nodes.append(TextNode(extracted_link[0], TextType.LINK, extracted_link[1]))

            text = split_text[1]

        if text != '':
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

            







