import urllib.request
import json, csv, re, os
import xml.etree.ElementTree as ET
from datetime import date

# recordList is the unprocessed input data, with emphasis on finding a bibid
recordList = []
# rejects represents records with no bibid; exported into 'no_bibid_[filename].csv'
rejects = []
# subjectConflicts is used to create a csv with instances of data in both ALMA and Piction SUBJECT fields, for comparison: 'subj_conflicts_[filename].csv'
junkDrawer = []
dataConflicts = []
projectList = []

copyrightStatus = {
    "128920":"Copyright Not Evaluated",
    "912443":"Copyright Not Evaluated",
    "549363":"Copyright Not Evaluated",
    "591556":"Copyright Not Evaluated",
    "281876":"Copyright Not Evaluated",
    "612010":"Copyright Not Evaluated",
    "168406":"Copyright Not Evaluated",
    "200620":"Copyright Not Evaluated",
    "398120":"Copyright Not Evaluated",
    "821802":"Copyright Not Evaluated",
    "271720":"Copyright Not Evaluated",
    "325304":"Copyright Not Evaluated",
    "843789":"Copyright Not Evaluated",
    "921291":"Copyright Not Evaluated",
    "844723":"Copyright Not Evaluated",
    "497603":"Copyright Not Evaluated",
    "746564":"Copyright Not Evaluated",
    "485796":"Copyright Not Evaluated",
    "839760":"Copyright Not Evaluated",
    "221807":"Copyright Not Evaluated",
    "396057":"Copyright Not Evaluated",
    "375144":"Copyright Not Evaluated",
    "845849":"Copyright Not Evaluated",
    "335791":"Copyright Not Evaluated",
    "599206":"Copyright Not Evaluated",
    "878417":"Copyright Not Evaluated",
    "402565":"Copyright Not Evaluated",
    "100448":"Copyright Not Evaluated",
    "927923":"Copyright Not Evaluated",
    "931265":"Copyright Not Evaluated",
    "845668":"Copyright Not Evaluated",
    "161980":"Copyright Not Evaluated",
    "163918":"Copyright Not Evaluated",
    "880549":"Copyright Not Evaluated",
    "360339":"Copyright Not Evaluated",
    "260240":"Copyright Not Evaluated",
    "773651":"Copyright Not Evaluated",
    "316290":"Copyright Not Evaluated",
    "807046":"Copyright Not Evaluated",
    "195447":"Copyright Not Evaluated",
    "835833":"Copyright Not Evaluated",
    "83655":"Copyright Not Evaluated",
    "788653":"Copyright Not Evaluated",
    "93280":"Copyright Not Evaluated",
    "550934":"Copyright Not Evaluated",
    "877260":"Copyright Not Evaluated",
    "854026":"Copyright Not Evaluated",
    "136113":"Copyright Not Evaluated",
    "598408":"Copyright Not Evaluated",
    "203264":"Copyright Not Evaluated",
    "963006":"Copyright Not Evaluated",
    "926877":"Copyright Not Evaluated",
    "821787":"Copyright Not Evaluated",
    "30274":"Copyright Not Evaluated",
    "955754":"Copyright Not Evaluated",
    "513932":"Copyright Not Evaluated",
    "961323":"Copyright Not Evaluated",
    "935098":"Copyright Not Evaluated",
    "172002":"Copyright Not Evaluated",
    "31528":"Copyright Not Evaluated",
    "32098":"Copyright Not Evaluated",
    "31615":"Copyright Not Evaluated",
    "179425":"Copyright Not Evaluated",
    "21043":"Copyright Not Evaluated",
    "36113":"Copyright Not Evaluated",
    "45583":"Copyright Not Evaluated",
    "44090":"Copyright Not Evaluated",
    "43999":"Copyright Not Evaluated",
    "63882":"Copyright Not Evaluated",
    "79068":"Copyright Not Evaluated",
    "64079":"Copyright Not Evaluated",
    "38677":"Copyright Not Evaluated",
    "67490":"Copyright Not Evaluated",
    "79086":"Copyright Not Evaluated",
    "79009":"Copyright Not Evaluated",
    "79001":"Copyright Not Evaluated",
    "79088":"Copyright Not Evaluated",
    "107896":"Copyright Not Evaluated",
    "91387":"Copyright Not Evaluated",
    "96402":"Copyright Not Evaluated",
    "949422":"Copyright Not Evaluated",
    "103363":"Copyright Not Evaluated",
    "103367":"Copyright Not Evaluated",
    "103368":"Copyright Not Evaluated",
    "103369":"Copyright Not Evaluated",
    "103370":"Copyright Not Evaluated",
    "122215":"Copyright Not Evaluated",
    "129856":"Copyright Not Evaluated",
    "129982":"Copyright Not Evaluated",
    "129416":"Copyright Not Evaluated",
    "185128":"Copyright Not Evaluated",
    "413033":"Copyright Not Evaluated",
    "961741":"Copyright Not Evaluated",
    "235760":"Copyright Not Evaluated",
    "786403":"Copyright Not Evaluated",
    "82907":"Copyright Not Evaluated",
    "613935":"Copyright Not Evaluated",
    "912564":"Copyright Not Evaluated",
    "815200":"Copyright Not Evaluated",
    "738870":"Copyright Not Evaluated",
    "4950":"Copyright Not Evaluated",
    "808491":"Copyright Not Evaluated",
    "178644":"Copyright Not Evaluated",
    "183985":"Copyright Not Evaluated",
    "829299":"Copyright Not Evaluated",
    "847658":"Copyright Not Evaluated",
    "765741":"Copyright Not Evaluated",
    "902171":"Copyright Not Evaluated",
    "867572":"Copyright Not Evaluated",
    "568244":"Copyright Not Evaluated",
    "955058":"Copyright Not Evaluated",
    "871591":"Copyright Not Evaluated",
    "567116":"Copyright Not Evaluated",
    "179287":"Copyright Not Evaluated",
    "811147":"Copyright Not Evaluated",
    "184069":"Copyright Not Evaluated",
    "259562":"Copyright Not Evaluated",
    "169636":"Copyright Not Evaluated",
    "1145224":"Copyright Not Evaluated",
    "169620":"Copyright Not Evaluated",
    "184078":"Copyright Not Evaluated",
    "181807":"Copyright Not Evaluated",
    "162102":"Copyright Not Evaluated",
    "826824":"Copyright Not Evaluated",
    "954354":"Copyright Not Evaluated",
    "957218":"Copyright Not Evaluated",
    "823562":"Copyright Not Evaluated",
    "400277":"Copyright Not Evaluated",
    "235952":"Copyright Not Evaluated",
    "205875":"Copyright Not Evaluated",
    "844229":"Copyright Not Evaluated",
    "247664":"Copyright Not Evaluated",
    "105934":"Copyright Not Evaluated",
    "462710":"Copyright Not Evaluated",
    "516961":"Copyright Not Evaluated",
    "69291":"Copyright Not Evaluated",
    "768234":"Copyright Not Evaluated",
    "616732":"Copyright Not Evaluated",
    "960924":"Copyright Not Evaluated",
    "875261":"Copyright Not Evaluated",
    "887967":"Copyright Not Evaluated",
    "894809":"Copyright Not Evaluated",
    "915629":"Copyright Not Evaluated",
    "933979":"Copyright Not Evaluated",
    "909667":"Copyright Not Evaluated",
    "889051":"Copyright Not Evaluated",
    "182404":"Copyright Not Evaluated",
    "84573":"Copyright Not Evaluated",
    "152435":"Copyright Not Evaluated",
    "958819":"Copyright Not Evaluated",
    "958818":"Copyright Not Evaluated",
    "957436":"Copyright Not Evaluated",
    "956122":"Copyright Not Evaluated",
    "957586":"Copyright Not Evaluated",
    "957828":"Copyright Not Evaluated",
    "957292":"Copyright Not Evaluated",
    "959169":"Copyright Not Evaluated",
    "957677":"Copyright Not Evaluated",
    "957116":"Copyright Not Evaluated",
    "957863":"Copyright Not Evaluated",
    "957119":"Copyright Not Evaluated",
    "957842":"Copyright Not Evaluated",
    "958326":"Copyright Not Evaluated",
    "957594":"Copyright Not Evaluated",
    "957148":"Copyright Not Evaluated",
    "159307":"Copyright Not Evaluated",
    "165068":"Copyright Not Evaluated",
    "957117":"Copyright Not Evaluated",
    "957150":"Copyright Not Evaluated",
    "880284":"Copyright Not Evaluated",
    "94238":"Copyright Not Evaluated",
    "336792":"Copyright Not Evaluated",
    "882134":"Copyright Not Evaluated",
    "948692":"Copyright Not Evaluated",
    "304796":"Copyright Not Evaluated",
    "962700":"Copyright Not Evaluated",
    "959672":"Copyright Not Evaluated",
    "787409":"Copyright Not Evaluated",
    "198056":"Copyright Not Evaluated",
    "279693":"Copyright Not Evaluated",
    "297035":"Copyright Not Evaluated",
    "438448":"Copyright Not Evaluated",
    "731818":"Copyright Not Evaluated",
    "475740":"Copyright Not Evaluated",
    "808002":"Copyright Not Evaluated",
    "755962":"Copyright Not Evaluated",
    "887766":"Copyright Not Evaluated",
    "608150":"Copyright Not Evaluated",
    "83410":"In Copyright",
    "112576":"In Copyright ",
    "160179":"No Copyright - United States",
    "872583":"No Copyright - United States",
    "874907":"No Copyright - United States",
    "315454":"No Copyright - United States",
    "182897":"No Copyright - United States",
    "84720":"No Copyright - United States",
    "819475":"No Copyright - United States",
    "393899":"No Copyright - United States",
    "715922":"No Copyright - United States",
    "193255":"No Copyright - United States",
    "266579":"No Copyright - United States",
    "874295":"No Copyright - United States",
    "796888":"No Copyright - United States",
    "415233":"No Copyright - United States",
    "873697":"No Copyright - United States",
    "193317":"No Copyright - United States",
    "193199":"No Copyright - United States",
    "812373":"No Copyright - United States",
    "400646":"No Copyright - United States",
    "286719":"No Copyright - United States",
    "100320":"No Copyright - United States",
    "623476":"No Copyright - United States",
    "468935":"No Copyright - United States",
    "235755":"No Copyright - United States",
    "671513":"No Copyright - United States",
    "611678":"No Copyright - United States",
    "400133":"No Copyright - United States",
    "127820":"No Copyright - United States",
    "445050":"No Copyright - United States",
    "760619":"No Copyright - United States",
    "375099":"No Copyright - United States",
    "295725":"No Copyright - United States",
    "385946":"No Copyright - United States",
    "736122":"No Copyright - United States",
    "637490":"No Copyright - United States",
    "157670":"No Copyright - United States",
    "242121":"No Copyright - United States",
    "454541":"No Copyright - United States",
    "519057":"No Copyright - United States",
    "963040":"No Copyright - United States",
    "315463":"No Copyright - United States",
    "703602":"No Copyright - United States",
    "519100":"No Copyright - United States",
    "519122":"No Copyright - United States",
    "726990":"No Copyright - United States",
    "517599":"No Copyright - United States",
    "725161":"No Copyright - United States",
    "89998":"No Copyright - United States",
    "516767":"No Copyright - United States",
    "286107":"No Copyright - United States",
    "506269":"No Copyright - United States",
    "593492":"No Copyright - United States",
    "517816":"No Copyright - United States",
    "804712":"No Copyright - United States",
    "462672":"No Copyright - United States",
    "519515":"No Copyright - United States",
    "207349":"No Copyright - United States",
    "247354":"No Copyright - United States",
    "517486":"No Copyright - United States",
    "519497":"No Copyright - United States",
    "519567":"No Copyright - United States",
    "247167":"No Copyright - United States",
    "616914":"No Copyright - United States",
    "519464":"No Copyright - United States",
    "359408":"No Copyright - United States",
    "517782":"No Copyright - United States",
    "144136":"No Copyright - United States",
    "658110":"No Copyright - United States",
    "462685":"No Copyright - United States",
    "369875":"No Copyright - United States",
    "854779":"No Copyright - United States",
    "517740":"No Copyright - United States",
    "295767":"No Copyright - United States",
    "516797":"No Copyright - United States",
    "160299":"No Copyright - United States",
    "589657":"No Copyright - United States",
    "653369":"No Copyright - United States",
    "531181":"No Copyright - United States",
    "753448":"No Copyright - United States",
    "238114":"No Copyright - United States",
    "164336":"No Copyright - United States",
    "202995":"No Copyright - United States",
    "399646":"No Copyright - United States",
    "704286":"No Copyright - United States",
    "967925":"No Copyright - United States",
    "369449":"No Copyright - United States",
    "238918":"No Copyright - United States",
    "238116":"No Copyright - United States",
    "275978":"No Copyright - United States",
    "237974":"No Copyright - United States",
    "483893":"No Copyright - United States",
    "136721":"No Copyright - United States",
    "621214":"No Copyright - United States",
    "238601":"No Copyright - United States",
    "96361":"No Copyright - United States",
    "183068":"No Copyright - United States",
    "112599":"No Copyright - United States",
    "519559":"No Copyright - United States",
    "775427":"No Copyright - United States",
    "267075":"No Copyright - United States",
    "512598":"No Copyright - United States",
    "306419":"No Copyright - United States",
    "296131":"No Copyright - United States",
    "965097":"No Copyright - United States",
    "819424":"No Copyright - United States",
    "236704":"No Copyright - United States",
    "715598":"No Copyright - United States",
    "294922":"No Copyright - United States",
    "237473":"No Copyright - United States",
    "166457":"No Copyright - United States",
    "793622":"No Copyright - United States",
    "549613":"No Copyright - United States",
    "285600":"No Copyright - United States",
    "163678":"No Copyright - United States",
    "308474":"No Copyright - United States",
    "218479":"No Copyright - United States",
    "182836":"No Copyright - United States",
    "555831":"No Copyright - United States",
    "490074":"No Copyright - United States",
    "118880":"No Copyright - United States",
    "715983":"No Copyright - United States",
    "128920":"No Copyright - United States",
    "395663":"No Copyright - United States",
    "143315":"No Copyright - United States",
    "397260":"No Copyright - United States",
    "219355":"No Copyright - United States",
    "912158":"No Copyright - United States",
    "147716":"No Copyright - United States",
    "249284":"No Copyright - United States",
    "550242":"No Copyright - United States",
    "912433":"No Copyright - United States",
    "293408":"No Copyright - United States",
    "952285":"No Copyright - United States",
    "315464":"No Copyright - United States",
    "223534":"No Copyright - United States",
    "912444":"No Copyright - United States",
    "691088":"No Copyright - United States",
    "298108":"No Copyright - United States",
    "471872":"No Copyright - United States",
    "915531":"No Copyright - United States",
    "379417":"No Copyright - United States",
    "912451":"No Copyright - United States",
    "202170":"No Copyright - United States",
    "912116":"No Copyright - United States",
    "912629":"No Copyright - United States",
    "830003":"No Copyright - United States",
    "567503":"No Copyright - United States",
    "732034":"No Copyright - United States",
    "727157":"No Copyright - United States",
    "721570":"No Copyright - United States",
    "750001":"No Copyright - United States",
    "576232":"No Copyright - United States",
    "857631":"No Copyright - United States",
    "356042":"No Copyright - United States",
    "293411":"No Copyright - United States",
    "744463":"No Copyright - United States",
    "554684":"No Copyright - United States",
    "235857":"No Copyright - United States",
    "547978":"No Copyright - United States",
    "162524":"No Copyright - United States",
    "912430":"No Copyright - United States",
    "269382":"No Copyright - United States",
    "236751":"No Copyright - United States",
    "315455":"No Copyright - United States",
    "656475":"No Copyright - United States",
    "167695":"No Copyright - United States",
    "227465":"No Copyright - United States",
    "616086":"No Copyright - United States",
    "272681":"No Copyright - United States",
    "760688":"No Copyright - United States",
    "325675":"No Copyright - United States",
    "772796":"No Copyright - United States",
    "967358":"No Copyright - United States",
    "235862":"No Copyright - United States",
    "565472":"No Copyright - United States",
    "193340":"No Copyright - United States",
    "314798":"No Copyright - United States",
    "899256":"No Copyright - United States",
    "585779":"No Copyright - United States",
    "282658":"No Copyright - United States",
    "534919":"No Copyright - United States",
    "528078":"No Copyright - United States",
    "207982":"No Copyright - United States",
    "912098":"No Copyright - United States",
    "572542":"No Copyright - United States",
    "377342":"No Copyright - United States",
    "549685":"No Copyright - United States",
    "238025":"No Copyright - United States",
    "963095":"No Copyright - United States",
    "932223":"No Copyright - United States",
    "671841":"No Copyright - United States",
    "907639":"No Copyright - United States",
    "237980":"No Copyright - United States",
    "702108":"No Copyright - United States",
    "137473":"No Copyright - United States",
    "174224":"No Copyright - United States",
    "236767":"No Copyright - United States",
    "911994":"No Copyright - United States",
    "258240":"No Copyright - United States",
    "912319":"No Copyright - United States",
    "519665":"No Copyright - United States",
    "912394":"No Copyright - United States",
    "666622":"No Copyright - United States",
    "400140":"No Copyright - United States",
    "470676":"No Copyright - United States",
    "323869":"No Copyright - United States",
    "869086":"No Copyright - United States",
    "400046":"No Copyright - United States",
    "387249":"No Copyright - United States",
    "213485":"No Copyright - United States",
    "323861":"No Copyright - United States",
    "619013":"No Copyright - United States",
    "223454":"No Copyright - United States",
    "308272":"No Copyright - United States",
    "397331":"No Copyright - United States",
    "514066":"No Copyright - United States",
    "866898":"No Copyright - United States",
    "282711":"No Copyright - United States",
    "736182":"No Copyright - United States",
    "746884":"No Copyright - United States",
    "314048":"No Copyright - United States",
    "323876":"No Copyright - United States",
    "395846":"No Copyright - United States",
    "396669":"No Copyright - United States",
    "608937":"No Copyright - United States",
    "104227":"No Copyright - United States",
    "764599":"No Copyright - United States",
    "654390":"No Copyright - United States",
    "912175":"No Copyright - United States",
    "286133":"No Copyright - United States",
    "154304":"No Copyright - United States",
    "764667":"No Copyright - United States",
    "968291":"No Copyright - United States",
    "678385":"No Copyright - United States",
    "82516":"No Copyright - United States",
    "383159":"No Copyright - United States",
    "915900":"No Copyright - United States",
    "411463":"No Copyright - United States",
    "795362":"No Copyright - United States",
    "917980":"No Copyright - United States",
    "634715":"No Copyright - United States",
    "960679":"No Copyright - United States",
    "373587":"No Copyright - United States",
    "315391":"No Copyright - United States",
    "752616":"No Copyright - United States",
    "398540":"No Copyright - United States",
    "883206":"No Copyright - United States",
    "469382":"No Copyright - United States",
    "640146":"No Copyright - United States",
    "315179":"No Copyright - United States",
    "315392":"No Copyright - United States",
    "318607":"No Copyright - United States",
    "84230":"No Copyright - United States",
    "569637":"No Copyright - United States",
    "199963":"No Copyright - United States",
    "750762":"No Copyright - United States",
    "948789":"No Copyright - United States",
    "93772":"No Copyright - United States",
    "279529":"No Copyright - United States",
    "279958":"No Copyright - United States",
    "755352":"No Copyright - United States",
    "820762":"No Copyright - United States",
    "965297":"No Copyright - United States",
    "957593":"No Copyright - United States",
    "153762":"No Copyright - United States",
    "767486":"No Copyright - United States",
    "253943":"No Copyright - United States",
    "503713":"No Copyright - United States",
    "794094":"No Copyright - United States",
    "210909":"No Copyright - United States",
    "439093":"No Copyright - United States",
    "415325":"No Copyright - United States",
    "501349":"No Copyright - United States",
    "647208":"No Copyright - United States",
    "211496":"No Copyright - United States",
    "764078":"No Copyright - United States",
    "116614":"No Copyright - United States",
    "153772":"No Copyright - United States",
    "669985":"No Copyright - United States",
    "516024":"No Copyright - United States",
    "236649":"No Copyright - United States",
    "776402":"No Copyright - United States",
    "311940":"No Copyright - United States",
    "238414":"No Copyright - United States",
    "818407":"No Copyright - United States",
    "288804":"No Copyright - United States",
    "629721":"No Copyright - United States",
    "246219":"No Copyright - United States",
    "957149":"No Copyright - United States",
    "912436":"No Copyright - United States",
    "961519":"No Copyright - United States",
    "164883":"No Copyright - United States",
    "388405":"No Copyright - United States",
    "243775":"No Copyright - United States",
    "479722":"No Copyright - United States",
    "92049":"No Copyright - United States",
    "287925":"No Copyright - United States",
    "961015":"No Copyright - United States",
    "502277":"No Copyright - United States",
    "965824":"No Copyright - United States",
    "748359":"No Copyright - United States",
    "800661":"No Copyright - United States",
    "912448":"No Copyright - United States",
    "967853":"No Copyright - United States",
    "132759":"No Copyright - United States",
    "579860":"No Copyright - United States",
    "933697":"No Copyright - United States",
    "332713":"No Copyright - United States",
    "400421":"No Copyright - United States",
    "155739":"No Copyright - United States",
    "345908":"No Copyright - United States",
    "266464":"No Copyright - United States",
    "548172":"No Copyright - United States",
    "653634":"No Copyright - United States",
    "964407":"No Copyright - United States",
    "305248":"No Copyright - United States",
    "253107":"No Copyright - United States",
    "235954":"No Copyright - United States",
    "956040":"No Copyright - United States",
    "345363":"No Copyright - United States",
    "330127":"No Copyright - United States",
    "508700":"No Copyright - United States",
    "450803":"No Copyright - United States",
    "394263":"No Copyright - United States",
    "442984":"No Copyright - United States",
    "540263":"No Copyright - United States",
    "406535":"No Copyright - United States",
    "253900":"No Copyright - United States",
    "963050":"No Copyright - United States",
    "438475":"No Copyright - United States",
    "474614":"No Copyright - United States",
    "180396":"No Copyright - United States",
    "337755":"No Copyright - United States",
    "269378":"No Copyright - United States",
    "550309":"No Copyright - United States",
    "378464":"No Copyright - United States",
    "516846":"No Copyright - United States",
    "136267":"No Copyright - United States",
    "388497":"No Copyright - United States",
    "105934":"No Copyright - United States",
    "784029":"No Copyright - United States",
    "138116":"No Copyright - United States",
    "549363":"No Copyright - United States",
    "378393":"No Copyright - United States",
    "955797":"No Copyright - United States",
    "580529":"No Copyright - United States",
    "714925":"No Copyright - United States",
    "629918":"No Copyright - United States",
    "442945":"No Copyright - United States",
    "89284":"No Copyright - United States",
    "962835":"No Copyright - United States",
    "440149":"No Copyright - United States",
    "591556":"No Copyright - United States",
    "955927":"No Copyright - United States",
    "962610":"No Copyright - United States",
    "580535":"No Copyright - United States",
    "168094":"No Copyright - United States",
    "168091":"No Copyright - United States",
    "580541":"No Copyright - United States",
    "899654":"No Copyright - United States",
    "757589":"No Copyright - United States",
    "160269":"No Copyright - United States",
    "386509":"No Copyright - United States",
    "318212":"No Copyright - United States",
    "175987":"No Copyright - United States",
    "283001":"No Copyright - United States",
    "287042":"No Copyright - United States",
    "580545":"No Copyright - United States",
    "956121":"No Copyright - United States",
    "698624":"No Copyright - United States",
    "844723":"No Copyright - United States",
    "936960":"No Copyright - United States",
    "241099":"No Copyright - United States",
    "902276":"No Copyright - United States",
    "955795":"No Copyright - United States",
    "532243":"No Copyright - United States",
    "802616":"No Copyright - United States",
    "955796":"No Copyright - United States",
    "285059":"No Copyright - United States",
    "183288":"No Copyright - United States",
    "599536":"No Copyright - United States",
    "955928":"No Copyright - United States",
    "822257":"No Copyright - United States",
    "957118":"No Copyright - United States",
    "957595":"No Copyright - United States",
    "912086":"No Copyright - United States",
    "134138":"No Copyright - United States",
    "957585":"No Copyright - United States",
    "886854":"No Copyright - United States",
    "912502":"No Copyright - United States",
    "912051":"No Copyright - United States",
    "948036":"No Copyright - United States",
    "815714":"No Copyright - United States",
    "631546":"No Copyright - United States",
    "138330":"No Copyright - United States",
    "130067":"No Copyright - United States",
    "84296":"No Copyright - United States",
    "387471":"No Copyright - United States",
    "234355":"No Copyright - United States",
    "123710":"No Copyright - United States",
    "131502":"No Copyright - United States",
    "883287":"No Copyright - United States",
    "822527":"No Copyright - United States",
    "92607":"No Copyright - United States",
    "312647":"No Copyright - United States",
    "887196":"No Copyright - United States",
    "802740":"No Copyright - United States",
    "957836":"No Copyright - United States",
    "123658":"No Copyright - United States",
    "958817":"No Copyright - United States",
    "83940":"No Copyright - United States",
    "148923":"No Copyright - United States",
    "217355":"No Copyright - United States",
    "552954":"No Copyright - United States",
    "121656":"No Copyright - United States",
    "755056":"No Copyright - United States",
    "621211":"No Copyright - United States",
    "865365":"No Copyright - United States",
    "451051":"No Copyright - United States",
    "394633":"No Copyright - United States",
    "656204":"No Copyright - United States",
    "393586":"No Copyright - United States",
    "389034":"No Copyright - United States",
    "812040":"No Copyright - United States",
    "408169":"No Copyright - United States",
    "145750":"No Copyright - United States",
    "170484":"No Copyright - United States",
    "170485":"No Copyright - United States",
    "170486":"No Copyright - United States",
    "170487":"No Copyright - United States",
    "145733":"No Copyright - United States",
    "269702":"No Copyright - United States",
    "561394":"No Copyright - United States",
    "301709":"No Copyright - United States",
    "395033":"No Copyright - United States",
    "396488":"No Copyright - United States",
    "390039":"No Copyright - United States",
    "390032":"No Copyright - United States",
    "133404":"No Copyright - United States",
    "395130":"No Copyright - United States",
    "396405":"No Copyright - United States",
    "386036":"No Copyright - United States",
    "67440":"No Copyright - United States",
    "841887":"No Copyright - United States",
    "68209":"No Copyright - United States",
    "65469":"No Copyright - United States",
    "68199":"No Copyright - United States",
    "58575":"No Copyright - United States",
    "71408":"No Copyright - United States",
    "67131":"No Copyright - United States",
    "68606":"No Copyright - United States",
    "818954":"No Copyright - United States",
    "865559":"No Copyright - United States",
    "66993":"No Copyright - United States",
    "67010":"No Copyright - United States",
    "183801":"No Copyright - United States",
    "594298":"No Copyright - United States",
    "68715":"No Copyright - United States",
    "69565":"No Copyright - United States",
    "855774":"No Copyright - United States",
    "68890":"No Copyright - United States",
    "865547":"No Copyright - United States",
    "66126":"No Copyright - United States",
    "67242":"No Copyright - United States",
    "67185":"No Copyright - United States",
    "67309":"No Copyright - United States",
    "67414":"No Copyright - United States",
    "586665":"No Copyright - United States",
    "311558":"No Copyright - United States",
    "67601":"No Copyright - United States",
    "843267":"No Copyright - United States",
    "68850":"No Copyright - United States",
    "864835":"No Copyright - United States",
    "864838":"No Copyright - United States",
    "865568":"No Copyright - United States",
    "66370":"No Copyright - United States",
    "66525":"No Copyright - United States",
    "66505":"No Copyright - United States",
    "66789":"No Copyright - United States",
    "67250":"No Copyright - United States",
    "67286":"No Copyright - United States",
    "67347":"No Copyright - United States",
    "67530":"No Copyright - United States",
    "67525":"No Copyright - United States",
    "67517":"No Copyright - United States",
    "864834":"No Copyright - United States",
    "865569":"No Copyright - United States",
    "66450":"No Copyright - United States",
    "66508":"No Copyright - United States",
    "66888":"No Copyright - United States",
    "66973":"No Copyright - United States",
    "67411":"No Copyright - United States",
    "67514":"No Copyright - United States",
    "506397":"No Copyright - United States",
    "68236":"No Copyright - United States",
    "67645":"No Copyright - United States",
    "68581":"No Copyright - United States",
    "865548":"No Copyright - United States",
    "865567":"No Copyright - United States",
    "66514":"No Copyright - United States",
    "73796":"No Copyright - United States",
    "957003":"No Copyright - United States",
    "388678":"No Copyright - United States",
    "886853":"No Copyright - United States",
    "815400":"No Copyright - United States",
    "124194":"No Copyright - United States",
    "134251":"No Copyright - United States",
    "136932":"No Copyright - United States",
    "610781":"No Copyright - United States",
    "865556":"No Copyright - United States",
    "67282":"No Copyright - United States",
    "67278":"No Copyright - United States",
    "605897":"No Copyright - United States",
    "43779":"No Copyright - United States",
    "56166":"No Copyright - United States",
    "815201":"No Copyright - United States",
    "842271":"No Copyright - United States",
    "66191":"No Copyright - United States",
    "66963":"No Copyright - United States",
    "67220":"No Copyright - United States",
    "66008":"No Copyright - United States",
    "957435":"No Copyright - United States",
    "842725":"No Copyright - United States",
    "234116":"No Copyright - United States",
    "66518":"No Copyright - United States",
    "66571":"No Copyright - United States",
    "66597":"No Copyright - United States",
    "66542":"No Copyright - United States",
    "66664":"No Copyright - United States",
    "390072":"No Copyright - United States",
    "68931":"No Copyright - United States",
    "947901":"No Copyright - United States",
    "66959":"No Copyright - United States",
    "826490":"No Copyright - United States",
    "821802":"No Copyright - United States",
    "851339":"No Copyright - United States",
    "818955":"No Copyright - United States",
    "67374":"No Copyright - United States",
    "721030":"No Copyright - United States",
    "102441":"No Copyright - United States",
    "228614":"No Copyright - United States",
    "739067":"No Copyright - United States",
    "845847":"No Copyright - United States",
    "67038":"No Copyright - United States",
    "235051":"No Copyright - United States",
    "403179":"No Copyright - United States",
    "600621":"No Copyright - United States",
    "234114":"No Copyright - United States",
    "835833":"No Copyright - United States",
    "559916":"No Copyright - United States",
    "764427":"No Copyright - United States",
    "245691":"No Copyright - United States",
    "957433":"No Copyright - United States",
    "643306":"No Copyright - United States",
    "138452":"No Copyright - United States",
    "957865":"No Copyright - United States",
    "961070":"No Copyright - United States",
    "763499":"No Copyright - United States",
    "236660":"No Copyright - United States",
    "738209":"No Copyright - United States",
    "956810":"No Copyright - United States",
    "559720":"No Copyright - United States",
    "957877":"No Copyright - United States",
    "509693":"No Copyright - United States",
    "234117":"No Copyright - United States",
    "957115":"No Copyright - United States",
    "397085":"No Copyright - United States",
    "957387":"No Copyright - United States",
    "958369":"No Copyright - United States",
    "735542":"No Copyright - United States",
    "559872":"No Copyright - United States",
    "957968":"No Copyright - United States",
    "283828":"No Copyright - United States",
    "957002":"No Copyright - United States",
    "336634":"No Copyright - United States",
    "336635":"No Copyright - United States",
    "336811":"No Copyright - United States",
    "336814":"No Copyright - United States",
    "336819":"No Copyright - United States",
    "815855":"No Copyright - United States",
    "666475":"No Copyright - United States",
    "337464":"No Copyright - United States",
    "263540":"No Copyright - United States",
    "337477":"No Copyright - United States",
    "530347":"No Copyright - United States",
    "957831":"No Copyright - United States",
    "68562":"No Copyright - United States",
    "514749":"No Copyright - United States",
    "956806":"No Copyright - United States",
    "96751":"No Copyright - United States",
    "815827":"No Copyright - United States",
    "103660":"No Copyright - United States",
    "598085":"No Copyright - United States",
    "684411":"No Copyright - United States",
    "962451":"No Copyright - United States",
    "957447":"No Copyright - United States",
    "957383":"No Copyright - United States",
    "958368":"No Copyright - United States",
    "182393":"No Copyright - United States",
    "132872":"No Copyright - United States",
    "678463":"No Copyright - United States",
    "145582":"No Copyright - United States",
    "745023":"No Copyright - United States",
    "949157":"No Copyright - United States",
    "956808":"No Copyright - United States",
    "508516":"No Copyright - United States",
    "826494":"No Copyright - United States",
    "958170":"No Copyright - United States",
    "449760":"No Copyright - United States",
    "614523":"No Copyright - United States",
    "209938":"No Copyright - United States",
    "125019":"No Copyright - United States",
    "336791":"No Copyright - United States",
    "887411":"No Copyright - United States",
    "224843":"No Copyright - United States",
    "958928":"No Copyright - United States",
    "958770":"No Copyright - United States",
    "959784":"No Copyright - United States",
    "826241":"No Copyright - United States",
    "957676":"No Copyright - United States",
    "958771":"No Copyright - United States",
    "948083":"No Copyright - United States",
    "800128":"No Copyright - United States",
    "958171":"No Copyright - United States",
    "821787":"No Copyright - United States",
    "963486":"No Copyright - United States",
    "957841":"No Copyright - United States",
    "829299":"No Copyright - United States",
    "956805":"No Copyright - United States",
    "154528":"No Copyright - United States",
    "958169":"No Copyright - United States",
    "138491":"No Copyright - United States",
    "872462":"No Copyright - United States",
    "106378":"No Copyright - United States",
    "213339":"No Copyright - United States",
    "338896":"No Copyright - United States",
    "957940":"No Copyright - United States",
    "958370":"No Copyright - United States",
    "768893":"No Copyright - United States",
    "628903":"No Copyright - United States",
    "628905":"No Copyright - United States",
    "962395":"No Copyright - United States",
    "735704":"No Copyright - United States",
    "611219":"No Copyright - United States",
    "160672":"No Copyright - United States",
    "957385":"No Copyright - United States",
    "957388":"No Copyright - United States",
    "957384":"No Copyright - United States",
    "957680":"No Copyright - United States",
    "562181":"No Copyright - United States",
    "735698":"No Copyright - United States",
    "132682":"No Copyright - United States",
    "151022":"No Copyright - United States",
    "826556":"No Copyright - United States",
    "957672":"No Copyright - United States",
    "957843":"No Copyright - United States",
    "725697":"No Copyright - United States",
    "808002":"No Copyright - United States",
    "154431":"No Copyright - United States",
    "710053":"No Copyright - United States",
    "94120":"No Copyright - United States",
    "117111":"No Copyright - United States",
    "958768":"No Copyright - United States",
    "430758":"No Copyright - United States",
    "141142":"No Copyright - United States",
    "130165":"No Copyright - United States",
    "957761":"No Copyright - United States",
    "958682":"No Copyright - United States",
    "949000":"No Copyright - United States",
    "725701":"No Copyright - United States",
    "666519":"No Copyright - United States",
    "958764":"No Copyright - United States",
    "165958":"No Copyright - United States",
    "957120":"No Copyright - United States",
    "540083":"No Copyright - United States",
    "52378":"No Copyright - United States",
    "741183":"No Copyright - United States",
    "957596":"No Copyright - United States",
    "957591":"No Copyright - United States",
    "957683":"No Copyright - United States",
    "858543":"No Copyright - United States",
    "676738":"No Copyright - United States",
    "957835":"No Copyright - United States",
    "314568":"No Copyright - United States",
    "957151":"No Copyright - United States",
    "957147":"No Copyright - United States",
    "957941":"No Copyright - United States",
    "129423":"No Copyright - United States",
    "811300":"No Copyright - United States",
    "957675":"No Copyright - United States",
    "179668":"No Copyright - United States",
    "957505":"No Copyright - United States",
    "635940":"No Copyright - United States",
    "957674":"No Copyright - United States",
    "957670":"No Copyright - United States",
    "957580":"No Copyright - United States",
    "957492":"No Copyright - United States",
    "958363":"No Copyright - United States",
    "1009067":"No Copyright - United States",
    "957682":"No Copyright - United States",
    "957840":"No Copyright - United States",
    "141094":"No Copyright - United States",
    "957587":"No Copyright - United States",
    "957678":"No Copyright - United States",
    "379810":"No Copyright - United States",
    "957386":"No Copyright - United States",
    "112402":"No Copyright - United States",
    "818151":"No Copyright - United States",
    "131051":"No Copyright - United States",
    "956807":"No Copyright - United States",
    "137192":"No Copyright - United States",
    "957290":"No Copyright - United States",
    "146155":"No Copyright - United States",
    "801047":"No Copyright - United States",
    "791191":"No Copyright - United States",
    "878417":"No Copyright - United States",
    "182225":"No Copyright - United States",
    "959107":"No Copyright - United States",
    "959994":"No Copyright - United States",
    "298652":"No Copyright - United States",
    "732177":"No Copyright - United States",
    "958168":"No Copyright - United States",
    "957834":"No Copyright - United States",
    "957449":"No Copyright - United States",
    "161816":"No Copyright - United States",
    "779184":"No Copyright - United States",
    "823425":"No Copyright - United States",
    "958680":"No Copyright - United States",
    "959167":"No Copyright - United States",
    "769871":"No Copyright - United States",
    "92354":"No Copyright - United States",
    "874958":"No Copyright - United States",
    "509343":"No Copyright - United States",
    "821801":"No Copyright - United States",
    "892207":"No Copyright - United States",
    "460853":"No Copyright - United States",
    "200620":"No Copyright - United States",
    "9775":"No Copyright - United States",
    "217656":"No Copyright - United States",
    "106315":"No Copyright - United States",
    "887766":"No Copyright - United States",
    "816489":"No Copyright - United States",
    "163918":"No Copyright - United States",
    "84610":"No Copyright - United States",
    "886069":"No Copyright - United States",
    "798406":"No Copyright - United States",
    "835155":"No Copyright - United States",
    "182862":"No Copyright - United States",
    "182870":"No Copyright - United States",
    "111178":"No Copyright - United States",
    "696240":"No Copyright - United States",
    "957833":"No Copyright - United States",
    "958679":"No Copyright - United States",
    "292208":"No Copyright - United States",
    "645272":"No Copyright - United States",
    "878805":"No Copyright - United States",
    "184085":"No Copyright - United States",
    "957681":"No Copyright - United States",
    "858848":"No Copyright - United States",
    "132457":"No Copyright - United States",
    "340301":"No Copyright - United States",
    "961549":"No Copyright - United States",
    "810587":"No Copyright - United States",
    "348262":"No Copyright - United States",
    "958681":"No Copyright - United States",
    "964404":"No Copyright - United States",
    "739068":"No Copyright - United States",
    "204369":"No Copyright - United States",
    "810030":"No Copyright - United States",
    "810031":"No Copyright - United States",
    "806814":"No Copyright - United States",
    "921291":"No Copyright - United States",
    "677972":"No Copyright - United States",
    "850115":"No Copyright - United States",
    "849770":"No Copyright - United States",
    "304458":"No Copyright - United States",
    "817076":"No Copyright - United States",
    "810229":"No Copyright - United States",
    "850116":"No Copyright - United States",
    "817922":"No Copyright - United States",
    "192336":"No Copyright - United States",
    "882573":"No Copyright - United States",
    "847971":"No Copyright - United States",
    "167315":"No Copyright - United States",
    "168406":"No Copyright - United States",
    "349141":"No Copyright - United States",
    "808377":"No Copyright - United States",
    "795383":"No Copyright - United States",
    "220179":"No Copyright - United States",
    "71600":"No Copyright - United States",
    "913132":"No Copyright - United States",
    "109128":"No Copyright - United States",
    "746564":"No Copyright - United States",
    "235710":"No Copyright - United States",
    "26171":"No Copyright - United States",
    "116659":"No Copyright - United States",
    "3984":"No Copyright - United States",
    "808762":"No Copyright - United States",
    "68474":"No Copyright - United States",
    "854680":"No Copyright - United States",
    "865617":"No Copyright - United States",
    "912441":"No Copyright - United States",
    "842952":"No Copyright - United States",
    "961738":"No Copyright - United States",
    "869161":"No Copyright - United States",
    "814053":"No Copyright - United States",
    "124482":"No Copyright - United States",
    "264843":"No Copyright - United States",
    "236227":"No Copyright - United States",
    "297479":"No Copyright - United States",
    "781168":"No Copyright - United States",
    "182886":"No Copyright - United States",
    "876483":"No Copyright - United States",
    "235709":"No Copyright - United States",
    "874513":"No Copyright - United States",
    "822109":"No Copyright - United States",
    "874426":"No Copyright - United States",
    "870286":"No Copyright - United States",
    "596592":"No Copyright - United States",
    "112161":"No Copyright - United States",
    "136532":"No Copyright - United States",
    "302554":"No Copyright - United States",
    "712359":"No Copyright - United States",
    "802713":"No Copyright - United States",
    "704540":"No Copyright - United States",
    "661570":"No Copyright - United States",
    "455544":"No Copyright - United States",
    "279615":"No Copyright - United States",
    "609204":"No Copyright - United States",
    "398508":"No Copyright - United States",
    "267420":"No Copyright - United States",
    "237111":"No Copyright - United States",
    "237167":"No Copyright - United States",
    "311804":"No Copyright - United States",
    "311817":"No Copyright - United States",
    "555984":"No Copyright - United States",
    "517344":"No Copyright - United States",
    "136809":"No Copyright - United States",
    "241450":"No Copyright - United States",
    "134867":"No Copyright - United States",
    "234961":"No Copyright - United States",
    "812147":"No Copyright - United States",
    "702252":"No Copyright - United States",
    "239173":"No Copyright - United States",
    "275476":"No Copyright - United States",
    "124541":"No Copyright - United States",
    "175635":"No Copyright - United States",
    "168265":"No Copyright - United States",
    "521297":"No Copyright - United States",
    "557672":"No Copyright - United States",
    "607700":"No Copyright - United States",
    "300495":"No Copyright - United States",
    "350118":"No Copyright - United States",
    "628897":"No Copyright - United States",
    "628899":"No Copyright - United States",
    "142595":"No Copyright - United States",
    "512568":"No Copyright - United States",
    "530453":"No Copyright - United States",
    "637653":"No Copyright - United States",
    "912005":"No Copyright - United States",
    "374590":"No Copyright - United States",
    "697242":"No Copyright - United States",
    "971664":"No Copyright - United States",
    "697265":"No Copyright - United States",
    "183278":"No Copyright - United States",
    "390800":"No Copyright - United States",
    "204516":"No Copyright - United States",
    "912438":"No Copyright - United States",
    "912449":"No Copyright - United States",
    "820541":"No Copyright - United States",
    "287037":"No Copyright - United States",
    "127239":"No Copyright - United States",
    "87276":"No Copyright - United States",
    "133264":"No Copyright - United States",
    "145976":"No Copyright - United States",
    "134262":"No Copyright - United States",
    "126657":"No Copyright - United States",
    "304830":"No Copyright - United States",
    "139505":"No Copyright - United States",
    "122759":"No Copyright - United States",
    "743525":"No Copyright - United States",
    "655418":"No Copyright - United States",
    "69554":"No Copyright - United States",
    "128064":"No Copyright - United States",
    "141999":"No Copyright - United States",
    "132867":"No Copyright - United States",
    "659159":"No Copyright - United States",
    "131888":"No Copyright - United States",
    "168439":"No Copyright - United States",
    "69433":"No Copyright - United States",
    "578837":"No Copyright - United States",
    "131049":"No Copyright - United States",
    "132453":"No Copyright - United States",
    "145469":"No Copyright - United States",
    "165212":"No Copyright - United States",
    "774073":"No Copyright - United States",
    "508507":"No Copyright - United States",
    "508501":"No Copyright - United States",
    "508503":"No Copyright - United States",
    "599562":"No Copyright - United States",
    "701189":"No Copyright - United States",
    "344462":"No Copyright - United States",
    "587937":"No Copyright - United States",
    "627185":"No Copyright - United States",
    "308706":"No Copyright - United States",
    "774078":"No Copyright - United States",
    "137325":"No Copyright - United States",
    "157746":"No Copyright - United States",
    "464923":"No Copyright - United States",
    "149487":"No Copyright - United States",
    "141998":"No Copyright - United States",
    "336959":"No Copyright - United States",
    "959383":"No Copyright - United States",
    "847210":"No Copyright - United States",
    "147504":"No Copyright - United States",
    "822984":"No Copyright - United States",
    "121820":"No Copyright - United States",
    "119685":"No Copyright - United States",
    "138960":"No Copyright - United States",
    "774394":"No Copyright - United States",
    "177677":"No Copyright - United States",
    "119926":"No Copyright - United States",
    "132865":"No Copyright - United States",
    "120037":"No Copyright - United States",
    "957437":"No Copyright - United States",
    "139664":"No Copyright - United States",
    "134252":"No Copyright - United States",
    "821770":"No Copyright - United States",
    "771018":"No Copyright - United States",
    "132056":"No Copyright - United States",
    "130615":"No Copyright - United States",
    "130556":"No Copyright - United States",
    "148109":"No Copyright - United States",
    "147483":"No Copyright - United States",
    "872181":"No Copyright - United States",
    "872444":"No Copyright - United States",
    "872324":"No Copyright - United States",
    "149093":"No Copyright - United States",
    "136207":"No Copyright - United States",
    "871437":"No Copyright - United States",
    "120040":"No Copyright - United States",
    "131889":"No Copyright - United States",
    "871865":"No Copyright - United States",
    "218970":"No Copyright - United States",
    "957829":"No Copyright - United States",
    "958367":"No Copyright - United States",
    "183037":"No Copyright - United States",
    "872182":"No Copyright - United States",
    "135675":"No Copyright - United States",
    "957830":"No Copyright - United States",
    "844390":"No Copyright - United States",
    "84968":"No Copyright - United States",
    "574581":"No Copyright - United States",
    "161815":"No Copyright - United States",
    "957878":"No Copyright - United States",
    "486734":"No Copyright - United States",
    "128246":"No Copyright - United States",
    "911508":"No Copyright - United States",
    "886553":"No Copyright - United States",
    "956329":"No Copyright - United States",
    "496165":"No Copyright - United States",
    "494884":"No Copyright - United States",
    "852583":"No Copyright - United States",
    "132858":"No Copyright - United States",
    "532224":"No Copyright - United States",
    "182861":"No Copyright - United States",
    "467314":"No Copyright - United States",
    "133064":"No Copyright - United States",
    "847173":"No Copyright - United States",
    "859067":"No Copyright - United States",
    "839750":"No Copyright - United States",
    "839760":"No Copyright - United States",
    "133066":"No Copyright - United States",
    "757072":"No Copyright - United States",
    "610164":"No Copyright - United States",
    "207368":"No Copyright - United States",
    "358079":"No Copyright - United States",
    "123854":"No Copyright - United States",
    "136208":"No Copyright - United States",
    "129352":"No Copyright - United States",
    "132768":"No Copyright - United States",
    "133043":"No Copyright - United States",
    "115270":"No Copyright - United States",
    "138450":"No Copyright - United States",
    "800660":"No Copyright - United States",
    "170048":"No Copyright - United States",
    "874908":"No Copyright - United States",
    "147503":"No Copyright - United States",
    "315394":"No Copyright - United States",
    "132915":"No Copyright - United States",
    "128921":"No Copyright - United States",
    "439727":"No Copyright - United States",
    "214674":"No Copyright - United States",
    "136933":"No Copyright - United States",
    "583236":"No Copyright - United States",
    "440012":"No Copyright - United States",
    "779572":"No Copyright - United States",
    "825919":"No Copyright - United States",
    "439887":"No Copyright - United States",
    "562805":"No Copyright - United States",
    "121679":"No Copyright - United States",
    "123030":"No Copyright - United States",
    "123430":"No Copyright - United States",
    "123432":"No Copyright - United States",
    "125631":"No Copyright - United States",
    "132917":"No Copyright - United States",
    "116606":"No Copyright - United States",
    "139421":"No Copyright - United States",
    "140633":"No Copyright - United States",
    "134480":"No Copyright - United States",
    "134481":"No Copyright - United States",
    "123285":"No Copyright - United States",
    "124376":"No Copyright - United States",
    "162102":"No Copyright - United States",
    "712354":"No Copyright - United States",
    "180181":"No Copyright - United States",
    "163918":"Not In Copyright - United States",
    "821802":"Not In Copyright - United States",
    "92049":"Not In Copyright - United States",
    "960206":"Not In Copyright - United States",
    "960205":"Not In Copyright - United States",
    "959637":"Not In Copyright - United States",
    "100278":"Not In Copyright - United States",
    "305262":"Not In Copyright - United States",
    "136532":"Not In Copyright - United States",
    "174224":"Not In Copyright - United States",
    "178263":"Not In Copyright - United States",
    "123285":"Not In Copyright - United States",
    "869837":"Not In Copyright - United States",
    "767022":"Not In Copyright - United States",
    "313911":"Not In Copyright - United States",
    "313912":"Not In Copyright - United States",
    "313913":"Not In Copyright - United States",
    "313914":"Not In Copyright - United States",
    "313915":"Not In Copyright - United States",
    "313916":"Not In Copyright - United States",
    "313917":"Not In Copyright - United States",
    "313918":"Not In Copyright - United States",
    "313919":"Not In Copyright - United States",
    "313920":"Not In Copyright - United States",
    "313921":"Not In Copyright - United States",
    "313922":"Not In Copyright - United States",
    "313923":"Not In Copyright - United States",
    "313924":"Not In Copyright - United States",
    "313925":"Not In Copyright - United States",
    "313926":"Not In Copyright - United States",
    "313927":"Not In Copyright - United States",
    "313928":"Not In Copyright - United States",
    "313929":"Not In Copyright - United States",
    "313930":"Not In Copyright - United States",
    "313931":"Not In Copyright - United States",
    "313932":"Not In Copyright - United States",
    "313933":"Not In Copyright - United States",
    "313934":"Not In Copyright - United States",
    "313935":"Not In Copyright - United States",
    "313936":"Not In Copyright - United States",
    "313937":"Not In Copyright - United States",
    "313938":"Not In Copyright - United States",
    "313939":"Not In Copyright - United States",
    "313940":"Not In Copyright - United States",
    "313941":"Not In Copyright - United States",
    "313942":"Not In Copyright - United States",
    "313943":"Not In Copyright - United States",
    "313944":"Not In Copyright - United States",
    "313945":"Not In Copyright - United States",
    "313946":"Not In Copyright - United States",
    "313947":"Not In Copyright - United States",
    "313948":"Not In Copyright - United States",
    "313949":"Not In Copyright - United States",
    "313950":"Not In Copyright - United States",
    "313951":"Not In Copyright - United States",
    "313952":"Not In Copyright - United States",
    "313953":"Not In Copyright - United States",
    "313954":"Not In Copyright - United States",
    "313955":"Not In Copyright - United States",
    "313956":"Not In Copyright - United States",
    "313957":"Not In Copyright - United States",
    "313958":"Not In Copyright - United States",
    "313959":"Not In Copyright - United States",
    "313960":"Not In Copyright - United States",
    "313961":"Not In Copyright - United States",
    "313962":"Not In Copyright - United States",
    "313963":"Not In Copyright - United States",
    "313964":"Not In Copyright - United States",
    "313965":"Not In Copyright - United States",
    "313966":"Not In Copyright - United States",
    "313967":"Not In Copyright - United States",
    "313968":"Not In Copyright - United States",
    "313969":"Not In Copyright - United States",
    "313970":"Not In Copyright - United States",
    "313971":"Not In Copyright - United States",
    "313972":"Not In Copyright - United States",
    "313973":"Not In Copyright - United States",
    "313974":"Not In Copyright - United States",
    "313975":"Not In Copyright - United States",
    "313976":"Not In Copyright - United States",
    "313977":"Not In Copyright - United States",
    "313978":"Not In Copyright - United States",
    "313979":"Not In Copyright - United States",
    "313980":"Not In Copyright - United States",
    "967351":"Not In Copyright - United States",
    "182844":"Not In Copyright - United States",
    "628659":"Not In Copyright - United States",
    "812965":"Not In Copyright - United States",
    "611710":"Not In Copyright - United States",
    "874244":"Not In Copyright - United States",
    "385768":"Not In Copyright - United States",
    "874513":"Not In Copyright - United States",
    "597737":"Not In Copyright - United States",
    "183067":"Not In Copyright - United States",
    "872286":"Not In Copyright - United States",
    "24857":"Not In Copyright - United States",
    "175620":"Not In Copyright - United States",
    "286252":"Not In Copyright - United States",
    "204838":"Not In Copyright - United States",
    "302517":"Not In Copyright - United States",
    "206133":"Not In Copyright - United States",
    "205225":"Not In Copyright - United States",
    "210915":"Not In Copyright - United States",
    "224655":"Not In Copyright - United States",
    "619069":"Not In Copyright - United States",
    "454550":"Not In Copyright - United States",
    "394241":"Not In Copyright - United States",
    "320331":"Not In Copyright - United States",
    "755136":"Not In Copyright - United States",
    "403181":"Not In Copyright - United States",
    "530490":"Not In Copyright - United States",
    "141541":"Not In Copyright - United States",
    "176125":"Not In Copyright - United States",
    "398526":"Not In Copyright - United States",
    "311664":"Not In Copyright - United States",
    "176193":"Not In Copyright - United States",
    "808002":"Not In Copyright - United States",
    "178655":"Not In Copyright - United States",
    "451929":"Not In Copyright - United States",
    "753994":"Not In Copyright - United States",
    "962512":"Not In Copyright - United States",
    "199963":"Not In Copyright - United States",
    "273884":"Not In Copyright - United States",
    "618993":"Not In Copyright - United States",
    "912432":"Not In Copyright - United States",
    "297464":"Not In Copyright - United States",
    "576653":"Not In Copyright - United States",
    "400446":"Not In Copyright - United States",
    "182848":"Not In Copyright - United States",
    "532447":"Not In Copyright - United States",
    "755253":"Not In Copyright - United States"}

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
    # elif "zxx" in value: return "No linguistic content"
    elif "zza" in value: return "Zaza"

