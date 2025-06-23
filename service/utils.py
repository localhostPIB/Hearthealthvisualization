import tempfile


def create_temp_file(img_bytes) -> str:
    """
    Creates a temporary file for the diagrams (Plot).

    :param img_bytes: the plot as bytes.
    :returns: The path of the temporary file.
    :rtype: str
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
        temp_img.write(img_bytes)
        temp_img.flush()
        return temp_img.name