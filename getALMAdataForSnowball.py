import urllib.request
import json, csv, re, os, sys
import xml.etree.ElementTree as ET
from datetime import date
import requests
import config
from pprint import pprint as pp
import time
import argparse

start = time.time()

curYear = date.today().year
today = str(date.today())

# redact api key before pushing
apikey = config.apiKey

reviewSet = []

def set_dict():
    itemDict = {}
    itemDict['FILENAME'] = ''
    itemDict['BIBID'] = ''
    itemDict['TITLE'] = ''
    itemDict['CREATOR'] = ''
    itemDict['PUBLISHER_ORIGINAL'] = ''
    itemDict['CALL_NUMBER'] = ''
    itemDict['FORMAT_EXTENT'] = ''
    itemDict['DESCRIPTION'] = ''
    itemDict['LANGUAGE'] = ''
    itemDict['SUBJECTS'] = ''
    itemDict['PLACE'] = ''
    itemDict['FORMAT'] = ''
    itemDict['BIOGRAPHICAL/HISTORICAL NOTE'] = ''
    itemDict['SUMMARY'] = ''
    itemDict['DATE_DISPLAY'] = ''
    itemDict['DATE_SORT'] = ''
    itemDict['STANDARDIZED_RIGHTS'] = ''
    itemDict['ARCHIVAL_COLLECTION'] = ''
    itemDict['ARCHIVAL_COLLECTION_list'] = {
                '1': '',
                '2': ''
            }
    itemDict['SUBJECTS_list'] = []
    itemDict['PLACE_list'] = []
    itemDict['FORMAT_list'] = []
    # will not be filled by this script:
    itemDict['DATE_DIGITAL'] = ''
    itemDict['ACCESS_STMT'] = ''
    itemDict['TITLE_ALTERNATIVE'] = ''
    itemDict['CONTRIBUTOR'] = ''
    itemDict['TRANSCRIPTION'] = ''
    itemDict['CITATION'] = ''
    itemDict['IN_COPYRIGHT'] = ''
    itemDict['PURPOSE'] = 'Public'
    itemDict['CATALOG_LINK'] = ''
    itemDict['OA_POLICY'] = ''
    itemDict['DISCLAIMER_STMT'] = ''
    itemDict['DCMIType'] = ''
    itemDict['CONTRIBUTING_INSTITUTION'] = ''

    return itemDict



# language list taken from some random ISO language list online - not this one specifically but it's probably the same: https://www.loc.gov/standards/iso639-2/php/English_list.php 
def languageFormatter(value):
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
    # elif "zxx" in value: return "No linguistic content"
    elif "zza" in value: return "Zaza"


def strip_bibid(bibid):
    if len(bibid) < 8:
        return bibid
    else:
        r = r'^99([0-9]*)8805867'
        bibid_search = re.findall(r, bibid)
        try:
            return bibid_search[0]
        except IndexError:
            return bibid


def rearrange_sortDate(date):
    dates = date.split('-')
    if len(dates) == 2:
        if int(dates[0]) > int(dates[1]):
            # pp(dates[0])
            # pp(dates[1])
            date = f'{dates[1]}-{dates[0]}'
    pp(date)
    return date