# parsing dates from raw value
def dateFormatter(dateString, calledBy):
    # print(dateString)
    dateSort = ''
    dateDisplay = ''
    # looking for dates like 1876-1987
    if len(re.findall('[0-9]{4}-[0-9]{4}',dateString)) > 0:
        dateList = re.findall('[0-9]{4}-[0-9]{4}',dateString)
        dateList.sort()
        dateSort = dateList[0] + '/' + dateList[-1]
        dateDisplay = dateList[0] + '-' + dateList[-1]
    # looking for dates like 1951-67
    elif len(re.findall('[0-9]{4}-[0-9]{2}',dateString)) > 0:
        dateList = re.findall('[0-9]{4}-[0-9]{2}',dateString)
        # dateList.sort()
        dateSort = dateList[0][0:4] + '/' + dateList[0][0:2]  + dateList[0][-2:]
        dateDisplay = dateList[0][0:4] + '-' + dateList[0][-2:]
    elif len(re.findall('[0-9]{4}',dateString)) > 0:
        dateList = re.findall('[0-9]{4}',dateString)
        dateList.sort()
        for d in dateList: 
            if len(dateSort) > 0:
                # print(d)
                dateSort = dateSort + '/' + d
                dateDisplay = dateDisplay + '-' + d
            else: 
                dateSort = d
                dateDisplay = d
    else:
        # looking for dates like 19-- 
        dateList = re.findall('[0-9]{3}-{1}?|[0-9]{2}-{2}?',dateString)
        if len(dateList) > 0:
            for d in dateList:   
                d = d.replace('-','0')
            dateList = dateList.sort()
            for d in dateList:
                if len(dateSort) > 0:
                    dateSort = dateSort + '/' + d
                    dateDisplay = dateDisplay + '-' + d
                else: 
                    dateSort = d
                    dateDisplay = d
    if 'dateSort' not in locals():
        dateSort = ''
    # removing initial 'd' carefully, since some dates have "december" in them - checking if the character after the 'd' is a number; 
    # could be done with regex too but, well, it isn't
    # if dateString[0] == 'd' and ord(dateString[1]) >= 48 and ord(dateString[1]) <= 57:
    #     dateDisplay = dateString.strip(" .,d").replace('[','').replace(']','')
    # else: 
    #     dateDisplay = dateString.strip(" .,").replace('[','').replace(']','')
    deleteList = ['n.d.', 'no date', 'undated']
    # print(dateString)
    for dl in deleteList:
        if dateDisplay == dl:
            dateDisplay = ''
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

