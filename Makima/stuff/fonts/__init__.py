

def list_all_fonts():
    import glob
    from os.path import basename, dirname, isfile

    mod_paths = glob.glob(dirname(__file__) + "/*.ttf")
    all_fonts = [
        dirname(f) + "/" + basename(f)
        for f in mod_paths
        if isfile(f) and f.endswith(".ttf")
    ]
    return all_fonts


ALL_FONTS = sorted(list_all_fonts())
__all__ = ALL_FONTS + ["ALL_FONTS"]