# parsing dates from raw value
def dateFormatter(dateString):
    dateSort = ''
    dateDisplay = ''
    # looking for 8-digit dates, take first 4 digits (year only)
    if len(re.findall('[0-9]{8}',dateString)) > 0:
        dateList = re.findall('[0-9]{8}',dateString)
        dateList.sort()
        dateSort = dateList[0][:4] + '/' + dateList[-1][:4]
        dateDisplay = dateList[0][:4] + '-' + dateList[-1][:4]
    # looking for dates like 1876-1987 with or without
    elif len(re.findall('[0-9]{4}\??-[0-9]{4}\??',dateString)) > 0:
        dateList = re.findall('[0-9]{4}',dateString)
        dateList.sort()
        # getting rid of ?
        dateSort = dateList[0].replace('?', '') + '/' + dateList[-1].replace('?', '')
        dateDisplay = dateList[0] + '-' + dateList[-1]
    # looking for dates like 1285-15--? (does NOT handle the reverse, but if that comes up this can be copypasted and repurposed)
    elif len(re.findall('[0-9]{4}\??-[0-9]{2}--\??',dateString)) > 0:
        dateList = re.findall('[0-9]{4}\??-[0-9]{2}--\??',dateString)
        dateSort = dateList[0][0:4] + '/' + dateList[0][5:7]  + '99'
        dateDisplay = dateList[0]
    # looking for dates like 1951-67 (first 2 digits will be applied to last 2, eg 1951/1967)
    elif len(re.findall('[0-9]{4}\??-[0-9]{2}\??',dateString)) > 0:
        dateList = re.findall('[0-9]{4}\??-[0-9]{2}\??',dateString)
        dateSortNoQ = dateList[0].replace('?', '')
        dateSort = dateSortNoQ[0:4] + '/' + dateSortNoQ[0:2]  + dateSortNoQ[-2:]
        dateDisplay = dateList[0][0:4] + '-' + dateList[0][-2:]
    # looking for 4 digit dates with or without ?
    elif len(re.findall('[0-9]{4}\??',dateString)) > 0:
        dateList = re.findall('[0-9]{4}\??',dateString)
        dateList.sort()
        for d in dateList: 
            if len(dateSort) > 0:
                dateSort = dateSort + '/' + d.replace('?', '')
                dateDisplay = dateDisplay + '-' + d
            else: 
                dateSort = d.replace('?', '')
                dateDisplay = d
    else:
        # looking for dates like 19-- 
        dateList = re.findall('[0-9]{3}-{1}?\??|[0-9]{2}-{2}?\??',dateString)
        if len(dateList) > 0 and dateList != None:
            for d in dateList:   
                d = d.replace('-','0')
            dateList = dateList.sort()
            try:
                for d in dateList:
                    if len(dateSort) > 0:
                        dateSort = dateSort + '/' + d.replace('?', '')
                        dateDisplay = dateDisplay + '-' + d
                    else: 
                        dateSort = d.replace('?', '')
                        dateDisplay = d
            except TypeError:
                if len(dateSort) > 0:
                    dateSort = dateSort + '/' + d.replace('?', '')
                    dateDisplay = dateDisplay + '-' + d
                else: 
                    dateSort = d.replace('?', '')
                    dateDisplay = d
                # print(d)]
    # standardized rights - get highest date in the date arrays, compare to curYear - 95
    if dateSort == '':
        dateArray = dateDisplay.split('-')
    else:
        dateArray = dateSort.split('/')
    maxDate = 0
    for d in dateArray: 
        try: 
            if d != '' and int(d) > maxDate:
                maxDate = int(d)
        except ValueError: 
            rights = 'Copyright Not Evaluated'
    # dateArray = [int(x) for x in dateArray]
    # maxDate = max(dateArray)
    rights = ''
    if maxDate <= curYear - 95:
        print("meets conditions for being out of copyright")
        rights = 'No Copyright - United States'
    else: 
        rights = 'Copyright Not Evaluated'
    # removing initial 'd' carefully, since some dates have "december" in them - checking if the character after the 'd' is a number; 
    # could be done with regex too but it isn't
    # if dateString[0] == 'd' and ord(dateString[1]) >= 48 and ord(dateString[1]) <= 57:
    #     dateDisplay = dateString.strip(" .,d").replace('[','').replace(']','')
    # else: 
    #     dateDisplay = dateString.strip(" .,").replace('[','').replace(']','')

    # into the trash with these
    deleteList = ['n.d.', 'no date', 'undated']

    for dl in deleteList:
        if dateDisplay == dl:
            dateDisplay = ''

    return [dateDisplay, dateSort, dateString, rights]

# truncating titles at the first word break after n=150 characters; increase 'length' input parameter to change n
def titleFormatter(content, length=150, suffix='...'):
    content = content.replace("[manuscript]","").replace("[", "").replace("]", "") 
    if content[-1:] == '/' or (content[-1:] == '.' and content[-3:] != '...') or content[-1:] == ',' :
        content = content.strip('/.,')
    if len(content) <= length:
        returnValue = content
    else:
        returnValue = ' '.join(content[:length+1].split(' ')[0:-1]) + suffix
    return returnValue

# the next 3 functions just concatenate with dash, pipe, and space delimeters respectively
def dashDelimeter(a,b):
    if len(a) > 0: 
        return a + '--' + b
    else:
        return b

def pipeDelimeter(a,b):
    try:
        if a == b: 
            return a
        elif len(a) > 0: 
            return a + '|' + b
        else:
            return b
    except:
        return a

def concatenator(a,b):
    if len(a) > 0:
        return a + ' ' + b
    else: 
        return b

# because a lot of values can come from multiple marc codes, we dump them all into a list and then resolve the list after we've been through all the fields
# initially created for place and subjects
def resolveList(value):
    valueString = ''
    for idx, val in enumerate(value):
        if idx < 6:
            valueString = pipeDelimeter(valueString, val)
    return valueString


