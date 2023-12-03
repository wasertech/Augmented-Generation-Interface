"""
Script to build the guidebook from markdown files.
"""

from glob import glob
from datasets import Dataset

def get_guidebook_files(func="**/*"):
    """
    Returns a list of all markdown files in the guidebook directory.
    """
    return glob(f'guidebook/{func}.md', recursive=True)

def get_guidebook_content():
    """
    Returns a list of all markdown files in the guidebook directory.
    """
    return [open(file, 'r', encoding='utf-8').read() for file in get_guidebook_files()]


guides = get_guidebook_content()
guidebook = Dataset.from_dict({"guide": guides})

print("Pushing GuidBook to HuggingFace Hub as Dataset...")
guidebook.push_to_hub("AGI")
