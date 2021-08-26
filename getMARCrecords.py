import urllib.request
import json, csv, re
import xml.etree.ElementTree as ET

# recordList is the unprocessed input data, with emphasis on finding a bibid
recordList = []
# rejects represents records with no bibid; exported into 'no_bibid_[filename].csv'
rejects = []
# subjectConflicts is used to create a csv with instances of data in both ALMA and Piction SUBJECT fields, for comparison: 'subj_conflicts_[filename].csv'
subjectConflicts = []
dataConflicts = []

filename = 'batch-35_chunk_0'
# TODO: add this as an argument 
# filename = 'batch-37-short'

with open('csv_batches/splits/' + filename + '.csv', mode='r') as infile:
    # there are lots of NUL values in the files, so we're replacing them with ''
    reader = csv.reader((line.replace('\0','') for line in infile), delimiter=",")
    count = 0
    # because we have to parse every line (except line 0) looking for a BIBID before adding it to the record list, I did a quick n dirty header row assignment
    header = []
    for row in reader:
        if count == 0: 
            header = row
        if count > 1:
            rowObj = {}
            # iterate over row list and assign to matching value in header row
            for idx, val in enumerate(row):
                rowObj[header[idx]] = val
            # bibid will be autmatically assigned from any existing bibid field, 
            # but if it's empty, we can try to take it from catalog link; 
            # we're accounting for only 2 catalog link structures, not sure if there are more
            if rowObj['BIBID'] == '' and rowObj['CATALOG_LINK'] != '':
                try: 
                    urlBibidIdx = rowObj['CATALOG_LINK'].index('BBRecID=') + 8
                    rowObj['BIBID'] = rowObj['CATALOG_LINK'][urlBibidIdx:]
                except ValueError:
                    try:
                        urlBibidIdx = rowObj['CATALOG_LINK'].index('bibId=')  + 6
                        rowObj['BIBID'] = rowObj['CATALOG_LINK'][urlBibidIdx:]
                    except ValueError:
                        print(rowObj['UMO ID'] + ': no bib id')
            rowObj['BIBID'] = rowObj['BIBID'].replace('/t','').replace('	','').replace(' ','').replace('.jpg','')
            recordList.append(rowObj)
        count += 1

# redact api key before pushing
apikey = 'REDACTED'

# items is the home for the processed data; this is what's exported to 'data_[filename].csv'
items = []

