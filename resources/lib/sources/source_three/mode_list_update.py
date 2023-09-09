import os, re
from os import path
from json import dump as json_dump, load as json_load


keys_path = re.sub('\\\\sources\\\\source_three', '\\\\modules\\\\keys', os.path.dirname(os.path.abspath(__file__)))

mode_keys = os.path.join(keys_path, 'modelist.json')
key_join = os.path.join

path_dicts = {'anysex_path': key_join(keys_path, 'keys_anysex.json'),
             'fs_path': key_join(keys_path, 'keys_fs.json'),
             'pg_path': key_join(keys_path, 'keys_pg.json'),
             'indian_path': key_join(keys_path, 'keys_indian.json'),
             'cc_path': key_join(keys_path, 'keys_cc.json'),
             'vikki_path': key_join(keys_path, 'keys_vikki.json'),
             'ptry_path': key_join(keys_path, 'keys_ptry.json'),
             'vtry_path': key_join(keys_path, 'keys_vtry.json'),
             'phat_path': key_join(keys_path, 'keys_phat.json'),
             'bigwank_path': key_join(keys_path, 'keys_bigwank.json'),
             'palmtube_path': key_join(keys_path, 'keys_palmtube.json'),
             'norop_path': key_join(keys_path, 'keys_norop.json'),
             'ok_path': key_join(keys_path, 'keys_ok.json'),
             'incest_path': key_join(keys_path, 'keys_incest.json'),
             'fpo_path': key_join(keys_path, 'keys_fpo.json'),
             'pha_path': key_join(keys_path, 'keys_pha.json'),
             'icom_path': key_join(keys_path, 'keys_icom.json'),
             'worm_path': key_join(keys_path, 'keys_worm.json'),
             'wolf_path': key_join(keys_path, 'key_wolf.json'),
             'wankoz_path': key_join(keys_path, 'keys_wankoz.json'),
             'xvideos_path': key_join(keys_path, 'keys_xvideos.json'),
             'anyporn_path': key_join(keys_path, 'keys_anyporn.json'),
             'xbabe_path': key_join(keys_path, 'keys_xbabe.json'),
             'bravo_path': key_join(keys_path, 'keys_bravo.json'),
             'helmm_path': key_join(keys_path, 'keys_helmm.json'),
             'plus_path': key_join(keys_path, 'keys_plus.json'),
             'helm_path': key_join(keys_path, 'keys_helm.json'),
             'xozilla_path': key_join(keys_path, 'keys_xozilla.json'),
             'pfeat_path': key_join(keys_path, 'keys_pfeat.json'),
             'analdin_path': key_join(keys_path, 'keys_analdin.json'),
             'shake_path': key_join(keys_path, 'keys_shake.json'),
             'jizz_path': key_join(keys_path, 'keys_jizz.json'),
             'groovy_path': key_join(keys_path, 'keys_groovy.json'),
             'huge_path': key_join(keys_path, 'keys_huge.json'),
             'perv_path': key_join(keys_path, 'keys_perv.json'),
             'lust_path': key_join(keys_path, 'keys_lust.json'),
             'xcafe_path': key_join(keys_path, 'keys_xcafe.json'),
             'k4k_path': key_join(keys_path, 'keys_k4k.json'),
             'zb_path': key_join(keys_path, 'keys_zb.json'),
             'alot_path': key_join(keys_path, 'keys_alot.json'),
             'xtube_path': key_join(keys_path, 'keys_xtube.json'),
             'mov3_path': key_join(keys_path, 'keys_mov3.json'),
             'hq_path': key_join(keys_path, 'keys_hq.json'),
             'iporn_path': key_join(keys_path, 'keys_iporn.json'),
             'freehd_path': key_join(keys_path, 'keys_freehd.json'),
             'tubefun_path': key_join(keys_path, 'keys_tubefun.json'),
             'xhand_path': key_join(keys_path, 'keys_xhand.json'),
             'xtits_path': key_join(keys_path, 'keys_xtits.json'),
             'milf_path': key_join(keys_path, 'keys_milf.json'),
             }



