#!/bin/bash
mkdir -p ./eval/
python benchmark.py --gold=./oie_corpus/all.oie --out=eval/Stanford.dat --stanford=./systems_output/stanford_output.txt
python benchmark.py --gold=./oie_corpus/all.oie --out=eval/OLLIE.dat --ollie=./systems_output/ollie_output.txt
#python benchmark.py --gold=./oie_corpus/all.oie --out=eval/ReVerb.dat --reverb=./systems_output/reverb_output.txt
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

#python benchmark.py --gold=./oie_corpus/all.oie --out=eval/GrapheneChrHeadNotSep.dat --graphene=./systems_output/graphene_chr_output_head_notseparate.txt
#python benchmark.py --gold=./oie_corpus/all.oie --out=eval/GrapheneChrNestNotSep.dat --graphene=./systems_output/graphene_chr_output_nest_notseparate.txt
#python benchmark.py --gold=./oie_corpus/all.oie --out=eval/GrapheneChrHead.dat --graphene=./systems_output/graphene_chr_output_head.txt
#python benchmark.py --gold=./oie_corpus/all.oie --out=eval/GrapheneChrNest.dat --graphene=./systems_output/graphene_chr_output_nest.txt

python pr_plot.py --in=./eval --out=./eval/eval.png
echo "DONE"
