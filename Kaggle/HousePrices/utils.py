__version__ = "0.01"

class Compare:
    """Context manager to track an object and print the change in shape.

    Examples:
        >> df.shape
        (5, 2)
        >>  with Compare(df) as cm:
                do_something_to(df)
                cm.register(df)

        Shape after:  (3, 1)
        Dropped 2 (-40.0%) rows
        Dropped 1 columns
    """
    def __init__(self, obj):
        self.old = obj

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        try:
            self.new
        except AttributeError:
            raise Exception("Call .register method on context manager to report changes in an object.")

        if self.new.shape == self.old.shape:
            print("No change in shape")
        else:
            # rows
            delta_rows = self.new.shape[0] - self.old.shape[0]
            if delta_rows != 0:
                abs_row_change_str = f"{'Dropped' if delta_rows < 0 else 'Added'} {abs(delta_rows)}"
                rel_row_change_str = f"{round(delta_rows / self.old.shape[0] * 100, 2)}%"
                row_change_str = f"{abs_row_change_str} ({rel_row_change_str}) rows"
            else:
                row_change_str = ""

            # cols
            delta_cols = self.new.shape[1] - self.old.shape[1]
            if delta_cols != 0:
                col_change_str = f"{'Dropped' if delta_cols < 0 else 'Added'} {abs(delta_cols)} columns"
            else:
                col_change_str = ""

            print(f"Shape before: {self.old.shape}\nShape after:  {self.new.shape}")
            print(row_change_str)
            print(col_change_str)

    def register(self, obj):
        """Register changes in object."""
        self.new = obj