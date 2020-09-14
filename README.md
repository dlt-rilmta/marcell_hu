# MARCELL annotation pipeline for Hungarian -- docker container

## build the docker image

```bash
make dbuild
```

## run the docker image

```bash
make drun
```

## usage

The API is listening for HTTP POST requests under the `/annotate` path.
There is only one parameter: `text` = raw text file path.
(Last line must be az empty line.)

```bash
curl -F "file=@<FILEPATH>" localhost:<port>/annotate
```

`<port>` is taken from the output of `make drun`.

## stop the docker image

```bash
make dstop
```

***

(Hungarian part)

## Leírás

- Magyar jogi szövegek elemzését teszi lehetővé a MARCELL projekt számára.
- Jelenleg elemezhető magyar jogi szövegek típusai, amiket elfogad a marcell_hu: 
*állásfoglalás, határozat, intézkedés, közlemény, nyilatkozat, parancs, rendelet, szakutasítás, tájékoztató, törvény, utasítás, végzés.*

## Installáció:
- Repozitórium klónozása:
`git clone https://github.com/dlt-rilmta/marcell_hu.git`
- Dependnciák telepítése:
`pip3 install -r requirements.txt`

## Command-line interface-es használata:
- Input: az [előre meghatározott típusok](https://github.com/dlt-rilmta/marcell_hu#le%C3%ADr%C3%A1s) közül egy darab elemzetlen (vagy elemzett) jogi szöveg.
- A modulok sorrendben való meghívása:
```bash 
cat input.txt | python3 main.py --conllu-comments tok,morph,pos,conv-morph,chunk,ner,fix-np,fix-ner,mmeta,term-iate,term-eurovoc,conll > output.conllup
```
- Annotate-tel, ami ugyanazt az eredményt adja, mintha meghívnánk az összes modult egymás után:
```bash
cat input.txt | python3 main.py --conllu-comments annotate > output.conllup

```

## Modulok:
- [e-magyar (emtsv) modulok](https://github.com/dlt-rilmta/emtsv#modules):
    - `emToken`, `emMorph`, `emTag`, `emChunk`, `emNER`, `emmorph2ud`, `emIOBUtils`, `emTerm`, `emCoNLL`
- MARCELL modul: 
    - `mMeta`: A törvényekből kinyerendő metaadatokat gyűjti össze és kommentként beleírja a kimeneti fájlba.
