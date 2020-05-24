import sys, fitz, os, getopt
import glob

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
        print("png2pdf.py -i <inputPath> -o <outputPath>")
        sys.exit(1)

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ipath=", "opath="])
    except getopt.GetoptError:
        print("png2pdf.py -i <inputPath> -o <outputPath>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("png2pdf.py -i <inputPath> -o <outputPath>")
            sys.exit()
        elif opt in ("-i", "--ipath"):
            inputPath = arg
        elif opt in ("-o", "--opath"):
            outputPath = arg

    png2pdf(inputPath, outputPath)


if __name__ == "__main__":
    main(sys.argv[1:])