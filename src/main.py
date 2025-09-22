from textnode import *



def main():
    test = TextNode("Hello, world!", TextType.PLAIN)
    test2 = TextNode("image", TextType.IMAGE, "http://example.com/image.png")
    print(test)
    print(test2)

if __name__ == "__main__":
    main()