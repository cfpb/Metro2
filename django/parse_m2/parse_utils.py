from datetime import datetime


date_format = "%m%d%Y"

class UnreadableFileException(Exception):
    pass

class UnreadableLineException(Exception):
    pass


def cast_to_type(input: str, type_str: str):
    """
    Given a string input and a type indicator, cast the
    string value to the given type. Throw an UnreadableLineException
    if it can't be cast.

    Inputs:
    `input` - the string to be converted
    `type_str` - one of the following: "string", "numeric",
                 "date", or "date optional"
    """
    if type_str == "string":
        return input.strip()
    if type_str == "numeric":
        try:
            return int(input)
        except ValueError:
            msg = f"Numeric value `{input}` could not be parsed as int"
            raise UnreadableLineException(msg)
    if type_str == "date" or type_str == "date optional":
        if len(input) != 8:
            msg = f"Date value `{input}` must have length 8, instead had {len(input)}"
            raise UnreadableLineException(msg)
        try:
            return datetime.strptime(input, date_format)
        except ValueError:
            if type_str == "date":
                msg = f"Date value `{input}` could not be parsed as date"
                raise UnreadableLineException(msg)
            else:
                return None


def get_field_value(field_ref: dict, field_name: str, line: str):
    """
    For one field listed in fields.py, get the value from the given segment
    and cast it to the type indicated.

    Inputs:
    `field` - a tuple in the form of (int, int) or (int, int, str)
              which represents the start index and end index of the
              target value, and a type (defaults to "string")
    `line` - the string (segment) from which to get the value
    """
    field = field_ref[field_name]

    # Unpack the tuple that contains the field info
    try:
        field_start, field_end, field_type = field
    except ValueError:
        field_start, field_end = field
        # default to string if no type is provided
        field_type = "string"

    try:
        # Throw an error if the desired indices don't exist in the string
        if len(line) < field_end:
            msg = f"Segment too short: looking for index {field_end}, " + \
                f"but segment length is {len(line)}"
            raise UnreadableLineException(msg)

        # Get the string between start and end indices.
        # The CRRG (and fields.py) uses string positions that start at 1,
        # but python indicates string position starting at 0.
        # So we use `field_start-1` to adjust for the difference.
        target_str = line[field_start - 1: field_end]

        # Cast the string to the given type
        result =  cast_to_type(target_str, field_type)

    except UnreadableLineException as e:
        # Add context to the error message that comes out of cast_to_type
        msg = f"Field name: `{field_name}`. Indices: {field_start}-{field_end}. Field_type `{field_type}`. " \
               + f"Input: `{line}`. Issue detail: " + str(e)
        raise UnreadableLineException(msg)

    return result