def get_bibid_dict(filename):
    # pp(filename)
    d = {}
    d['BIBID'] = ''
    d['FILENAME'] = ''    
    try:
        bibid = filename.split('_')[0]
        d['BIBID'] = bibid
        original_filename = filename.replace(bibid + '_', '')
        d['FILENAME'] = original_filename
    except Exception as e:
        pp(d)
        return d
    
    return d


def placeFormatter(valueText):
    if '(Ill.)' in valueText:
        valueText = 'Illinois--' + valueText[:-7]
    if '(Chicago, Ill.)' in valueText:
        valueText = 'Illinois--' + valueText[:-16]
    if '(Italy)' in valueText:
        valueText = 'Italy--' + valueText[:-8]
    if '(France)' in valueText:
        valueText = 'France--' + valueText[:-9]
    if '(Brazil)' in valueText:
        valueText = 'Brazil--' + valueText[:-9]
    if '(West Germany)' in valueText:
        valueText = 'West Germany--' + valueText[:-15]
    if '(Germany)' in valueText:
        valueText = 'Germany--' + valueText[:-10]
    if '(Ariz.)' in valueText:
        valueText = 'Arizona--' + valueText[:-8]
    if '(Conn.)' in valueText:
        valueText = 'Connecticut--' + valueText[:-8]
    if 'Canada, Eastern' in valueText:
        valueText = 'Eastern Canada'
    if 'East (U.S.)' in valueText:
        valueText = 'East United States'
    if 'Istanbul (Turkey)' in valueText:
        valueText = 'Turkey--' + valueText[:-9]
    if '(Philippines)' in valueText:
        valueText = 'Philippines--' + valueText[:-14]
    if '(Mexico)' in valueText:
        valueText = 'Mexico--' + valueText[:-9]
    if '(Québec)' in valueText:
        valueText = 'Québec--' + valueText[:-9]
    if '(Quebec)' in valueText:
        valueText = 'Québec--' + valueText[:-9]
    if '(Iowa)' in valueText:
        valueText = 'Iowa--' + valueText[:-7]
    if '(London, England)' in valueText:
        valueText = 'England--London--' + valueText[:-18]
    if '(Greenland)' in valueText:
        valueText = 'Greenland--' + valueText[:-12]
    if '(Calif.)' in valueText:
        valueText = 'California--' + valueText[:-9]
    if '(Fla.)' in valueText:
        valueText = 'Florida--' + valueText[:-7]
    if '(Ind.)' in valueText:
        valueText = 'Indiana--' + valueText[:-7]
    if '(S.D.)' in valueText:
        valueText = 'South Dakota--' + valueText[:-7]
    if '(N.Y.)' in valueText:
        valueText = 'New York--' + valueText[:-7]
    if '(Vt.)' in valueText:
        valueText = 'Vermont--' + valueText[:-6]
    if '(Indianapolis, Ind.)' in valueText:
        valueText = 'Indiana--Indianapolis--' + valueText[:-21]
    if valueText == 'Tulancingo (Hidalgo, Mexico)':
        valueText = 'Mexico--Tulancingo (Hidalgo)'
    if valueText == 'Coyoacán (Mexico)':
        valueText = 'Mexico--Coyoacán (Mexico City)'
    if valueText == 'Colorado River Valley (Colo.-Mexico)':
        valueText = 'North America--Colorado River Valley'
    if valueText == 'Arctic regions':
        valueText = 'Arctic Regions'
    if valueText == "East (U.S.)" or valueText == "East United States":
        valueText = "East United States"
    if valueText == "Canada, Eastern" or valueText == "Eastern Canada":
        valueText = "Eastern Canada"    
    if valueText == "Canada, Eastern|East (U.S.)|East United States|Eastern Canada":
        valueText = "East United States|Eastern Canada"
    if valueText == "East Indies":
        valueText = "Asia--East Indies"
    if valueText == "Hudson River Valley (N.Y. and N.J.)":
        valueText = "United States--Hudson River Valley"
    if valueText == "Montréal (Québec)":
        valueText = "Québec--Montréal"
    if valueText == "Wabash River Valley":
        valueText = "United States--Wabash River Valley"
    if valueText == "Québec (Province)":
        valueText = "Québec"
    if valueText == "Mecklenburg (Germany : Region)":
        valueText = "Germany--Mecklenburg Region"
    if valueText == "Minnesota--Saint Paul Region|Wisconsin|Saint Paul Region (Minn.)":
        valueText = "Minnesota--Saint Paul Region|Wisconsin"
    if valueText == "New York (N.Y.)":
        valueText = "New York (State)--New York"
    if valueText == "Northwest Passage":
        valueText = "Arctic Ocean--Northwest Passage"
    if valueText == "Parma":
        valueText = "Italy--Parma"
    if valueText == "Piacenza":
        valueText = "Italy--Piacenza"
    if valueText == "El Arahal (Spain)":
        valueText = "Spain--El Arahal"
    if valueText == "Thrace":
        valueText = "Mediterranean Region--Thrace"
    if valueText == "Yucatán Peninsula":
        valueText = "Central America--Yucatán Peninsula"
    if valueText == "United States Highway 1":
        valueText = "United States--United States Highway 1"
    if valueText == "United States Highway 1":
        valueText = "United States--United States Highway 1"
    if valueText == "Glacier National Park (Mont.)":
        valueText = "Montana--Glacier National Park"
    if valueText == "Mato Grosso (Brazil : State)":
        valueText = "Brazil--Matto Grosso (State)"
    if valueText == "Villa Bella (Bolivia)":
        valueText = "Bolivia--Villa Bella"
    if valueText == "Southwest, New":
        valueText = "New Southwest"

    return valueText


