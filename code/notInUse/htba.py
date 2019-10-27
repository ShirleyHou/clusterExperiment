def htb(data):
    """
    Function to compute the head/tail breaks algorithm on an array of data.
    Params:
    -------
    data (list): array of data to be split by htb.
    Returns:
    --------
    outp (list): list of data representing a list of break points.
    """
    # test input
    assert data, "Input must not be empty."
    assert all(isinstance(_, int) or isinstance(_, float) for _ in data), "All input values must be numeric."

    outp = []  # array of break points

    def htb_inner(data):
        """
        Inner ht breaks function for recursively computing the break points.
        """
        data_length = float(len(data))
        data_mean = sum(data) / data_length
        head = [_ for _ in data if _ > data_mean]
        outp.append(data_mean)
        while len(head) > 1 and len(head) / data_length < 0.25:
            return htb_inner(head)
    htb_inner(data)
    return outp