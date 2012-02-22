class sortable_list(list):
    def sorted(self, *args, **kwargs):
        # This next line scares the hell out of me O_o
        li = sortable_list(self)
        li.sort(*args, **kwargs)
        return li