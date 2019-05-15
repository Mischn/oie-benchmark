#!/bin/bash
mkdir -p ./eval/
python benchmark.py --gold=./oie_corpus/all.oie --out=eval/Stanford.dat --stanford=./systems_output/stanford_output.txt
python benchmark.py --gold=./oie_corpus/all.oie --out=eval/OLLIE.dat --ollie=./systems_output/ollie_output.txt
#python benchmark.py --gold=./oie_corpus/all.oie --out=eval/ReVerb.dat --reverb=./systems_output/reverb_output.txt
python benchmark.py --gold=./oie_corpus/all.oie --out=eval/ReVerb.dat --reverb2=./systems_output/reverb2_output.txt
python benchmark.py --gold=./oie_corpus/all.oie --out=eval/ClausIE.dat --clausie=./systems_output/clausie_output.txt
python benchmark.py --gold=./oie_corpus/all.oie --out=eval/OpenIE-4.dat --openiefour=./systems_output/openie4_output.txt
python benchmark.py --gold=./oie_corpus/all.oie --out=eval/PropS.dat --props=./systems_output/props_output.txt

#python benchmark.py --gold=./oie_corpus/all.oie --out=eval/GrapheneOldHead.dat --graphene=./systems_output/graphene_output_head.txt
#python benchmark.py --gold=./oie_corpus/all.oie --out=eval/GrapheneOldNest.dat --graphene=./systems_output/graphene_output_nest.txt

#python benchmark.py --gold=./oie_corpus/all.oie --out=eval/GrapheneNewHeadNotSep.dat --graphene=./systems_output/graphene_new_output_head_notseparate.txt
#python benchmark.py --gold=./oie_corpus/all.oie --out=eval/GrapheneNewNestNotSep.dat --graphene=./systems_output/graphene_new_output_nest_notseparate.txt
#python benchmark.py --gold=./oie_corpus/all.oie --out=eval/GrapheneNewHead.dat --graphene=./systems_output/graphene_new_output_head.txt
#python benchmark.py --gold=./oie_corpus/all.oie --out=eval/GrapheneNewNest.dat --graphene=./systems_output/graphene_new_output_nest.txt
python benchmark.py --gold=./oie_corpus/all.oie --out=eval/Graphene.dat --graphene=./systems_output/graphene_new_output_nest.txt

# Graphene as Framework
#python benchmark.py --gold=./oie_corpus/all.oie --out=eval/Graphene_Stanford.dat --graphene=./systems_output/graphene_as_framework/stanfordOpenIEExtractor.txt
#python benchmark.py --gold=./oie_corpus/all.oie --out=eval/Graphene_OLLIE.dat --graphene=./systems_output/graphene_as_framework/ollieExtractor.txt
#python benchmark.py --gold=./oie_corpus/all.oie --out=eval/Graphene_ReVerb.dat --graphene=./systems_output/graphene_as_framework/reverbExtractor.txt
#python benchmark.py --gold=./oie_corpus/all.oie --out=eval/Graphene_ClausIE.dat --graphene=./systems_output/graphene_as_framework/clausieExtractor.txt
#python benchmark.py --gold=./oie_corpus/all.oie --out=eval/Graphene_OpenIE-4.dat --graphene=./systems_output/graphene_as_framework/openie4Extractor.txt


python pr_plot.py --in=./eval --out=./eval/eval.png
echo "DONE"