def add_box_no_to_title(filename, title):
    box_search = re.findall("box_([0-9]*)",filename)
    if len(box_search) > 0:
        box_str = f' [box {box_search[0]}]'
        title = title.split(',')
        try:
            title = title[0] + box_str + ',' + title[1]
            return title
        except IndexError:
            title = title[0] + box_str
            return title
    else:
        return title


def valueAssignmentFromCode(record,code):
    # DCMIType
    if code == None:
        type_code = record.text[6]
        if type_code == 'g':
            itemDict['DCMIType'] = 'Moving Image'
        if type_code == 'r':
            itemDict['DCMIType'] = 'Physical Object'
        if type_code == 'i' or type_code == 'j':
            itemDict['DCMIType'] = 'Sound'
        if type_code in 'cedfr':
            itemDict['DCMIType'] = 'Still Image'
        if type_code in 'at':
            itemDict['DCMIType'] = 'Text'
        if type_code == 'p':
            itemDict['DCMIType'] = 'Text'
        if type_code == 'e':
            itemDict['FORMAT_list'].append('Cartographic materials')
    # language and date (#2)
    if code == '008' or code == '041': 
        if code == '008' and itemDict['LANGUAGE'] == '':
            itemDict['LANGUAGE'] = languageFormatter(record.text)
        else:
            langString = ''
            for value in record.findall('subfield'):
                if value.get('code') == 'a':
                    langString = languageFormatter(value.text)
                    langString = pipeDelimeter(itemDict['LANGUAGE'], langString)
            itemDict['LANGUAGE'] = langString
        if code == '008':
            if len(re.findall('[0-9]{8}',record.text[7:15])) > 0:
                eightdigits = record.text[7:11] + '-' + record.text[11:15]
                eightdigits = rearrange_sortDate(eightdigits)
                itemDict['DATE_DISPLAY'] = eightdigits
                itemDict['DATE_SORT'] = eightdigits.replace('-','/')
                if 'STANDARDIZED_RIGHTS' not in itemDict or itemDict['STANDARDIZED_RIGHTS'] == '':
                    rights = 'No Copyright - United States' if int(record.text[11:15]) < curYear - 95 else 'Copyright Not Evaluated' 
                    itemDict['STANDARDIZED_RIGHTS'] = rights
            elif len(re.findall('[0-9]{4}',record.text[7:11])) > 0:
                fourdigits = record.text[7:11]
                itemDict['DATE_DISPLAY'] = fourdigits
                itemDict['DATE_SORT'] = fourdigits
                if 'STANDARDIZED_RIGHTS' not in itemDict or itemDict['STANDARDIZED_RIGHTS'] == '':
                    rights = 'No Copyright - United States' if int(fourdigits) < curYear - 95 else 'Copyright Not Evaluated' 
                    itemDict['STANDARDIZED_RIGHTS'] = rights
            elif len(re.findall('[0-9]{2}',record.text[7:9])) > 0:
                twodigits = int(record.text[7:9])
                twodigits = record.text[7:9] + '00'
                print(record.text)
                itemDict['DATE_DISPLAY'] = twodigits
                itemDict['DATE_SORT'] = twodigits
                if 'STANDARDIZED_RIGHTS' not in itemDict or itemDict['STANDARDIZED_RIGHTS'] == '':
                    rights = 'No Copyright - United States' if int(twodigits) < curYear - 95 else 'Copyright Not Evaluated' 
                    itemDict['STANDARDIZED_RIGHTS'] = rights
            else:
                print('no date in 008')
                print(record.text) 
            
    elif code == '045': # date
        dateString = ''
        for value in record.findall('subfield'): 
            if dateString == '':
                dateString = value.text
            else: 
                dateString = dateString + ' ' + value.text
        if itemDict['DATE_DISPLAY'] == '':
            dateList = dateFormatter(dateString)
            itemDict['DATE_DISPLAY'] = dateList[0]
            itemDict['DATE_SORT'] = dateList[1] 
            if 'STANDARDIZED_RIGHTS' not in itemDict or itemDict['STANDARDIZED_RIGHTS'] == '':
                itemDict['STANDARDIZED_RIGHTS'] = dateList[3]
    elif code == '090' and len(itemDict['CALL_NUMBER']) == 0: # call number
        for value in record.findall('subfield'):
            if value.get('code').isalpha():
                if value.get('code') != 't' or value.get('code') != 'z' or value.get('code') != '9LOCAL':
                    itemDict['CALL_NUMBER'] = concatenator(itemDict['CALL_NUMBER'], value.text)
                    # pp(itemDict['CALL_NUMBER'])
    elif code == '852' and len(itemDict['CALL_NUMBER']) == 0: # call number
        for value in record.findall('subfield'):
            if value.get('code').isalpha():
                if value.get('code') not in 'kbt':
                    itemDict['CALL_NUMBER'] = concatenator(itemDict['CALL_NUMBER'], value.text)
                    pp(itemDict['CALL_NUMBER'])
    elif code == '099' and len(itemDict['CALL_NUMBER']) == 0: # call number
        for value in record.findall('subfield'):
            if value.get('code').isalpha():
                if value.get('code') != '9' or value.get('code') != '9LOCAL':
                    itemDict['CALL_NUMBER'] = concatenator(itemDict['CALL_NUMBER'], value.text)
                    # pp(itemDict['CALL_NUMBER'])
    elif code == '710' and len(itemDict['CALL_NUMBER']) == 0: # call number
        for value in record.findall('subfield'):
            if value.get('code') != None:
                if value.get('code') == 'n':
                    if value.text[-1] == '.':
                        value = value.text.strip('.')
                    else:
                        value = value.text
                    itemDict['CALL_NUMBER'] = concatenator(itemDict['CALL_NUMBER'], value)
                    # pp(itemDict['CALL_NUMBER'])
    elif code == '100' or code == '110': # creator
        for value in record.findall('subfield'): 
            code = value.get('code')
            if code == 'a' and code.isalpha():
                itemDict['CREATOR'] = concatenator(itemDict['CREATOR'], value.text)
            elif code != 'e' and code.isalpha():
                itemDict['CREATOR'] = concatenator(itemDict['CREATOR'], value.text)
        itemDict['CREATOR'] = itemDict['CREATOR'].strip(",. ")
    elif code == '245': # title, archival collection
        returnValue = ''
        for value in record.findall('subfield'): 
            code = value.get('code')
            if code not in 'cgh':
                if code == 'a' and 'Newberry Library' not in value.text:
                    itemDict['ARCHIVAL_COLLECTION_list']['1'] = value.text.strip('.,').replace('. /','')
                returnValue = concatenator(returnValue, value.text)
        itemDict['TITLE'] = add_box_no_to_title(itemDict['FILENAME'],titleFormatter(returnValue))
    elif code == '260': # PUBLISHER_ORIGINAL, date
        for value in record.findall('subfield'): 
            code = value.get('code')
            if code == 'b':
                itemDict['PUBLISHER_ORIGINAL'] = value.text.strip(',[]')
            if code == 'c' and itemDict['DATE_DISPLAY'] == '':
                # dateValue = value.text
                dateList = dateFormatter(value.text)
                itemDict['DATE_DISPLAY'] = dateList[0] 
                itemDict['DATE_SORT'] = dateList[1]
                if 'STANDARDIZED_RIGHTS' not in itemDict or itemDict['STANDARDIZED_RIGHTS'] == '':
                    itemDict['STANDARDIZED_RIGHTS'] = dateList[3]
    elif code == '300': # format extent
        for value in record.findall('subfield'): 
            valueText = value.text.replace(' cm.', ' cm').replace(' mm.', ' mm')
            itemDict['FORMAT_EXTENT'] = concatenator(itemDict['FORMAT_EXTENT'], valueText)
    elif code == '500': # description
        for value in record.findall('subfield'): 
            if value.get('code') == 'a':
                itemDict['DESCRIPTION'] = value.text
    elif code == '520': # summary
        valueObj = {
            'a': '',
            'b': ''
        }
        for value in record.findall('subfield'):
            if value.get('code') == 'a':
                valueObj['a']  = value.text
            if value.get('code') == 'b':
                valueObj['b']  = value.text
            # concat both but if there's only b or only a we strip out spaces at the front and end
            itemDict['SUMMARY'] = valueObj['a'] + ' ' +  valueObj['b'] 
            itemDict['SUMMARY'] = itemDict['SUMMARY'].strip(' ')
    elif code == '545': # bio/hist note
        biohistnote = ' '
        for value in record.findall('subfield'):
            if value.get('code') == 'a':
                biohistnote = value.text + biohistnote 
            elif value.get('code') == 'b':
                biohistnote = biohistnote + value.text
        itemDict['BIOGRAPHICAL/HISTORICAL NOTE'] = biohistnote 
    elif code == '610' or code == '650' or code == '611': # subject, place, format
        # using a, x, y subfields for subject and then using/supplimenting place with z
        subjectDict = {
            'a': '',
            'v': '',
            'x': '',
            'y': '',
            'z': ''
        }
        # pushing values into a list 
        for value in record.findall('subfield'): 
            try: 
                valueText = value.text.strip(',.')
            except: 
                pass
                # print(value.text)
            code = value.get('code')
            if code == 'a': subjectDict['a'] = valueText
            elif code == 'v': subjectDict['v'] = dashDelimeter(subjectDict['v'], valueText)
            elif code == 'z': subjectDict['z'] = dashDelimeter(subjectDict['z'], valueText)
        # fullValue = dashDelimeter(subjectDict['a'], dashDelimeter(subjectDict['x'], subjectDict['y']))
        if len(subjectDict['a']) > 0 and subjectDict['a'] not in itemDict['SUBJECTS_list'] and len(itemDict['SUBJECTS_list']) < 5:
            itemDict['SUBJECTS_list'].append(subjectDict['a'])
        stringVersion = ''
        for val in itemDict['SUBJECTS_list']:
            stringVersion = pipeDelimeter(stringVersion, val)
        itemDict['SUBJECTS'] = stringVersion
        if subjectDict['z'] not in itemDict['PLACE_list'] and len(subjectDict['z']) > 0:
            itemDict['PLACE_list'].append(subjectDict['z'])
            itemDict['PLACE_list'] = sorted(itemDict['PLACE_list'])
        if subjectDict['v'] not in itemDict['FORMAT_list'] and len(subjectDict['v']) > 0:
            itemDict['FORMAT_list'].append(subjectDict['v'])
            itemDict['FORMAT_list'] = sorted(itemDict['FORMAT_list'])
    elif code == '651': # place
        for value in record.findall('subfield'): 
            if value.get('code') == 'a':
                valueText = value.text
                valueText = placeFormatter(valueText)
                itemDict['PLACE_list'].append(valueText.strip(",. "))
            elif value.get('code') == 'v':
                valueText = value.text.strip('.,')
                if valueText not in itemDict['FORMAT_list']: 
                    itemDict['FORMAT_list'].append(valueText)
        placeString = ''
        placeList = list( dict.fromkeys(itemDict['PLACE_list']) )
        for idx, val in enumerate(placeList):
            if idx < 5:
                placeString = pipeDelimeter(placeString, val)
        # if len(placeString.split('|')) > 0:
        #     placeList = placeString.split('|')
        #     placeList = list( dict.fromkeys(placeList) )

        itemDict['PLACE'] = placeString
    elif code == '655': # format
            # try: 
        if itemDict['FORMAT'].count('|') <= 4:
            for value in record.findall('subfield'): 
                if value.get('code') == 'a':
                    valueText = value.text.strip(',') if value.text.endswith('etc.') else value.text.strip('.,')
                    if valueText not in itemDict['FORMAT_list']: 
                        itemDict['FORMAT_list'].append(valueText)
            formatString = ''
            for val in itemDict['FORMAT_list']:
                try:
                    parenDex = val.index('(')
                    firstCharAfter = val[parenDex + 1]
                    if firstCharAfter.islower():
                        val = val[:parenDex + 1] + firstCharAfter.upper() + val[parenDex + 2:]
                except:
                    pass
                formatString = pipeDelimeter(formatString, val)
            itemDict['FORMAT'] = formatString
    elif code == '710': # archival collection
        if root[0].find("record/leader").text[7] == 'c':
            for value in record.findall('subfield'): 
                if value.get('code') == 'a' and '(Newberry Library)' in value.text and value.text != 'Newberry Library.' and value.text != 'Newberry Library': # took out not in
                    itemDict['ARCHIVAL_COLLECTION'] = itemDict['ARCHIVAL_COLLECTION_list']['1'] + '|' + value.text.replace('(Newberry Library)', '')