# whitelist-based substitution of piction's project values
def pictionProject(projValue):
    valArray = projValue.split(';')
    returnArray = []
    valueSubstitutes = {
        "IMLS CLIR 2020":"IMLS CARES 2020",
        "25":"",
        ".":"",
        "1859: Much More than the Origin":"",
        "1919 Chicago Race Riots":"Chicago 1919",
        "Abraham Lincoln Project":"",
        "Adoption Program":"Adoption Program",
        "American Indian Histories and Cultures (Adam Matthew Digital)":"American Indian Histories and Cultures (Adam Matthew Digital)",
        "American Indian Newspapers (Adam Matthew Digital)":"American Indian Newspapers (Adam Matthew Digital)",
        "American Revolutionary War Era Maps (Boston Public Library)":"American Revolutionary War Era Maps (Boston Public Library)",
        "American Sheet Music Covers (Newberry Library)":"",
        "American West (Adam Matthew Digital":"American West (Adam Matthew Digital)",
        "American West (Adam Matthew Digital)":"American West (Adam Matthew Digital)",
        "American West (Adam Matthew Digital)":"American West (Adam Matthew Digital)",
        "Approaching the Mexican Revolution: Books":"Approaching the Mexican Revolution: Books",
        "Artifacts of Childhood: 700 Years of Children's Books":"Artifacts of Childhood: Children's Books",
        "Artifacts of Childhood: Children's Books at the Newberry":"Artifacts of Childhood: Children's Books",
        "Ayer Art Digital Collection":"",
        "Ayer Art Digital Collection (Newberry Library)":"",
        "Ballistics and Politics: Military Architecture Books at the Newberry":"Ballistics and Politics",
        "Ballyhoo! A Peek Under the Big Top":"Ballyhoo! A Peek Under the Big Top",
        "Booked for the Evening 2019":"",
        "Border Troubles in the War of 1812":"Border Troubles in the War of 1812",
        "Burnham":"Burnham in the Philippines",
        "Burnham in the Philippines: Plans for Manila and Baguio City":"Burnham in the Philippines",
        "Calligraphy is Always News: Recent Newberry Acquisitions":"Calligraphy Is Always News",
        "Cartographic Treasures of the Newberry Library":"Cartographic Treasures of the Newberry Library",
        "Caxton Club":"",
        "CBQ: Building an Empire":"CBQ: Building an Empire",
        "Chicago":"",
        "Chicago 1919: Confronting the Race Riots":"Chicago 1919",
        "Chicago and the Midwest":"",
        "Chicago and the Midwest (Newberry Library":"",
        "Chicago and the Midwest (Newberry Library)":"",
        "Chicago and the Midwest (Newberry Library)":"",
        "Chicago and the Midwest (Newberry Library)Chicago and the Midwest (Newberry Library)":"",
        "Chicago Calligraphy Collective":"Chicago Calligraphy Collective",
        "Chicago Fire":"Chicago Fire",
        "Chicago's Great 20th-Century Bookman":"Chicago's Great 20th-Century Bookman",
        "Civil WarThe Civil War in Art: Teaching and Learning through Chicago Collections":"Civil War in Art",
        "CLIR Wing Grant":"CLIR Wing Printing Specimens",
        "CLIR Wing Printing Samples":"CLIR Wing Printing Specimens",
        "CLIR Wing Printing Specimens":"CLIR Wing Printing Specimens",
        "Collecting America: How a Friendship Enriched Our Understanding of American Culture":"Collecting America",
        "Complete Letters of Willa Cather A Digital Scholarly Edition":"Willa Cather Archive Project (University of Nebraska-Lincoln)",
        "Creating Shakespeare":"Creating Shakespeare",
        "Daily Life Along the Chicago":"Daily Life Along the Chicago Burlington and Quincy Railroad",
        "Daily Life Along the Chicago Burlington and Quincy Railroad (Newberry Library)":"Daily Life Along the Chicago Burlington and Quincy Railroad",
        "Digital Collection for the Classroom":"Digital Collections for the Classroom",
        "Digital Collections for the Classroom":"Digital Collections for the Classroom",
        "Digital Collections in the Classroom":"Digital Collections for the Classroom",
        "Digital scriptorium":"Digital Scriptorium",
        "Digitial Collections for the Classroom":"Digital Collections for the Classroom",
        "Edward E. Ayer Digital Collection":"",
        "Edward E. Ayer Digital Collection (Newberry Library)":"",
        "Elizabeth I: Ruler and Legend":"Elizabeth I",
        "Encyclopedia of Chicago":"Encyclopedia of Chicago",
        "Ephemeral by Design":"Ephemeral by Design",
        "Ephemeral by Design: Organizing the Everyday":"Ephemeral by Design",
        "Everett D. Graff Collection of Western Americana (Newberry Library)":"",
        "Everywhere West (Blog)":"Everywhere West (Blog)",
        "Explore Chicago Collections":"Explore Chicago Collections",
        "Explore Chicago Collections (Newberry Library)":"Explore Chicago Collections",
        "Faith in the City: Chicago's Religious Diversity":"Faith in the City",
        "Filename Recon":"",
        "French Canadians in the Midwest":"French Canadians in the Midwest",
        "French Paleography":"French Paleography",
        "Frontier to Heartland":"Frontier to Heartland",
        "Frontier to Heartland: Four Centuries in Central North America":"Frontier to Heartland",
        "Fujita exhibit":"",
        "Global Commodities (Adam Matthew Digital)":"Global Commodities (Adam Matthew Digital)",
        "Global Heartland":"",
        "Goodman Exhibit":"Stagestruck City: Birth of the Goodman",
        "Great Lakes Collection (Newberry Library)":"",
        "Great Lakes Digital Collection (Newberry Library":"",
        "Great Lakes Digital Collection (Newberry Library)":"",
        "Hamilton":"Hamilton: The History Behind the Musical",
        "Hamilton Exhibit":"Hamilton: The History Behind the Musical",
        "Hamilton: The History Behind the Musical":"Hamilton: The History Behind the Musical",
        "Henri IV of France: The Vert Galant and His Reign":"",
        "Historic Maps in K-12 Classrooms":"Historic Maps in K-12 Classrooms",
        "History of Mass Tourism (Adam Matthew Digital)":"History of Mass Tourism (Adam Matthew Digital)",
        "History of the Goodman Theater":"Stagestruck City: Birth of the Goodman",
        "Home Front: Daily Life in the Civil War North":"Home Front: Daily Life in the Civil War North",
        "Home Front: Daily Life in the Civil War NorthChicago and the Midwest (Newberry Library)":"Home Front: Daily Life in the Civil War North|Chicago and the Midwest",
        "Humanism For Sale":"Humanism for Sale",
        "Humanism for Sale":"Humanism for Sale",
        "Humanities Mirror: Reading at the Newberry 1887-1987":"",
        "Illuminated Manuscripts and Printed Books: French Renaissance Gems of the Newberry":"Illuminated Manuscripts and Printed Books",
        "Illuminated Manuscripts and Printed Books: French Renaissance Gems of the Newberry":"Illuminated Manuscripts and Printed Books",
        "Illuminated Manuscripts and Printed Books: French Renaissance Gems of the Newberry Library":"Illuminated Manuscripts and Printed Books",
        "Indians of the Midwest":"Indians of the Midwest: An Archive of Endurance",
        "Indians of the Midwest: An Archive of Endurance":"Indians of the Midwest: An Archive of Endurance",
        "Internet Archive":"",
        "Introduction to Manuscript Studies":"",
        "Italian Paleography":"Italian Paleography",
        "Joint Acquisitions":"",
        "Joint purchase with Northwestern University (Newberry Library/Northwestern University (Evanston":"Northwestern University Joint Purchase",
        "Lewis and Clark and the Indian Country: 200 Years of American History":"Lewis and Clark and the Indian Country",
        "Library of Congress Musical Treasures Consortium":"Library of Congress Musical Treasures Consortium",
        "Lincoln at 200":"Lincoln at 200",
        "Love on Paper":"Love on Paper",
        "Make Big Plans":"Make Big Plans",
        "Make Big Plans: Daniel Burnham's Vision of an American Metropolis":"Make Big Plans",
        "Make Big Plans: Daniel Burnham's Vision of an American Metropolis (2014)":"Make Big Plans",
        "Making Modernism":"Making Modernism",
        "Mapline":"",
        "Mapping Manifest Destiny: Chicago and the American West":"Mapping Manifest Destiny",
        "Mapping Movement":"Mapping Movement",
        "Mapping Movement in American History and Culture":"Mapping Movement",
        "Mapping Movement in American History and CultureEdward E. Ayer Digital Collection (Newberry Library)":"Mapping Movement",
        "Mapping the French empire in North America":"Mapping the French Empire in North America",
        "Mapping the French Empire in North America":"Mapping the French Empire in North America",
        "Maps: Finding Our Place in the World":"Maps: Finding Our Place in the World",
        "Maps: Finding Our Place in the World (Exhibit)":"Maps: Finding Our Place in the World",
        "Maps: Finding Our Place in the World (exhibit)":"Maps: Finding Our Place in the World",
        "Marbled Papers and Fine Bindings by Norma B. Rubovits":"",
        "Melville: Finding America at Sea":"Melville: Finding America at Sea",
        "Midwest Manuscript Collection (Newberry Library)":"",
        "Midwest Mapping project":"",
        "Modern Manuscript Digital Collection (Newberry Library)":"",
        "Morrison Exhibit":"",
        "Music (Newberry Library)":"",
        "New Acquisition":"",
        "New Acquisitions":"",
        "New Acquisitions 2014":"",
        "New Aquisitions":"",
        "Newberry 125":"Newberry 125",
        "Newberry Library. John M. Wing Foundation":"",
        "Nova Reperta":"Nova Reperta",
        "Out of Many":"Out of Many",
        "Out of Many: Religious Pluralism in America":"Out of Many",
        "Outspoken":"Outspoken",
        "Outspoken: Chicago's Free Speech Tradition":"Outspoken",
        "Pictures from an Exposition: Visualizing the 1893 Worldâ€™s Fair":"Pictures from an Exposition",
        "Pictures from an Exposition: Visualizing the 1893 World's Fair":"Pictures from an Exposition",
        "Picturing America":"Picturing America",
        "Plainly Spoken":"Plainly Spoken",
        "Plainly Spoken Exhibit":"Plainly Spoken",
        "Pluralism":"Out of Many",
        "Politics":"",
        "Postcards Digital Collection (Newberry Library)":"",
        "Ptolemy's geography and Renaissance mapmakers":"",
        "Pullman Digital Collection (Newberry Library)":"",
        "Pullman Drawings 2005-":"Pullman Drawings 2005-",
        "Pullman: Labor":"",
        "Pullman: Labor":"",
        "Race Riots":"Chicago 1919",
        "Realizing the Newberry Idea":"Realizing the Newberry Idea",
        "Religious Change":"Religious Change",
        "Revolutionary France and Haiti":"Revolutionary France and Haiti",
        "Shakespeare":"",
        "Shakespreare":"",
        "Sir Arthur Conan Doyle: Beyond Sherlock Holmes":"Beyond Sherlock Holmes",
        "Sister Ann Ida Gannon Initiative":"",
        "Stagestruck City: Chicago's Theater Tradition and the Birth of the Goodman":"Stagestruck City: Birth of the Goodman",
        "Stock images":"",
        "Stock images images":"",
        "Stock imagesEdward E. Ayer Digital Collection (Newberry Library)":"",
        "The American West":"American West (Adam Matthew Digital)",
        "The Aztecs and the Making of Colonial Mexico":"Aztecs and the Making of Colonial Mexico",
        "The Bard is Born":"Bard Is Born",
        "The Civil War in Art: Teaching and Learning through Chicago Collections":"Civil War in Art",
        "The Civil War in Letters":"",
        "The Frontier in American Culture":"",
        "The History of Cartography":"",
        "The Legacy of Chicago Dance":"",
        "The Long Struggle for African-American Civil Rights in Chicago":"",
        "The Many Faces of Marie Antionette":"Many Faces of Marie Antoinette",
        "The Many Faces of Marie Antoinette":"Many Faces of Marie Antoinette",
        "The Newberry 125":"Newberry 125",
        "The Newberry 125":"Newberry 125",
        "The Old Soldier Scanning Project":"",
        "The Play's the Thing: 400 Years of Shakespeare on Stage":"",
        "The Theodore Roosevelt Project":"",
        "To be uploaded (C and MW)":"",
        "To the Ends of the Earth: Exploring the Poles":"",
        "Treasures of Faith: Twenty Years of Acquisitions":"Treasures of Faith",
        "What is the Midwest":"What Is the Midwest",
        "Willa Cather Archive Project":"Willa Cather Archive Project (University of Nebraska-Lincoln)",
        "Wing oversize ZPP 2083 .K614":"",
        "World Digital Library":"World Digital Library",
        "World War I Sheet Music":"",
        "World's Fairs (Adam Matthew Digital)":"World's Fairs (Adam Matthew Digital)"}
    for val in valArray:
        val = val.strip()
        if val != '':
            try:
                returnVal = valueSubstitutes[val] 
                returnArray.append(returnVal)
            except KeyError:
                projectList.append(val)

