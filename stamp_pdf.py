import os, sys
import cjson
# from optparse import OptionParser

def generate_stamp(stamp_ps, conf):
    title = conf['title']
    url = conf['url']
    
    stdout_old = sys.stdout
    
    sys.stdout = f_stamp_ps = open(stamp_ps, 'w')
    print '%!PS'
    print '/vpos 760 def % vertical position variable'
    print '/hpos 35 def'
    print '/Courier             % name the desired font'

    print '/newline'
    print '{/vpos vpos 10 sub def %decrease vpos'
    print 'hpos vpos moveto } def %go to that line' 

    print '10 selectfont        % choose the size in points' 

    print '.4 setgray'
    print 'hpos vpos moveto'
           
    print '(%s) show' % title
    print 'newline'
    print '(%s) show' % url
    print 'showpage'

    sys.stdout = stdout_old
    return

if len(sys.argv) < 3:
    print 'ERROR: Not enough arguments'
    print 'Usage: python stamp_pdf.py conf.json in.pdf out.pdf'

conf_file = sys.argv[1]
input_pdf = sys.argv[2]
output_pdf = sys.argv[3]

file_base = os.path.splitext(input_pdf)[0] 

conf = cjson.decode(open(conf_file, 'r').read())

stamp_ps = '%s_stamp.ps' % file_base
stamp_pdf = '%s_stamp.pdf' % file_base

generate_stamp(stamp_ps, conf)

os.system('ps2pdf -sPAPERSIZE=letter %s' % stamp_ps)
os.system('pdftk %s cat 1 output - | pdftk - stamp %s output - | pdftk A=- B=%s cat A1 B2-end output %s' % (input_pdf, stamp_pdf, input_pdf, output_pdf))

to_remove = [stamp_ps, stamp_pdf]

for file_to_remove in to_remove:
    os.remove(file_to_remove)
