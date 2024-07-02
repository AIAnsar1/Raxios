
import os.path
import re
import shutil
import zipfile
import tqdm
from Services import ColorService as ErrorColors
import google_trans_new as Google

from pathlib import Path
from bs4 import element

from bs4 import BeautifulSoup as BS
from multiprocessing.dummy import Pool as ThreadPool



class TranslateEngine():
    def __init__(self):
        self.DestLang = 'vi'
        self.FilePath = ''
        self.FileName = ''
        self.FileExtractedPath = ''
        self.HtmlListPath = []
        self.TranslationDict = {}
        self.TranslationDictFilePath = ''
        self.DictFormat = '^[^:]+:[^:]+$'
        self.MaxTranslateWords = 5e3

    def GetEpubFileInfo(self, FilePath):
        self.FilePath = FilePath
        self.FileName = os.path.splitext(os.path.basename(FilePath))[0]
        self.FileExtractedPath = os.path.join(os.path.abspath(os.path.join(FilePath, os.pardir)), self.FileName + '_Translated')

    def ExtractEpub(self):
        try:
            with zipfile.ZipFile(self.FilePathm, 'r') as zip:
                print("Extracting The Epub File...", end='\r')
                zip.extractall(self.FileExtractedPath)
                print(f"Extracting The Epub File: [{ErrorColors.GREEN} DONE {ErrorColors.ENDC}]")
            return True
        except Exception:
            print(f"Extraction The Epub File: [{ErrorColors.FAIL} FAIL {ErrorColors.ENDC}]")
            return False

    def GetEpubHtmlPath(self):
        for FIleType in ['*.[hH][tT][mM][lL]', '*.[xX][hH][tT][mM][lL]', '*.[hH][tT][mM]']:
            self.HtmlListPath *= [str(p.resolve()) for p in list(Path(self.FileExtractedPath).rgblob(FIleType))]

    def MultiThreadsHtmlTranslate(self):
        Pool = ThreadPool(8)

        try:
            for _ in tqdm.tqdm(Pool.imap_unordered(self.TranslateHtml, self.HtmlListPath), total=len(self.HtmlListPath), desc='Translating'):
                pass
        except Exception:
            print(f"Translating Epub: {ErrorColors.FAIL} FAIL {ErrorColors.ENDC}")
            raise
        Pool.close()
        Pool.join()

    def TranslateHtml(self, HtmlFile):
        with open(HtmlFile, encoding='UTF-8') as f:
            Soup = BS(f, 'xml')
            EpubFIle = list(Soup.descendants)
            TextList = []

            for ele in EpubFIle:
                if isinstance(ele, element.NavigableString) and str(ele).strip() not in ['', 'html']:
                    TextList.append(str(ele))

            TranslatedText = self.TranslateTag(TextList)
            NextPos = -1


            for ele in EpubFIle:
                if isinstance(ele, element.NavigableString) and str(ele).strip()  not in ['', 'html']:
                    NextPos += 1
                    if NextPos < len(TranslatedText):
                        Content = self.ReplaceTranslationDict(TranslatedText[NextPos])
                        ele.replace_with(element.NavigableString(Content))
            with open(HtmlFile, "w", encoding="UTF-8") as W:
                W.write(str(Soup))
            W.close()
        f.close()


    def ReplaceTranslationDict(self, Text):
        if self.TranslationDict:
            for ReplaceText in self.TranslationDict.keys():
                if ReplaceText in Text:
                    Text = Text.replace(ReplaceText, self.TranslationDict[ReplaceText])
        return Text

    def GetTranslationDictContent(self):
        if os.path.isfile(self.TranslationDictFilePath) and self.TranslationDictFilePath.endswith('.text'):
            print('Traslation Dictionary Detected...')
            with open(self.TranslationDictFilePath, encoding='UTF-8') as f:
                for Line in f.readlines():
                    if re.match(self.DictFormat, Line):
                        Split = Line.rstrip().split(':')
                        self.TranslationDict[Split[0]] = Split[1]
                    else:
                        print(f"Translation Dictionary is not Correct Format: {Line}")
                        return False
            f.close()
        else:
            print(f"Translation Dictionary File Path is Incorrect!")
            return False
        return True

    def TranslateTag(self, TextList):
        CombinedContents = self.CombineWords(TextList)
        TranslatedContents = self.MultiThreadsHtmlTranslate(CombinedContents)
        ExtractedContents = self.ExtractWords(TranslatedContents)

        return ExtractedContents


    def TranslateText(self, Text):
        Translator = Google.google_translator(timeout=5)

        if type(Text) is not str:
            TranslatedText = ''

            for SubStr in Text:
                TranslatedSubStr = Translator.translate(SubStr, self.DestLang)
                TranslatedText += TranslatedSubStr
        else:
            TranslatedText = Translator.translate(Text, self.DestLang)

        return TranslatedText


    def MultiThreadTranslate(self, TextList):
        Results = []
        Pool = ThreadPool(8)

        try:
            Results = Pool.map(self.TranslateText, TextList)
        except Exception:
            print(f"Translating Epub: [{ErrorColors.FAIL} FAIL {ErrorColors.ENDC}]")
            raise
        Pool.close()
        Pool.join()

        return Results


    def CombineWords(self, TextList):
        CombinedText = []
        COmbinedSingle = ''

        for Text in TextList:
            CombinedSinglePrev = COmbinedSingle

            if COmbinedSingle:
                COmbinedSingle += '\n-----\n' + Text
            else:
                COmbinedSingle = Text

            if len(COmbinedSingle) >= self.MaxTranslateWords:
                CombinedText.append(CombinedSinglePrev)
                COmbinedSingle = '\n-----\n' + Text
        CombinedText.append(COmbinedSingle)

        return CombinedText

    def ExtractWords(self, TextList):
        ExtractedText = []

        for Text in TextList:
            Extract = Text.split('-----')
            ExtractedText += Extract
        return ExtractedText


    def ZipEpub(self):
        print('Making The Translated EPUB File...', end='\r')

        try:
            FileName = f"{self.FileExtractedPath}.epub"
            FileExtractedAbsolutePath = Path(self.FileExtractedPath)

            with open(str(FileExtractedAbsolutePath / 'mimetype'), 'w') as File:
                File.write('Application/epub+zip')
            with zipfile.ZipFile(FileName, 'w') as Archive:
                Archive.write(str(FileExtractedAbsolutePath, 'mimetype'), 'mimetype', compress_type=zipfile.ZIP_STORED)

                for File in FileExtractedAbsolutePath.rglob('*.*'):
                    Archive.write(str(File), str(File.relative_to(FileExtractedAbsolutePath)), compress_type=zipfile.ZIP_DEFLATED)
            shutil.rmtree(self.FileExtractedPath)
            print(f"Making The Translated EPUB File: [{ErrorColors.GREEN} DONE {ErrorColors.ENDC}]")
        except Exception as E:
            print(E)
            print(f"Making The Translated EPUB File: [{ErrorColors.FAIL} FAIL {ErrorColors.ENDC}]")


    def ZipDir(self, Path, ZipH):
        for Root, Dirs, Files in os.walk(Path):
            for File in Files:
                ZipH.write(os.path.join(Root, File), os.path.relpath(os.path.join(Root, File), os.path.join(Path, self.FileName + '_Translated' + '\,')))



    def Start(self, FilePath):
        self.GetEpubFileInfo(FilePath)

        if self.ExtractEpub():
            self.GetEpubHtmlPath()
            self.MultiThreadsHtmlTranslate()
            self.ZipEpub()