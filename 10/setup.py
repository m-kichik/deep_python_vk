from distutils.core import setup, Extension


def main():
    setup(
        name="cjson",
        version="0.0.1",
        description="C API JSON Converter",
        author="rito4ka",
        author_email="kichik.mg@phystech.edu",
        ext_modules=[Extension("cjson", ["json.c"])],
    )


if __name__ == "__main__":
    main()
