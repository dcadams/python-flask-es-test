from mod import MOD
import xlrd
import csv

class FlyBase(MOD):
    species = "Drosophila melanogaster"

    @staticmethod
    def gene_href(gene_id):
        return "http://flybase.org/reports/" + gene_id + ".html"

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: WormBase=WBGene00004831
        return panther_id.split("=")[1]

    def load_genes(self):
        genes = MOD.genes

        gene_data_tlv_filename = "data/FlyGene.tsv"

        print("Fetching gene data from FlyGenes file...")

        with open(gene_data_tlv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader, None)

            for row in reader:
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
                    "gene_type": gene_type,
                    "gene_chromosomes": chromosomes,
                    "gene_chromosome_starts": row[6].value,
                    "gene_chromosome_ends": row[7].value,
                    "gene_chromosome_strand": row[8].value,
                    "gene_synonyms": map(lambda s: s.strip(), row[9].value.split(",")),
                    "species": "Drosophila melanogaster",
                    "name_key": row[1].value.lower(),
                    "id": row[0].value,
                    "href": FlyBase.gene_href(row[0].value),
                    "category": "gene"
                }

    def load_go(self):
        go_data_csv_filename = "data/FlyGOGeneMapping.tsv"

        print("Fetching go data from FlyGene tsv file...")

        with open(go_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            for i in xrange(24):
                next(reader, None)

            for row in reader:
                gene_ids = map(lambda s: s.strip(), row[4].split(","))
                for gene_id in gene_ids: 
                    self.add_go_annotation_to_gene(gene_id=gene_id, go_id=row[2])

    def load_diseases(self):
        disease_data_csv_filename = "data/FlyDiseaseGeneMapping.tsv"

        print("Fetching disease data from fly tsv file...")

        with open(disease_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader, None)

            for row in reader:
                if row[3] and row[3] != "":
                    omim_ids = map(lambda s: s.strip(), row[3].split(","))

                    for omim_id in omim_ids:
                        self.add_disease_annotation_to_gene(gene_id=None, omim_id="OMIM:"+omim_id)
