from enum import Enum
from htmlnode import *
from helpers import *
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
def block_to_blocktype(text):
    #regex for each type
    
    #heading - 1-6 # at start of line followed by space
    heading_reg = r"^(#{1,6})\s"

    #code - triple backticks, then code, then triple backticks
    code_reg = r"^```[\s\S]+```$"

    #quote - > at start of every line
    quote_reg = r"^(> .+(\n> .+)*)$"

    #unordered list - lines starting with - followed by space
    unordered_list_reg = r"^-\s"

    #ordered list - lines starting with number followed by . and space.  number must increment by 1
    ordered_list_reg = r"^(\d+\.\s)"

    if re.match(heading_reg, text):
        return BlockType.HEADING
    elif re.match(code_reg, text):
        return BlockType.CODE
    elif re.match(quote_reg, text, re.MULTILINE):
        return BlockType.QUOTE
    elif re.match(unordered_list_reg, text, re.MULTILINE):
        return BlockType.UNORDERED_LIST
    elif re.match(ordered_list_reg, text, re.MULTILINE):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    ret = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block != "":
            ret.append(block)
    
    return ret
    
def markdown_to_html_node(markdown):
    #create a parent node for the entire document
    html_node = ParentNode("div", [])
    #convert markdown to html
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_blocktype(block)
        #print(f"Block: {block}\nType: {block_type}\n")

        if block_type == BlockType.PARAGRAPH:
            html_node.children.append(block_to_paragraph(block))        
        elif block_type == BlockType.CODE:
            html_node.children.append(block_to_code(block))
        elif block_type == BlockType.QUOTE:
            html_node.children.append(block_to_quote(block))
        elif block_type == BlockType.HEADING:
            html_node.children.append(block_to_heading(block))
        elif block_type == BlockType.UNORDERED_LIST:
            html_node.children.append(block_to_unordered_list(block))
        elif block_type == BlockType.ORDERED_LIST:
            html_node.children.append(block_to_ordered_list(block))
        else:
            raise ValueError(f"Unknown block type: {block_type}")
    return html_node

def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        node_to_add = text_node_to_html_node(node)
        #replace newlines in text nodes with spaces
        if node_to_add.value is not None:
            node_to_add.value = node_to_add.value.replace("\n", " ")
        children.append(node_to_add)
    return children

def block_to_paragraph(block):
    paragraph = ParentNode("p", text_to_children(block))
    return paragraph

def block_to_code(block):
    code = ParentNode("code", [])
    #remove the ``` from start and end but do not remove \n or any other characters
    block = re.sub(r"^```[\w]*\n", "", block)
    block = re.sub(r"```$", "", block)
    text_node = TextNode(block, TextType.CODE)    
    return ParentNode("pre", [text_node_to_html_node(text_node)])

def block_to_quote(block):
    #remove > and space from start of every line
    block = re.sub(r"^>\s", "", block, flags=re.MULTILINE)
    quote = ParentNode("blockquote", text_to_children(block))
    return quote

def block_to_heading(block):
    #get number of # at start of line
    match = re.match(r"^(#{1,6})\s", block)
    if not match:
        raise ValueError(f"Invalid heading block: {block}")
    num_hashes = len(match.group(1))
    heading_tag = f"h{num_hashes}"

    #remove the # and space from start of line
    block = re.sub(r"^#{1,6}\s", "", block)
    heading = ParentNode(heading_tag, text_to_children(block))
    return heading

def block_to_unordered_list(block):
    items = block.split("\n")
    li_nodes = []
    for item in items:
        #remove the - and space from start of line
        item = re.sub(r"^-\s", "", item)
        li_nodes.append(ParentNode("li", text_to_children(item)))
    return ParentNode("ul", li_nodes)

def block_to_ordered_list(block):
    items = block.split("\n")
    li_nodes = []
    for item in items:
        #remove the number, . and space from start of line
        item = re.sub(r"^\d+\.\s", "", item)
        li_nodes.append(ParentNode("li", text_to_children(item)))
    return ParentNode("ol", li_nodes)

