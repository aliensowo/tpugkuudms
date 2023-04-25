import os
import optparse
from PyQt5.uic.pyuic import Driver


def get_opt(file_name: str):
    parser = optparse.OptionParser(usage="pyuic5 [options] <ui-file>")
    parser.add_option("-p", "--preview", dest="preview", action="store_true",
                      default=False,
                      help="show a preview of the UI instead of generating code")
    parser.add_option("-o", "--output", dest="output", default=file_name,
                      metavar="FILE",
                      help="write generated code to FILE instead of stdout")
    parser.add_option("-x", "--execute", dest="execute", action="store_true",
                      default=False,
                      help="generate extra code to test and display the class")
    parser.add_option("-d", "--debug", dest="debug", action="store_true",
                      default=False, help="show debug output")
    parser.add_option("-i", "--indent", dest="indent", action="store",
                      type="int", default=4, metavar="N",
                      help="set indent width to N spaces, tab if N is 0 [default: 4]")

    g = optparse.OptionGroup(parser, title="Code generation options")
    g.add_option("--import-from", dest="import_from", metavar="PACKAGE",
                 help="generate imports of pyrcc5 generated modules in the style 'from PACKAGE import ...'")
    g.add_option("--from-imports", dest="from_imports", action="store_true",
                 default=False, help="the equivalent of '--import-from=.'")
    g.add_option("--resource-suffix", dest="resource_suffix", action="store",
                 type="string", default="_rc", metavar="SUFFIX",
                 help="append SUFFIX to the basename of resource files [default: _rc]")
    parser.add_option_group(g)

    opts, args = parser.parse_args()
    return opts


if __name__ == '__main__':
    for file in os.listdir("gui"):
        if ".ui" in file:
            file_path = "gui/" + file
            opts = get_opt(file_path.replace(".ui", ".py"))
            driver = Driver(opts, file_path)
            driver.invoke()
