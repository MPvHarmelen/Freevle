class sortable_list(list):
    def sorted(self):
        # This next line scares the hell out of me O_o
        li = sortable_list(self)
        li.sort()
        return li