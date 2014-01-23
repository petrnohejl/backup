Backup
======

Backup slouží k zálohování dat pomocí programu WinRAR 3.62 (jiné verze nebyly 
testovány). Pomocí tohoto skriptu lze snadno zálohovat všechna důležitá data
v počítači například na externí disk. Program Rar je podmínkou pro správný běh 
skriptu. Před spuštěním zálohování je potřeba správně skript nakonfigurovat. 
Konfigurační konstanty se nachází na začátku skriptu v souboru backup.py.

Konstanta BACKUP_LIST určuje cestu k textovému souboru, ve kterém jsou uloženy 
na samostatných řádcích cesty jednotlivých adresářů, které se budou zálohovat. 
Název tohoto souboru je implicitně 'backuplist.txt'. Konstanta OUTPUT_DIRECTORY 
určuje cestu k adresáři, kam se budou ukládat vytvořené archívy. Konstanta 
WIN_RAR_PATH určuje cestu k programu Rar.

Po spuštění skriptu je potřeba zadat heslo pro RAR archivy. Heslo není povinné.
Poté se na standardní výstup vypisuje průběh zálohování jednotlivých souborů a 
adresářů. Ve výstupním adresáři se tvoří archívy ve formátu .rar, odpovídající
jednotlivým adresářům v seznamu BACKUP_LIST. Název archívu se generuje 
automaticky dle data zálohy, názvu adresáře a případně názvu nad-adresáře. Pro 
každý archív se zároveň vytvoří textový soubor s informacemi o průběhu 
zálohování (volaný příkaz programu Rar, název archívu, velikost, délka 
zálohování, upozornění na chyby). Na závěr se vytvoří ještě jeden textový
soubor, shrnující celý průběh zálohování.


Použití
=======

Backup je konzolová aplikace a je napsána v jazyce Python 2.7. Pro její
spuštění je třeba mít nainstalován interpret jazyka Python, který lze
stáhnout na adrese www.python.org.

```bash
$ python backup.py    # spustí zálohu dat dle konfigurace skriptu
```


Developed by
============

* [Petr Nohejl](http://petrnohejl.cz)


License
=======

    Copyright 2011 Petr Nohejl

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
