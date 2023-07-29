from pathlib import Path
import json
import time
import pdfkit
from PyPDF2 import PdfFileMerger
import shutil


def final_sanity_check(edbt_file_json, myFile):
    
        for paper in edbt_file_json:
            paper_file_name = paper['path']['$t'].split("/")[1]
            doc_file_path = Path("materials/dblp/docs/" + paper_file_name)
            if doc_file_path.exists():
                myFile.write("""
                     <li>
                     """);
                check_poster(paper, paper_file_name,  myFile)
        else:
            print("++++++++++++++++++++ Doc did not found of file name: " + paper_file_name + ", Title: " + paper['title']['$t'])
        myFile.write(""" 
                </ul>
             </div>
            """)
        myFile.write('</body>')
        myFile.write('</html>')

def get_authors(author_arr):
    author_string = ""
    if isinstance(author_arr, list):
        for i,obj in enumerate(author_arr):
            if i == 0:
                author_string = obj['$t']
            else:
                author_string = author_string + ", " + obj['$t']
    else:
        author_string = author_arr['$t']
    return author_string



def check_poster(paper, paper_file_name, myFile):
    if paper['poster']['$t']:
        poster_file_name = paper['poster']['$t'].split("/")[1]
        poster_file_path = Path("main_data/proceedings/poster/" + poster_file_name)
        if poster_file_path.exists():
            shutil.copy("main_data/proceedings/poster/" + poster_file_name, 'materials/dblp/poster')   # Transferring poster file to dblp material
            shutil.copy("main_data/proceedings/poster/" + poster_file_name, 'materials/doi-to-url/poster')   # Transferring poster file to doi-to-url material
            myFile.write(f"""
                      <img src="./dblp/poster/{poster_file_name}">
                      <div class="info_box">
                        <h3>{paper['title']['$t']}</h3>
                        <p class="authors">-{get_authors(paper['author'])}</p>
                         <div class="btn_box">
                          <a href="./dblp/docs/{paper_file_name}"><button class="btn">Download Paper</button></a>
                          <a href="./dblp/poster/{poster_file_name}"><button class="btn">Download Poster</button></a>
                """);
            check_pitch(paper, myFile)
        else:
            print("++++++++++++++++++++ Poster did not found of file name: " + poster_file_name + ", Title: " + paper['title']['$t'])
    else:
        myFile.write(f"""
                   <img src="./noimg.png" >
                      <div class="info_box">
                        <h3>{paper['title']['$t']}</h3>
                        <p class="authors">-{get_authors(paper['author'])}</p>
                         <div class="btn_box">
                          <a href="./dblp/paper/{paper_file_name}"><button class="btn">Download Paper</button></a>
            """)
        check_pitch(paper)

def check_pitch(paper, myFile):
    if paper['pitch']['$t']:
        pitch_file_name = paper['pitch']['$t'].split("/")[1]
        pitch_file_path = Path("main_data/proceedings/pitch/" + pitch_file_name)
        if pitch_file_path.exists():
            shutil.copy("main_data/proceedings/pitch/" + pitch_file_name, 'materials/dblp/pitch')   # Transferring pitch file to dblp material
            shutil.copy("main_data/proceedings/pitch/" + pitch_file_name, 'materials/doi-to-url/pitch')   # Transferring pitch file to doi-to-url material
            myFile.write(f"""
                          <a href="./dblp/pitch/{pitch_file_name}"><button class="btn">Download Pitch</button></a>
                        </div>
                      </div>
                    </li>
                """);
        else:
            print("++++++++++++++++++++ Pitch did not found of file name: " + pitch_file_name + ", Title: " + paper['title']['$t'])
    else:
        myFile.write("""
                        </div>
                      </div>
                    </li>
            """)