data = [

        {"icon_image": "DefaultMovies.png"},

        [
            ["anyadult", "Any Tube"], ["bravoadult", "Bravo TUBE"], ["ccadult", "CC Adult"],
            ["fs", "Family Strokes"], ["anysexadult", "Any Sex Tube"], ["helmadult", "Helm Tube"], ["helmmadult", "Helmm TUBE"], ["icomadult", "Icom Tube"],
            ["india", "India"], ["norop", "Norop Tube"], ["pbig", "BIGWANK TUBE"], ["perfectgirls", "Perfect Girls"],
            ["pfpo", "FPO TUBE"], ["phaadult", "Pha Tube"], ["phat", "PHAT TUBE"], ["pincest", "INCEST TUBE"], ["plusadult", "Plus Tube"],
            ["pok", "OK TUBE"], ["ppalm", "PALM TUBE"], ["ptry", "PTRY TUBE"], ["vikitube", "Viki Tube"], ["vtry", "VTRY TUBE"],
            ["wankozadult", "Wankoz Tube"], ["wolfadult", "Wolf Tube"], ["wormadult", "Worm Tube"], ["xbabeadult", "Xbabe Tube"],
            ["xvideosadult", "Xvideos Tube"], ["xozillaadult", "Xozilla Tube"], ["pfeatadult", "Pfeat Tube"], ["analdinadult", "Analdin Tube"],
            ["shakeadult", "Shake Tube"], ["jizzadult", "Jizz Tube"], ["groovyadult", "Groovy Tube"], ["hugeadult", "Huge Tube"],
            ["pervadult", "Perv Tube"], ["lustadult", "Lust Tube"], ["xcafeadult", "Xcafe Tube"], ["k4kadult", "K4K Tube"],
            ["zbadult", "ZB Tube"], ["alotadult", "Alot Tube"], ["xtubeadult", "Xtube Tube"], ["mov3adult", "Mov3 Tube"], ["hqadult", "HQ Tube"],
            ["ipornadult", "Iporn Tube"], ["freehdadult", "Freehd Tube"], ["tubefunadult", "Tubefun Tube"], ["xhandadult", "Xhand Tube"], ["xtitsadult", "Xtits Tube"],
            ["milfadult", "Milf Tube"]
         ], # mode_list_key_one

        [["norophome","Home"],["noropsearchs","Search"]],

        [["vikkihome","Home"],["vikkicat","Categories"],["vikkisearchs","Search"]],

        [["pghome","Home"],["pgname","Names"],["pgnamefilter","Top Names"],["pgcat","Category"],["pgsearchs","Search"]],

        [["cchome","Home"],["cccat","Category"],["cc_name","Names"],["cc_namefilter","Top Names"],["ccsearchs","Search"]],

        [["fshome","Home"],["fssearchs","Search"]],

        [["anysexhome","Home"],["anysexcat","Category"],["anysexname","Names"], ["anysexnamefilter","Top Names"], ["anysexsearch","Search"]],

        [["indiahome","Home"],["indiasearchs","Search"]],

        [["ptryhome","Home"],["ptrycat","Category"],["ptryname","Names"],["ptrynamefilter","Top Names"],["ptrysearchs","Search"]],

        [["vtryhome","Home"],["vtrycat","Category"],["vtryname","Names"],["vtrynamefilter","Top Names"],["vtrysearchs","Search"]],

        [["phathome","HOME"],["phatnames","NAMES"],["phatnamesfilter","Top Names"],["phatchannel","CHANNEL"], ["phatsearchs","Search"]],

        [["bigwankhome","HOME"],["bigwankcat","CATEGORY"],["bigwanknames","NAMES"], ["bigwanknamesfilter","Top Names"],["bigwanksearchs","Search"]],

        [["palmhome","HOME"],["palmcat","CATEGORY"],["palmnames","NAMES"], ["palmnamesfilter","Top Names"],["palmsearchs","Search"]],

        [["okhome","HOME"],["oknames","NAMES"],["oknamesfilter","Top Names"],["okchannel","CHANNEL"],["oksearchs","Search"]],

        [["fpohome","HOME"],["fponames","NAMES"],["fponamesfilter","Top Names"],["fposearchs","Search"]],

        [["incesthome","HOME"]],

        [["phahome","HOME"],["phanames","NAMES"],["phanamesfilter","Top Names"],["phacat","CATEGORY"], ["phachannel","CHANNEL"], ["phasearchs","Search"]],

        [["icomhome","HOME"],["icomcat","CATEGORY"], ["icomsearchs","Search"]],

        [["wormhome","HOME"],["wormnames","NAMES"],["wormnamesfilter","Top Names"],["wormcat","CATEGORY"],["wormchannel","CHANNEL"], ["wormsearchs","Search"]],

        [["wolfhome","HOME"],["wolfcat","CATEGORY"],["wolfnames","NAMES"], ["wolfnamesfilter","Top Names"],["wolfsearchs","Search"]],

        [["wankozhome","HOME"],["wankozcat","CATEGORY"],["wankoznames","NAMES"], ["wankoznamesfilter","Top Names"],["wankozsearchs","Search"]],

        [["xvideoshome","HOME"],["xvideosnames","NAMES"],["xvideonamesfilter","Top Names"],["xvideoschannel","CHANNEL"], ["xvideossearchs","Search"]],

        [["anyhome","HOME"], ["anycat","CATEGORY"], ["anycatall","CATEGORY ALL"],["anychannel","CHANNEL"], ["anysearchs","Search"]],

        [["xbabehome","HOME"], ["xbabesearchs","Search"]],

        [["bravohome","HOME"],["bravocat","CATEGORY"],["bravonames","NAMES"], ["bravonamesfilter","Top Names"],["bravosearchs","Search"]],

        [["helmmhome","HOME"],["helmmcat","CATEGORY"],["helmmsearchs","Search"]],

        [["plushome","HOME"], ["pluscat","CATEGORY"],["plusnames","NAMES"],["plusnamesfilter","Top Names"],["plussearchs","Search"]],

        [["helmhome","HOME"], ["helmsearchs","Search"]],
        
        [["xozillahome","Home"],
         ["xozillaname","Names"],["xozillanamefilter","Top Names"],["xozillacat","Category"],["xozillaallcat","All Category"],["xozillachannel","Channel"],["xozillasearchs","Search"]],

        [["pfeathome","Home"],["pfeatvideo","Feat Videos"],["pfeatcat","Category"],["pfeatchannel","Channel"],["pfeatsearchs","Search"]],

        [["analdinhome","Home"],["analdinmodels","Names"],["analdinmodelsfilter","Top Names"],
         ["analdincat","Category"], ["analdincatAll","All Category"], ["analdinchannel","Channel"],["analdinplaylist","Playlist"],["analdinsearchs","Search"]],

        [["shakehome","Home"], ["shakename", "Names"], ["shaketopname", "Top Names"],["shakecat", "Category"],["shakechannel", "Channel"],["shakesearchs","Search"]],

        [["jizzhome","Home"],["jizzname", "Names"], ["jizztopname", "Top Names"],["jizzcat", "Category"],["jizzchannel", "Channel"],["jizzsearchs","Search"]],

        [["groovyhome","Home"], ["groovysearchs","Search"]],

        [["hugehome","Home"],["hugesearchs","Search"]],

        [["pervhome","Home"], ["pervcat", "Category"],["pervsearchs","Search"]],
        
        [["lusthome","Home"], ["lustcat", "Category"], ["lustchannel", "Chennel"], ["lustsearchs","Search"]],
        
        [["xcafehome","Home"],["xcafname", "Names"], ["xcafetopname","Top Names"], ["xcafcat", "Category"], ["xcafchannel", "Channel"], ["xcafesearchs","Search"]],
        
        [["k4khome","Home"], ["k4kname", "Names"],["k4ktopname","Top Names"],["k4kcat", "Category"], ["k4kchannel", "Channel"],["k4ksearchs","Search"]],

        [["zbhome","Home"], ["zbname", "Names"],["zbtopname","Top Names"],["zbcat", "Category"], ["zbchannel", "Channel"],["zbsearchs","Search"]],
        
        [["alothome","Home"], ["alotvideo", "Video"],["alotcat", "Category"],["alotsearchs","Search"]],
        
        [["xtubehome","Home"], ["xtubename", "Names"],["xtubetopname","Top Names"], ["xtubecat", "Category"], ["xtubesearchs","Search"]],

        [["mov3home","Home"], ["mov3videos", "Videos"], ["mov3name", "Names"],["mov3topname","Top Names"], ["mov3cat", "Category"], ["mov3searchs","Search"]],

        [["hqhome","Home"],["hqcat", "Category"], ["hqsearchs","Search"]],

        [["ipornhome","Home"], ["ipornvideo", "Videos"], ["iporncat", "Category"], ["ipornname", "Names"],["iporntopname","Top Names"], ["ipornsearchs","Search"]],

        [["freehdhome","Home"], ["freehdvideo", "Videos"], ["freehdcat", "Category"], ["freehdname", "Names"],["freehdtopname","Top Names"],
         ["freehdsearchs","Search"]],

        [["tubefunhome","Home"], ["tubefunvideo", "Videos"], ["tubefuncat", "Category"], ["tubefunname", "Names"],["tubefuntopname","Top Names"],
         ["tubefunsearchs","Search"]],

        [["xhandhome","Home"], ["xhandchannel", "Sites"], ["xhandplaylist", "Playlist"], ["xhandcat", "Category"], ["xhandname", "Names"],
         ["xhandtopname","Top Names"], ["xhandsearchs","Search"]],

        [["xtitshome","Home"], ["xtitsplaylist", "Playlist"], ["xtitschannel", "Channel"], ["xtitscat", "Category"], ["xtitsname", "Names"],
         ["xtitstopname","Top Names"], ["xtitssearchs","Search"]],

        [["milfhome","Home"],["milfcat", "Category"], ["milfname", "Names"], ["milftopname","Top Names"], ["milfsearchs","Search"]]
    ]