# language list taken from some random ISO language list online - not this one specifically but it's probably the same: https://www.loc.gov/standards/iso639-2/php/English_list.php 
def languager(value):
    if   "eng" in value: return "English"
    elif "aar" in value: return "Afar"
    elif "abk" in value: return "Abkhaz"
    elif "ace" in value: return "Achinese"
    elif "ach" in value: return "Acoli"
    elif "ada" in value: return "Adangme"
    elif "ady" in value: return "Adygei"
    elif "afa" in value: return "Afroasiatic (Other)"
    elif "afh" in value: return "Afrihili (Artificial language)"
    elif "afr" in value: return "Afrikaans"
    elif "ain" in value: return "Ainu"
    elif "-ajm" in value: return "Aljamía"
    elif "aka" in value: return "Akan"
    elif "akk" in value: return "Akkadian"
    elif "alb" in value: return "Albanian"
    elif "ale" in value: return "Aleut"
    elif "alg" in value: return "Algonquian (Other)"
    elif "alt" in value: return "Altai"
    elif "amh" in value: return "Amharic"
    elif "ang" in value: return "English, Old (ca. 450-1100)"
    elif "anp" in value: return "Angika"
    elif "apa" in value: return "Apache languages"
    elif "ara" in value: return "Arabic"
    elif "arc" in value: return "Aramaic"
    elif "arg" in value: return "Aragonese"
    elif "arm" in value: return "Armenian"
    elif "arn" in value: return "Mapuche"
    elif "arp" in value: return "Arapaho"
    elif "art" in value: return "Artificial (Other)"
    elif "arw" in value: return "Arawak"
    elif "asm" in value: return "Assamese"
    elif "ast" in value: return "Bable"
    elif "ath" in value: return "Athapascan (Other)"
    elif "aus" in value: return "Australian languages"
    elif "ava" in value: return "Avaric"
    elif "ave" in value: return "Avestan"
    elif "awa" in value: return "Awadhi"
    elif "aym" in value: return "Aymara"
    elif "aze" in value: return "Azerbaijani"
    elif "bad" in value: return "Banda languages"
    elif "bai" in value: return "Bamileke languages"
    elif "bak" in value: return "Bashkir"
    elif "bal" in value: return "Baluchi"
    elif "bam" in value: return "Bambara"
    elif "ban" in value: return "Balinese"
    elif "baq" in value: return "Basque"
    elif "bas" in value: return "Basa"
    elif "bat" in value: return "Baltic (Other)"
    elif "bej" in value: return "Beja"
    elif "bel" in value: return "Belarusian"
    elif "bem" in value: return "Bemba"
    elif "ben" in value: return "Bengali"
    elif "ber" in value: return "Berber (Other)"
    elif "bho" in value: return "Bhojpuri"
    elif "bih" in value: return "Bihari (Other)"
    elif "bik" in value: return "Bikol"
    elif "bin" in value: return "Edo"
    elif "bis" in value: return "Bislama"
    elif "bla" in value: return "Siksika"
    elif "bnt" in value: return "Bantu (Other)"
    elif "bos" in value: return "Bosnian"
    elif "bra" in value: return "Braj"
    elif "bre" in value: return "Breton"
    elif "btk" in value: return "Batak"
    elif "bua" in value: return "Buriat"
    elif "bug" in value: return "Bugis"
    elif "bul" in value: return "Bulgarian"
    elif "bur" in value: return "Burmese"
    elif "byn" in value: return "Bilin"
    elif "cad" in value: return "Caddo"
    elif "cai" in value: return "Central American Indian (Other)"
    elif "-cam" in value: return "Khmer"
    elif "car" in value: return "Carib"
    elif "cat" in value: return "Catalan"
    elif "cau" in value: return "Caucasian (Other)"
    elif "ceb" in value: return "Cebuano"
    elif "cel" in value: return "Celtic (Other)"
    elif "cha" in value: return "Chamorro"
    elif "chb" in value: return "Chibcha"
    elif "che" in value: return "Chechen"
    elif "chg" in value: return "Chagatai"
    elif "chi" in value: return "Chinese"
    elif "chk" in value: return "Chuukese"
    elif "chm" in value: return "Mari"
    elif "chn" in value: return "Chinook jargon"
    elif "cho" in value: return "Choctaw"
    elif "chp" in value: return "Chipewyan"
    elif "chr" in value: return "Cherokee"
    elif "chu" in value: return "Church Slavic"
    elif "chv" in value: return "Chuvash"
    elif "chy" in value: return "Cheyenne"
    elif "cmc" in value: return "Chamic languages"
    elif "cnr" in value: return "Montenegrin"
    elif "cop" in value: return "Coptic"
    elif "cor" in value: return "Cornish"
    elif "cos" in value: return "Corsican"
    elif "cpe" in value: return "Creoles and Pidgins, English-based (Other)"
    elif "cpf" in value: return "Creoles and Pidgins, French-based (Other)"
    elif "cpp" in value: return "Creoles and Pidgins, Portuguese-based (Other)"
    elif "cre" in value: return "Cree"
    elif "crh" in value: return "Crimean Tatar"
    elif "crp" in value: return "Creoles and Pidgins (Other)"
    elif "csb" in value: return "Kashubian"
    elif "cus" in value: return "Cushitic (Other)"
    elif "cze" in value: return "Czech"
    elif "dak" in value: return "Dakota"
    elif "dan" in value: return "Danish"
    elif "dar" in value: return "Dargwa"
    elif "day" in value: return "Dayak"
    elif "del" in value: return "Delaware"
    elif "den" in value: return "Slavey"
    elif "dgr" in value: return "Dogrib"
    elif "din" in value: return "Dinka"
    elif "div" in value: return "Divehi"
    elif "doi" in value: return "Dogri"
    elif "dra" in value: return "Dravidian (Other)"
    elif "dsb" in value: return "Lower Sorbian"
    elif "dua" in value: return "Duala"
    elif "dum" in value: return "Dutch, Middle (ca. 1050-1350)"
    elif "dut" in value: return "Dutch"
    elif "dyu" in value: return "Dyula"
    elif "dzo" in value: return "Dzongkha"
    elif "efi" in value: return "Efik"
    elif "egy" in value: return "Egyptian"
    elif "eka" in value: return "Ekajuk"
    elif "elx" in value: return "Elamite"
    elif "enm" in value: return "English, Middle (1100-1500)"
    elif "epo" in value: return "Esperanto"
    elif "-esk" in value: return "Eskimo languages"
    elif "-esp" in value: return "Esperanto"
    elif "est" in value: return "Estonian"
    elif "-eth" in value: return "Ethiopic"
    elif "ewe" in value: return "Ewe"
    elif "ewo" in value: return "Ewondo"
    elif "fan" in value: return "Fang"
    elif "fao" in value: return "Faroese"
    elif "-far" in value: return "Faroese"
    elif "fat" in value: return "Fanti"
    elif "fij" in value: return "Fijian"
    elif "fil" in value: return "Filipino"
    elif "fin" in value: return "Finnish"
    elif "fiu" in value: return "Finno-Ugrian (Other)"
    elif "fon" in value: return "Fon"
    elif "fre" in value: return "French"
    elif "-fri" in value: return "Frisian"
    elif "frm" in value: return "French, Middle (ca. 1300-1600)"
    elif "fro" in value: return "French, Old (ca. 842-1300)"
    elif "frr" in value: return "North Frisian"
    elif "frs" in value: return "East Frisian"
    elif "fry" in value: return "Frisian"
    elif "ful" in value: return "Fula"
    elif "fur" in value: return "Friulian"
    elif "gaa" in value: return "Gã"
    elif "-gae" in value: return "Scottish Gaelix"
    elif "-gag" in value: return "Galician"
    elif "-gal" in value: return "Oromo"
    elif "gay" in value: return "Gayo"
    elif "gba" in value: return "Gbaya"
    elif "gem" in value: return "Germanic (Other)"
    elif "geo" in value: return "Georgian"
    elif "ger" in value: return "German"
    elif "gez" in value: return "Ethiopic"
    elif "gil" in value: return "Gilbertese"
    elif "gla" in value: return "Scottish Gaelic"
    elif "gle" in value: return "Irish"
    elif "glg" in value: return "Galician"
    elif "glv" in value: return "Manx"
    elif "gmh" in value: return "German, Middle High (ca. 1050-1500)"
    elif "goh" in value: return "German, Old High (ca. 750-1050)"
    elif "gon" in value: return "Gondi"
    elif "gor" in value: return "Gorontalo"
    elif "got" in value: return "Gothic"
    elif "grb" in value: return "Grebo"
    elif "grc" in value: return "Greek, Ancient (to 1453)"
    elif "gre" in value: return "Greek, Modern (1453-)"
    elif "grn" in value: return "Guarani"
    elif "gsw" in value: return "Swiss German"
    elif "-gua" in value: return "Guarani"
    elif "guj" in value: return "Gujarati"
    elif "gwi" in value: return "Gwich'in"
    elif "hai" in value: return "Haida"
    elif "hat" in value: return "Haitian French Creole"
    elif "hau" in value: return "Hausa"
    elif "haw" in value: return "Hawaiian"
    elif "heb" in value: return "Hebrew"
    elif "her" in value: return "Herero"
    elif "hil" in value: return "Hiligaynon"
    elif "him" in value: return "Western Pahari languages"
    elif "hin" in value: return "Hindi"
    elif "hit" in value: return "Hittite"
    elif "hmn" in value: return "Hmong"
    elif "hmo" in value: return "Hiri Motu"
    elif "hrv" in value: return "Croatian"
    elif "hsb" in value: return "Upper Sorbian"
    elif "hun" in value: return "Hungarian"
    elif "hup" in value: return "Hupa"
    elif "iba" in value: return "Iban"
    elif "ibo" in value: return "Igbo"
    elif "ice" in value: return "Icelandic"
    elif "ido" in value: return "Ido"
    elif "iii" in value: return "Sichuan Yi"
    elif "ijo" in value: return "Ijo"
    elif "iku" in value: return "Inuktitut"
    elif "ile" in value: return "Interlingue"
    elif "ilo" in value: return "Iloko"
    elif "ina" in value: return "Interlingua (International Auxiliary Language Association)"
    elif "inc" in value: return "Indic (Other)"
    elif "ind" in value: return "Indonesian"
    elif "ine" in value: return "Indo-European (Other)"
    elif "inh" in value: return "Ingush"
    elif "-int" in value: return "Interlingua (International Auxiliary Language Association)"
    elif "ipk" in value: return "Inupiaq"
    elif "ira" in value: return "Iranian (Other)"
    elif "-iri" in value: return "Irish"
    elif "iro" in value: return "Iroquoian (Other)"
    elif "ita" in value: return "Italian"
    elif "jav" in value: return "Javanese"
    elif "jbo" in value: return "Lojban (Artificial language)"
    elif "jpn" in value: return "Japanese"
    elif "jpr" in value: return "Judeo-Persian"
    elif "jrb" in value: return "Judeo-Arabic"
    elif "kaa" in value: return "Kara-Kalpak"
    elif "kab" in value: return "Kabyle"
    elif "kac" in value: return "Kachin"
    elif "kal" in value: return "Kalâtdlisut"
    elif "kam" in value: return "Kamba"
    elif "kan" in value: return "Kannada"
    elif "kar" in value: return "Karen languages"
    elif "kas" in value: return "Kashmiri"
    elif "kau" in value: return "Kanuri"
    elif "kaw" in value: return "Kawi"
    elif "kaz" in value: return "Kazakh"
    elif "kbd" in value: return "Kabardian"
    elif "kha" in value: return "Khasi"
    elif "khi" in value: return "Khoisan (Other)"
    elif "khm" in value: return "Khmer"
    elif "kho" in value: return "Khotanese"
    elif "kik" in value: return "Kikuyu"
    elif "kin" in value: return "Kinyarwanda"
    elif "kir" in value: return "Kyrgyz"
    elif "kmb" in value: return "Kimbundu"
    elif "kok" in value: return "Konkani"
    elif "kom" in value: return "Komi"
    elif "kon" in value: return "Kongo"
    elif "kor" in value: return "Korean"
    elif "kos" in value: return "Kosraean"
    elif "kpe" in value: return "Kpelle"
    elif "krc" in value: return "Karachay-Balkar"
    elif "krl" in value: return "Karelian"
    elif "kro" in value: return "Kru (Other)"
    elif "kru" in value: return "Kurukh"
    elif "kua" in value: return "Kuanyama"
    elif "kum" in value: return "Kumyk"
    elif "kur" in value: return "Kurdish"
    elif "-kus" in value: return "Kusaie"
    elif "kut" in value: return "Kootenai"
    elif "lad" in value: return "Ladino"
    elif "lah" in value: return "Lahndā"
    elif "lam" in value: return "Lamba (Zambia and Congo)"
    elif "-lan" in value: return "Occitan (post 1500)"
    elif "lao" in value: return "Lao"
    elif "-lap" in value: return "Sami"
    elif "lat" in value: return "Latin"
    elif "lav" in value: return "Latvian"
    elif "lez" in value: return "Lezgian"
    elif "lim" in value: return "Limburgish"
    elif "lin" in value: return "Lingala"
    elif "lit" in value: return "Lithuanian"
    elif "lol" in value: return "Mongo-Nkundu"
    elif "loz" in value: return "Lozi"
    elif "ltz" in value: return "Luxembourgish"
    elif "lua" in value: return "Luba-Lulua"
    elif "lub" in value: return "Luba-Katanga"
    elif "lug" in value: return "Ganda"
    elif "lui" in value: return "Luiseño"
    elif "lun" in value: return "Lunda"
    elif "luo" in value: return "Luo (Kenya and Tanzania)"
    elif "lus" in value: return "Lushai"
    elif "mac" in value: return "Macedonian"
    elif "mad" in value: return "Madurese"
    elif "mag" in value: return "Magahi"
    elif "mah" in value: return "Marshallese"
    elif "mai" in value: return "Maithili"
    elif "mak" in value: return "Makasar"
    elif "mal" in value: return "Malayalam"
    elif "man" in value: return "Mandingo"
    elif "mao" in value: return "Maori"
    elif "map" in value: return "Austronesian (Other)"
    elif "mar" in value: return "Marathi"
    elif "mas" in value: return "Maasai"
    elif "-max" in value: return "Manx"
    elif "may" in value: return "Malay"
    elif "mdf" in value: return "Moksha"
    elif "mdr" in value: return "Mandar"
    elif "men" in value: return "Mende"
    elif "mga" in value: return "Irish, Middle (ca. 1100-1550)"
    elif "mic" in value: return "Micmac"
    elif "min" in value: return "Minangkabau"
    elif "mis" in value: return "Miscellaneous languages"
    elif "mkh" in value: return "Mon-Khmer (Other)"
    elif "-mla" in value: return "Malagasy"
    elif "mlg" in value: return "Malagasy"
    elif "mlt" in value: return "Maltese"
    elif "mnc" in value: return "Manchu"
    elif "mni" in value: return "Manipuri"
    elif "mno" in value: return "Manobo languages"
    elif "moh" in value: return "Mohawk"
    elif "-mol" in value: return "Moldavian"
    elif "mon" in value: return "Mongolian"
    elif "mos" in value: return "Mooré"
    elif "mul" in value: return "Multiple languages"
    elif "mun" in value: return "Munda (Other)"
    elif "mus" in value: return "Creek"
    elif "mwl" in value: return "Mirandese"
    elif "mwr" in value: return "Marwari"
    elif "myn" in value: return "Mayan languages"
    elif "myv" in value: return "Erzya"
    elif "nah" in value: return "Nahuatl"
    elif "nai" in value: return "North American Indian (Other)"
    elif "nap" in value: return "Neapolitan Italian"
    elif "nau" in value: return "Nauru"
    elif "nav" in value: return "Navajo"
    elif "nbl" in value: return "Ndebele (South Africa)"
    elif "nde" in value: return "Ndebele (Zimbabwe)"
    elif "ndo" in value: return "Ndonga"
    elif "nds" in value: return "Low German"
    elif "nep" in value: return "Nepali"
    elif "new" in value: return "Newari"
    elif "nia" in value: return "Nias"
    elif "nic" in value: return "Niger-Kordofanian (Other)"
    elif "niu" in value: return "Niuean"
    elif "nno" in value: return "Norwegian (Nynorsk)"
    elif "nob" in value: return "Norwegian (Bokmål)"
    elif "nog" in value: return "Nogai"
    elif "non" in value: return "Old Norse"
    elif "nor" in value: return "Norwegian"
    elif "nqo" in value: return "N'Ko"
    elif "nso" in value: return "Northern Sotho"
    elif "nub" in value: return "Nubian languages"
    elif "nwc" in value: return "Newari, Old"
    elif "nya" in value: return "Nyanja"
    elif "nym" in value: return "Nyamwezi"
    elif "nyn" in value: return "Nyankole"
    elif "nyo" in value: return "Nyoro"
    elif "nzi" in value: return "Nzima"
    elif "oci" in value: return "Occitan (post-1500)"
    elif "oji" in value: return "Ojibwa"
    elif "ori" in value: return "Oriya"
    elif "orm" in value: return "Oromo"
    elif "osa" in value: return "Osage"
    elif "oss" in value: return "Ossetic"
    elif "ota" in value: return "Turkish, Ottoman"
    elif "oto" in value: return "Otomian languages"
    elif "paa" in value: return "Papuan (Other)"
    elif "pag" in value: return "Pangasinan"
    elif "pal" in value: return "Pahlavi"
    elif "pam" in value: return "Pampanga"
    elif "pan" in value: return "Panjabi"
    elif "pap" in value: return "Papiamento"
    elif "pau" in value: return "Palauan"
    elif "peo" in value: return "Old Persian (ca. 600-400 B.C.)"
    elif "per" in value: return "Persian"
    elif "phi" in value: return "Philippine (Other)"
    elif "phn" in value: return "Phoenician"
    elif "pli" in value: return "Pali"
    elif "pol" in value: return "Polish"
    elif "pon" in value: return "Pohnpeian"
    elif "por" in value: return "Portuguese"
    elif "pra" in value: return "Prakrit languages"
    elif "pro" in value: return "Provençal (to 1500)"
    elif "pus" in value: return "Pushto"
    elif "que" in value: return "Quechua"
    elif "raj" in value: return "Rajasthani"
    elif "rap" in value: return "Rapanui"
    elif "rar" in value: return "Rarotongan"
    elif "roa" in value: return "Romance (Other)"
    elif "roh" in value: return "Raeto-Romance"
    elif "rom" in value: return "Romani"
    elif "rum" in value: return "Romanian"
    elif "run" in value: return "Rundi"
    elif "rup" in value: return "Aromanian"
    elif "rus" in value: return "Russian"
    elif "sad" in value: return "Sandawe"
    elif "sag" in value: return "Sango (Ubangi Creole)"
    elif "sah" in value: return "Yakut"
    elif "sai" in value: return "South American Indian (Other)"
    elif "sal" in value: return "Salishan languages"
    elif "sam" in value: return "Samaritan Aramaic"
    elif "san" in value: return "Sanskrit"
    elif "-sao" in value: return "Samoan"
    elif "sas" in value: return "Sasak"
    elif "sat" in value: return "Santali"
    elif "-scc" in value: return "Serbian"
    elif "scn" in value: return "Sicilian Italian"
    elif "sco" in value: return "Scots"
    elif "-scr" in value: return "Croatian"
    elif "sel" in value: return "Selkup"
    elif "sem" in value: return "Semitic (Other)"
    elif "sga" in value: return "Irish, Old (to 1100)"
    elif "sgn" in value: return "Sign languages"
    elif "shn" in value: return "Shan"
    elif "-sho" in value: return "Shona"
    elif "sid" in value: return "Sidamo"
    elif "sin" in value: return "Sinhalese"
    elif "sio" in value: return "Siouan (Other)"
    elif "sit" in value: return "Sino-Tibetan (Other)"
    elif "sla" in value: return "Slavic (Other)"
    elif "slo" in value: return "Slovak"
    elif "slv" in value: return "Slovenian"
    elif "sma" in value: return "Southern Sami"
    elif "sme" in value: return "Northern Sami"
    elif "smi" in value: return "Sami"
    elif "smj" in value: return "Lule Sami"
    elif "smn" in value: return "Inari Sami"
    elif "smo" in value: return "Samoan"
    elif "sms" in value: return "Skolt Sami"
    elif "sna" in value: return "Shona"
    elif "snd" in value: return "Sindhi"
    elif "-snh" in value: return "Sinhalese"
    elif "snk" in value: return "Soninke"
    elif "sog" in value: return "Sogdian"
    elif "som" in value: return "Somali"
    elif "son" in value: return "Songhai"
    elif "sot" in value: return "Sotho"
    elif "spa" in value: return "Spanish"
    elif "srd" in value: return "Sardinian"
    elif "srn" in value: return "Sranan"
    elif "srp" in value: return "Serbian"
    elif "srr" in value: return "Serer"
    elif "ssa" in value: return "Nilo-Saharan (Other)"
    elif "-sso" in value: return "Sotho"
    elif "ssw" in value: return "Swazi"
    elif "suk" in value: return "Sukuma"
    elif "sun" in value: return "Sundanese"
    elif "sus" in value: return "Susu"
    elif "sux" in value: return "Sumerian"
    elif "swa" in value: return "Swahili"
    elif "swe" in value: return "Swedish"
    elif "-swz" in value: return "Swazi"
    elif "syc" in value: return "Syriac"
    elif "syr" in value: return "Syriac, Modern"
    elif "-tag" in value: return "Tagalog"
    elif "tah" in value: return "Tahitian"
    elif "tai" in value: return "Tai (Other)"
    elif "-taj" in value: return "Tajik"
    elif "tam" in value: return "Tamil"
    elif "-tar" in value: return "Tatar"
    elif "tat" in value: return "Tatar"
    elif "tel" in value: return "Telugu"
    elif "tem" in value: return "Temne"
    elif "ter" in value: return "Terena"
    elif "tet" in value: return "Tetum"
    elif "tgk" in value: return "Tajik"
    elif "tgl" in value: return "Tagalog"
    elif "tha" in value: return "Thai"
    elif "tib" in value: return "Tibetan"
    elif "tig" in value: return "Tigré"
    elif "tir" in value: return "Tigrinya"
    elif "tiv" in value: return "Tiv"
    elif "tkl" in value: return "Tokelauan"
    elif "tlh" in value: return "Klingon (Artificial language)"
    elif "tli" in value: return "Tlingit"
    elif "tmh" in value: return "Tamashek"
    elif "tog" in value: return "Tonga (Nyasa)"
    elif "ton" in value: return "Tongan"
    elif "tpi" in value: return "Tok Pisin"
    elif "-tru" in value: return "Truk"
    elif "tsi" in value: return "Tsimshian"
    elif "tsn" in value: return "Tswana"
    elif "tso" in value: return "Tsonga"
    elif "-tsw" in value: return "Tswana"
    elif "tuk" in value: return "Turkmen"
    elif "tum" in value: return "Tumbuka"
    elif "tup" in value: return "Tupi languages"
    elif "tur" in value: return "Turkish"
    elif "tut" in value: return "Altaic (Other)"
    elif "tvl" in value: return "Tuvaluan"
    elif "twi" in value: return "Twi"
    elif "tyv" in value: return "Tuvinian"
    elif "udm" in value: return "Udmurt"
    elif "uga" in value: return "Ugaritic"
    elif "uig" in value: return "Uighur"
    elif "ukr" in value: return "Ukrainian"
    elif "umb" in value: return "Umbundu"
    elif "und" in value: return "Undetermined"
    elif "urd" in value: return "Urdu"
    elif "uzb" in value: return "Uzbek"
    elif "vai" in value: return "Vai"
    elif "ven" in value: return "Venda"
    elif "vie" in value: return "Vietnamese"
    elif "vol" in value: return "Volapük"
    elif "vot" in value: return "Votic"
    elif "wak" in value: return "Wakashan languages"
    elif "wal" in value: return "Wolayta"
    elif "war" in value: return "Waray"
    elif "was" in value: return "Washoe"
    elif "wel" in value: return "Welsh"
    elif "wen" in value: return "Sorbian (Other)"
    elif "wln" in value: return "Walloon"
    elif "wol" in value: return "Wolof"
    elif "xal" in value: return "Oirat"
    elif "xho" in value: return "Xhosa"
    elif "yao" in value: return "Yao (Africa)"
    elif "yap" in value: return "Yapese"
    elif "yid" in value: return "Yiddish"
    elif "yor" in value: return "Yoruba"
    elif "ypk" in value: return "Yupik languages"
    elif "zap" in value: return "Zapotec"
    elif "zbl" in value: return "Blissymbolics"
    elif "zen" in value: return "Zenaga"
    elif "zha" in value: return "Zhuang"
    elif "znd" in value: return "Zande languages"
    elif "zul" in value: return "Zulu"
    elif "zun" in value: return "Zuni"
    elif "zxx" in value: return "No linguistic content"
    elif "zza" in value: return "Zaza"

