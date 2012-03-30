class my_list(list):
    def sorted(self):
        # This next line scares the hell out of me O_o
        li = my_list(self)
        li.sort()
        return li