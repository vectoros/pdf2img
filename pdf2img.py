import sys, fitz, os, getopt
import glob

def pdf2png(pdfPath, imagePath):
    inputFile=os.path.split(pdfPath)[1]
    inputFileName=os.path.splitext(inputFile)[0]
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # default 792x612, dpi=96
        scaleX = 2
        scaleY = 2
        mat = fitz.Matrix(scaleX, scaleY).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)

        outputPath = imagePath + os.path.sep + inputFileName

        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
        print('output path:', outputPath)
        pix.writePNG(outputPath + os.path.sep + inputFileName + '_%s.png' % pg)


def png2pdf(pngPath, pdfPath):
    doc = fitz.open()
    for img in sorted(glob.glob(pngPath + os.path.sep +"*")):
        imgdoc = fitz.open(img)
        pdfbytes = imgdoc.convertToPDF()
        imgpdf=fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)
    if os.path.exists(pdfPath):
        os.remove(pdfPath)
    doc.save(pdfPath)
    doc.close()


def main(argv):
    inputPath=''
    outputPath=''

    if len(argv) < 1:
        print("pdf2img.py -i <inputPath> -o <outputPath>")
        sys.exit(1)

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ipath=", "opath="])
    except getopt.GetoptError:
        print("pdf2img.py -i <inputPath> -o <outputPath>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("pdf2img.py -i <inputPath> -o <outputPath>")
            sys.exit()
        elif opt in ("-i", "--ipath"):
            inputPath = arg
        elif opt in ("-o", "--opath"):
            outputPath = arg

    pdfFiles=os.listdir(inputPath)
    for item in pdfFiles:
        print('convert ', item)
        pdf2png(inputPath + os.path.sep + item, outputPath)


if __name__ == "__main__":
    main(sys.argv[1:])