# parsing dates from raw value
def dateFormatter(dateString):
    # looking for dates like 1951-67
    dateList = re.findall('[0-9]{4}-[0-9]{2}',dateString)
    if len(dateList) > 0:
        dateSort = dateList[0][0:4] + '/' + dateList[0][0:2]  + dateList[0][-2:]
    else:
        # looking for any 4-digit numeric string (prone to false hits, cross your fingers)
        dateList = re.findall('[0-9]{4}',dateString)
        if len(dateList) > 0:
            if dateList[0] != dateList[-1]:
                dateSort = min(dateList) + '/' + max(dateList)
            else: 
                dateSort = dateList[0]
        else:
            # looking for dates like 19-- 
            dateList = re.findall('[0-9]{2}--?',dateString)
            if len(dateList) > 0:
                dateSort = dateList[0]
    if 'dateSort' not in locals():
        dateSort = ''
    # removing initial 'd' carefully, since some dates have "december" in them - checking if the character after the 'd' is a number; 
    # could be done with regex too but, well, it isn't
    if dateString[0] == 'd' and ord(dateString[1]) >= 48 and ord(dateString[1]) <= 57:
        dateDisplay = dateString.strip(" .,d").replace('[','').replace(']','')
    else: 
        dateDisplay = dateString.strip(" .,").replace('[','').replace(']','')
    return [dateDisplay, dateSort, dateString]

