from src.app.Model.CodeModel import CodeModel


from src.app.helper.GeneratorCode import GeneratorCodes


class routeController():

    def getMID(self, code, merchantId):
        return CodeModel(code, merchantId).get_code()

    def addMID(self, merchantId):
        genCode = GeneratorCodes(9).generator()
        return CodeModel(genCode, merchantId).add_code()

    def updateMID(self, code, merchantId):
        return CodeModel(code, merchantId).update_code()

    def deleteMID(self, code, merchantId):
        return CodeModel(code, merchantId).delete_code()

    def cacheMID(self, code, merchantId):
        return CodeModel(code, merchantId).cache_code()











