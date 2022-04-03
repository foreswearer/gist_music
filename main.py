# main method to run conversion and analysis.
# don't use unless needed AND you know what you are doing
import gen_visualizations

import convert_mp3_wav

if __name__ == '__main__':
    # converts all mp3 files to wav from current directory/data files
    convert_mp3_wav.convert_all()
    gen_visualizations.print_all()