data_incest = {"incesthome":["http://www.incestflix.com/","http://12inch.incestflix.webcam/covers/UMfHpdkh.png","Home"]}

data_fpo = {"fpohome":["https://www.fpo.xxx/","https://www.fpo.xxx/contents/videos_screenshots/411000/411567/preview.jpg","Home"],  
            "fposearchs":["https://www.fpo.xxx/search/",
                           "https://www.fpo.xxx/contents/videos_screenshots/411000/411567/preview.jpg",
                           "Search"
                           ]
             }

data_norop = {"norophome":["https://pornorop.com/","https://cdn.pornorop.com/storage/c2/df/77/c2df77fd149c1c8e639b71d1cc51108d.jpg","Home"],
              "noropsearchs":["https://pornorop.com/search/",
                           "https://cdn.pornorop.com/storage/c2/df/77/c2df77fd149c1c8e639b71d1cc51108d.jpg",
                           "Search"]
             }


data_indian = {"indiahome":["https://www.indianpornvideo.org/","https://www.indianpornvideo.org/media/videos/10000/5000/x-sensual-anal-discoveries-sofy-soul.jpgg","Home"],
               "indiasearchs":["https://www.indianpornvideo.org/search.php",
                           "https://www.indianpornvideo.org/media/videos/10000/5000/x-sensual-anal-discoveries-sofy-soul.jpg",
                           "Search"
                           ]

               }

