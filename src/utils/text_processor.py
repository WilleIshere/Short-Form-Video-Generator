
def combine_text_files(out_path: str, *in_paths: str):
    with open(out_path, 'w', encoding='utf-8') as outfile:
        for idx, file in enumerate(in_paths):
            with open(file, 'r', encoding='utf-8') as infile:
                contents = infile.read()
                outfile.write(contents)
                if idx != len(in_paths) - 1 and not contents.endswith('\n'):
                    outfile.write('\n')