# truncating titles at the first word break after n=150 characters; increase 'length' input parameter to change n
def titler(content, length=150, suffix='...'):
    content = content.text.replace("[", "").replace("]", "") 
    if content[-1:] == '/' or (content[-1:] == '.' and content[-3:] != '...') or content[-1:] == ',' :
        val = content[:-1].strip()
        content = val
    if len(content) <= length:
        returnValue = content
    else:
        returnValue = ' '.join(content[:length+1].split(' ')[0:-1]) + suffix
    return returnValue

for i in recordList:
    # print(i['BIBID'])
    itemDict = {}
    # many filenames for each bibid, so no use in calling the api for every file; do it once then check all the rest
    alreadyDoneIndex = next((index for (index, d) in enumerate(items) if len(items) > 0 and 'BIBID' in d and d['BIBID'] == i['BIBID']), None)
    if alreadyDoneIndex != None:
        print(i['BIBID'] + ' already done, reusing...')
        itemDict = items[alreadyDoneIndex]
        # have to make sure we're not reusing the filename too
        itemDict['FILENAME'] = i['FILE NAME']
    else: 
        itemUrl = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs?mms_id=99' + str(i['BIBID']) + '8805867&view=full&expand=None&apikey=' + apikey 
        itemData = urllib.request.urlopen(itemUrl)
        parsedXml = ET.parse(itemData)
        root = parsedXml.getroot()
        # root length = 0 is means something is wrong with your bibid (ie doesn't exist)
        if len(root) > 0:
            print(itemUrl)
            # print(root[0].find('mms_id').text)
            itemDict['BIBID'] = i['BIBID']
            itemDict['apiurl'] = itemUrl
            itemDict['FILENAME'] = i['FILE NAME']
            itemDict['TITLE'] = '' if root[0].find('title') is None else titler(root[0].find('title'))
            itemDict['CREATOR'] = ''
            itemDict['CREATOR_list'] = []
            # abandoned approach to getting creator
            # itemDict['CREATOR'] = '' if root[0].find('author') is None else root[0].find('author').text 
            itemDict['LANGUAGE'] = ''
            itemDict['LANGUAGE_list'] = ''
            itemDict['SUBJECT'] = ''
            itemDict['SUBJECT_list'] = []
            itemDict['PLACE'] = ''
            itemDict['PLACE_list'] = []
            itemDict['FORMAT'] = ''
            itemDict['FORMAT_list'] = []
            itemDict['BIO_HIST'] = ''
            itemDict['BIO_HIST_list'] = []
            itemDict['SUMMARY'] = ''
            itemDict['SUMMARY_list'] = []
            itemDict['DATE_DISPLAY'] = ''
            itemDict['DATE_DISPLAY_list'] = []
            itemDict['DATE_SORT'] = ''
            itemDict['DATE_SORT_list'] = {
                'dateDisplay': '',
                'dateSort': ''
            }
            # date raw can be used to verify dateFormatter results
            # itemDict['DATE_raw'] = ''
            itemDict['FORMAT_EXTENT'] = ''
            itemDict['FORMAT_EXTENT_list'] = []
            itemDict['CALL_NUMBER'] = ''
            itemDict['CALL_NUMBER_list'] = []
            itemDict['ARCHIVAL_COLLECTION'] = root[0].find("record/leader").text[7]
            itemDict['ARCHIVAL_COLLECTION_code'] = root[0].find("record/leader").text[7] + ': ' + root[0].find("record/leader").text
            itemDict['ARCHIVAL_COLLECTION_list'] = {
                '245': '',
                '710': ''
            }
            itemDict['CATALOG_LINK'] = 'https://i-share-nby.primo.exlibrisgroup.com/permalink/01CARLI_NBY/i5mcb2/alma' + str(i['BIBID'])
            itemDict['CONTRIBUTING_INSTITUTION'] = "Newberry Library"
            itemDict['OA_POLICY'] = "The Newberry makes its collections available for any lawful purpose, commercial or non-commercial, without licensing or permission fees to the library, subject to the following terms and conditions: https://www.newberry.org/rights-and-reproductions"
            itemDict['DISCLAIMER_NOTE'] = "All materials in the Newberry Library’s collections have research value and reflect the society in which they were produced. They may contain language and imagery that are offensive because of content relating to: ability, gender, race, religion, sexuality/sexual orientation, and other categories. More information: https://www.newberry.org/sites/default/files/textpage-attachments/Statement_on_Potentially_Offensive_Materials.pdf"
            itemDict['piction_PROJECT'] = i['PROJECT']
            # showing Jennifer some samples of piction/alma subject "conflicts" - may remove this version of the data if a decision is made to prioritize one 
            itemDict['piction_SUBJECT'] = i['SUBJECTS']
            itemDict['piction_INTERNALNOTES'] = i['INTERNALNOTES']
            itemDict['piction_FULLVOLUME'] = i['FULLVOLUME']
            itemDict['piction_APPROVED'] = i['APPROVED']
            # piction folder ??

            # these two add dash or pipe delimeters; dash is used in places, pipe is used in all multivalues
            def dashDelimeter(a,b):
                if len(a) > 0: 
                    return a + '--' + b
                else:
                    return b
            def pipeDelimeter(a,b):
                if len(a) > 0: 
                    return a + '|' + b
                else:
                    return b
            
            # rather than filling in blanks, we're looking at each value
            # uses MARC codes since I was concerned about capitalization differences 
            # switches to text field name when possible for readability
            for record in root[0].find('record'):
                def itemer(record, key):
                    # language exists in different fields depending on whether there's more than one
                    if key == '041' or key == '008':
                        if key == '008':
                            itemDict['LANGUAGE'] = languager(record.text)
                        else:
                            langString = ''
                            for value in record.findall('subfield'):
                                code = value.get('code')
                                if code == 'a':
                                    langString = languager(value.text)
                                else: 
                                    langString = langString + "|" + languager(value.text)
                            itemDict['LANGUAGE'] = langString
                    # archival collection is a concatenation of two fields; not always required and not all required data is always present
                    # this doesn't provide any warning on failure atm 
                    if key == 'ARCHIVAL_COLLECTION':
                        if itemDict['ARCHIVAL_COLLECTION'] == 'c': 
                            for value in record.findall('subfield'): 
                                if value.get('code') == 'a':
                                    itemDict['ARCHIVAL_COLLECTION'] = itemDict['TITLE'] + '|' + value.text
                            # print(itemDict['ARCHIVAL_COLLECTION'])
                    # subject is hard
                    if key == 'SUBJECT': 
                        # using a, x, y subfields for subject and then using/supplimenting place with z
                        subjectDict = {
                            'a': '',
                            'x': '',
                            'y': '',
                            'z': ''
                        }
                        # pushing values into a list 
                        for value in record.findall('subfield'): 
                            valueText = value.text
                            if value.text[-1:] == '.' or value.text[-1:] == ',':
                                valueText = value.text[:-1]
                            code = value.get('code')
                            if code == 'a': subjectDict['a'] = valueText
                            elif code == 'z': subjectDict['z'] = dashDelimeter(subjectDict['z'], valueText)
                        # fullValue = dashDelimeter(subjectDict['a'], dashDelimeter(subjectDict['x'], subjectDict['y']))
                        if len(subjectDict['a']) > 0 and subjectDict['a'] not in itemDict['SUBJECT_list'] and len(itemDict['SUBJECT_list']) < 5:
                            itemDict['SUBJECT_list'].append(subjectDict['a'])
                        stringVersion = ''
                        for val in itemDict['SUBJECT_list']:
                            stringVersion = pipeDelimeter(stringVersion, val)
                        itemDict['SUBJECT'] = stringVersion
                        if subjectDict['z'] not in itemDict['PLACE_list'] and len(subjectDict['z']) > 0:
                            itemDict['PLACE_list'].append(subjectDict['z'])
                            itemDict['PLACE_list'] = sorted(itemDict['PLACE_list'])
                    if key == 'PLACE': 
                        for value in record.findall('subfield'): 
                            if value.get('code') == 'a':
                                valueText = value.text
                                if '(Ill.)' in valueText:
                                    valueText = 'Illinois--' + valueText[:-7]
                                if '(Chicago, Ill.)' in valueText:
                                    valueText = 'Illinois--' + valueText[:-16]
                                if '(Italy)' in valueText:
                                    valueText = 'Italy--' + valueText[:-8]
                                if '(France)' in valueText:
                                    valueText = 'France--' + valueText[:-9]
                                if '(West Germany)' in valueText:
                                    valueText = 'West Germany--' + valueText[:-15]
                                if '(Germany)' in valueText:
                                    valueText = 'Germany--' + valueText[:-10]
                                if valueText not in itemDict['PLACE_list']: 
                                    itemDict['PLACE_list'].append(valueText)
                        stringVersion = ''
                        for idx, val in enumerate(itemDict['PLACE_list']):
                            if idx < 5:
                                stringVersion = pipeDelimeter(stringVersion, val)
                        itemDict['PLACE'] = stringVersion
                    if key == 'FORMAT':
                        keyList = key + '_list'
                        for value in record.findall('subfield'): 
                            if value.get('code') == 'a':
                                valueText = value.text
                                if value.text[-1:] == '.' or value.text[-1:] == ',':
                                    valueText = value.text[:-1]
                                if valueText not in itemDict[keyList]: 
                                    itemDict[keyList].append(valueText)
                            if value.get('code') == 'y' and (itemDict['DATE_SORT_list']['dateDisplay'] == '' or itemDict['DATE_SORT_list']['dateSort'] == ''):
                                dateString = dateFormatter(value.text)
                                itemDict['DATE_SORT_list']['dateDisplay'] = dateString[0]
                                itemDict['DATE_SORT_list']['dateSort'] = dateString[1]
                                # itemDict['DATE_raw'] = dateString[2]
                        stringVersion = ''
                        for val in itemDict[keyList]:
                            stringVersion = pipeDelimeter(stringVersion, val)
                        itemDict[key] = stringVersion
                    if key == 'FORMAT_EXTENT':
                        for value in record.findall('subfield'): 
                            valueText = value.text.replace(' cm.', ' cm').replace(' mm.', ' mm')
                            if len(itemDict['FORMAT_EXTENT']) > 0:
                                itemDict['FORMAT_EXTENT'] = itemDict['FORMAT_EXTENT'] + " " + valueText
                            else: 
                                itemDict['FORMAT_EXTENT'] = valueText
                    if key == 'CREATOR':
                        for value in record.findall('subfield'): 
                            code = value.get('code')
                            if code != 'e' and code.isalpha():
                                # remove trailing . and ,
                                valueText = ''
                                if value.text[-1:] == '.':
                                    valueText = value.text[:-1]
                                # elif value.text[-1:] == ',' and code != 'a':
                                #     valueText = value.text[:-1]
                                else:
                                    valueText = value.text
                                if len(itemDict[key]) > 0:
                                    itemDict[key] = itemDict[key] + " " + valueText
                                else: 
                                    itemDict[key] = valueText
                    if key == 'DATE_DISPLAY' or key == 'DATE_SORT':
                        # needs to grab date from other fields if its not in here
                        dateString =''
                        for value in record.findall('subfield'): 
                            if dateString == '':
                                dateString = value.text
                            else: 
                                dateString = dateString + ' ' + value.text
                        # re.search("^The.*Spain$", txt)
                        dateList = dateFormatter(dateString)
                        itemDict['DATE_DISPLAY'] = dateList[0]
                        itemDict['DATE_SORT'] = dateList[1]
                        # itemDict['DATE_raw'] = dateString[2]
                            # if value.text[:1] == 'd' or value.text[:1] == '[':
                            #     valueText = value.text[1:]
                            # if len(itemDict[key]) > 0 and itemDict[key].find('?') == -1:
                            #     if int(itemDict[key]) and int(itemDict[key]) < int(valueText):
                            #         itemDict[key] = itemDict[key] + delimiter + valueText
                            # elif int(valueText):
                            #     itemDict[key] =  valueText 
                            # else: 
                            #     print('date error, value: ' + valueText + '; api url: ' + itemUrl)
                    if key == 'BIO_HIST' or key == 'SUMMARY':
                        for value in record.findall('subfield'):
                            if value.get('code') == 'a' or value.get('code') == 'b':
                                itemDict[key] = value.text 
                    if key == 'CALL_NUMBER':
                        for value in record.findall('subfield'):
                            if value.get('code').isalpha():
                                if len(itemDict[key]) > 0:
                                    itemDict[key] = itemDict[key] + " " + value.text 
                                else: 
                                    itemDict[key] = value.text
                
                marcCode = record.get('tag')
                if marcCode == '100': itemer(record, 'CREATOR')
                if marcCode == '245': itemer(record, 'TITLE')
                if marcCode == '650': itemer(record, 'SUBJECT')
                if marcCode == '651': itemer(record, 'PLACE')
                if marcCode == '655': itemer(record, 'FORMAT')
                if marcCode == '545': itemer(record, 'BIO_HIST')
                if marcCode == '520': itemer(record, 'SUMMARY')
                if marcCode == '045': itemer(record, 'DATE_DISPLAY')
                if marcCode == '045': itemer(record, 'DATE_SORT')
                if marcCode == '300': itemer(record, 'FORMAT_EXTENT')
                if marcCode == '008': itemer(record, '008')
                if marcCode == '041': itemer(record, '041')
                if marcCode == '099': itemer(record, 'CALL_NUMBER')
                if marcCode == '852': itemer(record, 'CALL_NUMBER')
                if marcCode == '710': itemer(record, 'ARCHIVAL_COLLECTION')
                # if marcCode == '856': itemer(record, 'CATALOG_LINK')
                if len(itemDict['PLACE']) == 0: 
                    stringVersion = ''

                    for idx, val in enumerate(itemDict['PLACE_list']):
                        if idx < 5:
                            stringVersion = pipeDelimeter(stringVersion, val)
                    itemDict['PLACE'] = stringVersion
                # if itemDict['TITLE'][-1:] == '/' or itemDict['TITLE'][-1:] == '.':
                if itemDict['TITLE'][-1:] == '/' or (itemDict['TITLE'][-1:] == '.' and itemDict['TITLE'][-3:] != '...') or itemDict['TITLE'][-1:] == ',' :
                    val = itemDict['TITLE'][:-1].strip()
                    itemDict['TITLE'] = val
                if itemDict['CREATOR'][-1:] == ',':
                    itemDict['CREATOR'] = itemDict['CREATOR'][:-1].strip()
                if itemDict['ARCHIVAL_COLLECTION'] == 'm': 
                    itemDict['ARCHIVAL_COLLECTION'] = ''
                if itemDict['ARCHIVAL_COLLECTION'] == 'c': 
                    # root[0].find("record/leader").text
                    itemDict['ARCHIVAL_COLLECTION'] = 'value has "c" in 8th position but has no value for 710'
                if itemDict['DATE_SORT_list']['dateSort'] == '' or itemDict['DATE_SORT_list']['dateDisplay'] == '':
                    try: 
                        dateString = dateFormatter(root[0].find("date_of_publication").text)
                        itemDict['DATE_DISPLAY'] = dateString[0]
                        itemDict['DATE_SORT'] = dateString[1]
                    except AttributeError:
                        continue 
                    # itemDict['DATE_raw'] = dateString[2]
                else:
                    itemDict['DATE_DISPLAY'] = itemDict['DATE_SORT_list']['dateDisplay']
                    itemDict['DATE_SORT'] = itemDict['DATE_SORT_list']['dateSort']
                # reusing piction data:
                # if itemDict['TITLE'] == '' and i['TITLE'] != '': itemDict['TITLE'] = i['TITLE'] # title
                # if itemDict['CREATOR'] == '' and i['CREATOR'] != '': itemDict['CREATOR'] = i['CREATOR'] # creator
                # if itemDict['CALL_NUMBER'] == '' and i['CALLNUMBER'] != '': itemDict['CALL_NUMBER'] = i['CALLNUMBER'] # call number
                # # if itemDict['SUBJECT'] == '' and i['SUBJECTS'] != '': itemDict['SUBJECT'] = "|".join([x.strip() for x in i['SUBJECTS'].split(';')])# subject
                # if itemDict['FORMAT'] == '' and i['FORMAT'] != '': itemDict['FORMAT'] = i['FORMAT'] # format
                # if itemDict['FORMAT_EXTENT'] == '' and i['FORMAT_EXTENT'] != '': itemDict['FORMAT_EXTENT'] = i['FORMAT_EXTENT'].replace(' cm.', ' cm').replace(' mm.', ' mm') # format_extent
                # if itemDict['PLACE'] == '' and i['PLACE'] != '': itemDict['PLACE'] = i['PLACE'] # place
                # if itemDict['LANGUAGE'] == '' and i['LANGUAGE'] != '': itemDict['LANGUAGE'] = "|".join([x.strip() for x in i['LANGUAGE'].split(';')]) # language
                # if itemDict['CATALOG_LINK'] == '' and i['CATALOG_LINK'] != '': itemDict['CATALOG_LINK'] = i['CATALOG_LINK'] # cataloglink
                if itemDict['TITLE'] == '' and i['TITLE'] != '': 
                    conflict = {'filename': itemDict['FILENAME'], 'bibid': itemDict['BIBID'], 'field': 'TITLE', 'pictionvalue': i['TITLE']}
                    dataConflicts.append(conflict)
                    # itemDict['TITLE'] = i['TITLE'] # title
                if itemDict['CREATOR'] == '' and i['CREATOR'] != '': 
                    conflict = {'filename': itemDict['FILENAME'], 'bibid': itemDict['BIBID'], 'field': 'CREATOR', 'pictionvalue': i['CREATOR']}
                    dataConflicts.append(conflict)
                    # itemDict['CREATOR'] = i['CREATOR'] # creator
                if itemDict['CALL_NUMBER'] == '' and i['CALLNUMBER'] != '': 
                    conflict = {'filename': itemDict['FILENAME'], 'bibid': itemDict['BIBID'], 'field': 'CALLNUMBER', 'pictionvalue': i['CALLNUMBER']}
                    dataConflicts.append(conflict)
                    # itemDict['CALL_NUMBER'] = i['CALLNUMBER'] # call number
                if itemDict['FORMAT'] == '' and i['FORMAT'] != '': 
                    conflict = {'filename': itemDict['FILENAME'], 'bibid': itemDict['BIBID'], 'field': 'FORMAT', 'pictionvalue': i['FORMAT']}
                    dataConflicts.append(conflict)
                    # itemDict['FORMAT'] = i['FORMAT'] # format
                if itemDict['FORMAT_EXTENT'] == '' and i['FORMAT_EXTENT'] != '': 
                    conflict = {'filename': itemDict['FILENAME'], 'bibid': itemDict['BIBID'], 'field': 'FORMAT_EXTENT', 'pictionvalue': i['FORMAT_EXTENT']}
                    dataConflicts.append(conflict)
                    # itemDict['FORMAT_EXTENT'] = i['FORMAT_EXTENT'].replace(' cm.', ' cm').replace(' mm.', ' mm') # format_extent
                if itemDict['PLACE'] == '' and i['PLACE'] != '': 
                    conflict = {'filename': itemDict['FILENAME'], 'bibid': itemDict['BIBID'], 'field': 'PLACE', 'pictionvalue': i['PLACE']}
                    dataConflicts.append(conflict)
                    # itemDict['PLACE'] = i['PLACE'] # place
                if itemDict['LANGUAGE'] == '' and i['LANGUAGE'] != '': 
                    conflict = {'filename': itemDict['FILENAME'], 'bibid': itemDict['BIBID'], 'field': 'LANGUAGE', 'pictionvalue': i['LANGUAGE']}
                    dataConflicts.append(conflict)
                    # itemDict['LANGUAGE'] = "|".join([x.strip() for x in i['LANGUAGE'].split(';')]) # language
                if itemDict['CATALOG_LINK'] == '' and i['CATALOG_LINK'] != '': 
                    conflict = {'filename': itemDict['FILENAME'], 'bibid': itemDict['BIBID'], 'field': 'CATALOG_LINK', 'pictionvalue': i['CATALOG_LINK']}
                    dataConflicts.append(conflict)
                    # itemDict['CATALOG_LINK'] = i['CATALOG_LINK'] # cataloglink

            del itemDict['CREATOR_list']
            del itemDict['SUBJECT_list']
            del itemDict['PLACE_list']
            del itemDict['FORMAT_list']
            del itemDict['BIO_HIST_list']
            del itemDict['SUMMARY_list']
            del itemDict['DATE_DISPLAY_list']
            del itemDict['DATE_SORT_list']
            del itemDict['FORMAT_EXTENT_list']
            del itemDict['LANGUAGE_list']
            del itemDict['CALL_NUMBER_list']
            del itemDict['ARCHIVAL_COLLECTION_list']
            # del itemDict['CATALOG_LINK_list']
        else: 
            rejectObj = {
                'UMO ID': i['UMO ID'],
                'FILE NAME': i['FILE NAME']
            }
            rejects.append(rejectObj)
            print("failure: API results have a length of 0 on UMO " + i['UMO ID'] )
    if len(itemDict) > 0:
        items.append(itemDict)