def fileHandler(file_name):
    options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
        }
    pdfkit.from_file(file_name + '.html', 'paper_with_pagenumbers/'+ 'toc_' + file_name, options=options)
    pdfs = ['paper_with_pagenumbers/'+ 'toc_' + file_name, 'paper_with_pagenumbers/' + file_name]
    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(pdf)
    if not os.path.isdir('materials/dblp'):
        os.mkdir('materials/dblp')
    if not os.path.isdir('materials/doi-to-url'):
        os.mkdir('materials/doi-to-url')
    if not os.path.isdir('materials/dblp/docs'):
        os.mkdir('materials/dblp/docs')
    if not os.path.isdir('materials/doi-to-url/docs'):
        os.mkdir('materials/doi-to-url/docs')
    if not os.path.isdir('materials/dblp/poster'):
        os.mkdir('materials/dblp/poster')
    if not os.path.isdir('materials/doi-to-url/poster'):
        os.mkdir('materials/doi-to-url/poster')
    if not os.path.isdir('materials/dblp/pitch'):
        os.mkdir('materials/dblp/pitch')
    if not os.path.isdir('materials/doi-to-url/pitch'):
        os.mkdir('materials/doi-to-url/pitch')
    merger.write('materials/dblp/docs/' + file_name)
    merger.write('materials/doi-to-url/docs/' + file_name)
    merger.close()



if __name__ == "__main__":
    pass
    import sys,os
    if not os.path.isdir('materials/'):
        os.mkdir('materials/')
    with open('materials/index.html', 'w') as myFile:
        myFile.write('<html>')
        myFile.write("""
                        <head>
                          <meta charset="utf-8">
                          <style>
                            * {margin: 0; padding: 0;}

                            
                            ul {
                              list-style-type: none;
                              width: 100%;
                            }

                           
                            li img {
                              float: left;
                              margin: 0 15px 0 0;
                            }

                            li p{
                              font-size: 0.9em;
                            }
                            li {
                              padding: 10px;
                              overflow: auto;
                            }
                            img{
                                width: 288px;
                                height: 200px;
                                border: 11px solid #124664;
                                border-radius: 20px;
                            }
                            .info_box{
                                  background: #124665;
                                  color: #fff;
                                  padding: 25px;
                                  border-radius: 20px;
                                  margin-top: 38px;
                            }
                            .headline{
                              background: #124664;
                              margin: 0;
                              padding: 30px 70px;
                              color: #fff;
                              font-size: 1.6em;
                              text-align: center;
                            }
                            .list_box{
                              width: 70%;
                              margin: auto;
                              margin-top: 25px;
                            }
                            .authors{
                              font-style: italic;
                            }
                            .btn_box{
                              display: flex;
                            }
                            .btn{
                              background: #fff;
                              border-radius: 10px;
                              padding: 10px 15px;
                              margin-top: 12px;
                              margin-right: 10px;
                              outline: none;
                              border: none;
                              cursor: pointer;
                            }
                            .btn:hover{
                              background: #3180af;
                              color: #fff; 
                            }
                          </style>
                        </head>
        """)
        myFile.write('<body style="font: normal 15px/1.5 Helvetica, Verdana, sans-serif;">')
        myFile.write("""
                        <div>
                          <p class="headline">Material Index</p>
                        </div>
                        <div class="list_box">
                          <ul>                             
                    """)
        edbt_file_path = Path("edbt.json")
        if edbt_file_path.exists():
            edbt_file = open(edbt_file_path,)
            edbt_file_json = json.load(edbt_file)
            edbt_file.close()
            print("---------------- File edbt.json exists, adding TOC to " + str(len(edbt_file_json)) + " papers .... ----------------")
            paper_index = 1;
            for paper in edbt_file_json:
                paper_file_name = paper['path']['$t'].split("/")[1]
                #if paper_file_name == 'p49.pdf':
                fileHandler(paper_file_name)
                time.sleep(0.1)
                paper_index += 1
            shutil.copy('./noimg.png', './materials')
            final_sanity_check(edbt_file_json, myFile)
        else:
            print("---------------- File edbt.json does not exist, restart the process! ----------------")
    