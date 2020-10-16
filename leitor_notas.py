from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
#import numpy as np
import tabula
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk

root = Tk()

y1 = 235
x1 = 43
y2 = 235 + 186
x2 = 43 + 500

areas=[y1,x1,y2,x2]

p1=43.00
p2=45.50
p3=17.35
p4=57.75
p5=23.90
p6=124.20
p7=32.25
p8=48.00
p9=55.3
p10=95.25

colu=[p1,
      p1+p2,
      p1+p2+p3,
      p1+p2+p3+p4,
      p1+p2+p3+p4+p5,
      p1+p2+p3+p4+p5+p6,
      p1+p2+p3+p4+p5+p6+p7,
      p1+p2+p3+p4+p5+p6+p7+p8,
      p1+p2+p3+p4+p5+p6+p7+p8+p9,
      p1+p2+p3+p4+p5+p6+p7+p8+p9+p10]

root.title('Leitor de Notas de Negociação')
root.geometry('550x300')

title = Label(root, text='Leitor de Notas de Negociação', padx=50)
title.pack()
title.config(font=("Courier", 20, 'bold'))

def opens():

    Label(root, text='Pode demorar um pouco...').pack()

    root.filename = filedialog.askopenfilename(initialdir='/',
                                               title='Selecionar a Nota',
                                               multiple=True)

    global img

    final_df = pd.DataFrame()

    for file in root.filename:

        print(file)

        dado_sujo = tabula.read_pdf(file,
                                    columns=colu,
                                    area=areas,
                                    guess=False,
                                    pages='all',
                                    multiple_tables=False)[0]

        dado_limpo=pd.DataFrame()

        dado_limpo['Tipo (C/V)'] = dado_sujo.iloc[:, 2]
        ano = file[-12:-8]
        mes = file[-8:-6]
        dia = file[-6:-4]
        data=f'{dia}/{mes}/{ano}'
        dado_limpo['Data'] = data
        #dado_limpo['Nº Ordem'] = np.arange(1, len(dado_limpo)+1)
        dado_limpo['Ativo'] = dado_sujo.iloc[:, 5]
        dado_limpo['Preço R$'] = dado_sujo.iloc[:, 8]
        dado_limpo['Quantidade'] = dado_sujo.iloc[:, 7]
        dado_limpo['Valor R$'] = dado_sujo.iloc[:, 9]

        ativo_lista=[]

        for a in dado_limpo['Ativo'].values:

            simbs = a.split()

            while (('PNB' in simbs[-1])  | ('#'  in simbs[-1]) | ('UNT' in simbs[-1]) |
                   ('N1'  in simbs[-1])  | ('N2' in simbs[-1]) | ('NM'  in simbs[-1]) |
                   ('EJ'  in simbs[-1])  | ('EB' in simbs[-1]) | ('EDJ' in simbs[-1]) |
                   ('ED' in simbs[-1])
                  ):
                if len(simbs)>1:
                    simbs = simbs[:-1]
                else:
                    break

            ativo_limpo = simbs
            ativo_limpo = ' '.join(ativo_limpo)

            if ativo_limpo[-2:] == 'PN':
                ativo_limpo = ativo_limpo[:-2] + ' 4'
            if ativo_limpo[-2:] == 'ON':
                ativo_limpo = ativo_limpo[:-2] + ' 3'
            ativo_lista.append(ativo_limpo)

        dado_limpo['Ativo'] = ativo_lista

        dado_limpo = dado_limpo[['Data','Tipo (C/V)','Ativo','Preço R$','Quantidade','Valor R$']] #'Nº Ordem'

        final_df = final_df.append(dado_limpo)

    final_df.to_clipboard(index=False)

    img = ImageTk.PhotoImage(Image.open('chuck.jpg'))
    panel = Label(root, image = img)
    panel.pack()
    panel.pack(side = "bottom", fill = "both", expand = "yes")

    messagebox.showinfo(title='Pronto!',message='Copiado. Basta colar em alguma planilha de sua preferência.')

myButton = Button(root, text='Selecionar Arquivos', command=opens).pack()

#myButton2 = Button(root, text='Copiar Informações', command=copy).pack()

root.mainloop() #rodando o programa de fato, fazer o loop
