from typing import Dict
import os
import docx2txt
import pdfplumber
import re
import math
import pathlib
import flet
from flet import (
    Column,
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    FilePickerUploadEvent,
    FilePickerUploadFile,
    Page,
    ProgressRing,
    Ref,
    Row,
    Text,
    icons,
)

os.environ["FLET_SECRET_KEY"] = os.urandom(12).hex()

count = 0
counted_words = ''
maxWords = 0
finalPenalty = (0, 0, 0)
alert = ''
extension = ''
mypath = ''

def getWordCount(data):
    global counted_words
    counted_words = ''
    data=data.split()
    counted_words = data
    return len(data)

def penalty(count, maxWords):
    excess = 0
    pen = 0
    marksDeducted = 0
    if maxWords != 0:
        excess = count - maxWords
        if excess > 0:   
            pen = (excess/maxWords)
            pen = pen * 100
            marksDeducted = (pen // 5)*5 + 5;       
        else:
            excess = 0    
    if pen >= 50:
        marksDeducted = "mark 0 should be recorded"
      
    return excess, math.floor(pen), marksDeducted        

def count_docx2(file_name):
    global counted_words
    counted_words = ''
    document = docx2txt.process(file_name)
    data = document.split()
    counted_words = data
    wordcount = len(data)
    return wordcount    

def wordCountFromPDF(file_name):
    doc = pdfplumber.open(file_name)
    text = ''
    for page in doc.pages:
        text += page.extract_text()
    text = re.sub(' +', ' ', text)
    text = " ".join(text.split())
    text = re.sub(r'- ', '-', text)
    text = re.sub(r' -', '-', text)
    text = re.sub(r' \.', '. ', text)
    text = re.sub(r'\. ', '. ', text)
    text = re.sub(r', ', ', ', text)
    text = re.sub(r' ,', ', ', text)
    text = re.sub(r'•', '', text)
    text = text.replace(r'/\d\.\s+|[a-z]\)\s+|[A-Z]\.\s+|[IVX]+\.\s+/g', "")
    footer_pattern = r'(page|Page|PAGE)\s*\d+\s*(of|OF|Of)\s*\d+'
    header_pattern =r'(January|February|March|April|May|June|July|August|September|October|November|December|january|february|march|april|may|june|july|august|september|october|november|december|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\s*\d{2}\s*(\,|\s)\s*\d{4}'
    text = re.sub(footer_pattern, ' ', text)
    text = re.sub(header_pattern, ' ', text)
    text = re.sub(r'\s{2}',' ',text)
    text = getWordCount(text)
    return text

def main(page: Page):      
    page.title = "Word and Penalty Calculator"
    page.theme_mode = flet.ThemeMode.LIGHT
    page.padding = 25
    page.window_width = 800        # window's width is 200 px
    page.window_height = 800       # window's height is 200 px
    page.window_min_width = 450
    #page.window_resizable = False  # window is not resizable
    #page.update()

    page.add(flet.Row([flet.Column(spacing=15), flet.Row(spacing=15)]))

    img = flet.Image(
        src=f"computer2.jpeg",
        width=150,
        height=150,
        )       

    img_row2 = flet.Row([flet.Column([
        flet.Text("Select file: docx or pdf", size=15, color=flet.colors.GREEN, weight=flet.FontWeight.BOLD)
    ])], alignment=flet.MainAxisAlignment.CENTER)
    page.add(img_row2) 

    row_counted_words = flet.Column(scroll=flet.ScrollMode.ALWAYS, expand=True)

    prog_bars: Dict[str, ProgressRing] = {}
    files = Ref[Column]()
    upload_button = Ref[ElevatedButton]()
    calc_button = Ref[ElevatedButton]()

    img_row4 = flet.Row([flet.Column([
    ])], alignment=flet.MainAxisAlignment.CENTER)
    img_row5 = flet.Row([flet.Column([
    ])], alignment=flet.MainAxisAlignment.CENTER)
    img_row6 = flet.Row([flet.Column([
    ])], alignment=flet.MainAxisAlignment.CENTER)
    img_row7 = flet.Row([flet.Column([
    ])], alignment=flet.MainAxisAlignment.CENTER)

    pr_bar_calc = flet.Column(
            [flet.ProgressRing(), flet.Text("Calculating...")],
            horizontal_alignment=flet.CrossAxisAlignment.CENTER
        )
    
    img_row12 = flet.Row([flet.Column([
    
    ])], alignment=flet.MainAxisAlignment.CENTER)
    
    def word_count(e):
        global mypath
        global finalPenalty
        global count
        extension = pathlib.Path(mypath).suffix
        page.banner.open = False
        if extension != '':
            if extension not in ['.docx', '.pdf']:
                page.add(flet.Text(value='Unsupported file type. Select docx or pdf!'))
            else:
                if extension == '.docx':
                    count = count_docx2(mypath)
                    
                elif extension == '.pdf':
                    count = wordCountFromPDF(mypath)

                finalPenalty = penalty(count, maxWords)
                #print(str(count) + ", " + str(maxWords))

    def send_click(e:FilePickerResultEvent):
        if mypath == '':
            page.banner.content = flet.Text(
                "You need to select and then upload a docx or a pdf file first!"
            )
            page.banner.open = True
            page.update()
        elif maxWords2.value == '':
            page.banner.content = flet.Text(
                "Because max word counts was not specified, default value of 0 will be used!"
            )
            page.banner.open = True
            page.update()
            
        if mypath != '':
            global maxWords
            global count
            global finalPenalty
            img_row12.controls.clear()
            maxWords = int(maxWords2.value)
            row_counted_words.controls.clear()
            img_row4.controls.clear()
            img_row5.controls.clear()
            img_row6.controls.clear()
            img_row7.controls.clear()
            img_row12.controls.append(pr_bar_calc)
            page.update()
            word_count(e)
            img_row12.controls.clear()
            row_counted_words.controls.append(Text(value=counted_words, expand=1)) 
            img_row4.controls.append(flet.Text("Counted Words: " + str(count), size=15, color=flet.colors.GREEN, weight=flet.FontWeight.BOLD));
            img_row5.controls.append(flet.Text("Max Words: " + str(maxWords), size=15, color=flet.colors.GREEN, weight=flet.FontWeight.BOLD));
            img_row6.controls.append(flet.Text("Excess of words: " + str(finalPenalty[0]) + ', ' + str(finalPenalty[1]) + '%', size=15, color=flet.colors.GREEN, weight=flet.FontWeight.BOLD));
            img_row7.controls.append(flet.Text("Marks deducted: " + str(finalPenalty[2]), size=15, color=flet.colors.GREEN, weight=flet.FontWeight.BOLD));
            
            page.update()

    def close_banner(e):
        page.banner.open = False
        page.update()

    page.banner = flet.Banner(
        bgcolor=flet.colors.AMBER_100,
        leading=flet.Icon(flet.icons.WARNING_AMBER_ROUNDED, color=flet.colors.AMBER, size=40),
        content=flet.Text(
            "You need to select a docx or a pdf document first!"
        ),
        actions=[
            flet.TextButton("Dismiss", on_click=close_banner),    
        ],
    )        

    def on_upload_progress(e: FilePickerUploadEvent):
        prog_bars[e.file_name].value = e.progress
        prog_bars[e.file_name].update()

    def file_picker_result(e: FilePickerResultEvent):
        img_row4.controls.clear()
        img_row5.controls.clear()
        img_row6.controls.clear()
        img_row7.controls.clear()
        row_counted_words.controls.clear()
        page.banner.open = False
        calc_button.current.disabled = True
        upload_button.current.disabled = True if e.files is None else False
        prog_bars.clear()
        files.current.controls.clear()
        if e.files is not None:
            for f in e.files:
                if pathlib.Path(f.name).suffix not in ['.docx','.pdf']:
                    page.banner.content = flet.Text(
                    "Only docx or pdf files are accepted!"
                    )
                    page.banner.open = True
                    upload_button.current.disabled = True
                else:    
                    prog = ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
                    prog_bars[f.name] = prog
                    files.current.controls.append(Row([prog, Text(f.name)]))
        page.update()

    def upload_files(e):
        uf = []
        if file_picker.result is not None and file_picker.result.files is not None:
            for f in file_picker.result.files:
                uf.append(
                    FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )
            file_picker.upload(uf)
            calc_button.current.disabled = False
            page.update()
            global mypath
            mypath = os.path.join('uploads',f.name)
            #print(mypath)

    file_picker = FilePicker(on_result=file_picker_result, on_upload=on_upload_progress)
    
    img_row8 = flet.Row([flet.Column([
    ])], alignment=flet.MainAxisAlignment.CENTER)
    img_row8.controls.append(file_picker)
    page.add(img_row8)

    img_row9 = flet.Row([flet.Column([
    ])], alignment=flet.MainAxisAlignment.CENTER)
    img_row9.controls.append(ElevatedButton(
            "Select files...",
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: file_picker.pick_files(allow_multiple=False,file_type=flet.FilePickerFileType.CUSTOM, allowed_extensions=['docx','pdf']),
        ))
    page.add(img_row9)

    img_row10 = flet.Row([flet.Column([
    ])], alignment=flet.MainAxisAlignment.CENTER)
    img_row10.controls.append(Column(ref=files))
    page.add(img_row10)

    img_row11 = flet.Row([flet.Column([
    ])], alignment=flet.MainAxisAlignment.CENTER)
    img_row11.controls.append(ElevatedButton(
            "Upload",
            ref=upload_button,
            icon=icons.UPLOAD,
            on_click=upload_files,
            disabled=True,
        ))
    page.add(img_row11)
        
    chat = flet.Row([flet.Column([
    ])], alignment=flet.MainAxisAlignment.CENTER)
    maxWords2 = flet.TextField(label="Specify Max Word Count", hint_text="Default value = 0", value = 0, width=200)

    page.add(  
        chat, flet.Row([flet.Column([flet.Row(controls=[maxWords2, flet.ElevatedButton("Calculate", ref=calc_button, disabled=True, on_click=send_click)])])], alignment=flet.MainAxisAlignment.CENTER)
    )

    page.add(img_row12)

    page.add(img_row4)
    page.add(img_row5)
    page.add(img_row6)
    page.add(img_row7)
    page.add(row_counted_words)
    #img_row12.controls.clear()

if __name__ == '__main__':
    flet.app(target=main, assets_dir="assets", upload_dir="uploads", view=flet.WEB_BROWSER)