data_fs = {"fshome":["https://familystrokesporn.com/","https://familystrokesporn.com/wp-content/uploads/2019/01/Ride-This-Disco-Stick-Nina-Kayy-354x199.jpg","Home"],
            "fssearchs":["https://familystrokesporn.com/",
                           "https://familystrokesporn.com/wp-content/uploads/2019/01/Ride-This-Disco-Stick-Nina-Kayy-354x199.jpg",
                           "Search"
                           ]
           }

data_cc = {"cchome":["https://adult-movies.cc/",
                     "https://adult-movies.cc/media/thumbs/5/c/0/f/d/b067cc735ce4a886dec5f3517aba755a.mp4/b067cc735ce4a886dec5f3517aba755a.mp4-6b.jpg","Home"],
           "ccsearchs":["https://adult-movies.cc/searchgate.php" ,
                           "https://adult-movies.cc/media/thumbs/5/c/0/f/d/b067cc735ce4a886dec5f3517aba755a.mp4/b067cc735ce4a886dec5f3517aba755a.mp4-6b.jpg",
                           "Search"
                           ]
           }
data_vikki = {"vikkihome":["https://www.vikiporn.com/","https://cdni.vikiporn.com/contents/videos_screenshots/158000/158665/342x192/1.jpg?ver=3","Home"],
              "vikkisearchs":["https://www.vikiporn.com/search/",
                           "https://cdni.vikiporn.com/contents/videos_screenshots/158000/158665/342x192/1.jpg?ver=3",
                           "Search"
                           ]
             }

data_pg = {"pghome":["https://www.perfectgirls.xxx/","https://static.perfectgirls.xxx/contents/videos_screenshots/138000/138360/640x360/3.jpg","Home"],
           "pgsearchs":["https://www.perfectgirls.xxx/search/","https://static.perfectgirls.xxx/contents/videos_screenshots/138000/138360/640x360/3.jpg","Search"]
           }

data_anysex = {"anysexhome":["https://anysex.com/","https://screenshots.anysex.com/videos_screenshots/396000/396007/170x128/1.jpg","Home"],               
               "anysexsearch":["https://anysex.com/search/","https://screenshots.anysex.com/videos_screenshots/396000/396007/170x128/1.jpg","Search"]}

data_ptry = {"ptryhome":["https://www.porntry.com/","https://img.porntry.com/22611000/22611060/medium@2x/1.jpg","Home"],
             "ptrysearchs":["https://www.porntry.com/search/",
                           "https://img.porntry.com/22611000/22611060/medium@2x/1.jpg",
                           "Search"
                           ]
             }

data_vtry = {"vtryhome":["https://www.veryfreeporn.com/","https://img.veryfreeporn.com/15830000/15830611/medium@2x/1.jpg","Home"],
             "vtrysearchs":["https://www.veryfreeporn.com/search/",
                        "https://img.veryfreeporn.com/15830000/15830611/medium@2x/1.jpg",
                        "Search"
                        ]
             }

data_phat = {"phathome":["https://www.pornhat.com/","https://static.pornhat.com/contents/videos_screenshots/77000/77938/640x360/1.jpg","Home"],
             "phatsearchs":["https://www.pornhat.com/search/","https://static.pornhat.com/contents/videos_screenshots/77000/77938/640x360/1.jpg","Search"]
             }


data_bigwank = {"bigwankhome":["https://www.bigwank.com/","https://img.bigwank.com/93344000/93344333/medium@2x/1.jpg","Home"],
                "bigwanksearchs":["https://www.bigwank.com/search/","https://img.bigwank.com/93344000/93344333/medium@2x/1.jpg","Search"]
             }


