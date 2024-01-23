import re

no_width_space = '\u200C'
single_space = ' '
to_be_changed_map = {'ئ': 'ی', 'ي': 'ی', 'یٰ':'ی', 'ك': 'ک', 'ة': 'ه', 'ؤ': 'و', 'آ': 'ا',
              'أ': 'ا', 'ٱ': 'ا', 'إ': 'ا','1': '۱', '2': '۲', '3': '۳', '4': '۴',
              '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹', '0': '۰', '-': ' ', '/': ' ', '\\': ' ',
              '\u200c': no_width_space, '\u200B': no_width_space, '\u200D': no_width_space, '\u00ad': no_width_space,
              '\xad': no_width_space, '\u200f': no_width_space,
              '\u0020': single_space, '\u00a0': single_space, '\u0009': single_space, '\u000a': single_space,
              '\u2002': single_space, '\u2003': single_space, '\u2004': single_space, '\u2005': single_space,
              '\u2006': single_space, '\u2007': single_space, '\u2008': single_space, '\u2009': single_space,
              '\u200a': single_space,
              '﷽': "بسم-الله-الرحمن-الرحیم", 'ﷻ': "الله-جل-جلاله",
              'ﷺ': "صلی-الله-علیه-وسلم", 'ﷲ': "الله", 'ﷳ': "اکبر",
              'ﷴ': "محمد", 'ﷵ': "صلی-الله-علیه-وسلم", 'ﷶ': "رسول",
              'ﷷ': 'علیه-السلام', 'ﷸ': "صلی-الله-علیه-وسلم", 'ﷹ': "صلی-الله-علیه-وسلم",
              '%': "درصد", '٪': "درصد", '_': ' ', 'ـ': ' ', 'ۀ': 'ه', 'ة': 'ه'
              }

to_be_deleted_chars = ['\u064b', '\u064c', '\u064d', '\u064e', '\u064f', '\u0650',
                 '\u0651', '\u0621', '\u0652', '\u0670', '\u0654', '\u0640',
                 '۞', '۩','\ufdf2', '\u0611', '\u0612', '\u0613',
                 '\u0614', '\u0615', '\u0616', '\u0617', '\u0618', '\u0619',
                 '\u0620', '!', ',', '?', ':', '،', '؛', '.', '(', ')', '؟', '«', '»',
                 '#', '*', '《', '》', '\"', '[', ']', '{', '}'] # fathe, zamme, in-place type of "صلی الله", punctuations, ...

special_subwords_after = ["ی", "ای", "ها", "های", "هایی", "تر", "تری", "ترین", "گر", "گری", "وری", 
                           "ام", "ات", "اش", "مان", "تان", "شان", "گانه", ] # how to deal with words like شأن
special_subwords_before = ["می", "نمی"]
numbers = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']

# replaces or deletes the arabic characters (or other invalid characters)
def replace_or_delete_invalid_chars(str: str):
    norm_str = []
    for i in range(len(str)):
        if str[i] in to_be_deleted_chars:
            continue
        elif str[i] in to_be_changed_map:
            # avoiding to add multiple space characters one after each other
            if len(norm_str) >= 1 and (norm_str[-1] == no_width_space or norm_str[-1] == single_space)\
                    and (to_be_changed_map[str[i]] == no_width_space or to_be_changed_map[str[i]] == single_space):
                continue
            else:
                norm_str.append(to_be_changed_map[str[i]])
        else:
            norm_str.append(str[i])
    
    return "".join(norm_str)


# making space between numbers and words if needed (fixing something like ماده۷۴)
def make_space_between_numbers_and_words(str: str):
    norm_str = []
    for i in range(len(str)):
        if len(norm_str) >= 1:
            if str[i] in numbers and norm_str[-1] not in numbers:
                if norm_str[-1] == no_width_space:
                    norm_str[-1] = single_space
                else:
                    norm_str.append(single_space)
                
            elif str[i] == no_width_space and norm_str[-1] in numbers:
                norm_str.append(single_space)
                continue
            elif str[i] not in numbers and norm_str[-1] in numbers:
                norm_str.append(single_space)
            
        norm_str.append(str[i])
    
    return "".join(norm_str)

# replaces single spaces with no-width space if the next or previous word is in special words list
def concat_special_subwords(str: str):
    norm_str = []
    words = str.split(single_space)
    length = len(words)

    for i in range(length):
        space_type = ""
        if i - 1 >= 0 and words[i - 1] in special_subwords_before:
            space_type = no_width_space
        elif words[i] in special_subwords_after:
            space_type = no_width_space
        else:
            space_type = single_space
        
        norm_str.append(space_type)        
        norm_str.append(words[i])
    
    return "".join(norm_str)


# normalizes the given string using some other functions
def normalize(str: str):
    str = replace_or_delete_invalid_chars(str)
    str = make_space_between_numbers_and_words(str)
    str = concat_special_subwords(str)
    return str

    
