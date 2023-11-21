#!/usr/bin/env python3

import omg  # omgifol 0.4.0 (devinacker fork)
import os
import sys
import omg.txdef
import PIL

CWILV_MAX = 20

# Imports the sky patch from the patch object "old_patch_obj" into the wad
# "new_wad" with the texture edit object "textures". "new_pname" is the new patch name
# and "new_tname" is the new texture name.
def import_std_sky(new_wad, textures, old_patch_obj, new_pname, new_tname):
    new_wad.patches[new_pname] = old_patch_obj
    textures[new_tname] = omg.txdef.TextureDef()
    textures[new_tname].name = new_tname
    textures[new_tname].width, textures[new_tname].height = 256, 128
    textures[new_tname].patches.append(omg.txdef.PatchDef())
    textures[new_tname].patches[-1].name = new_pname
    textures[new_tname].patches[-1].x, textures[new_tname].patches[-1].y = 0, 0

def add_level_name_patches(new_wad, res_dir):
    for i in range(0, CWILV_MAX + 1):
        imgid = "CWILV{0:02}".format(i)
        patch = omg.Graphic(from_file=f"{res_dir}/{imgid}.png")
        patch.offsets = (0, 0)
        new_wad.patches[imgid] = patch

def verify_files_exist(res_dir, drop_dir, output_dir):
    drop_files = [
        "ATTACK.WAD",
        "BLACKTWR.WAD",
        "BLOODSEA.WAD",
        "CANYON.WAD",
        "CATWALK.WAD",
        "COMBINE.WAD",
        "DOOM2.WAD",
        "FISTULA.WAD",
        "GARRISON.WAD",
        "GERYON.WAD",
        "MANOR.WAD",
        "MEPHISTO.WAD",
        "MINOS.WAD",
        "NESSUS.WAD",
        "PARADOX.WAD",
        "SUBSPACE.WAD",
        "SUBTERRA.WAD",
        "TEETH.WAD",
        "TTRAP.WAD",
        "VESPERAS.WAD",
        "VIRGIL.WAD"
    ]

    res_files = [
        "INTERPIC.lmp",
        "TITLEPIC.lmp",
        "UMAPINFO.txt"
    ]  # plus CWILV[00-CWILV_MAX]

    for file in drop_files:
        if not os.path.isfile(f"{drop_dir}/{file}"):
            raise Exception(f"missing user-provided resource {file}")

    for file in res_files:
        if not os.path.isfile(f"{res_dir}/{file}"):
            raise Exception(f"missing resource {file}")
    
    for file in ["CWILV{0:02}.png".format(i) for i in range(0, CWILV_MAX+1)]:
        if not os.path.isfile(f"{res_dir}/{file}"):
            raise Exception(f"missing resource {file}")

    if not os.path.isdir(output_dir):
        raise Exception(f"missing output directory")