data_palm = {"palmhome":["https://palmtube.com/","https://t2.palmtube.com/63/26364/14.jpg","Home"],
             "palmsearchs":["https://palmtube.com/channel/","https://t2.palmtube.com/63/26364/14.jpg","Search"]
             }



data_ok = {"okhome":["https://ok.porn/","https://static.ok.porn/contents/models/80/s1_Abella Danger.jpg","Home"],
             "oksearchs":["https://ok.porn/search/","https://static.ok.porn/contents/models/80/s1_Abella Danger.jpg","Search"]
           }

data_pha = {"phahome":["https://www.alphaporno.com/","https://img3-ap.alphaxcdn.com/386000/386761/640x360/2.jpg","HOME"],
                "phasearchs":["https://www.alphaporno.com/search/","https://img3-ap.alphaxcdn.com/386000/386761/640x360/2.jpg","SEARCH"]
             }


data_icom = {"icomhome":["https://www.pornicom.com/","https://cdni.pornicom.com/contents/videos_screenshots/768000/768576/390x293/1.jpg?ver=3","HOME"],
                "icomsearchs":["https://www.pornicom.com/search/","https://cdni.pornicom.com/contents/videos_screenshots/768000/768576/390x293/1.jpg?ver=3","SEARCH"]
             }

data_worm = {"wormhome":["https://www.pornworms.com/","https://images.pornworms.com/media/videos/tmb/000/334/080/1.jpg","HOME"],
            "wormsearchs":["https://www.pornworms.com/search/video/","https://images.pornworms.com/media/videos/tmb/000/334/080/1.jpg","SEARCH"]
             }

data_wolf = {"wolfhome":["https://www.tubewolf.com/","https://img3-tw.alphaxcdn.com/298000/298841/640x360/6.jpg","HOME"],
                "wolfsearchs":["https://www.tubewolf.com/s/","https://img3-tw.alphaxcdn.com/298000/298841/640x360/6.jpg","SEARCH"]
             }

data_wankoz = {"wankozhome":["https://www.wankoz.com/","https://www.wankoz.com/contents/models/780/s1_53.jpg","HOME"],
               "wankozsearchs":["https://www.wankoz.com/search/","https://www.wankoz.com/contents/models/780/s1_53.jpg","SEARCH"]
             }

data_xvideos = {"xvideoshome":["https://www.xvideos.com/",
                               "https://img-hw.xvideos-cdn.com/videos/thumbs169ll/3c/c2/19/3cc21955f9976085b137948d24132745/3cc21955f9976085b137948d24132745.4.jpg",
                               "HOME"],
                "xvideossearchs":["https://www.xvideos.com/search/",
                                  "https://img-hw.xvideos-cdn.com/videos/thumbs169ll/3c/c2/19/3cc21955f9976085b137948d24132745/3cc21955f9976085b137948d24132745.4.jpg",
                                  "SEARCH"]
             }


data_any = {"anyhome":["https://anyporn.com/","https://static-ap3.cdnanp.com/videos_screenshots/878000/878506/240x180/5.jpg","HOME"],
            "anysearchs":["https://anyporn.com/search/","https://static-ap3.cdnanp.com/videos_screenshots/878000/878506/240x180/5.jpg","SEARCH"]
            }

data_xbabe = {"xbabehome":["https://xbabe.com/","https://img2-xb.hellcdn.net/264000/264539/640x360/3.jpg","HOME"],
              "xbabesearchs":["https://xbabe.com/search/?q=","https://img2-xb.hellcdn.net/264000/264539/640x360/3.jpg","SEARCH"]
             }

data_bravo = {"bravohome":["https://www.bravoporn.com/","https://static-bp.cdnbm.net/970000/970025/240x180/14.jpg","HOME"],
              "bravosearchs":["https://www.bravoporn.com/s/","https://static-bp.cdnbm.net/970000/970025/240x180/14.jpg","SEARCH"]
             }
#remove
data_helmm = {"helmmhome":["https://hellmoms.com/","https://img3-hm.hellcdn.net/102000/102517/640x360/3.jpg","HOME"],
              "helmmsearchs":["https://hellmoms.com/s/","https://img3-hm.hellcdn.net/102000/102517/640x360/3.jpg","SEARCH"]
             }

data_plus = {"plushome":["https://www.porn-plus.com/fresh/","https://static-pp2.cdnanp.com/contents/videos_screenshots/877000/877748/300x225/10.jpg","HOME"],
             "plussearchs":["https://www.porn-plus.com/s/","https://static-pp2.cdnanp.com/contents/videos_screenshots/877000/877748/300x225/10.jpg","SEARCH"]
            }

