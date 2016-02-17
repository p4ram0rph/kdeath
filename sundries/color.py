class colors:
    BOLD = '\033[1m'
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    CIANO = '\033[1m'
    ORAN= '\033[91m'
    GREY= '\033[37m'
    DARKGREY = '\033[1;30m'
    UNDERLINE = '\033[4m'

def setcolor(text,color=''):
    colorfinal = ''
    if   color.lower()=='blue':colorfinal=colors.BOLD+colors.BLUE+text+colors.ENDC
    elif color.lower()=='red':colorfinal=colors.BOLD+colors.RED+text+colors.ENDC
    elif color.lower()=='green':colorfinal=colors.BOLD+colors.GREEN+text+colors.ENDC
    elif color.lower()=='yellow':colorfinal=colors.BOLD+colors.YELLOW+text+colors.ENDC
    elif color.lower()=='grey':colorfinal=colors.BOLD+colors.GREY+text+colors.ENDC
    elif color.lower()=='darkgrey':colorfinal=colors.BOLD+colors.DARKGREY+text+colors.ENDC
    return colorfinal


def banner(v,a):
    ASCII = ("""
#   _  _  ____  ____    __   ____  _   _ 
#  ( )/ )(  _ \( ___)  /__\ (_  _)( )_( )
#   )  (  )(_) ))__)  /(__)\  )(   ) _ ( 
#  (_)\_)(____/(____)(__)(__)(__) (_) (_)
    Version: {}
    Author:  {}\n""".format(v,a))
    return ASCII