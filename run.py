from src.main import main
import sys


if __name__ == '__main__':
    print('Setting environment variables...')

    import os
    ffmpeg_path = "ffmpeg_bin/ffmpeg"
    ffmpeg_dir = os.path.abspath(os.path.dirname(ffmpeg_path))
    os.environ['PATH'] = f'{ffmpeg_dir}:{os.environ["PATH"]}'

    print('Running application...')
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)
