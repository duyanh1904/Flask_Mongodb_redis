from src.app.model.code_model import CodeModel
from src.app.helper.generator_code import GeneratorCodes


class RouteController:

    def get_mid(self, merchant_id):
        return CodeModel.get_code(merchant_id)

    def add_mid(self, merchant_id):
        gen_code = GeneratorCodes(9).generator()                    #create random code
        return CodeModel(gen_code, merchant_id).add_code()

    def update_mid(self, code, merchant_id):
        return CodeModel(code, merchant_id).update_code()

    def delete_mid(self,merchant_id):
        return CodeModel.delete_code(merchant_id)
