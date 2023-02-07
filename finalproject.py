# Ali Yazdanifar
import os
import time
# import networkx as nx
# from matplotlib import pyplot as plt, rcParams
# from networkx.drawing.nx_pydot import graphviz_layout

charcount = dict()


# this function read data from text file
def readfile(filename="input"):
    text = ""
    my_file = open(filename + ".txt", "r")
    # data = my_file.readline()
    for i in my_file:
        text += i
    my_file.close()
    return text


# this function fill charcount dictionary and sort chars according to weights
def maketable():
    _set, data = set(), readfile()
    charcount.clear()
    for i in data:
        _set.add(i)
    for i in _set:
        charcount[i] = list()
        charcount[i].append(data.count(i))
    sorted_dict = sorted(charcount, key=lambda item: charcount[item[0]])
    temp = [Node(charcount[i][0], i) for i in sorted_dict]
    sorted_dict = temp
    return sorted_dict


class Node:
    def __init__(self, weg: int, val=""):
        self.value = val  # its for value of each character
        self.weight = weg  # its for weight of each character
        self.specialnumber = None  # its for save 0, 1 for each char to calculate haffmancode
        self.left = None
        self.right = None
        self.huffmancode = None

    def makechild(self, node_left, node_right):
        self.right = node_right
        self.left = node_left


class Tree:
    def __init__(self):
        self.nodes = maketable()
        self.__maketree__()

    def __maketree__(self):
        while 1 < len(self.nodes):
            temp = Node(self.nodes[0].weight + self.nodes[1].weight)
            self.nodes[0].specialnumber = '0'
            self.nodes[1].specialnumber = '1'
            temp.makechild(self.nodes[0], self.nodes[1])
            del self.nodes[0]
            del self.nodes[0]
            self.nodes.append(temp)
            self.nodes = sorted(self.nodes, key=lambda weg: weg.weight)

    def huffmancode(self):
        i, last_nod, curr, num = 0, list(), self.nodes[0], ""
        length = len(charcount)
        while i < length:
            if curr.value != "":
                curr.huffmancode = num
                charcount[curr.value].append(num)
                num = num[0:len(num) - 1]
                i += 1
                while curr == last_nod[-1].right:
                    curr = last_nod[-1]
                    num = num[0:len(num) - 1]
                    last_nod.pop()
                    if not last_nod:
                        break
                else:
                    curr = last_nod[-1]
                    curr = curr.right
                    num += curr.specialnumber
            else:
                num += curr.left.specialnumber
                last_nod.append(curr)
                curr = curr.left

    def writetofile(self):
        my_file = open("Huffman_codes.txt", 'w')
        content = ""
        for i in charcount:
            if i == '\n':
                content = content + "ENTER" + ' ' + charcount[i][1] + '\n'
            elif i == ' ':
                content = content + "SPACE" + ' ' + charcount[i][1] + '\n'
            elif i == '\t':
                content = content + "TAB" + ' ' + charcount[i][1] + '\n'
            else:
                content = content + i + ' ' + charcount[i][1] + '\n'
            my_file.write(content)
            content = ""
        my_file.close()

    def makeoutput(self):
        data = readfile()
        my_file = open("output.txt", 'w')
        content = ""
        for i in data:
            content += charcount[i][1]
        my_file.write(content)
        my_file.close()

    # def show_tree(self):
    #     i, length, last_nod, curr, dinodes, temp, dup_nodes = 0, len(charcount), list(), self.nodes[
    #         0], list(), list(), list()
    #     counter = 1
    #     while i < length:
    #         if curr.value != "":
    #             if curr.value == '\n':
    #                 temp.append("Enter")
    #             elif curr.value == ' ':
    #                 temp.append("space")
    #             elif curr.value == '\t':
    #                 temp.append("tab")
    #             else:
    #                 if '0' <= curr.value <= '9':
    #                     temp.append(str(' ' * counter * 2) + str(curr.weight) + str(' ' * counter * 2))
    #                 else:
    #                     temp.append(curr.value)
    #             dinodes.append(temp.copy())
    #             i += 1
    #             while curr == last_nod[-1].right:
    #                 curr = last_nod[-1]
    #                 temp.pop()
    #                 last_nod.pop()
    #                 if not last_nod:
    #                     break
    #             else:
    #                 curr = last_nod[-1]
    #                 temp.pop()
    #                 curr = curr.right
    #
    #         else:
    #             if curr.weight not in dup_nodes:
    #                 dup_nodes.append(curr.weight)
    #                 temp.append(str(curr.weight))
    #             else:
    #                 temp.append(str(' ' * counter) + str(curr.weight) + str(' ' * counter))
    #             last_nod.append(curr)
    #             curr = curr.left
    #             counter += 1
    #     G = nx.Graph()
    #     for i in dinodes:
    #         nx.add_path(G, i)
    #     os.environ["PATH"] += os.pathsep + "/usr/bin/dot"
    #     rcParams['figure.figsize'] = 14, 10
    #     pos = graphviz_layout(G, prog='dot')
    #     nx.draw(G, pos=pos,
    #             node_color='lightgreen',
    #             node_size=1500,
    #             with_labels=True,
    #             arrows=True)
    #     plt.show()


if __name__ == "__main__":
    choose = 0
    # Menu :
    while choose != 4:
        os.system('cls')
        choose = int(input(
            "use data from :\n1 - file (input.txt)\n2 - console\n3 - show tree\n4 - EXIT\nEnter your desired option : "))
        if choose == 1:
            a = Tree()
            a.huffmancode()
            a.writetofile()
            a.makeoutput()
            os.system('cls')
            print("Done!")
            time.sleep(1)
        elif choose == 2:
            os.system('cls')
            content = ""
            new_data = input("Enter your text : ")
            temp = readfile()
            my_file = open("input.txt", 'w')
            my_file.write(new_data)
            my_file.close()
            a = Tree()
            a.huffmancode()
            for i in new_data:
                content += charcount[i][1]
            print(f"output : {content}")
            my_file = open("input.txt", 'w')
            my_file.write(temp)
            my_file.close()
            input()
        # elif choose == 3:
        #     a = Tree()
        #     a.show_tree()
    os.system('cls')

# some example for test:
#       aaaaeeeefffhhiimmnnssttloprux
# aaaaaaaaaaeeeeeeeeeeeeeeeiiiiiiiiiiiiooouuuussssssssssssst
# aaaaabbbbbbbbbccccccccccccdddddddddddddeeeeeeeeeeeeeeeeffffffffffffffffffffffffffffffffffffffffffffff
# an
# WDOMO 	OMNNooomn
# sw][p;-21-o0
