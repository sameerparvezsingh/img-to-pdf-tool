import tkinter as tk
from tkinter import CENTER, Canvas
from PIL import Image
import os
from tkinter import filedialog
#from fpdf import FPDF
import img2pdf
import PyPDF2
import uuid

from tkinter.filedialog import askopenfilename, askopenfilenames
from pathlib import Path

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

imagesToWorkOn = {}
pdfFilesToworkOn={}
fileList=[]

def upload_imgs():
    global imagesToWorkOn
    imagesToWorkOn['filename']=filedialog.askopenfilenames(filetypes=[('JPG','*.jpg'),('PNG','*.png'),('JPEG','*.jpeg')],
    initialdir = os.getcwd(), title='Select File/imagesToWorkOn')
    if len(imagesToWorkOn['filename'])!=0:
        enable(download_button)
        #enable(download_button_2)
        enable(save_a4_button)

def save_pdf():
    try:
        img_list = []
        for file in imagesToWorkOn['filename']:
            img_list.append(Image.open(file).convert('RGB'))
        save_file_name = filedialog.asksaveasfilename(filetypes = [('*.pdf')], initialdir=os.getcwd(), title='Save File')
        if save_file_name is None or save_file_name == "" or save_file_name == " ":
            save_file_name = str(uuid.uuid4())
        img_list[0].save(f'{save_file_name}.pdf',optimize = True, quality=50, save_all=True, append_images = img_list[1:])
        disable(download_button)
    except:
        return


# def saveas2():
#     try:
#         #img_list = []
        
#         pdf = FPDF()
#         # imagelist is the list with all image filenames
#         for file in imagesToWorkOn['filename']:
#             pdf.add_page()
#             pdf.image(file,0,0,210,197)

#         save_file_name = filedialog.asksaveasfilename(filetypes = [('PDF','*.pdf')], initialdir=os.getcwd(), title='Save File')
#         pdf.output(f'{save_file_name}.pdf', "F")
        
#         disable(download_button_2)
#     except:
#         return

def save_as_a4():
    try:
        #img_list = []
        
        # use a fixed dpi of 300 instead of reading it from the image
        #dpix = dpiy = 300
        #layout_fun = img2pdf.get_fixed_dpi_layout_fun((dpix, dpiy))
        a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
        layout_fun = img2pdf.get_layout_fun(a4inpt)
        save_file_name = filedialog.asksaveasfilename(filetypes = [('*.pdf')], initialdir=os.getcwd(), title='Save File')
        if save_file_name is None or save_file_name == "" or save_file_name == " ":
            save_file_name = str(uuid.uuid4())
        with open(f'{save_file_name}.pdf',"wb") as f:
            f.write(img2pdf.convert(imagesToWorkOn['filename'], layout_fun=layout_fun))
        f.close()
        disable(save_a4_button)
    except:
        return

def uploadPdf():
    global pdfFilesToworkOn
    pdfFilesToworkOn['pdffilename']=filedialog.askopenfilenames(filetypes=[('pdf','*.pdf')],
    initialdir = os.getcwd(), title='Select pdf File')
    print(pdfFilesToworkOn)
    if len(pdfFilesToworkOn['pdffilename'])!=0:
        enable(pdf_download_button)

def pdfMerger():
    try:
        pdfList=[]
        # Call the PdfFileMerger
        mergedObject = PyPDF2.PdfFileMerger()
        for file in pdfFilesToworkOn['pdffilename']:
            pdfList.append(file)

        for pdf in pdfList:
            print(pdf)
            pdfFileObj = open(pdf, 'rb')
            print(type(pdfFileObj))
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            mergedObject.append(PyPDF2.PdfFileReader(pdf, strict=False))
            pdfFileObj.close()
        
        save_file_name = filedialog.asksaveasfilename(filetypes = [('PDF','*.pdf')], initialdir=os.getcwd(), title='Save File')
        # Write all the files into a file which is named as shown below
        mergedObject.write(f'{save_file_name}.pdf')
    except ValueError:
        error_items["text"] = "PDF not supported"
        print('Something seems wrong with pdf, trying to correct')



# upload button
upload_images_button = tk.Button(mainWindow, text='SELECT IMAGES', width = 20, height =1,font=('arial',14,'bold'), bg='white',fg='green', command=upload_imgs)
upload_images_button.grid(row =2, column = 0, pady =40)
upload_images_button.place(relx=0.5, rely=0.1, anchor=CENTER)

# Download button
download_button = tk.Button(mainWindow, text='SAVE PDF', width = 20, height =1,font=('arial',14,'bold'), 
        bg='white',fg='red', command=save_pdf)
# download_button.grid(row=3, column=0)
download_button.place(relx=0.5, rely=0.2, anchor=CENTER)
disable(download_button)

# download_button_2 = tk.Button(mainWindow, text='SAVE A4 PDF v1', width = 20, height =1,font=('arial',14,'bold'), bg='white',fg='red', command=saveas2)
# download_button_2.grid(row=5, column=0)
# disable(download_button_2)

#button to save a4 pdfs
save_a4_button = tk.Button(mainWindow, text='SAVE A4 PDF', width = 20, height =1,font=('arial',14,'bold'), 
        bg='white',fg='red', command=save_as_a4)
