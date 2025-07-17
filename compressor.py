import pypdf
import os
import tkinter as tk
from tkinter import CENTER
from tkinter.filedialog import askopenfilename, askopenfilenames


fileList=[]

# GUI application window
mainWindow = tk.Tk()
mainWindow.title('Img to Pdf converter application')
mainWindow.geometry('600x700')
#mainWindow.iconphoto(False, tk.PhotoImage(file = 'pdf.png'))
mainWindow.resizable(0,0)

def disable(button):
    button['state']='disabled'

def enable(button):
    button['state']='active'

#open pdf files one by one
open_single_pdf_button = tk.Button(mainWindow, text="Open PDF(s)", width = 10, height =2,font=('arial',14,'bold'), bg='white',fg='green',
                command=lambda: open_file(fileList))
open_single_pdf_button.place(relx=0.5, rely=0.67, anchor=CENTER)

#button to compress pdf with lossless compression
compress_pdf_button = tk.Button(mainWindow, text='Compress PDF', width = 16, height =1,font=('arial',14,'bold'), bg='white',fg='green', command=lambda: pdfCompressor(fileList))
compress_pdf_button.place(relx=0.5, rely=0.87, anchor=CENTER)
disable(compress_pdf_button)

#button to save merged files
pdf_download_button2 = tk.Button(mainWindow, text='SAVE Merged PDF', width = 16, height =1,font=('arial',14,'bold'), bg='white',fg='red', command=lambda: merge_pdfs(fileList))
pdf_download_button2.place(relx=0.5, rely=0.8, anchor=CENTER)
disable(pdf_download_button2)

#label to show errors
error_items = tk.Label(mainWindow, text="", bg='white',fg='red')
error_items.place(relx=0.5, rely=0.9, anchor=CENTER)

def open_file(files):
    try:
        filepath = askopenfilename(
        filetypes=[("PDF Files","*.pdf"), ("All Files", "*.*")]
        )
        files.append(filepath)
        enable(compress_pdf_button)
    except Exception as e:
        error_items["text"] = f"PDF not supported, {e}"
        print('Something seems wrong with the pdf')
    # if not(filepath and Path(filepath).exists()):
    #     return
    # if(type(filepath) is tuple):
    #     filepath=list(filepath)
    #     for f in filepath:
    #         files.append(f)
    # else:
    #     files.append(filepath)
    # # files.append(filepath)
    # # list out all filenames
    # lbl_items["text"] = '\n'.join(str(f) for f in files)
    # if len(files) >= 1 and pdf_download_button2['state'] == "disabled":
    #     enable(compress_pdf_button)
    # if len(files) >= 2:
    #     disable(compress_pdf_button)



def pdfCompressor(files):
    try:
        print("Trying to compress the file")
        openFile = pypdf.PdfWriter(clone_from=files[0])

        #lossless compression
        for page in openFile.pages:
            page.compress_content_streams()  # This is CPU intensive!

        #compress picture quality in pdf
        for page in openFile.pages:
            for img in page.images:
                img.replace(img.image, quality=80)

        save_file_name = tk.filedialog.asksaveasfilename(filetypes = [('PDF','*.pdf')], initialdir=os.getcwd(), title='Save File')

        with open(f"{save_file_name}.pdf", "wb") as f:
            openFile.write(f)
    except Exception as e:
        error_items["text"] = f"PDF not supported, {e}"
        print('Something seems wrong with the pdf')



def main():
    mainWindow.mainloop()

if __name__ == '__main__':
    main()
