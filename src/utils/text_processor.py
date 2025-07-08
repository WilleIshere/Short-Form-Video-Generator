def text_to_words(in_path: str, out_path: str):
    with open(in_path, 'r', encoding='utf-8') as f:
        file = "".join(f.readlines())
        file = file.replace('\n', '')
        file = file.replace(' ', '\n')

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(file)

def combine_text_files(out_path: str, *in_paths: str):
    with open(out_path, 'w', encoding='utf-8') as outfile:
        for idx, file in enumerate(in_paths):
            with open(file, 'r', encoding='utf-8') as infile:
                contents = infile.read()
                outfile.write(contents)
                if idx != len(in_paths) - 1 and not contents.endswith('\n'):
                    outfile.write('\n')