save_a4_button.grid(row=7, column=0)
save_a4_button.place(relx=0.5, rely=0.26, anchor=CENTER)
disable(save_a4_button)

#button to select multiple pdfs
upload_pdf_button = tk.Button(mainWindow, text='SELECT PDF(s)', width = 20, height =1,font=('arial',14,'bold'), bg='white',fg='green', command=uploadPdf)
upload_pdf_button.grid(row =13, column = 0, pady =10)
upload_pdf_button.place(relx=0.5, rely=0.4, anchor=CENTER)

#button to save merged pdfs in alphabetical order
pdf_download_button = tk.Button(mainWindow, text='SAVE Merged PDF', width = 20, height =1,font=('arial',14,'bold'), bg='white',fg='red', command=pdfMerger)
# pdf_download_button.grid(row=14, column=0) 
pdf_download_button.place(relx=0.5, rely=0.46, anchor=CENTER)
disable(pdf_download_button)


def open_file(files):
    filepath = askopenfilename(
        filetypes=[("PDF Files","*.pdf"), ("All Files", "*.*")]
    )
    # if not(filepath and Path(filepath).exists()):
    #     return
    if(type(filepath) is tuple):
        filepath=list(filepath)
        for f in filepath:
            files.append(f)
    else:
        files.append(filepath)
    # files.append(filepath)
    # list out all filenames
    lbl_items["text"] = '\n'.join(str(f) for f in files)
    if len(files) >= 1 and pdf_download_button['state'] == "disabled":
        enable(list_clear_button)
        enable(element_clear_button)
    if len(files) >= 2:
        enable(pdf_download_button2)
        #pdf_download_button2["state"] = "normal"

def merge_pdfs(files):
    try:
        pdfList=files
        # Call the PdfFileMerger
        mergedObject = PyPDF2.PdfFileMerger()
        # for file in pdfFilesToworkOn['pdffilename']:
        #     pdfList.append(file)

        for pdf in pdfList:
            print(pdf)
            pdfFileObj = open(pdf, 'rb')
            print(type(pdfFileObj))
            #pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            mergedObject.append(PyPDF2.PdfFileReader(pf, strict=False))
            pdfFileObj.close()
        
        save_file_name = filedialog.asksaveasfilename(filetypes = [('PDF','*.pdf')], initialdir=os.getcwd(), title='Save File')
        # Create the merger pdf file with manual name 
        mergedObject.write(f'{save_file_name}.pdf')
    except Exception as e:
        error_items["text"] = f"PDF not supported, {e}"
        print('Something seems wrong with the pdf')
    

def removeElement(list):
    if len(list)!=0:
        del list[-1]
    lbl_items["text"] = '\n'.join(str(f) for f in list)
    if len(list) < 1:
        disable(pdf_download_button2)
        disable(list_clear_button)
        disable(element_clear_button)

def resetList(list):
    list.clear()
    lbl_items["text"] = '\n'.join(str(f) for f in list)
    disable(pdf_download_button2)
    disable(list_clear_button)
    disable(element_clear_button)


# --- Ask open files ---
info_select_file_label = tk.Label(mainWindow, text="Please choose PDFs to join: (2 and above)")
info_select_file_label.grid(row=17, column=0, padx=5, pady=5)
info_select_file_label.place(relx=0.5, rely=0.6, anchor=CENTER)

#open pdf files one by one
open_single_pdf_button = tk.Button(mainWindow, text="Open PDF(s)", width = 10, height =2,font=('arial',14,'bold'), bg='white',fg='green',
                command=lambda: open_file(fileList))
open_single_pdf_button.place(relx=0.5, rely=0.67, anchor=CENTER)

#button to clear all selected files
list_clear_button = tk.Button(mainWindow, text='clear all', width = 12, height =1,font=('arial',9,'bold'), bg='white',fg='red', command=lambda: resetList(fileList))
list_clear_button.place(relx=0.7, rely=0.65, anchor=CENTER)
disable(list_clear_button)

#button to clear last selected file
element_clear_button = tk.Button(mainWindow, text='clear one selection', width = 15, height =1,font=('arial',9,'bold'), bg='white',fg='red', command=lambda: removeElement(fileList))
element_clear_button.place(relx=0.71, rely=0.69, anchor=CENTER)
disable(element_clear_button)

#label to show selected files in an order
lbl_items = tk.Label(mainWindow, text="", wraplength=180, justify="left")
lbl_items.place(relx=0.18, rely=0.67, anchor=CENTER)

#button to save merged files
pdf_download_button2 = tk.Button(mainWindow, text='SAVE Merged PDF', width = 16, height =1,font=('arial',14,'bold'), bg='white',fg='red', command=lambda: merge_pdfs(fileList))
pdf_download_button2.place(relx=0.5, rely=0.8, anchor=CENTER)
disable(pdf_download_button2)


#label to show errors
error_items = tk.Label(mainWindow, text="", bg='white',fg='red')
error_items.place(relx=0.5, rely=0.9, anchor=CENTER)


# --- Button to exit ---
btn_exit = tk.Button(mainWindow, text="Exit", bg='white',fg='red', command=mainWindow.destroy, bd=2)
btn_exit.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.FALSE)

def main():
    mainWindow.mainloop()

if __name__ == '__main__':
    main()
