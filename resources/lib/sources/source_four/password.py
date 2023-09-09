import xbmc, xbmcgui, xbmcplugin, xbmcaddon, sys

from resources.lib.sources.source_four import (vikitube, cc, fstroke, tube_norop, pgirls, india, ptry, vtry,
                                               phat, bigwank, palm, p_ok, p_incest, p_fpo, p_any, p_bravo, p_pha, p_plus,
                                               p_wankos, p_worm, p_wolf, p_xbabe, p_helm, p_helmm, p_xvideo, p_icom,
                                               p_anysex, p_prox, p_flix, p_phd, xcafe, shake, huge, jizz, perv, groovy,
                                               k4k, zb, lust, alot, xtube, mov3, hqbang, xtits, freehd, iporn, tubefun,
                                               xhand, milf,plove,pyes, plouder)

def parent_control(utility):
    """Open access to videos is correct password is provided."""

    keyboard = xbmc.Keyboard()
    keyboard.setHeading('Enter password')
    keyboard.setHiddenInput(True)
    keyboard.doModal()

    if keyboard.isConfirmed():

        entry = keyboard.getText().lower()
        if entry == 'relax': utility.menu()
        elif entry != 'relax':sys.exit()

    else:
        sys.exit()

password_dict = {"vikitube":    vikitube,
                 "ccadult":     cc,
                 "fs":          fstroke,
                 "norop":       tube_norop,
                 "perfectgirls":pgirls,
                 "india":       india,
                 "ptry":        ptry,
                 "vtry":        vtry,
                 "phat":        phat,
                 "pbig":        bigwank,
                 "ppalm":       palm,
                 "pok":         p_ok,
                 "pincest":     p_incest,
                 "pfpo":        p_fpo,
                 "anyadult":    p_any,
                 "bravoadult":  p_bravo,
                 "phaadult":    p_pha,
                 "plusadult":   p_plus,
                 "wankozadult": p_wankos,
                 "wormadult":   p_worm,
                 "wolfadult":   p_wolf,
                 "xbabeadult":  p_xbabe,
                 "helmadult":   p_helm,
                 "helmmadult":  p_helmm,
                 "xvideosadult":p_xvideo,
                 "icomadult":   p_icom,
                 "anysexadult": p_anysex,
                 "xozillaadult":p_prox,
                 "pfeatadult":  p_flix,
                 "analdinadult":p_phd,
                 "xcafeadult":  xcafe,
                 "shakeadult":  shake,
                 "hugeadult":   huge,
                 "jizzadult":   jizz,
                 "pervadult":   perv,
                 "groovyadult": groovy,
                 "k4kadult":    k4k,
                 "zbadult":     zb,
                 "lustadult":   lust,
                 "alotadult":   alot,
                 "xtubeadult":  xtube,
                 "mov3adult":   mov3,
                 "hqadult":     hqbang,
                 "xtitsadult":  xtits,
                 "freehdadult": freehd,
                 "ipornadult":  iporn,
                 "tubefunadult":tubefun,
                 "xhandadult":  xhand,
                 "milfadult":   milf,
                 "ploveadult":  plove,
                 "pyesadult":   pyes,
                 "plouderadult":plouder,
                }

def confirm_password(arg):
    """Return key value if argument parse is found as key in dictionary object."""
    
    for item in password_dict:

        if arg == item:

            parent_control(password_dict[item])

        else:

            continue

if __name__ == "__main__":

    print(password_dict)
