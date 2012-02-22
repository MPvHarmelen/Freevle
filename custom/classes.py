class sortable_list(list):
    """
    list() -> new empty list
    list(iterable) -> new list initialized from iterable's items
    sortable_list has a sorted() attribute that works the same as sort(), except
    it returns the sorted list in stead of sorting the list and returning None.
    """
    def sorted(self, *args, **kwargs):
        # This next line scares the hell out of me O_o
        li = sortable_list(self)
        li.sort(*args, **kwargs)
        return li