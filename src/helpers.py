from htmlnode import *
from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            #check it for current type
            split = node.text.split(delimiter)
            inside_delimiter = False
            for part in split:
                if len(part) == 0:
                    inside_delimiter = not inside_delimiter
                    continue
                
                if inside_delimiter:
                    new_nodes.append(TextNode(part, text_type))
                else:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                inside_delimiter = not inside_delimiter

            if not inside_delimiter:
                # we ended while still inside a delimiter, raise exception
                raise ValueError(f"Unmatched delimiter {delimiter} in text: {node.text}")
        else:
            # doesn't match, just add it
            new_nodes.append(node)
            continue
    return new_nodes

def extract_markdown_images(text):
    # regex that finds link and splits into alt text and url
    whole_link_reg = r"!\[([^\]]*)\]\(([^)]+)\)"
    return re.findall(whole_link_reg, text)

def extract_markdown_links(text):
    #regex that finds link and splits into text and url
    whole_link_reg = r"(?<!\!)\[([^\]]+)\]\(([^)]+)\)"
    return re.findall(whole_link_reg, text)

def split_nodes_image(old_nodes):
    #regext that finds image link and selects whole thing
    whole_image_link_reg_select_all = r"(!\[([^\]]*)\]\(([^)]+)\))"
    return split_nodes_help(old_nodes, whole_image_link_reg_select_all, TextType.IMAGE)        

def split_nodes_link(old_nodes):
    #regex that finds link and selects whole thing
    whole_link_reg_select_all = r"(?<!\!)(\[([^\]]*)\]\(([^)]+)\))"
    return split_nodes_help(old_nodes, whole_link_reg_select_all, TextType.LINK)

def split_nodes_help(old_nodes, reg, text_type):
    new_nodes = []
    for node in old_nodes:
        current_index = 0
        if node.text_type == TextType.TEXT:
            found_links = re.findall(reg, node.text)

            for found_link in found_links:
                alt_text = found_link[1]
                link = found_link[2]

                start_index = node.text.find(found_link[0])
                end_index = start_index + len(found_link[0])

                #there is plain text we need to add first
                if current_index != start_index:
                    new_text = TextNode(node.text[current_index:start_index], TextType.TEXT)
                    #print(f"Insert beginning text node with text: {new_text.text}")
                    new_nodes.append(new_text)
                    current_index = start_index
                
                #the first/next thing is a link
                new_nodes.append(TextNode(alt_text, text_type, link))
                #print(f"insert link/image text with val: {alt_text}-{link}")
                current_index = end_index

            #there may be text after the last link
            if current_index < len(node.text):
                new_nodes.append(TextNode(node.text[current_index:], TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = [node]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes

