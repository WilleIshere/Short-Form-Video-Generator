def clean():
    """
    Cleans the data by removing unnecessary files and directories.
    """
    import os
    import shutil

    directories_to_clean = [
        'subtitle_images',
        'tts_output',
        'video_chunks'
    ]

    for directory in directories_to_clean:
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory, exist_ok=True)