directory = '.'
for folder in os.listdir(directory):
	folder_path = os.path.join(directory, folder)
	recordList = []
	for file in os.listdir(folder_path):
		d = {}
		d['BIBID'] = file.split('_')[0]
		d['FILENAME'] = file.replace(d['BIBID'], '')
		recordList.append(d)

	items = []
	for i in recordList:
		itemDict = set_dict()
		alreadyDoneIndex = next((index for (index, d) in enumerate(items) if len(items) > 0 and 'BIBID' in d and d['BIBID'] == i['BIBID']), None)
		if alreadyDoneIndex != None:
			# copy entire item
			itemDict = dict(items[alreadyDoneIndex])
			# change filename in new one 
			# itemDict['FILENAME'] = i['FILENAME']
			itemDict['FILENAME'] = i['BIBID'] + '_' + i['FILENAME']
		# if this bibid isn't already in items, it goes through the full process; ie, this is the bulk of the script
		else: 
			# using length to if bibid already has the 99/8805867 pre- and suffix 
			# sample url: https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs?mms_id=998600358805867&view=full&expand=None&apikey=xxxd
			if len(i['BIBID']) > 8: 
				itemUrl = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs?mms_id=' + str(i['BIBID']) + '&view=full&expand=None&apikey=' + apikey 
			else: 
				itemUrl = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs?mms_id=99' + str(i['BIBID']) + '8805867&view=full&expand=None&apikey=' + apikey 
			print(itemUrl)
			try: 
				itemData = urllib.request.urlopen(itemUrl)
				parsedXml = ET.parse(itemData)
				root = parsedXml.getroot()
				# pp(root)
			except: 
				root = ''

			# if the data returned has a root value, we continue; if it doesn't, it's dumped into the reject pile
			if len(root) > 0:

				itemDict['BIBID'] = strip_bibid(i['BIBID'])
				# itemDict['FILENAME'] = i['FILENAME']
				itemDict['FILENAME'] =  i['BIBID'] + '_' + i['FILENAME']
				itemDict['TITLE'] = '' if root[0].find('title') is None else titleFormatter(root[0].find('title').text)
				# same length test as above
				# if len(i['BIBID']) > 8: 
				#     itemDict['CATALOG_LINK'] = '<a href="https://i-share-nby.primo.exlibrisgroup.com/permalink/01CARLI_NBY/i5mcb2/alma' + str(i['BIBID']) + '">View record</a>'
				# else: 
				#     itemDict['CATALOG_LINK'] = '<a href="https://i-share-nby.primo.exlibrisgroup.com/permalink/01CARLI_NBY/i5mcb2/alma99' + str(i['BIBID']) + '8805867">View record</a>'
				if len(i['BIBID']) > 8: 
					itemDict['CATALOG_LINK'] = f"<a href='https://i-share-nby.primo.exlibrisgroup.com/permalink/01CARLI_NBY/i5mcb2/alma{str(i['BIBID'])}'' target='_blank'>View record</a>"
				else: 
					itemDict['CATALOG_LINK'] = f"<a href='https://i-share-nby.primo.exlibrisgroup.com/permalink/01CARLI_NBY/i5mcb2/alma99{str(i['BIBID'])}8805867' target='_blank'>View record</a>"           
				itemDict['CONTRIBUTING_INSTITUTION'] = "Newberry Library"
				itemDict['OA_POLICY'] = "The Newberry makes its collections available for any lawful purpose, commercial or non-commercial, without licensing or permission fees to the library, subject to <a href='https://www.newberry.org/rights-and-reproductions' target='_blank'>these terms and conditions.</a>"
				itemDict['DISCLAIMER_STMT'] = "All materials in the Newberry Library’s collections have research value and reflect the society in which they were produced. They may contain language and imagery that are offensive because of content relating to: ability, gender, race, religion, sexuality/sexual orientation, and other categories. <a href='https://www.newberry.org/sites/default/files/textpage-attachments/Statement_on_Potentially_Offensive_Materials.pdf' target='_blank'>More information</a>"
			   
				if 'ayer' in itemDict['FILENAME'].lower():
					itemDict['ARCHIVAL_COLLECTION_list']['1'] = 'Edward E. Ayer Collection'
				if 'gr' in itemDict['FILENAME'].lower() or 'graff' in itemDict['FILENAME'].lower():
					itemDict['ARCHIVAL_COLLECTION_list']['1'] = 'Everett D. Graff Collection'
				if 'mms' in itemDict['FILENAME'].lower() or 'midwest' in itemDict['FILENAME'].lower():
					itemDict['ARCHIVAL_COLLECTION_list']['1'] = 'Midwest Manuscript Collection'
				if 'modms' in itemDict['FILENAME'].lower():
					itemDict['ARCHIVAL_COLLECTION_list']['1'] = 'Modern Manuscript Collection'

				for record in root[0].find('record'):
					# link to crosswalk:
					# https://docs.google.com/spreadsheets/d/1etIvF5Vjn1kty51qevsZ9mlWTOl_U9p_iCzWk_WOP9M/edit#gid=1296018796
											
					marcCode = record.get('tag')
					# pp(marcCode)
					valueAssignmentFromCode(record, marcCode)
					
					# resolving lists created by multiple marc codes
					if ('PLACE' not in itemDict or len(itemDict['PLACE']) == 0) and len(itemDict['PLACE_list']) > 0: 
						itemDict['PLACE'] = resolveList(itemDict['PLACE_list'])
					if ('SUBJECTS' not in itemDict or len(itemDict['SUBJECTS']) == 0) and len(itemDict['SUBJECTS_list']) > 0: 
						itemDict['SUBJECTS']  = resolveList(itemDict['SUBJECTS_list'])
					if ('FORMAT' not in itemDict or len(itemDict['FORMAT']) == 0) and len(itemDict['FORMAT_list']) > 0: 
						itemDict['FORMAT']  = resolveList(itemDict['FORMAT_list'])
					if itemDict['STANDARDIZED_RIGHTS'] == 'Not In Copyright - United States':
						itemDict['STANDARDIZED_RIGHTS'] = 'No Copyright - United States'
					if itemDict['STANDARDIZED_RIGHTS'] == 'No copyright - United States':
						itemDict['STANDARDIZED_RIGHTS'] = 'No Copyright - United States'

				# remove format-helping values
				del itemDict['SUBJECTS_list']
				del itemDict['PLACE_list']
				del itemDict['FORMAT_list']
				del itemDict['ARCHIVAL_COLLECTION_list']
				reviewSet.append(itemDict)
				
		if 'SUBJECTS_list' in itemDict.keys():
			del itemDict['SUBJECTS_list']
		if 'ARCHIVAL_COLLECTION_list' in itemDict.keys():
			del itemDict['ARCHIVAL_COLLECTION_list']
		if 'PLACE_list' in itemDict.keys():
			del itemDict['PLACE_list']
		if 'FORMAT_list' in itemDict.keys():
			del itemDict['FORMAT_list']
		# pp(itemDict['DATE_SORT'])
		if itemDict['TITLE'] == '':
			itemDict['PURPOSE'] = 'Pending process'
		items.append(itemDict)
		pp(itemDict['FILENAME'])
		pp(itemDict['TITLE'])
		

	dataFilename = f'Central_{folder}_metadata.csv'
	print("length of item array: " + str(len(items)))
	if len(items) > 0:
		keys = items[0].keys()
		with open(f'{folder}/{dataFilename}', 'w', newline='', errors='ignore', encoding='utf-8')  as output_file:
			dict_writer = csv.DictWriter(output_file, keys)
			dict_writer.writeheader()
			dict_writer.writerows(items)
			pp(f'Wrote spreadsheet: {output_file}')
	else: 
		print("Big error.  Items array was length = 0")

	if len(reviewSet) > 0:
		dataFile = open(f'{folder}/json_reviewSet_' + dataFilename + '.json', 'w')
		dataFile.write(json.dumps(reviewSet, indent=4))
		keys = reviewSet[0].keys()
		reviewFilename = 'review_' + dataFilename
		with open(reviewFilename, 'w', newline='', errors='ignore', encoding='utf-8')  as output_file:
			dict_writer = csv.DictWriter(output_file, keys)
			dict_writer.writeheader()
			dict_writer.writerows(reviewSet)


	end = time.time()
	totalIterationTime = end - start
	totalIterationTime = totalIterationTime / 60
	pp(f'Time to download metadata (mins): {totalIterationTime}')


	



