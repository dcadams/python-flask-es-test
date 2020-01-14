from base import Base
from mod import MOD

import csv


class Fly(Base):
    species = 'Drosophila melanogaster'
    gene_data_tsv_filename = "data/FlyGene.tsv"
    go_data_csv_filename = "data/FlyGOGeneMapping.tsv"
    disease_data_csv_filename = "data/FlyDiseaseGeneMapping.tsv"

    @staticmethod
    def gene_href(gene_id):
        return "http://www.flybase.org/species/c_elegans/gene/" + gene_id

    def load_genes(self):
  #      import pudb; pudb.set_trace()
        genes = MOD.genes

        print("Fetching gene data from FlyGene tsv file...")

        with open(self.gene_data_tsv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')

            for row in reader:
                if row[3] == "":
                    gene_type = None
                else:
                    gene_type = row[3]

                chromosomes = []
                if row[5]:
                    chromosomes = [row[5]]

                genes[row[0]] = {
                    "gene_symbol": row[1],
                    "name": row[1],
                    "description": row[4],
                    "gene_synonyms": map(lambda s: s.strip(), row[9].split(",")),
                    "gene_type": gene_type,
                    "gene_chromosomes": chromosomes,
                    "gene_chromosome_starts": row[6],
                    "gene_chromosome_ends": row[7],
                    "gene_chromosome_strand": row[8],
                    "external_ids": [],
                    "species": self.species,
    
                    "gene_biological_process": [],
                    "gene_molecular_function": [],
                    "gene_cellular_component": [],
    
                    "homologs": [],
    
                    "name_key": row[1].lower(),
                    "id": row[0],
                    "href": Fly.gene_href(row[0]),
                    "category": "gene"
                }
