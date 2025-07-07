from src.main import main

if __name__ == '__main__':
    print('Starting up...')

    print('Setting environment variables...')
    import os

os.environ["PATH"] = "/your/custom/ffmpeg/folder:" + os.environ["PATH"]

    print('Running application...')
    main()
