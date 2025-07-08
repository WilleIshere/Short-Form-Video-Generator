from src.main import main

if __name__ == '__main__':
    print('Starting up...')

    print('Setting environment variables...')

    import os
    ffmpeg_path = "ffmpeg_bin/ffmpeg"
    ffmpeg_dir = os.path.abspath(os.path.dirname(ffmpeg_path))
    os.environ['PATH'] = f'{ffmpeg_dir}:{os.environ["PATH"]}'

    print('Running application...')
    main()