# directory = r'./csv_batches/splits/'
directory = r'./csv_batches/test/'
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        print(filename)
        # filename = 'batch-35_chunk_0'
        # TODO: add this as an argument 
        # filename = 'batch-37-short'

        # with open(filename + '.csv', mode='r') as infile:
        with open(directory + filename, mode='r') as infile:
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
                        except:
                            try:
                                urlBibidIdx = rowObj['CATALOG_LINK'].index('bibId=')  + 6
                                rowObj['BIBID'] = rowObj['CATALOG_LINK'][urlBibidIdx:]
                            except:
                                try: 
                                    urlBibidIdxEnd = rowObj['CATALOG_LINK'].index('8805867')
                                    urlBibidIdxStart = rowObj['CATALOG_LINK'].index('99') + 2
                                    rowObj['BIBID'] = rowObj['CATALOG_LINK'][urlBibidIdxStart:urlBibidIdx]
                                except:
                                    print(rowObj['UMO ID'] + ': no bib id')
                    rowObj['BIBID'] = rowObj['BIBID'].replace('/t','').replace('	','').replace(' ','').replace('.jpg','').replace('.0','').replace('.','')
                    recordList.append(rowObj)
                count += 1

        # redact api key before pushing
        apikey = 'xxxx'

        # items is the home for the processed data; this is what's exported to 'data_[filename].csv'
        items = []

        
        for i in recordList:
            # try:
            #     if i['FILE NAME'].index(' ') > 0:
            #         junkItem = {'FILENAME': i['FILE NAME'], 'BIBID': i['BIBID'], 'UMO': i['UMO ID']}
            #         print('junk!')
            #         junkDrawer.append(junkItem)
            # except:
            # if i['BIBID'] == '209795': print(i['BIBID'])
            itemDict = {}
            # many filenames for each bibid, so no use in calling the api for every file; do it once then check all the rest
            alreadyDoneIndex = next((index for (index, d) in enumerate(items) if len(items) > 0 and 'BIBID' in d and d['BIBID'] == i['BIBID']), None)
            if alreadyDoneIndex != None:
                # print(i['BIBID'] + ' already done, reusing...')
                itemDict = items[alreadyDoneIndex]
                # have to make sure we're not reusing the filename too
                itemDict['FILENAME'] = i['FILE NAME']
            elif i['BIBID'] != '': 
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
                    itemDict['SUBJECTS'] = ''
                    itemDict['SUBJECT_list'] = []
                    itemDict['PLACE'] = ''
                    itemDict['PLACE_list'] = []
                    itemDict['FORMAT'] = ''
                    itemDict['FORMAT_list'] = []
                    itemDict['BIOGRAPHICAL/HISTORICAL NOTE'] = ''
                    itemDict['BIOGRAPHICAL/HISTORICAL NOTE_list'] = []
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
                    itemDict['DATE_raw'] = ''
                    itemDict['FORMAT_EXTENT'] = ''
                    itemDict['FORMAT_EXTENT_list'] = []
                    itemDict['CALLNUMBER'] = ''
                    itemDict['CALLNUMBER_list'] = []
                    itemDict['ARCHIVAL_COLLECTION'] = root[0].find("record/leader").text[7]
                    # itemDict['ARCHIVAL_COLLECTION_code'] = root[0].find("record/leader").text[7] + ': ' + root[0].find("record/leader").text
                    itemDict['ARCHIVAL_COLLECTION_list'] = {
                        '245': '',
                        '710': ''
                    }
                    itemDict['CATALOG_LINK'] = 'https://i-share-nby.primo.exlibrisgroup.com/permalink/01CARLI_NBY/i5mcb2/alma' + str(i['BIBID'])
                    itemDict['CONTRIBUTING_INSTITUTION'] = "Newberry Library"
                    itemDict['OA_POLICY'] = "The Newberry makes its collections available for any lawful purpose, commercial or non-commercial, without licensing or permission fees to the library, subject to the following terms and conditions: https://www.newberry.org/rights-and-reproductions"
                    itemDict['DISCLAIMER_STMT'] = "All materials in the Newberry Library’s collections have research value and reflect the society in which they were produced. They may contain language and imagery that are offensive because of content relating to: ability, gender, race, religion, sexuality/sexual orientation, and other categories. More information: https://www.newberry.org/sites/default/files/textpage-attachments/Statement_on_Potentially_Offensive_Materials.pdf"
                    try: 
                        itemDict['STANDARDIZED_RIGHTS'] = copyrightStatus[itemDict['BIBID']]
                    except KeyError: 
                        itemDict['STANDARDIZED_RIGHTS'] = ''
                    # showing Jennifer some samples of piction/alma subject "conflicts" - may remove this version of the data if a decision is made to prioritize one 
                    # itemDict['piction_SUBJECT'] = i['SUBJECTS']
                    itemDict['piction_INTERNALNOTES'] = i['INTERNALNOTES']
                    if len(i['FULLVOLUME']) > 0:
                        returnValue = ''
                        try:
                            returnValue = 'fullvolume=yes' if i['FULLVOLUME'].index('yes') > 0 or i['FULLVOLUME'].index('Yes') > 0 else ''
                        except:
                            try: 
                                returnValue = 'fullvolume=no' if i['FULLVOLUME'].index('no') > 0 or i['FULLVOLUME'].index('No') > 0 else ''
                            except: 
                                returnValue = ''
                        if len(itemDict['piction_INTERNALNOTES'] ) > 0:
                            itemDict['piction_INTERNALNOTES']  = itemDict['piction_INTERNALNOTES']  + '; ' + returnValue
                        else: 
                            itemDict['piction_INTERNALNOTES']  = returnValue
                    if root[0].find("record/leader").text[7] == 'c':
                        if len(itemDict['piction_INTERNALNOTES'] ) > 0:
                            itemDict['piction_INTERNALNOTES']  = itemDict['piction_INTERNALNOTES']  + '; needs_arch_coll_title'
                        else: 
                            itemDict['piction_INTERNALNOTES']  = 'needs_arch_coll_title'
                    # itemDict['piction_FULLVOLUME'] = i['FULLVOLUME']
                    # itemDict['piction_APPROVED'] = i['APPROVED']
                    # piction folder ??
                    itemDict['piction_PROJECT'] = pictionProject(i['PROJECT'])

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
                            if key == 'TITLE':
                                returnValue = ''
                                for value in record.findall('subfield'): 
                                    code = value.get('code')
                                    if code not in 'xyz':
                                        if len(returnValue) > 0:
                                            returnValue = returnValue + ' ' + value.text
                                        else: 
                                            returnValue = value.text
                                itemDict['TITLE'] = returnValue
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
                                else: 
                                    itemDict['ARCHIVAL_COLLECTION'] = ''
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
                                    try: 
                                        if value.text[-1:] == '.' or value.text[-1:] == ',':
                                            valueText = value.text[:-1]
                                    except: continue
                                    code = value.get('code')
                                    if code == 'a': subjectDict['a'] = valueText
                                    elif code == 'z': subjectDict['z'] = dashDelimeter(subjectDict['z'], valueText)
                                # fullValue = dashDelimeter(subjectDict['a'], dashDelimeter(subjectDict['x'], subjectDict['y']))
                                if len(subjectDict['a']) > 0 and subjectDict['a'] not in itemDict['SUBJECT_list'] and len(itemDict['SUBJECT_list']) < 5:
                                    itemDict['SUBJECT_list'].append(subjectDict['a'])
                                stringVersion = ''
                                for val in itemDict['SUBJECT_list']:
                                    stringVersion = pipeDelimeter(stringVersion, val)
                                itemDict['SUBJECTS'] = stringVersion
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
                                try: 
                                    if itemDict['FORMAT'].count('|') > 5:
                                        print(itemDict['FORMAT'])
                                except:
                                    for value in record.findall('subfield'): 
                                        if value.get('code') == 'a':
                                            valueText = value.text
                                            if value.text[-1:] == '.' or value.text[-1:] == ',':
                                                valueText = value.text[:-1]
                                            if valueText not in itemDict[keyList]: 
                                                itemDict[keyList].append(valueText)
                                        # if value.get('code') == 'y' and itemDict['DATE_SORT'] == '' and itemDict['DATE_DISPLAY'] == '':
                                        #     dateString = dateFormatter(value.text, 'format')
                                        #     itemDict['DATE_DISPLAY'] = dateString[0]
                                        #     itemDict['DATE_SORT'] = dateString[1]
                                        #     itemDict['DATE_raw'] = dateString[2]
                                stringVersion = ''
                                for val in itemDict[keyList]:
                                    try:
                                        parenDex = val.index('(')
                                        firstCharAfter = val[parenDex + 1]
                                        # print(val[parenDex + 1])
                                        if firstCharAfter.islower():
                                            val = val[:parenDex + 1] + firstCharAfter.upper() + val[parenDex + 2:]
                                    except:
                                        val = val
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
                                dateString = ''
                                for value in record.findall('subfield'): 
                                    if dateString == '':
                                        dateString = value.text
                                    else: 
                                        dateString = dateString + ' ' + value.text
                                    # print (dateString)
                                # re.search("^The.*Spain$", txt)
                                dateList = dateFormatter(dateString, 'date')
                                itemDict['DATE_DISPLAY'] = dateList[0]
                                itemDict['DATE_SORT'] = dateList[1]
                                itemDict['DATE_raw'] = dateString[2]
                                    # if value.text[:1] == 'd' or value.text[:1] == '[':
                                    #     valueText = value.text[1:]
                                    # if len(itemDict[key]) > 0 and itemDict[key].find('?') == -1:
                                    #     if int(itemDict[key]) and int(itemDict[key]) < int(valueText):
                                    #         itemDict[key] = itemDict[key] + delimiter + valueText
                                    # elif int(valueText):
                                    #     itemDict[key] =  valueText 
                                    # else: 
                                    #     print('date error, value: ' + valueText + '; api url: ' + itemUrl)
                            if key == 'BIOGRAPHICAL/HISTORICAL NOTE' or key == 'SUMMARY':
                                for value in record.findall('subfield'):
                                    if value.get('code') == 'a' or value.get('code') == 'b':
                                        itemDict[key] = value.text 
                            if key == 'CALLNUMBER':
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
                        if marcCode == '545': itemer(record, 'BIOGRAPHICAL/HISTORICAL NOTE')
                        if marcCode == '520': itemer(record, 'SUMMARY')
                        if marcCode == '300': itemer(record, 'FORMAT_EXTENT')
                        if marcCode == '008': itemer(record, '008')
                        if marcCode == '041': itemer(record, '041')
                        if marcCode == '099': itemer(record, 'CALLNUMBER')
                        if marcCode == '852': itemer(record, 'CALLNUMBER')
                        if marcCode == '710': itemer(record, 'ARCHIVAL_COLLECTION')
                        if marcCode == '045': itemer(record, 'DATE_DISPLAY')
                        if marcCode == '045': itemer(record, 'DATE_SORT')
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
                            itemDict['ARCHIVAL_COLLECTION'] = 'Archival Collection Title Needed'
                        if itemDict['DATE_SORT'] != '' and itemDict['STANDARDIZED_RIGHTS'] == '':
                            lastDate = max(itemDict['DATE_SORT'].split('/'))
                            curYear = date.today().year
                            if int(lastDate) >= curYear - 95:
                                itemDict['STANDARDIZED_RIGHTS'] = 'No Copyright - United States'
                            else: 
                                itemDict['STANDARDIZED_RIGHTS'] = 'Copyright Not Evaluated'
                        elif itemDict['DATE_SORT'] == '' and itemDict['STANDARDIZED_RIGHTS'] == '':
                            itemDict['STANDARDIZED_RIGHTS'] = 'Copyright Not Evaluated'
                        # getting DCMI Type from file format if A/V; else, getting from Piction Type value
                        if itemDict['FILENAME'].endswith(".mov") or itemDict['FILENAME'].endswith(".avi") or itemDict['FILENAME'].endswith(".mp4") or itemDict['FILENAME'].endswith(".m2t") or itemDict['FILENAME'].endswith(".m4v"):
                            itemDict['DCMIType'] = "Moving Image"
                        elif itemDict['FILENAME'].endswith(".wav") or  itemDict['FILENAME'].endswith(".mp3"):
                            itemDict['DCMIType'] = "Sound"
                        else:
                            itemDict['DCMIType'] = i['TYPE'].replace('; ','|').replace(';','|')
                            # itemDict['DCMIType'] = typer(i['TYPE'])

                    del itemDict['CREATOR_list']
                    del itemDict['SUBJECT_list']
                    del itemDict['PLACE_list']
                    del itemDict['FORMAT_list']
                    del itemDict['BIOGRAPHICAL/HISTORICAL NOTE_list']
                    del itemDict['SUMMARY_list']
                    del itemDict['DATE_DISPLAY_list']
                    del itemDict['DATE_SORT_list']
                    del itemDict['FORMAT_EXTENT_list']
                    del itemDict['LANGUAGE_list']
                    del itemDict['CALLNUMBER_list']
                    del itemDict['ARCHIVAL_COLLECTION_list']
                    # del itemDict['CATALOG_LINK_list']
                else: 
                    rejectObj = {
                        'UMO ID': i['UMO ID'],
                        'FILE NAME': i['FILE NAME'],
                        'BIBID': i['BIBID']
                    }
                    rejects.append(rejectObj)
                    print("failure: API results have a length of 0 on UMO: " + i['UMO ID'] + " / BIBID: " + i['BIBID'])
            else: 
                rejectObj = {
                    'UMO ID': i['UMO ID'],
                    'FILE NAME': i['FILE NAME'],
                    'BIBID': i['BIBID']
                }
                rejects.append(rejectObj)
                print('no bib id, moving on...')
            if len(itemDict) > 0:
                try:
                    if itemDict['FILENAME'].index(' ') > 0:
                        junkDrawer.append(itemDict)
                except ValueError:
                    items.append(itemDict)

        outputdirectory = './output/'

        dataFilename = 'data_'  + filename

        dataFile = open(outputdirectory + 'json_' + dataFilename + '.json', "w")
        dataFile.write(json.dumps(items, indent=4))

        print("length of item array: " + str(len(items)))
        if len(items) > 0:
            keys = items[0].keys()
            with open(outputdirectory + dataFilename, 'w', newline='')  as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(items)
        else: 
            print("Big error.  Items array was length = 0")

        if len(rejects) > 0:
            rejectsFilename = 'no_bibid_' + filename
            keys = rejects[0].keys()
            with open(outputdirectory + rejectsFilename, 'w') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(rejects)

        if len(junkDrawer) > 0:
            junkDrawerFilename = 'junkDrawer_' + filename
            keys = junkDrawer[0].keys()
            with open(outputdirectory + junkDrawerFilename, 'w') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(junkDrawer)
            dataFile = open(outputdirectory + 'json_' + junkDrawerFilename + '.json', "w")
            dataFile.write(json.dumps(junkDrawer, indent=4))


        if len(projectList) > 0:
            projectListFilename = 'projectList.txt'
            textfile = open(projectListFilename, "w")
            for element in projectList:
                textfile.write(element + "\n")
            textfile.close()
