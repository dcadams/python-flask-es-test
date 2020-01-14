from base import Base
from mod import MOD

import xlrd


class Worm(Base):
    species = "Caenorhabditis elegans"
    gene_data_xls_filename = "data/WormGenes.xlsx"
    go_data_csv_filename = "data/WormGoGeneMapping.tsv"
    disease_data_csv_filename = "data/WormDiseaseGeneMapping.tsv"
    

    @staticmethod
    def gene_href(gene_id):
        return "http://www.wormbase.org/species/c_elegans/gene/" + gene_id

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: WormBase=WBGene00004831
        return panther_id.split("=")[1]

    def load_genes(self):
        genes = MOD.genes

        print("Fetching gene data from WormGenes xlsx file...")

        workbook = xlrd.open_workbook(self.gene_data_xls_filename)
        sheet = workbook.sheet_by_index(0)

        for i in range(1, sheet.nrows):
            row = sheet.row(i)

            if row[3].value == "":
                gene_type = None
            else:
                gene_type = row[3].value

            chromosomes = []
            if row[5].value:
                chromosomes = [row[5].value]

            genes[row[0].value] = {
                "gene_symbol": row[1].value,
                "name": row[1].value,
                "description": row[4].value,
                "gene_synonyms": map(lambda s: s.strip(), row[9].value.split(",")),
                "gene_type": gene_type,
                "gene_chromosomes": chromosomes,
                "gene_chromosome_starts": row[6].value,
                "gene_chromosome_ends": row[7].value,
                "gene_chromosome_strand": row[8].value,
                "external_ids": [],
                "species": "Caenorhabditis elegans",

                "gene_biological_process": [],
                "gene_molecular_function": [],
                "gene_cellular_component": [],

                "homologs": [],

                "name_key": row[1].value.lower(),
                "id": row[0].value,
                "href": Worm.gene_href(row[0].value),
                "category": "gene"
            }
