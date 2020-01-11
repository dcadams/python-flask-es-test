from mod import MOD
import xlrd
import csv


class FlyBase(MOD):
    species = 'Drosophila melanogaster'

    @staticmethod
    def gene_href(gene_id):
        return "http://www.flybase.org/species/c_elegans/gene/" + gene_id

    def load_genes(self):
  #      import pudb; pudb.set_trace()
        genes = MOD.genes

        gene_data_tsv_filename = "data/FlyGene.tsv"

        print("Fetching gene data from FlyGene tsv file...")

        with open(gene_data_tsv_filename, 'rb') as f:
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
                    "href": FlyBase.gene_href(row[0]),
                    "category": "gene"
                }

    def load_go(self):
        go_data_csv_filename = "data/FlyGOGeneMapping.tsv"

        print("Fetching go data from FlyBase tsv file...")

        with open(go_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')

            for row in reader:
                gene_id = row[1]
                fb_ids = [row[4]]
                
            # Missing id so doesn't get loaded.
            # self.add_go_annotation_to_gene(gene_id=row[1], go_id=row[4])

    def load_diseases(self):
        disease_data_csv_filename = "data/FlyDiseaseGeneMapping.tsv"

        print("Fetching disease data from Fly tsv file...")

        with open(disease_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader, None)

            for row in reader:
                if row[3] and row[3] != "":
                    omim_ids = map(lambda s: s.strip(), row[3].split(","))

                    for omim_id in omim_ids:
                        self.add_disease_annotation_to_gene(gene_id=None, omim_id="OMIM:"+omim_id)