data_helm = {"helmhome":["https://hellporno.com/","https://img2-hp.hellcdn.net/354000/354314/640x360/7.jpg","HOME"],
             "helmsearchs":["https://hellporno.com/search/","https://img2-hp.hellcdn.net/354000/354314/640x360/7.jpg","SEARCH"]
            }

data_xozilla = {"xozillahome":["https://www.xozilla.com/","https://i.xozilla.com/contents/videos_screenshots/27000/27371/300x169/27.jpg","Home"],
                "xozillasearchs":["https://www.xozilla.com/search/",
                        "https://i.xozilla.com/contents/videos_screenshots/27000/27371/300x169/27.jpg",
                        "Search"
                        ]
             }
data_pfeat = {"pfeathome":["https://www.pornfeat.com/","https://www.pornfeat.com/wp-content/uploads/2021/11/thumbnail-my-selfish-stepsister-needs-dick-s23e8-800x550.jpg","Home"],
              "pfeatvideo":["https://www.pornfeat.com/videos/","https://www.pornfeat.com/wp-content/uploads/2021/11/thumbnail-my-selfish-stepsister-needs-dick-s23e8-800x550.jpg","Feat Video"],
             "pfeatsearchs":["https://www.pornfeat.com/search/",
                        "https://www.pornfeat.com/wp-content/uploads/2021/11/thumbnail-my-selfish-stepsister-needs-dick-s23e8-800x550.jpg",
                        "Search"
                        ]
             }
data_analdin = {"analdinhome":["https://www.analdin.com/","https://i.analdin.com/contents/videos_screenshots/203000/203483/293x165/23.jpg","Home"],
             "analdinsearchs":["https://www.analdin.com/search/",
                        "https://i.analdin.com/contents/videos_screenshots/203000/203483/293x165/23.jpg",
                        "Search"
                        ]
             }

data_shake = {"shakehome":["https://xxxshake.com/","https://i.xxxshake.com/contents/videos_screenshots/149000/149262/640x360/1.jpg","Home"],
              "shakesearchs":["https://xxxshake.com/search/",
                           "https://i.xxxshake.com/contents/videos_screenshots/149000/149262/640x360/1.jpg",
                           "Search"
                           ]
             }

data_jizz = {"jizzhome":["https://jizzberry.com/","https://i.jizzberry.com/contents/videos_screenshots/112000/112112/640x360/1.jpg","Home"],
             "jizzsearchs":["https://jizzberry.com/search/",
                           "https://i.jizzberry.com/contents/videos_screenshots/112000/112112/640x360/1.jpg",
                           "Search"
                           ]
             }

data_groovy = {"groovyhome":["https://xgroovy.com/","https://i.xgroovy.com/contents/videos_screenshots/272000/272690/640x360/1.jpg","Home"],
               "groovysearchs":["https://xgroovy.com/search/",
                           "https://i.xgroovy.com/contents/videos_screenshots/272000/272690/640x360/1.jpg",
                           "Search"
                           ]
             }

data_huge = {"hugehome":["https://www.theyarehuge.com/","https://cdn.theyarehuge.com/contents/videos_screenshots/135000/135769/320x180/3.jpg","Home"],
             "hugesearchs":["https://www.theyarehuge.com/search/",
                           "https://cdn.theyarehuge.com/contents/videos_screenshots/135000/135769/320x180/3.jpg",
                           "Search"
                           ]
             }

data_perv = {"pervhome":["https://www.pervclips.com/","https://cdn.pervclips.com/tube/contents/videos_screenshots/1063783000/1063783776/367x275/3.jpg?ver=3","Home"],
             "pervsearchs":["https://www.pervclips.com/search/",
                           "https://cdn.pervclips.com/tube/contents/videos_screenshots/1063783000/1063783776/367x275/3.jpg?ver=3",
                           "Search"
                           ]
             }

data_lust = {"lusthome":["https://mylust.com/","https://i.mylust.com/videos_screenshots/958000/958372/200x150/3.jpg","Home"],
             "lustsearchs":["https://mylust.com/search/",
                           "https://i.mylust.com/videos_screenshots/958000/958372/200x150/3.jpg",
                           "Search"
                           ]
             }

data_xcafe = {"xcafehome":["https://xcafe.com/","https://i.xcafe.com/videos_screenshots/194000/194807/300x170/1.jpg","Home"],
              "xcafesearchs":["https://xcafe.com/search/",
                           "https://i.xcafe.com/videos_screenshots/194000/194807/300x170/1.jpg",
                           "Search"
                           ]
             }

data_k4k = {"k4khome":["https://4kporn.xxx/","https://st.4kporn.xxx/contents/videos_screenshots/854000/854381/320x180/1.jpg","Home"],
            "k4ksearchs":["https://4kporn.xxx/search/",
                           "https://st.4kporn.xxx/contents/videos_screenshots/854000/854381/320x180/1.jpg",
                           "Search"
                           ]
             }


