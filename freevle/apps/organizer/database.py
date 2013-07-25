from freevle import db

class CommaSeperatedInteger(db.TypeDecorator):
    impl = db.String

    def process_bind_param(self, value, dialect):
        if type(value) != list:
            raise TypeError('expected list instance, {} found'
                            ''.format(type(value)))
        for i, v in enumerate(value):
            if type(v) != int:
                raise TypeError('sequence item {}: expected int instance, {} found'
                                ''.format(i, type(v)))
        out = ','.join(str(x) for x in value)
        if len(out) > self.impl.length:
            raise ValueError("the list is too long to save in this String "
                             "column with length {}.".format(self.impl.length))
            # And if you're now here to rewrite this code to use db.Text, don't!
            # If you need a list this long, you ought to be making a table for it.
        return out

    def process_result_value(self, value, dialect):
        return list(int(x) for x in value.split(','))
