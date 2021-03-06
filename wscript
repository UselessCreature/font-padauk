#!/usr/bin/python3

# import codecs, os

# set some default output folders (most are already set by default)
DOCDIR = ["documentation", "web"]
TESTDIR='tests'
STANDARDS = 'tests/reference'

# set the version control system for srcdist
VCS = 'git'

APPNAME='Padauk'
FAMILY = APPNAME
DESC_SHORT='Burmese Unicode TrueType font with OpenType and Graphite support'

# retrieve all the authorship information from one of the master UFOs
getufoinfo('source/masters/Padauk-Regular.ufo')
BUILDLABEL="beta"

# mystrings = {
#    'Regular' : 'ပုံမှန်',
#    'Bold' : 'စာလုံးမဲ',
#    'Padauk' : 'ပိတောက်',
#    'Padauk Book' : 'ပိတောက်စာအုပ်'
#}
#namestrings = {
#    '-Regular' :     ('Padauk', 'Regular'),
#    '-BookBold' :    ('Padauk Book', 'Bold'),
#    '-Bold' :        ('Padauk', 'Bold'),
#    '-Book' :        ('Padauk Book', 'Regular')
#}

opts = preprocess_args({'opt' : '--no2'}, {'opt' : '--bake'})
devver = getversion()

scriptcode = 'mymr' if '--no2' in opts else 'mym2'

#tests = fonttest(extras = {
#    'xtest1' : tests({'xtest1' : cmd('cmptxtrender -p -k -e ot -s mym2 -l "${lang}" -e ot -s dflt -L mym2 -L dflt -t ${SRC[1]} -o ${TGT} --copy=otfonts --strip ${fileinfo} ${SRC[0]} ${SRC[0]}')})
#})
if '--bake' in opts:
    testCommand('bake', cmd='${FONTBAKERY} check-googlefonts -n -m ERROR --ghmarkdown padauk-bakery.md ${SRC} ; true', extracmds=["fontbakery"], shapers=0, ext=".md", coverage="fonts", shell=1, fontmode='collect')

# Set up the FTML tests
ftmlTest('tools/ftml.xsl')

d = designspace('source/Padauk.designspace',
    #params = '-l ${DS:FILENAME_BASE}_createinstance.log',
    #target = process('${DS:FILENAME_BASE}.ttf',
    #    cmd('${TTFAUTOHINT} -n -W ${DEP} ${TGT}'),
    #),
    target = '${DS:FILENAME_BASE}.ttf',
    instanceparams = "-W",
    ap = '${DS:FILENAME_BASE}.xml',
    classes = 'source/padauk_classes.xml',
    opentype = fea('source/${DS:FILENAME_BASE}.fea',
        master = 'source/padauk.fea',
        make_params="--omitaps='_R'",
        params = '-m source/${DS:FILENAME_BASE}.map',
        depends = ["source/padauk"+x+".feax" for x in
            ('_GPOS', '-mym2_GSUB', '-dflt_GSUB')]),
    graphite = gdl('source/${DS:FILENAME_BASE}.gdl',
        master = 'source/myanmar5.gdl',
        params = '-w3521 -w3530 -q -d -D -v5 -e gdlerr-' + '${DS:FILENAME_BASE}' + '.txt', make_params="-m _R",
        depends = ['source/myfeatures.gdl']),
    script = ['mym2', 'DFLT'],
    extra_srcs = ['tools/bin/makegdl', 'source/myfeatures.gdl'],
    pdf = fret(params="-r -oi"),
    woff = woff('web/${DS:FILENAME_BASE}.woff', params = '-v ' + VERSION + ' -m ../source/padauk-WOFF-metadata.xml')
)

# Make khamti package
kpackage = package(appname="PadaukNamKio", version=devver)
dpackage = package(appname="Deemawso", version=devver)
for f in d.fonts:
    font(target = process('khamti/'+f.target.replace('Padauk', 'NamKio'),
                        # cmd('ttfremap -r -c ${SRC} ${DEP} ${TGT}', ['source/namkio_remap.txt']),
                        cmd('psfdeflang -L kht ${DEP} ${TGT}'),
                        name('Namkio Khamti' + (' Book' if 'Book' in f.target else ""))),
            opentype = internal(),
            source = f.target,
            lang = 'kht',
            package = kpackage)
    font(target = process("deemawso/" + f.target.replace('Padauk', 'Deemawso'),
                        cmd('psfdeflang -L kyu ${DEP} ${TGT}'),
                        name('Deemawso' + (' Book' if 'Book' in f.target else ""))),
            opentype = internal(),
            source = f.target,
            lang = 'kyu',
            package = dpackage)

def configure(ctx) :
    ctx.find_program('ttfautohint')
#    ctx.find_program('ttx')
