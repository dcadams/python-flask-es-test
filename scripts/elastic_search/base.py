from mod import MOD

import csv


class Base(MOD):
    go_data_csv_filename = None
    disease_data_csv_filename = None
    

    def load_go(self):
        print("Fetching go data from {class_name} tsv file...").format(class_name=self.__class__.__name__)

        with open(self.go_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')

            for i in xrange(24):
                next(reader, None)

            for row in reader:
                self.add_go_annotation_to_gene(gene_id=row[1], go_id=row[4])

    def load_diseases(self):
        print("Fetching disease data from {class_name} tsv file...").format(class_name=self.__class__.__name__)

        with open(self.disease_data_csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader, None)

            for row in reader:
                if row[2] and row[2] != "":
                    omim_ids = map(lambda s: s.strip(), row[2].split(","))

                    for omim_id in omim_ids:
                        self.add_disease_annotation_to_gene(gene_id=None, omim_id="OMIM:"+omim_id)
