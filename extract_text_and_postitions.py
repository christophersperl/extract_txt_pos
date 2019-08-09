# Extract text from PDF-File, attach coordinates to text
# 09.08.2019 SC V1.0.0
#
# found @ https://pdfminer-docs.readthedocs.io/programming.html#performing-layout-analysis
# ( modified )
#
# CLI usage: python extract_text_and_positions path.pdf
###

import sys
import re

from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter


def main(argv):
    try:
        fp = open(argv, 'rb')

        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pages = PDFPage.get_pages(fp)

        for page in pages:
            interpreter.process_page(page)
            layout = device.get_result()
            for lobj in layout:
                if isinstance(lobj, LTTextBox):
                    x, y, text = lobj.bbox[0], lobj.bbox[3], lobj.get_text()

                    text = text.replace('\r', '').replace('\n', '')  # replace CR LF
                    text = re.sub(' +', ' ', text)  # remove double whitespace
                    out_name = argv.replace('.pdf', '.txt')  # name of output

                    f = open(out_name, 'a', encoding='utf-8')
                    f.write('<x: {:<22}, y: {:<22}, text: {}>\n'.format(x, y, text))

        f.close()
        print('Success')

    except:
        print('Error in Processing')


if __name__ == '__main__':
    """ here the first command line argument is used"""
    try:
        main(sys.argv[1])
    except:
        print('Argument Position Error')