for item in items:
    if item['SUBJECT'] != '' and item['piction_SUBJECT'] != '':
        confObj = {
            'CATLINK': item['CATALOG_LINK'],
            'Piction SUBJECT': item['piction_SUBJECT'],
            'ALMA SUBJECT': item['SUBJECT']
        }
        subjectConflicts.append(confObj)

directory = './output/'

dataFilename = 'data_'  + filename + '.csv'

dataFile = open(directory + 'json_' + dataFilename + '.json', "w")
dataFile.write(json.dumps(items, indent=4))

print("length of item array: " + str(len(items)))
if len(items) > 0:
    keys = items[0].keys()
    with open(directory + dataFilename, 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(items)
else: 
    print("Big error.  Items array was length = 0")

if len(rejects) > 0:
    rejectsFilename = 'no_bibid_' + filename + '.csv'
    keys = rejects[0].keys()
    with open(directory + rejectsFilename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(rejects)

if len(subjectConflicts) > 0:
    subj_conflictsFilename = 'subj_conflicts_' + filename + '.csv'
    keys = subjectConflicts[0].keys()
    with open(directory + subj_conflictsFilename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(subjectConflicts)

if len(dataConflicts) > 0:
    data_conflictsFilename = 'data_conflicts_' + filename + '.csv'
    keys = dataConflicts[0].keys()
    with open(directory + data_conflictsFilename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dataConflicts)
