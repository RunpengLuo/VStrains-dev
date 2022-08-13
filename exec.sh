#/bin/zsh
conda init zsh
conda activate spades-hapConstruction-env

# 5 HIV
python src/__init__.py -a spades -g benchmark/fastq/5-strain-HIV-20000x/output_careful/assembly_graph_after_simplification.gfa -p benchmark/fastq/5-strain-HIV-20000x/output_careful/contigs.paths -o acc_5_hiv_careful/ -d
python eval_script/quast_evaluation.py -cs benchmark/fastq/5-strain-HIV-20000x/output_careful/contigs.fasta ~/Desktop/benchmark/shortread/vgflow+savage/vgflow5hiv/haps.final.fasta acc_5_hiv_careful/strain.fasta -ref benchmark/strains/5-strain-HIV.fasta -o quast5hiv/

# 6 POLIO
python src/__init__.py -a spades -g benchmark/fastq/6-strain-poliovirus/output_careful/assembly_graph_after_simplification.gfa -p benchmark/fastq/6-strain-poliovirus/output_careful/contigs.paths -o acc_6_polio/ -d
python eval_script/quast_evaluation.py -cs benchmark/fastq/6-strain-poliovirus/output_careful/contigs.fasta ~/Desktop/benchmark/shortread/vgflow+savage/vgflow6polio/haps.final.fasta acc_6_polio/strain.fasta -ref benchmark/strains/6-strain-polio.fasta -o quast6polio/

# 10 HCV
python src/__init__.py -a spades -g benchmark/fastq/10-strain-HCV-20000x/output_careful/assembly_graph_after_simplification.gfa -p benchmark/fastq/10-strain-HCV-20000x/output_careful/contigs.paths -o acc_10_hcv/ -d -mc 0
python eval_script/quast_evaluation.py -cs benchmark/fastq/10-strain-HCV-20000x/output_careful/contigs.fasta ~/Desktop/benchmark/shortread/vgflow+savage/vgflow10hcv/haps.final.fasta acc_10_hcv/strain.fasta -ref benchmark/strains/10-strain-HCV.fasta -o quast10hcv/

# 15 ZIKV
python src/__init__.py -a spades -g benchmark/fastq/15-strain-ZIKV-20000x/output_careful/assembly_graph_after_simplification.gfa -p benchmark/fastq/15-strain-ZIKV-20000x/output_careful/contigs.paths -o acc_15_zikv_careful/ -d
python eval_script/quast_evaluation.py -cs benchmark/fastq/15-strain-ZIKV-20000x/output_careful/contigs.fasta ~/Desktop/benchmark/shortread/vgflow+savage/vgflow15zikv/haps.final.fasta acc_15_zikv_careful/strain.fasta -ref benchmark/strains/15-strain-ZIKV.fasta -o quast15zikv/