data_zb = {"zbhome":["https://zbporn.com/","https://cdnth.zbporn.com/contents/videos_screenshots/617000/617143/264x198/1.jpg","Home"],
           "zbsearchs":["https://zbporn.com/search/",
                           "https://cdnth.zbporn.com/contents/videos_screenshots/617000/617143/264x198/1.jpg",
                           "Search"
                           ]
             }

data_alot = {"alothome":["https://www.alotporn.com/","https://bcdn.alotporn.com/contents/videos_screenshots/358000/358985/360x203/1.jpg","Home"],
              "alotvideo":["https://www.alotporn.com/latest-updates/","https://bcdn.alotporn.com/contents/videos_screenshots/358000/358985/360x203/1.jpg","Video"],
             "alotsearchs":["https://www.alotporn.com/search/",
                           "https://bcdn.alotporn.com/contents/videos_screenshots/358000/358985/360x203/1.jpg",
                           "Search"
                           ]
             }


data_xtube = {"xtubehome":["https://sextubefun.com/","https://sextubefun.com/media/thumbs/6/3/e/c/3/63e708861fde07.19683200.mp4/63e708861fde07.19683200.mp4-1.jpg","Home"],
              "xtubesearchs":["https://sextubefun.com/search/",
                           "https://sextubefun.com/media/thumbs/6/3/e/c/3/63e708861fde07.19683200.mp4/63e708861fde07.19683200.mp4-1.jpg",
                           "Search"
                           ]
             }


data_mov3 = {"mov3home":["https://www.3movs.com/","https://img.3movs.com/contents/videos_screenshots/0/720/321x181/1.jpg","Home"],
              "mov3videos":["https://www.3movs.com/videos/","https://img.3movs.com/contents/videos_screenshots/0/720/321x181/1.jpg","Videos"],
              "mov3searchs":["https://www.3movs.com/search_videos/",
                           "https://img.3movs.com/contents/videos_screenshots/0/720/321x181/1.jpg",
                           "Search"
                           ]
             }


data_hq = {"hqhome":["https://hqbang.com/","https://hqbang.com/contents/videos_screenshots/4000/4644/336x189/1.jpg","Home"],
           "hqsearchs":["https://hqbang.com/search/",
                           "https://hqbang.com/contents/videos_screenshots/4000/4644/336x189/1.jpg",
                           "Search"
                           ]
             }

data_iporn = {"ipornhome":["https://iporntoo.com/","https://iporntoo.com/media/thumbs/6/1/6/2/f/6162fc89256b07.85964424.mp4/6162fc89256b07.85964424.mp4-1.jpg","Home"],
           "ipornvideo":["https://iporntoo.com/videos/","https://iporntoo.com/media/thumbs/6/1/6/2/f/6162fc89256b07.85964424.mp4/6162fc89256b07.85964424.mp4-1.jpg","Video"],
           "ipornsearchs":["https://iporntoo.com/search/",
                           "https://iporntoo.com/media/thumbs/6/1/6/2/f/6162fc89256b07.85964424.mp4/6162fc89256b07.85964424.mp4-1.jpg",
                           "Search"
                           ]
             }

data_freehd = {"freehdhome":["https://freehdporn.xxx/","https://freehdporn.xxx/media/thumbs/6/3/9/b/f/639bf0f9283b20.03466854.mp4/639bf0f9283b20.03466854.mp4-8.jpg","Home"],
           "freehdvideo":["https://freehdporn.xxx/videos/","https://freehdporn.xxx/media/thumbs/6/3/9/b/f/639bf0f9283b20.03466854.mp4/639bf0f9283b20.03466854.mp4-8.jpg","Video"],
           "freehdsearchs":["https://freehdporn.xxx/search/",
                           "https://freehdporn.xxx/media/thumbs/6/3/9/b/f/639bf0f9283b20.03466854.mp4/639bf0f9283b20.03466854.mp4-8.jpg",
                           "Search"
                           ]
             }

data_tubefun = {"tubefunhome":["https://sextubefun.com/","https://sextubefun.com/media/thumbs/6/4/1/2/9/64129282b5c8c0.17659827.mp4/64129282b5c8c0.17659827.mp4-1.jpg","Home"],
           "tubefunvideo":["https://sextubefun.com/videos/","https://sextubefun.com/media/thumbs/6/4/1/2/9/64129282b5c8c0.17659827.mp4/64129282b5c8c0.17659827.mp4-1.jpg","Video"],
           "tubefunsearchs":["https://sextubefun.com/search/",
                           "https://sextubefun.com/media/thumbs/6/4/1/2/9/64129282b5c8c0.17659827.mp4/64129282b5c8c0.17659827.mp4-1.jpg",
                           "Search"
                           ]
             }

