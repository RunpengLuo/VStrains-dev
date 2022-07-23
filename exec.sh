#/bin/zsh
conda init zsh
conda activate spades-hapConstruction-env

# 5 HIV
python src/__init__.py -a spades -g benchmark/fastq/5-strain-HIV-20000x/output_careful/assembly_graph_after_simplification.gfa -p benchmark/fastq/5-strain-HIV-20000x/output_careful/contigs.paths -o acc_5hiv_careful/
python eval_script/quast_evaluation.py -c1 benchmark/fastq/5-strain-HIV-20000x/output_careful/contigs.fasta -c2 ~/Desktop/benchmark/shortread/vgflow+savage/vgflow5hiv/haps.final.fasta -c3 acc_5hiv_careful/strain.fasta -ref benchmark/strains/5-strain-HIV.fasta -o quast5hiv/

# 6 POLIO
python src/__init__.py -a spades -g benchmark/fastq/6-strain-poliovirus/output/assembly_graph_after_simplification.gfa -p benchmark/fastq/6-strain-poliovirus/output/contigs.paths -o acc_6_polio/
python eval_script/quast_evaluation.py -c1 benchmark/fastq/6-strain-poliovirus/output/contigs.fasta -c2 ~/Desktop/benchmark/shortread/vgflow+savage/vgflow6polio/haps.final.fasta -c3 acc_6_polio/strain.fasta -ref benchmark/strains/6-strain-polio.fasta -o quast6polio/

# 15 ZIKV
python src/__init__.py -a spades -g benchmark/fastq/15-strain-ZIKV-20000x/output_careful/assembly_graph_after_simplification.gfa -p benchmark/fastq/15-strain-ZIKV-20000x/output_careful/contigs.paths -o acc_15_zikv_careful/
python eval_script/quast_evaluation.py -c1 benchmark/fastq/15-strain-ZIKV-20000x/output_careful/contigs.fasta -c2 ~/Desktop/benchmark/shortread/vgflow+savage/vgflow15zikv/haps.final.fasta -c3 acc_15_zikv_careful/strain.fasta -ref benchmark/strains/15-strain-ZIKV.fasta -o quast15zikv/