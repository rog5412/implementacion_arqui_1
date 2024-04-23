from src.extractors.txt_extractor import TXTExtractor
from os.path import join
import luigi, os, json

class TXTTransformer(luigi.Task):
    
    def requires(self):
        return TXTExtractor()

    def run(self):
        result = []
        for file in self.input():
            with file.open() as txt_file:
                lines = txt_file.read().split(";")
                header = lines[0].strip().split(",")
                for line in lines[1:]:
                    values = line.strip().split(",")
                    if len(values) >= 8:
                        result.append(
                            {
                                "invoice": values[0],
                                "description": values[2],
                                "quantity": values[3],
                                "price": values[5],
                                "total": float(values[3]) * float(values[5]),
                                "provider": values[6],
                                "country": values[7]    
                            }
                        )
        with self.output().open('w') as out:
            out.write(json.dumps(result, indent=4))

    def output(self):
        project_dir = os.path.dirname(os.path.abspath("loader.py"))
        result_dir = join(project_dir, "result")
        return luigi.LocalTarget(join(result_dir, "txt.json"))