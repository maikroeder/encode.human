"""
CSV file reading and production of annotated lines
"""
import logging
import codecs
logging.basicConfig()
LOGGER = logging.getLogger()


def unfold(lines, attrkeys):
    """
    Unfold the lines
    """
    unfolded = []
    line_number = 0
    for line in lines:
        line_number = line_number + 1
        url, attrs = line.split('\t')
        new_line = {}
        new_line['line_number'] = line_number
        new_line["File URL"] = url
        for attr in attrs.split(';'):
            attr = attr.strip()
            if attr:
                key, value = attr.split('=')
                key = key.strip()
                if not key in attrkeys:
                    template = "Unknown non-essential attribute on line %s: %s"
                    LOGGER.warn(template % (line_number, key))
                value = value.strip()
                new_line[key] = value
        for key in attrkeys:
            if not key in new_line:
                new_line[key] = None
        unfolded.append(new_line)
    return unfolded


def check(lines, essential):
    """
    Make sure the essential attributes are present on each line.
    Also make sure that the replicate field is not empty.
    """
    checked_lines = []
    for line in lines:
        missing = False
        for attr in essential:
            if not attr in line or line[attr] is None:
                if line['dataType'] == 'AffyExonArray':
                    pass
                else:
                    template = 'Skipping line %s: Attribute missing: %s'
                    LOGGER.error(template % (line['line_number'], attr))
                missing = True
        if not missing:
            replicate = line['replicate']
            replicate = str(replicate).strip()
            if replicate in ('', 'None'):
                template = 'Skipping line %s: Replicate is empty: %s'
                LOGGER.error(template % (line['line_number'], replicate))
                missing = True

        if not missing:
            checked_lines.append(line)

    return checked_lines


def filter_unknown(lines, raw, processed):
    """
    The type should be either raw or processed. If it is neither, the type should be
    added to the raw.txt or the processed.txt file.
    """
    filtered = []
    for line in lines:
        if line['type'] in raw or line['type'] in processed:
            filtered.append(line)
        else:
            template = 'Unknown type on line %s: %s (%s)'
            message = 'Include it either in the raw.txt or processed.txt files'
            LOGGER.error(template % (line['line_number'], line['type'], message))
    return filtered



def parse(file_path):
    """
    Parse a CSV file and return the parsed lines and the context
    information needed for rendering.
    """
    lines = []
    inputfile = codecs.open(file_path, 'r', encoding='utf-8')
    lines = inputfile.readlines()
    inputfile.close()

    inputfile = codecs.open('encode/human/attributes.txt', 'r', encoding='utf-8')
    attrkeys = [a.strip() for a in inputfile.readlines() if a.strip()]
    inputfile.close()

    lines = unfold(lines, attrkeys)

    inputfile = codecs.open('encode/human/essential.txt', 'r', encoding='utf-8')
    essential = [a.strip() for a in inputfile.readlines() if a.strip()]
    inputfile.close()

    lines = check(lines, essential)

    inputfile = codecs.open('encode/human/raw.txt', 'r', encoding='utf-8')
    raw = [a.strip() for a in inputfile.readlines() if a.strip()]
    inputfile.close()

    inputfile = codecs.open('encode/human/processed.txt', 'r', encoding='utf-8')
    processed = [a.strip() for a in inputfile.readlines() if a.strip()]
    inputfile.close()

    lines = filter_unknown(lines, raw, processed)
    return lines
