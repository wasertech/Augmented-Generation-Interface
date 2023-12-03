"""
Translate the guidebook to other languages.
This script uses interpres (Translator) to translate sentences.
Please make sure you have installed it in the current environment before running this script.
"""

import os, sys
from glob import glob

try:
    import questionary as q
    from translator import Translator
    from translator.language import get_nllb_lang
except ImportError as ie:
    raise ImportError("Please install the translator module to translate the guidebook.\
        \nUsing pip:\n$\
        pip install interpres") from ie

def get_guidebook_files(func="**/*"):
    """
    Returns a list of all markdown files in the guidebook directory.
    """
    return glob(f'guidebook/{func}.md', recursive=True)

def get_guidebook_content(md_list: list):
    """
    Returns a list of all markdown files in the guidebook directory.
    """
    return [open(file, 'r', encoding='utf-8').read() \
        for file in md_list]

def split_markdown_guide(md: str):
    """Splits markdown guide into action, guide and examples.

    Args:
        md (str): Markdown guide.

    Returns:
        tuple: Action, guide and examples. 
    """
    return [md.split("\n")[0].lstrip("# ")] + \
            [x.strip() for x in md.split("## Intent Examples")]

def get_guides_intent_examples(guidebook: list):
    """Get guides and intent examples from guidebook.

    Args:
        guidebook (list): List of markdown guides.

    Returns:
        tuple: actions, guides and intent examples.
    """
    actions, guides, intent_examples = [], [], []
    for x in guidebook:
        action, guide, intent_example = split_markdown_guide(x)
        actions.append(action)
        guides.append(guide)
        intent_examples.append(intent_example)
    return actions, guides, intent_examples


def filter_for_translation(examples: list, exclude: list):
    """Filter out intent examples that are not suitable for translation.

    Args:
        intent_examples (list): List of intent examples.

    Returns:
        list: Filtered list of intent examples.
    """
    return [i for i in examples if i not in exclude]

def make_dir(path: str):
    """Creates directories"""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def save_to_file(guidebook_dict: dict, lang: str):
    """Save translated guidebook to file.

    Args:
        guidebook_dict (dict): Guidebook dictionary.
        lang (str): Language to save to.
    """
    for fname, content in guidebook_dict.items():
        iname = content[lang]['intent']
        dpath = f"guidebook/{iname}/{lang}"
        fpath = f"{dpath}/{fname}.md"
        print(f"Saving {fpath}...", end="")
        
        make_dir(dpath)
        
        with open(fpath, "w", encoding="utf-8") as mdf:
            mdf.write(f"# {content[lang]['action']}\n\n")
            mdf.write(f"{content[lang]['guide']}\n\n")
            mdf.write("## Intent Examples\n\n")
            for e in content[lang]['intent_examples']:
                mdf.write(f"- {e}\n")
            mdf.write("\n")
        print("Done.")

LANG = "en"
print(f"Translating from {LANG.upper()}...", end="")

en_files = get_guidebook_files(func=f"**/{LANG}/*")
en_guides = get_guidebook_content(en_files)
print(f"Found {len(en_guides)} guides.", end="\n"*2)

guidebook_dict = {}

actions, guides, intent_examples = get_guides_intent_examples(en_guides)

for file, action, guide, intent_example in zip(en_files, actions, guides, intent_examples):
    
    assert file and action and guide and intent_example, \
        f"Error in file: {file}\naction: {action}\nguide: {guide}\nintent_example: {intent_example}"
    
    # Here I would like to split the filepath (guidebook/{intent:**}/{lang:*}/{filename}.md)
    g = file.split("/")[0]
    f = file.split("/")[-1].removesuffix(".md")
    _i_l = file.removeprefix(g+"/").removesuffix('/'+f+".md")
    l = _i_l.split("/")[-1]
    i = _i_l.removesuffix('/'+l)
    
    assert f not in guidebook_dict, f"Duplicate intent: {f}"
    
    guidebook_dict[f] = {
        f'{l}': {
            'intent': f'{i}',
            'action': f'{action}',
            'guide': guide.split("\n\n")[-1].strip(),
            'intent_examples': [
                i.replace('"', "").replace("- ", "").strip() \
                for i in intent_example.split("\n")
            ]
        }
    }

TRANS_LANG = q.text("Enter the language you want to translate to:").ask()
if not TRANS_LANG:
    print("Please type a language.")
    sys.exit(1)

print(f"Translating to {TRANS_LANG.upper()}...", end="\n"*2)

MX_FACTOR = 1.25
max_length = int(max(len(x) for x in guides) * MX_FACTOR)
print(f"Max length: {max_length}", end="\n"*2)

BATCH_SIZE = q.text("Enter the batch size:", default="64").ask()
if not BATCH_SIZE:
    print("Please type a batch size.")
    sys.exit(1)

try:
    BATCH_SIZE = int(BATCH_SIZE)
except ValueError:
    print("Batch size: Please enter a valid integer.")
    sys.exit(1)

print(f"Batch size: {BATCH_SIZE}", end="\n"*2)

MODEL_ID = q.text("Enter the model ID:", default="facebook/nllb-200-distilled-600M").ask()

print(f"Model ID: {MODEL_ID}", end="\n"*2)

if "nllb" in MODEL_ID:
    _LANG = get_nllb_lang(LANG)
    _TRANS_LANG = get_nllb_lang(TRANS_LANG)
else:
    _LANG = LANG
    _TRANS_LANG = TRANS_LANG

NPROC = q.text("Enter the number of processes:", default="4").ask()
if not NPROC:
    print("Please type a number of processes.")
    sys.exit(1)

try:
    NPROC = int(NPROC)
except ValueError:
    print("Number of processes: Please enter a valid integer.")
    sys.exit(1)

print(f"Number of processes: {NPROC}", end="\n"*2)

try:
    print("Loading Translator...", end="")
    translator = Translator(
            _LANG, _TRANS_LANG,
            max_length=max_length, batch_size=BATCH_SIZE,
            model_id=MODEL_ID, n_proc=NPROC
        )
    print("Done.", end="\n"*2)
except ValueError as ve:
    raise ImportError(f"Could not load translator with model ID: {MODEL_ID}.") from ve

to_exclude = [
    "..",
    "../..",
    "cls",
    "dir",
    "dirs",
    '/home',
    "home",
    "~",
    ".",
    "cd",
    "cd ..",
    "cd ../..",
    "ls please",
    "ls",
    "ls -l",
    "ls -a",
    "ls -la",
    "ls -al",
    "ls -lh",
    "ls -hl",
    "ls -lha",
    "ls -lah",
    "ls -alh",
    "ls -ahl",
    "echo ~",
    "pwd",
    "echo $PWD",
    # Specific to english to french translation
    "how to french kiss",
    "how are you in french",
    "how to say i love you in french",
    "how to make french fries",
    "how to make french toast",
    "how to french braid",
    # Add more here as needed...
    # "",
]

for intent, content in guidebook_dict.items():
    print(f"Translating intent: {intent}...", end="")
    action = content[LANG]['action']
    guide = content[LANG]['guide']
    intent_examples = filter_for_translation(
        content[LANG]['intent_examples'],
        exclude=to_exclude
        )
    
    guidebook_dict[intent][TRANS_LANG] = {
        'intent': content[LANG]['intent'],
        'action': translator.translate(action)[0],
        'guide': translator.translate(guide)[0],
        'intent_examples': list(set(translator.translate(intent_examples)))
    }
    print("Done.")

save_to_file(guidebook_dict, TRANS_LANG)

print(f"Saved translated guidebook to {TRANS_LANG.upper()}.", end="\n"*2)