data_xhand = {"xhandhome":["https://xhand.com/","https://i.xhand.com/contents/videos_screenshots/40000/40908/410x230/14.jpg","Home"],
           "xhandsearchs":["https://xhand.com/search/",
                           "https://i.xhand.com/contents/videos_screenshots/40000/40908/410x230/14.jpg",
                           "Search"
                           ]
             }

data_xtits = {"xtitshome":["https://www.xtits.xxx/","https://www.xtits.xxx/contents/videos_screenshots/19000/19647/402x225/11.jpg","Home"],
           "xtitssearchs":["https://www.xtits.xxx/search/",
                           "https://www.xtits.xxx/contents/videos_screenshots/19000/19647/402x225/11.jpg",
                           "Search"
                           ]
             }


data_milf = {"milfhome":["https://www.milffox.com/","https://s1.milffox.com/t/3/442/02379a9737c094044bacbcb80d8654dd_normal.jpg","Home"],
           "milfsearchs":["https://www.milffox.com/search/",
                           "https://s1.milffox.com/t/3/442/02379a9737c094044bacbcb80d8654dd_normal.jpg",
                           "Search"
                           ]
             }
        
        
def dump_data(filename, data):

    with open(filename, 'w') as fh:

        json_dump(data, fh)


def load_data(filename):

    with open(filename) as fh:

        content = json_load(fh)

        return content

write_path_data = [
                   (path_dicts['pha_path'], data_pha),
                   (path_dicts['icom_path'], data_icom),
                   (path_dicts['worm_path'], data_worm),
                   (path_dicts['wolf_path'], data_wolf),
                   (path_dicts['wankoz_path'], data_wankoz),
                   (path_dicts['xvideos_path'], data_xvideos),
                   (path_dicts['anyporn_path'], data_any),
                   (path_dicts['xbabe_path'], data_xbabe),
                   (path_dicts['bravo_path'], data_bravo),
                   (path_dicts['helmm_path'], data_helmm),
                   (path_dicts['plus_path'], data_plus),
                   (path_dicts['helm_path'], data_helm),
                   (path_dicts['fs_path'], data_fs),
                   (path_dicts['pg_path'], data_pg),
                   (path_dicts['indian_path'], data_indian),
                   (path_dicts['cc_path'], data_cc),
                   (path_dicts['vikki_path'], data_vikki),
                   (path_dicts['ptry_path'], data_ptry),
                   (path_dicts['vtry_path'], data_vtry),
                   (path_dicts['phat_path'], data_phat),
                   (path_dicts['bigwank_path'], data_bigwank),
                   (path_dicts['palmtube_path'], data_palm),
                   (path_dicts['norop_path'], data_norop),
                   (path_dicts['ok_path'], data_ok),
                   (path_dicts['incest_path'], data_incest),
                   (path_dicts['fpo_path'], data_fpo),
                   (path_dicts['anysex_path'], data_anysex),
                   (path_dicts['xozilla_path'], data_xozilla),
                   (path_dicts['pfeat_path'], data_pfeat),
                   (path_dicts['analdin_path'], data_analdin),
                   (path_dicts['shake_path'],data_shake),
                   (path_dicts['jizz_path'],data_jizz),
                   (path_dicts['groovy_path'],data_groovy),
                   (path_dicts['huge_path'],data_huge),
                   (path_dicts['perv_path'],data_perv),
                   (path_dicts['lust_path'],data_lust),
                   (path_dicts['xcafe_path'],data_xcafe),
                   (path_dicts['k4k_path'],data_k4k),
                   (path_dicts['zb_path'], data_zb),
                   (path_dicts['alot_path'],data_alot),
                   (path_dicts['xtube_path'],data_xtube),
                   (path_dicts['mov3_path'],data_mov3),
                   (path_dicts['hq_path'],data_hq),
                   (path_dicts['iporn_path'], data_iporn),
                   (path_dicts['freehd_path'],data_freehd),
                   (path_dicts['tubefun_path'],data_tubefun),
                   (path_dicts['xhand_path'],data_xhand),
                   (path_dicts['xtits_path'],data_xtits),
                   (path_dicts['milf_path'],data_milf)
                  ]

def view_keys(filepath):

    d_data = dict()
    count = 0

    for item in load_data(filename = filepath):

        if count > 1:

            d_data[count] = item

        count += 1

    return d_data


def assign_num(filename, check_name):

    data = list(zip(view_keys(filename).keys(), view_keys(filename).values()))

    for item in data:

        print(item)

        if item[1][0][0] == check_name:

            name = item[0]

        else:continue

    return name

if __name__ == "__main__":

    dump_data(mode_keys, data)

    for item in write_path_data:

        dump_data(item[0], item[1])
        
    print(assign_num(mode_keys, 'pghome'))