def _main():
    base_dir = os.getcwd()
    res_dir = f"{base_dir}/res/"
    drop_dir = f"{base_dir}/drophere/"
    output_dir = f"{base_dir}/output/"
    output_wad_fname = "UMASTER.WAD"

    try:
        verify_files_exist(res_dir, drop_dir, output_dir)
    except Exception as e:
        print("Error while checking for required files:", e)
        return -1

    new_wad = omg.WAD()

    with open(f"{res_dir}/UMAPINFO.txt", "rb") as umapinfo_file:
        new_wad.data["UMAPINFO"] = omg.Lump(umapinfo_file.read())

    with open(f"{res_dir}/TITLEPIC.lmp", "rb") as titlepic_file:
        new_wad.graphics["TITLEPIC"] = omg.Lump(titlepic_file.read())

    with open(f"{res_dir}/INTERPIC.lmp", "rb") as interpic_file:
        new_wad.graphics["INTERPIC"] = omg.Lump(interpic_file.read())

    # individual levels
    doom2 = map_wad = omg.WAD(f"{drop_dir}/DOOM2.WAD")
    new_wad.txdefs = doom2.txdefs
    new_tex = omg.txdef.Textures(new_wad.txdefs)

    map_wad = omg.WAD(f"{drop_dir}/ATTACK.WAD")
    new_wad.maps["MAP01"] = map_wad.maps["MAP01"]

    map_wad = omg.WAD(f"{drop_dir}/CANYON.WAD")
    new_wad.maps["MAP02"] = map_wad.maps["MAP01"]

    map_wad = omg.WAD(f"{drop_dir}/CATWALK.WAD")
    new_wad.maps["MAP03"] = map_wad.maps["MAP01"]

    map_wad = omg.WAD(f"{drop_dir}/COMBINE.WAD")
    new_wad.maps["MAP04"] = map_wad.maps["MAP01"]
    import_std_sky(new_wad, new_tex, map_wad.data["RSKY1"], "PSKYCOMB", "TSKYCOMB")

    map_wad = omg.WAD(f"{drop_dir}/FISTULA.WAD")
    new_wad.maps["MAP05"] = map_wad.maps["MAP01"]

    map_wad = omg.WAD(f"{drop_dir}/GARRISON.WAD")
    new_wad.maps["MAP06"] = map_wad.maps["MAP01"]

    map_wad = omg.WAD(f"{drop_dir}/MANOR.WAD")
    new_wad.maps["MAP07"] = map_wad.maps["MAP01"]
    import_std_sky(new_wad, new_tex, map_wad.patches["STARS"], "PSKYTITA", "TSKYTITA")

    map_wad = omg.WAD(f"{drop_dir}/PARADOX.WAD")
    new_wad.maps["MAP08"] = map_wad.maps["MAP01"]

    map_wad = omg.WAD(f"{drop_dir}/SUBSPACE.WAD")
    new_wad.maps["MAP09"] = map_wad.maps["MAP01"]

    map_wad = omg.WAD(f"{drop_dir}/SUBTERRA.WAD")
    new_wad.maps["MAP10"] = map_wad.maps["MAP01"]

    map_wad = omg.WAD(f"{drop_dir}/TTRAP.WAD")
    new_wad.maps["MAP11"] = map_wad.maps["MAP01"]

    map_wad = omg.WAD(f"{drop_dir}/VIRGIL.WAD")
    new_wad.maps["MAP12"] = map_wad.maps["MAP03"]
    import_std_sky(new_wad, new_tex, map_wad.data["RSKY1"], "PSKYSLEE", "TSKYSLEE")

    map_wad = omg.WAD(f"{drop_dir}/MINOS.WAD")
    new_wad.maps["MAP13"] = map_wad.maps["MAP05"]

    map_wad = omg.WAD(f"{drop_dir}/BLOODSEA.WAD")
    new_wad.maps["MAP14"] = map_wad.maps["MAP07"]

    map_wad = omg.WAD(f"{drop_dir}/MEPHISTO.WAD")
    new_wad.maps["MAP15"] = map_wad.maps["MAP07"]

    map_wad = omg.WAD(f"{drop_dir}/NESSUS.WAD")
    new_wad.maps["MAP16"] = map_wad.maps["MAP07"]

    map_wad = omg.WAD(f"{drop_dir}/GERYON.WAD")
    new_wad.maps["MAP17"] = map_wad.maps["MAP08"]

    map_wad = omg.WAD(f"{drop_dir}/VESPERAS.WAD")
    new_wad.maps["MAP18"] = map_wad.maps["MAP09"]

    map_wad = omg.WAD(f"{drop_dir}/BLACKTWR.WAD")
    new_wad.maps["MAP19"] = map_wad.maps["MAP25"]

    map_wad = omg.WAD(f"{drop_dir}/TEETH.WAD")
    new_wad.maps["MAP20"] = map_wad.maps["MAP31"]
    new_wad.maps["MAP21"] = map_wad.maps["MAP32"]
    # why not? (https://doomwiki.org/wiki/DoomEd_4.2)
    new_wad.data["TAGDESC"] = map_wad.data["TAGDESC"]

    add_level_name_patches(new_wad, res_dir)

    # save texture changes
    new_wad.txdefs = new_tex.to_lumps()

    output_path = f"{output_dir}/{output_wad_fname}"
    new_wad.to_file(output_path)

    print("Success. Output PWAD is", os.path.normpath(os.path.relpath(output_path)))

    return 0

if __name__ == "__main__":
    sys.exit(_main())
